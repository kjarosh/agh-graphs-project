from typing import List

from networkx import Graph

from agh_graphs.production import Production
from agh_graphs.utils import find_overlapping_vertices, get_neighbors_at, \
    get_all_E_vertices_from_layer, get_node_at, join_overlapping_vertices


class P10(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        self.__check_prod_input(graph, prod_input)

        layer = graph.nodes()[prod_input[0]]['layer']
        overlapping_vertices = find_overlapping_vertices(graph)
        vertices_to_join = set()
        for overlapping_vertice1, overlapping_vertice2 in overlapping_vertices:
            vertices_to_join.add(overlapping_vertice1)
            vertices_to_join.add(overlapping_vertice2)

        vertices_to_join_group1 = [vertice for vertice in vertices_to_join
                                   if graph.nodes()[vertice]['position'] == graph.nodes()[list(vertices_to_join)[0]][
                                       'position']]
        vertices_to_join_group2 = [vertice for vertice in vertices_to_join if vertice not in vertices_to_join_group1]

        vertice1_group1_neighbours = get_neighbors_at(graph, vertices_to_join_group1[0], layer)
        vertice2_group1_neighbours = get_neighbors_at(graph, vertices_to_join_group1[1], layer)
        vertice1_group2_neighbours = get_neighbors_at(graph, vertices_to_join_group2[0], layer)
        vertice2_group2_neighbours = get_neighbors_at(graph, vertices_to_join_group2[1], layer)

        vertice1_group1_I_neighbours = [neighbour for neighbour in vertice1_group1_neighbours if
                                graph.nodes()[neighbour]['label'] == "I"]
        vertice2_group1_I_neighbours = [neighbour for neighbour in vertice2_group1_neighbours if
                                        graph.nodes()[neighbour]['label'] == "I"]
        vertice1_group2_I_neighbours = [neighbour for neighbour in vertice1_group2_neighbours if
                                        graph.nodes()[neighbour]['label'] == "I"]
        vertice2_group2_I_neighbours = [neighbour for neighbour in vertice2_group2_neighbours if
                                        graph.nodes()[neighbour]['label'] == "I"]

        common_I_neighbour_vertices_to_join = []
        if vertice1_group1_I_neighbours == vertice1_group2_I_neighbours:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[0])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[0])
        elif vertice1_group1_I_neighbours == vertice2_group2_I_neighbours:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[0])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[1])
        elif vertice2_group1_I_neighbours == vertice1_group2_I_neighbours:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[1])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[0])
        elif vertice2_group1_I_neighbours == vertice2_group2_I_neighbours:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[1])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[1])

        if graph.has_edge(common_I_neighbour_vertices_to_join[0], common_I_neighbour_vertices_to_join[1]):
            graph.remove_edge(common_I_neighbour_vertices_to_join[0], common_I_neighbour_vertices_to_join[1])

        join_overlapping_vertices(graph, vertices_to_join_group1[0], vertices_to_join_group1[1], layer)
        join_overlapping_vertices(graph, vertices_to_join_group2[0], vertices_to_join_group2[1], layer)

        return prod_input

    @staticmethod
    def __check_prod_input(graph, prod_input):

        if len(set(prod_input)) != 3:
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
            if 1 > len([I_node for I_node in E_vertice_neighbours if graph.nodes()[I_node]['label'] == "I"]) > 2:
                raise ValueError('each E vertice must be connected with I vertice')
            E_vertice_E_neighbours = [neighbour for neighbour in E_vertice_neighbours if
                                      graph.nodes()[neighbour]['label'] == "E"]
            if 1 > len(E_vertice_E_neighbours) > 2:
                raise ValueError('each E vertice must be connected with at least one E vertice')
            corresponding_vertice = get_node_at(graph, layer - 1, graph.nodes()[E_vertice]['position'])
            if corresponding_vertice is not None:
                E_vertices_position_prev_layer.append(corresponding_vertice)

        if len(E_vertices_position_prev_layer) != 4 and len(E_vertices_position_prev_layer) != 6:
            raise ValueError('positions of corresponding vertices between layers are incorrect')
        corresponding_positions = [graph.nodes()[E_vertice]['position'] for E_vertice in E_vertices_position_prev_layer]
        noncorresponding_E_vertices = [E_vertice for E_vertice in E_vertices if
                                       graph.nodes()[E_vertice]['position'] not in corresponding_positions]
        possible_positions = []
        for i in range(len(corresponding_positions) - 1):
            x1, y1 = corresponding_positions[i]
            for j in range(i + 1, len(corresponding_positions)):
                x2, y2 = corresponding_positions[j]
                possible_positions.append(((x1 + x2) / 2, (y1 + y2) / 2))
        for E_vertice in noncorresponding_E_vertices:
            x, y = graph.nodes()[E_vertice]['position']
            if (x, y) not in possible_positions:
                raise ValueError('position of noncorresponding vertice is incorrect')

        overlapping_vertices = find_overlapping_vertices(graph)

        if len(overlapping_vertices) != 4 or \
                any(overlapping_vertice1 not in set(all_I_neighbours)
                    or overlapping_vertice2 not in set(all_I_neighbours)
                    for overlapping_vertice1, overlapping_vertice2 in overlapping_vertices):
            raise ValueError('incorrect shape of graph')

        vertices_to_join = set()
        for overlapping_vertice1, overlapping_vertice2 in overlapping_vertices:
            vertices_to_join.add(overlapping_vertice1)
            vertices_to_join.add(overlapping_vertice2)

        if len(vertices_to_join) != 4:
            raise ValueError('too many overlapping vertices')

        vertices_to_join_group1 = [vertice for vertice in vertices_to_join
                                   if graph.nodes()[vertice]['position'] == graph.nodes()[list(vertices_to_join)[0]]['position']]
        vertices_to_join_group2 = [vertice for vertice in vertices_to_join if vertice not in vertices_to_join_group1]

        if len(vertices_to_join_group1) != 2 or len(vertices_to_join_group2) != 2:
            raise ValueError('too many overlapping vertices')

        vertice1_neighbours = get_neighbors_at(graph, vertices_to_join_group1[0], layer)
        vertice2_neighbours = get_neighbors_at(graph, vertices_to_join_group1[1], layer)
        vertice3_neighbours = get_neighbors_at(graph, vertices_to_join_group2[0], layer)
        vertice4_neighbours = get_neighbors_at(graph, vertices_to_join_group2[1], layer)

        I_neighbours_vertice1 = [neighbour for neighbour in vertice1_neighbours if
                                graph.nodes()[neighbour]['label'] == "I"]
        I_neighbours_vertice2 = [neighbour for neighbour in vertice2_neighbours if
                                graph.nodes()[neighbour]['label'] == "I"]
        I_neighbours_vertice3 = [neighbour for neighbour in vertice3_neighbours if
                                 graph.nodes()[neighbour]['label'] == "I"]
        I_neighbours_vertice4 = [neighbour for neighbour in vertice4_neighbours if
                                 graph.nodes()[neighbour]['label'] == "I"]

        if len(I_neighbours_vertice1) != 1 or len(I_neighbours_vertice2) != 1 or \
            len(I_neighbours_vertice3) != 1 or len(I_neighbours_vertice4) != 1:
            raise ValueError('vertices to join wrongly connected with I vertices')

        common_I_neighbour_vertices_to_join = []
        if I_neighbours_vertice1==I_neighbours_vertice3:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[0])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[0])
        elif I_neighbours_vertice1==I_neighbours_vertice4:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[0])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[1])
        elif I_neighbours_vertice2==I_neighbours_vertice3:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[1])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[0])
        elif I_neighbours_vertice2==I_neighbours_vertice4:
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group1[1])
            common_I_neighbour_vertices_to_join.append(vertices_to_join_group2[1])
        else:
            raise ValueError('vertices to join wrongly connected with I vertices')

        noncommon_I_neighbour_vertices_to_join = [vertice for vertice in vertices_to_join
                                                  if vertice not in common_I_neighbour_vertices_to_join]
        if len(noncommon_I_neighbour_vertices_to_join) != 2:
            raise ValueError('vertices to join wrongly connected with I vertices')
        if len(set(common_I_neighbour_vertices_to_join).intersection(set(noncommon_I_neighbour_vertices_to_join))) != 0:
            raise ValueError('vertices to join wrongly connected')

        common_vertice1_neighbours = get_neighbors_at(graph, common_I_neighbour_vertices_to_join[0], layer)
        common_vertice2_neighbours = get_neighbors_at(graph, common_I_neighbour_vertices_to_join[1], layer)

        if common_I_neighbour_vertices_to_join[1] not in common_vertice1_neighbours:
            raise ValueError('vertices to join with common I neighbour are not connected')
        if 1 > len(set(common_vertice1_neighbours).intersection(set(common_vertice2_neighbours))) > 2:
            raise ValueError('vertices to join with common I neighbour are wrongly connected')

        noncommon_vertice1_neighbours = get_neighbors_at(graph, noncommon_I_neighbour_vertices_to_join[0], layer)
        noncommon_vertice2_neighbours = get_neighbors_at(graph, noncommon_I_neighbour_vertices_to_join[1], layer)

        if noncommon_I_neighbour_vertices_to_join[1] in noncommon_vertice1_neighbours:
            raise ValueError('vertices to join with non-common I neighbour are connected')
        if 1 > len(set(noncommon_vertice1_neighbours).intersection(set(noncommon_vertice2_neighbours))) > 2:
            raise ValueError('vertices to join with common I neighbour are wrongly connected')
