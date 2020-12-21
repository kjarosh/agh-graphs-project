from typing import List
from networkx import Graph
from agh_graphs.production import Production
from utils import get_neighbors_at, gen_name, sort_segments_by_angle, add_break_in_segment, add_interior


class P4(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        [i] = prod_input
        i_data = graph.nodes[i]
        self.__check_prod_input(graph, prod_input)

        i_data['label'] = 'i'
        i_layer = i_data['layer']
        new_layer = i_layer + 1

        i_neighbors = get_neighbors_at(graph, i, i_layer)
        e1 = [e for e in i_neighbors if all(n not in i_neighbors for n in get_neighbors_at(graph, e, i_layer))][0]
        (e2, e3) = [e for e in i_neighbors if e != e1]
        e12 = self.get_node_between(graph, e1, e2, i_layer)
        e13 = self.get_node_between(graph, e1, e3, i_layer)

        # create new layer
        new_e1 = gen_name()
        new_e2 = gen_name()
        new_e3 = gen_name()
        new_e12 = gen_name()
        new_e13 = gen_name()

        graph.add_node(new_e1, layer=new_layer, position=graph.nodes[e1]['position'], label='E')
        graph.add_node(new_e2, layer=new_layer, position=graph.nodes[e2]['position'], label='E')
        graph.add_node(new_e3, layer=new_layer, position=graph.nodes[e3]['position'], label='E')
        graph.add_node(new_e12, layer=new_layer, position=graph.nodes[e12]['position'], label='E')
        graph.add_node(new_e13, layer=new_layer, position=graph.nodes[e13]['position'], label='E')

        graph.add_edge(new_e1, new_e12)
        graph.add_edge(new_e12, new_e2)
        graph.add_edge(new_e1, new_e13)
        graph.add_edge(new_e13, new_e3)
        graph.add_edge(new_e2, new_e3)

        sorted_segments = sort_segments_by_angle(graph, [(new_e1, new_e2), (new_e1, new_e3)])
        segment_to_break = sorted_segments[orientation % 2]
        (v1, v2) = segment_to_break
        b = self.get_node_between(graph, v1, v2, new_layer)
        b_opposite_1 = [e for e in [new_e1, new_e2, new_e3] if e not in segment_to_break][0]
        b_opposite_2 = [e for e in [new_e12, new_e13] if e != b][0]
        graph.add_edge(b, b_opposite_1)
        graph.add_edge(b, b_opposite_2)

        i1 = add_interior(graph, b, b_opposite_1, b_opposite_2)
        i2 = add_interior(graph, b, b_opposite_1, v2)
        i3 = add_interior(graph, b, b_opposite_2, v1)

        graph.add_edge(i1, i)
        graph.add_edge(i2, i)
        graph.add_edge(i3, i)

        return [i1, i2, i3]

    @staticmethod
    def __check_prod_input(graph, prod_input):
        assert len(prod_input) == 1
        i_node_id = prod_input[0]
        i_node_data = graph.nodes[i_node_id]
        i_node_layer = i_node_data['layer']

        assert i_node_data['label'] == 'I'

        neighbors = get_neighbors_at(graph, i_node_id, i_node_layer)
        assert len(neighbors) == 3
        for n_id in neighbors:
            assert graph.nodes[n_id]['label'] == 'E'

    @staticmethod
    def get_node_between(graph, e1, e2, layer):
        neighbors = []
        for n in graph.neighbors(e1):
            if n in graph.neighbors(e2) and graph.nodes[n]['layer'] == layer and graph.nodes[n]['label'] == 'E':
                neighbors.append(n)
        assert len(neighbors) == 1
        return neighbors[0]

    @staticmethod
    def get_node_opposite(neighbors, all):
        e_opposite = next([e for e in all if e not in neighbors], None)
        assert e_opposite is not None
        return e_opposite
