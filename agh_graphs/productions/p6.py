from typing import List

from networkx import Graph
from agh_graphs.production import Production
from agh_graphs.utils import get_neighbors_at, find_overlapping_vertices, join_overlapping_vertices, get_common_neighbors


class P6(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        """
        Apply 6th production on graph

        `prod_input` is list of 6 interiors as follows: `[upper, upper, lower, lower, lower, lower]`,
        where `upper` is vertex on upper layer and `lower` on lower layer. Order of vertices in one
        layer is irrelevant.

        `orientation` and `**kwargs` are ignored

        Returns empty list, as no new vertices were added.
        """

        self.__check_prod_input(graph, prod_input)

        up_layer = graph.nodes()[prod_input[0]]['layer']
        down_layer = graph.nodes()[prod_input[2]]['layer']
        v1_up, v2_up = get_common_neighbors(graph, prod_input[0], prod_input[1], up_layer)
        pos_v1 = graph.nodes()[v1_up]['position']
        pos_v2 = graph.nodes()[v2_up]['position']

        x = (pos_v1[0] + pos_v2[0]) / 2
        y = (pos_v1[1] + pos_v2[1]) / 2
        pos_center = (x, y)

        to_merge = [[], [], []]
        for interior in prod_input[2:]:
            for v in get_neighbors_at(graph, interior, down_layer):
                if graph.nodes()[v]['position'] == pos_v1:
                    to_merge[0].append(v)
                elif graph.nodes()[v]['position'] == pos_v2:
                    to_merge[1].append(v)
                elif graph.nodes()[v]['position'] == pos_center:
                    if v not in to_merge[2]:
                        to_merge[2].append(v)

        for v1, v2 in to_merge:
            join_overlapping_vertices(graph, v1, v2, down_layer)

        return []

    @staticmethod
    def __check_prod_input(graph: Graph, prod_input: List[str]):

        # Check number of vertices delivered
        if len(set(prod_input)) != 6:
            raise ValueError('Too few interiors in pord_input (6 required)')

        # Check layers
        up_layer = graph.nodes()[prod_input[0]]['layer']
        down_layer = graph.nodes()[prod_input[2]]['layer']
        if any(graph.nodes()[interior]['layer'] != up_layer for interior in prod_input[:2]):
            raise ValueError('First two interior are not in the same layer')
        if any(graph.nodes()[interior]['layer'] != down_layer for interior in prod_input[2:]):
            raise ValueError('Four last interiors are not in the same layer')
        if up_layer + 1 != down_layer:
            raise ValueError('Upper layer is not right above lower one')

        # Check delivered vertices labels
        if any(graph.nodes()[interior]['label'] != 'i' for interior in prod_input[:2]):
            raise ValueError('First two interior don not have "i" label')
        if any(graph.nodes()[interior]['label'] != 'I' for interior in prod_input[2:]):
            raise ValueError('Four last interior don not have "I" label')

        # Check connections between delivered vertices
        neighbors_in_lower_layer = {prod_input[0]: set(), prod_input[1]: set()}
        for upper_interior in prod_input[:2]:
            for bottom_neighbor in get_neighbors_at(graph, upper_interior, down_layer):
                neighbors_in_lower_layer[upper_interior].add(bottom_neighbor)
        for lower_interior in prod_input[2:]:
            if lower_interior not in neighbors_in_lower_layer[prod_input[0]]\
              and lower_interior not in neighbors_in_lower_layer[prod_input[1]]:
                raise ValueError('Upper interiors not connected properly to lower ones')
        if len(neighbors_in_lower_layer[prod_input[0]]) != 2:
            raise ValueError('Upper interiors not connected properly to lower ones')
        if len(neighbors_in_lower_layer[prod_input[1]]) != 2:
            raise ValueError('Upper interiors not connected properly to lower ones')

        # maps lower interiors to its parent in upper layer
        lower_to_upper = dict()
        for upper in neighbors_in_lower_layer:
            for lower in neighbors_in_lower_layer[upper]:
                lower_to_upper[lower] = upper

        # Check common neighbors of upper interiors
        upper_neighbors = get_common_neighbors(graph, prod_input[0], prod_input[1], up_layer)
        if len(upper_neighbors) != 2:
            raise ValueError('Upper interiors don not have 2 common neighbors')

        # Get those neighbors and their positions as well as center position between them
        v1_up, v2_up = upper_neighbors
        pos_v1 = graph.nodes()[v1_up]['position']
        pos_v2 = graph.nodes()[v2_up]['position']
        x = (pos_v1[0] + pos_v2[0]) / 2
        y = (pos_v1[1] + pos_v2[1]) / 2
        pos_center = (x, y)

        # Check if they are connected
        if not graph.has_edge(v1_up, v2_up):
            raise ValueError('Upper vertices are not connected')

        # Prepare list of vertices in lower layer
        pairs_of_lower = [set(), set(), set()]
        for interior in prod_input[2:]:
            for v in get_neighbors_at(graph, interior, down_layer):
                if graph.nodes()[v]['position'] == pos_v1:
                    pairs_of_lower[0].add((v, lower_to_upper[interior]))
                elif graph.nodes()[v]['position'] == pos_v2:
                    pairs_of_lower[1].add((v, lower_to_upper[interior]))
                elif graph.nodes()[v]['position'] == pos_center:
                    if v not in pairs_of_lower[2]:
                        pairs_of_lower[2].add((v, lower_to_upper[interior]))

        # Check if pair is indeed pair of vertices
        for pair in pairs_of_lower:
            s = set(map(lambda x: x[0], pair))
            if len(s) != 2:
                raise ValueError('Connections between lower vertices are incorrect')

        # separate vertices based on side it is on (vertices on one side are connected)
        vertices_by_side = {prod_input[0]: list(), prod_input[1]: list()}
        for pair in pairs_of_lower:
            for v in pair:
                vertices_by_side[v[1]].append(v[0])
        # Now vertices_by_side should be dict where keys are id's of interiors in upper layer
        # and values are lists of vertices in loser layer on belonging to this parent
        # also last element on this list is center between two previous

        # Check if vertices on one side are properly connected
        for side in vertices_by_side:
            v1, v2, v3 = vertices_by_side[side]
            if not graph.has_edge(v1, v3):
                raise ValueError('Connections between lower vertices are incorrect')
            if not graph.has_edge(v2, v3):
                raise ValueError('Connections between lower vertices are incorrect')

        # Check if middle vertices are properly connected to two interiors each
        for side in vertices_by_side:
            v1, v2, v3 = vertices_by_side[side]     # v3 is vertex in the middle
            lower_interiors = get_neighbors_at(graph, side, down_layer)
            for interior in lower_interiors:
                if interior not in graph.neighbors(v3):
                    raise ValueError('Connections between lower vertices are incorrect')

        # Check if vertices on opposite sides are connected
        # (they obviously shouldn't be right?)
        for v in vertices_by_side[prod_input[0]]:
            if any(graph.has_edge(v, v_other) for v_other in vertices_by_side[prod_input[1]]):
                raise ValueError('Connections between lower vertices are incorrect')

        # Check if labels are E
        all_vertices = vertices_by_side[prod_input[0]] + vertices_by_side[prod_input[1]] + [v1_up, v2_up]
        if any(graph.nodes()[v]['label'] != 'E' for v in all_vertices):
            raise ValueError('Not all vertices have label E')

