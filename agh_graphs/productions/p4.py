from typing import List

from networkx import Graph

from agh_graphs.production import Production
from agh_graphs.utils import get_neighbors_at, gen_name, sort_segments_by_angle, add_interior, \
    get_vertex_between


class P4(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        e1, e2, e3, e12, e13 = self.__check_prod_input(graph, prod_input)
        [i] = prod_input
        i_data = graph.nodes[i]

        i_data['label'] = 'i'
        i_layer = i_data['layer']
        new_layer = i_layer + 1

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
        b = get_vertex_between(graph, v1, v2, new_layer, 'E')
        assert b is not None
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
        i_id = prod_input[0]
        i_data = graph.nodes[i_id]
        i_layer = i_data['layer']

        assert i_data['label'] == 'I'

        i_neighbors = get_neighbors_at(graph, i_id, i_layer)
        assert len(i_neighbors) == 3

        nodes_with_other_neighbors = [e for e in i_neighbors
                                      if all(n not in i_neighbors for n in get_neighbors_at(graph, e, i_layer))]
        assert len(nodes_with_other_neighbors) == 1
        e1 = nodes_with_other_neighbors[0]
        (e2, e3) = [e for e in i_neighbors if e != e1]
        e12 = get_vertex_between(graph, e1, e2, i_layer, 'E')
        e13 = get_vertex_between(graph, e1, e3, i_layer, 'E')
        assert e12 is not None
        assert e13 is not None

        cycle_list = [e3, e13, e1, e12, e2]
        for i, e in enumerate(cycle_list):
            assert graph.nodes[e]['label'] == 'E'
            prev_e = cycle_list[(i - 1) % len(cycle_list)]
            next_e = cycle_list[(i + 1) % len(cycle_list)]
            assert all(n in get_neighbors_at(graph, e, i_layer) for n in [prev_e, next_e])

        return e1, e2, e3, e12, e13
