from typing import List

from networkx import Graph
from agh_graphs.production import Production
from agh_graphs.utils import get_neighbors_at, find_overlapping_vertices, join_overlapping_vertices, get_all_E_vertices_from_layer, get_node_at


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

        all_I_neighbours = []

        for interior in prod_input:
            interior_neighbours = get_neighbors_at(graph, interior, layer)
            if 2 > len(interior_neighbours) > 3:
                raise ValueError('wrongly connected interior vertices')

            for neighbour in interior_neighbours:
                if graph.nodes()[neighbour]['label'] != 'E':
                    raise ValueError('interior vertices can be connect only with E vertices')

                all_I_neighbours.append(neighbour)

        E_vertices = get_all_E_vertices_from_layer(graph, layer)
        E_vertices_position_prev_layer = []
        if any(E_vertice not in all_I_neighbours for E_vertice in E_vertices):
            raise ValueError('wrongly connected E vertices')
        for E_vertice in E_vertices:
            E_vertice_neighbours = get_neighbors_at(graph, E_vertice, layer)
            if len([I_node for I_node in E_vertice_neighbours if graph.nodes()[I_node]['label'] == "I"]) != 2:
                raise ValueError('each E vertice must be connected with two I vertices')
            E_vertice_E_neighbours = [neighbour for neighbour in E_vertice_neighbours if graph.nodes()[neighbour]['label'] == "E"]
            if 2 > len(E_vertice_E_neighbours) > 4:
                raise ValueError('each E vertice must be connected with at least two E vertices')
            corresponding_vertice = get_node_at(graph, layer-1, graph.nodes()[E_vertice]['position'])
            if corresponding_vertice is not None:
                E_vertices_position_prev_layer.append(corresponding_vertice)

        if len(E_vertices_position_prev_layer) != 2 and len(E_vertices_position_prev_layer) != 4:
            raise ValueError('positions of corresponding vertices between layers are incorrect')
        corresponding_positions = [graph.nodes()[E_vertice]['position'] for E_vertice in E_vertices_position_prev_layer]
        noncorresponding_E_vertices = [E_vertice for E_vertice in E_vertices if graph.nodes()[E_vertice]['position'] not in corresponding_positions]
        possible_positions = []
        for i in range(len(corresponding_positions)-1):
            x1, y1 = corresponding_positions[i]
            for j in range(i+1, len(corresponding_positions)):
                x2, y2 = corresponding_positions[j]
                possible_positions.append(((x1+x2)/2, (y1+y2)/2))
        for E_vertice in noncorresponding_E_vertices:
            x, y = graph.nodes()[E_vertice]['position']
            if (x, y) not in possible_positions:
                raise ValueError('positions of noncorresponding vertices are incorrect')

        overlapping_vertices = find_overlapping_vertices(graph)

        if len(overlapping_vertices) != 2 or \
                any(overlapping_vertice1 not in set(all_I_neighbours)
                    or overlapping_vertice2 not in set(all_I_neighbours)
                    for overlapping_vertice1, overlapping_vertice2 in overlapping_vertices):
            raise ValueError('incorrect shape of graph')

        vertices_to_join = [neighbour for neighbour in set(all_I_neighbours) if
                            graph.nodes()[neighbour]['position'] == graph.nodes()[overlapping_vertices[0][0]]['position']]

        if len(vertices_to_join) != 2:
            raise ValueError('too many overlapping vertices')

        vertice1_neighbours = get_neighbors_at(graph, vertices_to_join[0], layer)
        vertice2_neighbours = get_neighbors_at(graph, vertices_to_join[1], layer)

        common_neighbours = set(vertice1_neighbours).intersection(set(vertice2_neighbours))

        if len(common_neighbours) != 2:
            raise ValueError('vertices to join wrongly connected')

        I_neighbours_vertice1 = [neighbour for neighbour in vertice1_neighbours if graph.nodes()[neighbour]['label'] == "I"]
        I_neighbours_vertice2 = [neighbour for neighbour in vertice2_neighbours if graph.nodes()[neighbour]['label'] == "I"]

        if len(I_neighbours_vertice1) != 2 or len(I_neighbours_vertice2) != 2:
            raise ValueError('vertices to join wrongly connected with I vertices')

        if len(set(I_neighbours_vertice1).intersection(I_neighbours_vertice2)) != 0:
            raise ValueError('vertices to join have common I neighbour')
