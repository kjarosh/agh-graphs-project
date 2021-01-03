from typing import List

from networkx import Graph

from agh_graphs.production import Production
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, angle_with_x_axis
import math
from math import isclose


class P5(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        eps = kwargs.get('epsilon', 1e-6)
        self.__check_prod_input(graph, prod_input, eps)

        [i] = prod_input
        i_data = graph.nodes[i]
        i_data['label'] = 'i'
        i_layer = i_data['layer']
        new_layer = i_layer + 1

        # get 'E' nodes from the left side of production
        [e1, e2, e3] = self.get_corner_nodes(graph, i, i_layer, orientation)

        e12 = self.get_node_between(graph, e1, e2, i_layer, eps)
        e23 = self.get_node_between(graph, e2, e3, i_layer, eps)
        e31 = self.get_node_between(graph, e3, e1, i_layer, eps)

        # create new 'E' nodes in the next layer
        new_e1 = gen_name()
        new_e2 = gen_name()
        new_e3 = gen_name()

        new_e12 = gen_name()
        new_e23 = gen_name()
        new_e31 = gen_name()

        graph.add_node(new_e1, layer=new_layer, position=graph.nodes[e1]['position'], label='E')
        graph.add_node(new_e2, layer=new_layer, position=graph.nodes[e2]['position'], label='E')
        graph.add_node(new_e3, layer=new_layer, position=graph.nodes[e3]['position'], label='E')

        graph.add_node(new_e12, layer=new_layer, position=graph.nodes[e12]['position'], label='E')
        graph.add_node(new_e23, layer=new_layer, position=graph.nodes[e23]['position'], label='E')
        graph.add_node(new_e31, layer=new_layer, position=graph.nodes[e31]['position'], label='E')

        # create edges between new 'E' nodes
        graph.add_edge(new_e1, new_e12)
        graph.add_edge(new_e12, new_e2)

        graph.add_edge(new_e2, new_e23)
        graph.add_edge(new_e23, new_e3)

        graph.add_edge(new_e3, new_e31)
        graph.add_edge(new_e31, new_e1)

        graph.add_edge(new_e23, new_e31)
        graph.add_edge(new_e12, new_e31)
        graph.add_edge(new_e2, new_e31)

        # create new 'I' nodes and edges between new 'I' nodes and new 'E' nodes
        i1 = add_interior(graph, new_e1, new_e12, new_e31)
        i3 = add_interior(graph, new_e3, new_e23, new_e31)
        i2a = add_interior(graph, new_e2, new_e12, new_e31)
        i2b = add_interior(graph, new_e2, new_e23, new_e31)

        # create edges between new 'I' nodes and parent 'i' node
        graph.add_edge(i1, i)
        graph.add_edge(i3, i)
        graph.add_edge(i2a, i)
        graph.add_edge(i2b, i)

        return [i1, i3, i2a, i2b]

    @staticmethod
    def __check_prod_input(graph, prod_input, eps):
        assert len(prod_input) == 1
        i_node_id = prod_input[0]
        i_node_data = graph.nodes[i_node_id]
        i_node_layer = i_node_data['layer']

        assert i_node_data['label'] == 'I'

        neighbours = get_neighbors_at(graph, i_node_id, i_node_layer)
        assert len(neighbours) == 3

        for n_id in neighbours:
            assert graph.nodes[n_id]['label'] == 'E'

        for e1, e2 in zip(neighbours, neighbours[1:] + neighbours[:1]):
            # find common 'E' neighbours in the same layer and exactly in the middle of e1_e2 segment
            (e1_x, e1_y) = graph.nodes[e1]['position']
            (e2_x, e2_y) = graph.nodes[e2]['position']
            middle_position = ((e1_x + e2_x) / 2, (e1_y + e2_y) / 2)
            common_neighbours = [n for n in graph.neighbors(e1)
                                 if n in graph.neighbors(e2)
                                 and graph.nodes[n]['layer'] == i_node_layer
                                 and graph.nodes[n]['label'] == 'E'
                                 and P5.is_close(graph.nodes[n]['position'], middle_position, eps)]
            assert len(common_neighbours) == 1

    @staticmethod
    def get_corner_nodes(graph, i, i_layer, orientation):
        """
        Get 'E' nodes that are neighbours of 'I' node at i_layer level.
        Order of returned nodes is not random. Methods returns nodes e1, e2 and e3 in counterclockwise order. Moreover
        we assume that the triangle will be cut into half by a segment from e2 to point in the middle of e1_e3 segment.
        If orientation is 0, method will assume that the longest segment is divided in half. If not, the segment is
        chosen by switching segment 'orientation' times in counterclockwise direction.
        """

        [a, b, c] = get_neighbors_at(graph, i, i_layer)

        # find counterclockwise order of nodes
        (a_x, a_y) = graph.nodes[a]['position']
        (b_x, b_y) = graph.nodes[b]['position']
        (c_x, c_y) = graph.nodes[c]['position']

        m = P5.calc_mean(a_x, a_y, b_x, b_y, c_x, c_y)

        ma_angle = angle_with_x_axis(m, (a_x, a_y))
        mb_angle = angle_with_x_axis(m, (b_x, b_y))
        mc_angle = angle_with_x_axis(m, (c_x, c_y))

        angles_counterclockwise = sorted([(a, ma_angle), (b, mb_angle), (c, mc_angle)], key=lambda p: p[1])
        nodes_counterclockwise = [p[0] for p in angles_counterclockwise]

        # find longest edge
        ab = P5.calc_distance_between(graph, a, b)
        bc = P5.calc_distance_between(graph, b, c)
        ca = P5.calc_distance_between(graph, c, a)

        if max(ab, bc, ca) == ab:
            middle_offset = nodes_counterclockwise.index(c)
        elif max(ab, bc, ca) == bc:
            middle_offset = nodes_counterclockwise.index(a)
        else:
            middle_offset = nodes_counterclockwise.index(b)

        offset = (orientation + (1 - middle_offset)) % 3

        return nodes_counterclockwise[offset:] + nodes_counterclockwise[:offset]  # rotate table according to offset

    @staticmethod
    def get_node_between(graph, e1, e2, layer, eps):
        """
        Returns a node that is a neighbour of both e1 and e2 and lies exactly between e1 and e2, at i_layer level.
        """
        (e1_x, e1_y) = graph.nodes[e1]['position']
        (e2_x, e2_y) = graph.nodes[e2]['position']
        desired_position = ((e1_x + e2_x) / 2, (e1_y + e2_y) / 2)
        neighbours = [n for n in graph.neighbors(e1)
                      if n in graph.neighbors(e2)
                      and graph.nodes[n]['layer'] == layer
                      and P5.is_close(graph.nodes[n]['position'], desired_position, eps)
                      and graph.nodes[n]['label'] == 'E']
        assert len(neighbours) == 1
        return neighbours[0]

    @staticmethod
    def calc_distance_between(graph, e1, e2):
        """
        Calculates distance between node e1 and node e2.
        """
        (e1_x, e1_y) = graph.nodes[e1]['position']
        (e2_x, e2_y) = graph.nodes[e2]['position']
        return math.sqrt((e1_x - e2_x) ** 2 + (e1_y - e2_y) ** 2)

    @staticmethod
    def calc_mean(e1_x, e1_y, e2_x, e2_y, e3_x, e3_y):
        """
        Calculates mean of x and y coordinates of e1, e2 and e3
        """
        return (e1_x + e2_x + e3_x) / 3, (e1_y + e2_y + e3_y) / 3

    @staticmethod
    def is_close(pos1, pos2, eps):
        x1, y1 = pos1
        x2, y2 = pos2
        return isclose(x1, x2, abs_tol=eps) and isclose(y1, y2, abs_tol=eps)
