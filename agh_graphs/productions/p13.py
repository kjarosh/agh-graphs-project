import itertools
from typing import List

from networkx import Graph

from agh_graphs.production import Production
from agh_graphs.utils import get_neighbors_at, get_common_neighbors, join_overlapping_vertices


class P13(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        to_merge = self.__check_prod_input(graph, prod_input)
        lower_layer = graph.nodes()[prod_input[2]]['layer']

        v1, v2 = to_merge
        join_overlapping_vertices(graph, v1, v2, lower_layer)

        return []

    @staticmethod
    def __check_prod_input(graph, prod_input):
        assert len(prod_input) == 4

        upper_layer = graph.nodes()[prod_input[0]]['layer']
        lower_layer = graph.nodes()[prod_input[2]]['layer']
        assert all(graph.nodes()[i]['layer'] == upper_layer for i in prod_input[:2])
        assert all(graph.nodes()[i]['layer'] == lower_layer for i in prod_input[2:])
        # upper layer means lower index
        assert upper_layer + 1 == lower_layer

        assert all(graph.nodes()[i]['label'] == 'i' for i in prod_input[:2])
        assert all(graph.nodes()[i]['label'] == 'I' for i in prod_input[2:])

        upper_i1, upper_i2 = prod_input[:2]
        upper_neighbors = get_common_neighbors(graph, upper_i1, upper_i2, upper_layer)
        assert len(upper_neighbors) == 2

        upper_v1, upper_v2 = upper_neighbors
        pos_upper_v1, pos_upper_v2 = [graph.nodes()[v]['position'] for v in upper_neighbors]
        assert graph.has_edge(upper_v1, upper_v2)

        neighbors_in_lower_layer = {upper_i1: set(), upper_i2: set()}
        for upper_interior in upper_i1, upper_i2:
            for bottom_neighbor in get_neighbors_at(graph, upper_interior, lower_layer):
                neighbors_in_lower_layer[upper_interior].add(bottom_neighbor)

        if prod_input[2] in neighbors_in_lower_layer[upper_i1]:
            assert prod_input[2] in neighbors_in_lower_layer[upper_i1] \
                   and prod_input[3] in neighbors_in_lower_layer[upper_i2]
            lower_i1, lower_i2 = prod_input[2:]
        else:
            assert prod_input[3] in neighbors_in_lower_layer[upper_i1] \
                   and prod_input[2] in neighbors_in_lower_layer[upper_i2]
            lower_i2, lower_i1 = prod_input[2:]

        lower_connected_neighbors = get_common_neighbors(graph, lower_i1, lower_i2, lower_layer)
        assert len(lower_connected_neighbors) == 1
        lower_connected_neighbor = lower_connected_neighbors[0]

        lower_i1_neighbors = get_neighbors_at(graph, lower_i1, lower_layer)
        lower_i1_neighbors.remove(lower_connected_neighbor)
        lower_i2_neighbors = get_neighbors_at(graph, lower_i2, lower_layer)
        lower_i2_neighbors.remove(lower_connected_neighbor)

        to_merge = [(v1, v2) for v1, v2 in itertools.product(lower_i1_neighbors, lower_i2_neighbors)
                    if graph.nodes()[v1]['position'] == graph.nodes()[v2]['position']]
        assert len(to_merge) == 1
        to_merge = to_merge[0]
        pos_lower_connected_neighbor, pos_lower_to_merge = [graph.nodes()[v]['position']
                                                            for v in [lower_connected_neighbor, to_merge[0]]]

        if pos_lower_connected_neighbor == pos_upper_v1:
            assert pos_lower_connected_neighbor == pos_upper_v1 \
                   and pos_lower_to_merge == pos_upper_v2
        else:
            assert pos_lower_to_merge == pos_upper_v1 \
                   and pos_lower_connected_neighbor == pos_upper_v2

        all_vertices = upper_neighbors + lower_connected_neighbors + lower_i1_neighbors + lower_i2_neighbors
        for e in all_vertices:
            assert graph.nodes[e]['label'] == 'E'

        return to_merge
