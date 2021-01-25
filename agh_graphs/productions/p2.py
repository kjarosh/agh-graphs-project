from typing import List

from networkx import Graph

from agh_graphs.production import Production
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, sort_segments_by_angle, add_break_in_segment, \
    sort_vertices_by_coordinates


class P2(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        [i] = prod_input
        i_data = graph.nodes[i]
        self.__check_prod_input(graph, prod_input)

        i_data['label'] = 'i'
        i_layer = i_data['layer']
        new_layer = i_layer + 1

        i_neighbors = get_neighbors_at(graph, i, i_layer)

        # e1 doesn't mean e1 with (x1, y1)
        vx_e1 = gen_name()
        vx_e2 = gen_name()
        vx_e3 = gen_name()

        e1_pos = graph.nodes[i_neighbors[0]]['position']
        e2_pos = graph.nodes[i_neighbors[1]]['position']
        e3_pos = graph.nodes[i_neighbors[2]]['position']

        graph.add_node(vx_e1, layer=new_layer, position=e1_pos, label='E')
        graph.add_node(vx_e2, layer=new_layer, position=e2_pos, label='E')
        graph.add_node(vx_e3, layer=new_layer, position=e3_pos, label='E')

        graph.add_edge(vx_e1, vx_e2)
        graph.add_edge(vx_e2, vx_e3)
        graph.add_edge(vx_e3, vx_e1)

        sorted_segments = sort_segments_by_angle(graph, [(vx_e1, vx_e2), (vx_e2, vx_e3), (vx_e3, vx_e1)])
        segment_to_break = sorted_segments[orientation % 3]
        b = add_break_in_segment(graph, segment_to_break)
        b_neighbors = get_neighbors_at(graph, b, i_layer + 1)
        remaining = [x for x in [vx_e1, vx_e2, vx_e3] if x not in b_neighbors][0]
        graph.add_edge(b, remaining)

        i1 = add_interior(graph, b_neighbors[0], b, remaining)
        i2 = add_interior(graph, b_neighbors[1], b, remaining)

        graph.add_edge(i1, i)
        graph.add_edge(i2, i)

        return sort_vertices_by_coordinates(graph, [i1, i2])

    @staticmethod
    def __check_prod_input(graph, prod_input):
        i_node_id = prod_input[0]
        i_node_data = graph.nodes[i_node_id]
        i_node_layer = i_node_data['layer']

        assert i_node_data['label'] == 'I'

        neighbors = get_neighbors_at(graph, i_node_id, i_node_layer)
        assert len(neighbors) == 3
        for n_id in neighbors:
            assert graph.nodes[n_id]['label'] == 'E'
            n_expected_neighbors = [x for x in neighbors if x != n_id]
            n_neighbors = get_neighbors_at(graph, n_id, i_node_layer)
            for expected_neighbor in n_expected_neighbors:
                assert expected_neighbor in n_neighbors
