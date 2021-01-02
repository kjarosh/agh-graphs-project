from typing import List

from networkx import Graph
from agh_graphs.production import Production
from agh_graphs.utils import get_neighbors_at, find_overlapping_vertices, join_overlapping_vertices


class P8(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:

        self.__check_prod_input(graph, prod_input)

        overlapping_vertices = find_overlapping_vertices(graph)[0]
        layer = graph.nodes()[prod_input[0]]['layer']

        neighbours = set()
        for interior in prod_input:
            neighbours |= set(get_neighbors_at(graph, interior, layer))

        vertices_to_join = [neighbour for neighbour in neighbours
                            if graph.nodes()[neighbour]['position'] == graph.nodes()[overlapping_vertices[0]]['position']]

        if len(vertices_to_join) == 2:
            join_overlapping_vertices(graph, vertices_to_join[0], vertices_to_join[1], layer)

        return prod_input

    @staticmethod
    def __check_prod_input(graph, prod_input):

        if len(set(prod_input)) != 4:
            raise ValueError('too few interiors')
        layer = graph.nodes()[prod_input[0]]['layer']
        if any(graph.nodes()[interior]['layer'] != layer for interior in prod_input[1:]):
            raise ValueError('interior vertices come from different layers')
        if any(graph.nodes()[interior]['label'] != 'I' for interior in prod_input):
            raise ValueError('interior vertices must have I label')

        all_neighbours = []

        for interior in prod_input:
            interior_neighbours = get_neighbors_at(graph, interior, layer)
            if len(interior_neighbours) != 3:
                raise ValueError('wrongly connected interior vertices')

            for neighbour in interior_neighbours:
                if graph.nodes()[neighbour]['label'] != 'E':
                    raise ValueError('interior vertices can be connect only with E vertices')

                all_neighbours.append(neighbour)

        if len(set(all_neighbours)) != 6:
            raise ValueError('incorrect number of E vertices')

        overlapping_vertices = find_overlapping_vertices(graph)

        if len(overlapping_vertices) != 2 or \
                any(overlapping_vertice1 not in set(all_neighbours)
                    or overlapping_vertice2 not in set(all_neighbours)
                    for overlapping_vertice1, overlapping_vertice2 in overlapping_vertices):
            raise ValueError('incorrect shape of graph')
