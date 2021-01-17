from typing import List

from networkx import Graph
from agh_graphs.production import Production
from agh_graphs.utils import get_neighbors_at, join_overlapping_vertices, get_common_neighbors

from agh_graphs.visualize import visualize_graph_3d
from matplotlib import pyplot


def common_elements(list1, list2):
    return list(set(list1).intersection(list2))


def are_connected(graph, vertices):
    for v1, v2 in [(vertices[i], vertices[j])
                   for i in range(len(vertices))
                   for j in range(i + 1, len(vertices))]:
        if not graph.has_edge(v1, v2):
            return False
    return True


class P7(Production):
    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        layer, to_merge = self.__check_prod_input(graph, prod_input)

        for v1, v2 in to_merge:
            join_overlapping_vertices(graph, v1, v2, layer)

        return []


    @staticmethod
    def __check_prod_input(graph: Graph, prod_input: List[str]):

        # Check number of vertices delivered
        if len(prod_input) != 6:
            raise ValueError('Wrong number of interiors in prod_input (6 required)')

        nodes = [(node_id, graph.nodes()[node_id]) for node_id in prod_input]
        up_layer_nodes = [node_id for node_id, data in nodes if data['label'] == 'i']
        down_layer_nodes = [node_id for node_id, data in nodes if data['label'] == 'I']
        if len(up_layer_nodes) != 2:
            raise ValueError('Wrong number of interiors in first layer (2 required)')
        if len(down_layer_nodes) != 4:
            raise ValueError('Wrong number of interiors in second layer (4 required)')

        # Check layers
        up_layer = graph.nodes()[up_layer_nodes[0]]['layer']
        down_layer = graph.nodes()[down_layer_nodes[0]]['layer']
        if any(graph.nodes()[node]['layer'] != up_layer for node in up_layer_nodes):
            raise ValueError('"i" interiors are not in the same layer')
        if any(graph.nodes()[node]['layer'] != down_layer for node in down_layer_nodes):
            raise ValueError('"I" interiors are not in the same layer')
        if up_layer + 1 != down_layer:
            raise ValueError('Upper layer is not right above lower one')

        # Check connections between delivered vertices
        interior_neighbours0 = [node_id for node_id in graph.neighbors(up_layer_nodes[0])
                                if graph.nodes()[node_id]['label'] == 'I']
        interior_neighbours1 = [node_id for node_id in graph.neighbors(up_layer_nodes[1])
                                if graph.nodes()[node_id]['label'] == 'I']
        if len(interior_neighbours0) != len(interior_neighbours1) != 2:
            raise ValueError('Upper interiors not connected properly to lower ones')
        if len(common_elements(interior_neighbours0, interior_neighbours1)) != 0:
            raise ValueError('Upper interiors not connected properly to lower ones')
        if len(common_elements(interior_neighbours0, down_layer_nodes)) != 2:
            raise ValueError('Upper interiors not connected properly to lower ones')
        if len(common_elements(interior_neighbours1, down_layer_nodes)) != 2:
            raise ValueError('Upper interiors not connected properly to lower ones')

        # Check correctness of the graph connections

        def check_structure(interior_nodes, layer_num):
            for interior_node in interior_nodes:
                neighbours = get_neighbors_at(graph, interior_node, layer_num)
                if len(neighbours) > 3:
                    raise ValueError('Wrong number of neighbours of an interior vertex')
                for n in neighbours:
                    if graph.nodes()[n]['label'] != "E":
                        raise ValueError('Vertex does not have "E" label')

            common_neighbors = get_common_neighbors(graph, interior_nodes[0], interior_nodes[1],
                                                    layer_num)
            if len(common_neighbors) > 2:
                raise ValueError('Interiors have more than 2 common neighbors')

        # Check correctness of upper layer
        check_structure(up_layer_nodes, up_layer)
        # Check correctness of lower layer
        check_structure(interior_neighbours0, down_layer)
        check_structure(interior_neighbours1, down_layer)

        # check nodes with the same position
        n1 = sorted(set(
            get_neighbors_at(graph, interior_neighbours0[0], down_layer) +
            get_neighbors_at(graph, interior_neighbours0[1], down_layer)
        ))

        n2 = sorted(set(
            get_neighbors_at(graph, interior_neighbours1[0], down_layer) +
            get_neighbors_at(graph, interior_neighbours1[1], down_layer)
        ))
        c = common_elements(n1, n2)
        if len(c) != 1:
            raise ValueError('There is not exactly 1 common vertex on the line')
        nn = [x for x in graph.neighbors(c[0]) if graph.nodes()[x]['label'] == 'I']
        if len(common_elements(nn, prod_input)) != 2:
            raise ValueError('Wrong number of interior neighbours of the common vertex')

        n1.remove(c[0])
        n2.remove(c[0])

        n1_pos = [graph.nodes()[n]['position'] for n in n1]
        n2_pos = [graph.nodes()[n]['position'] for n in n2]
        n1 = [n for n in n1 for pos in n2_pos if graph.nodes()[n]['position'] == pos]
        n2 = [n for n in n2 for pos in n1_pos if graph.nodes()[n]['position'] == pos]
        if len(n1) != 2:
            raise ValueError('There are not exactly 2 vertices with the same position')
        if len(n2) != 2:
            raise ValueError('There are not exactly 2 vertices with the same position')
        if not are_connected(graph, n1):
            raise ValueError('Vertices on the line not connected')
        if not are_connected(graph, n2):
            raise ValueError('Vertices on the line not connected')
        a1 = [v for v in n1 if len(common_elements([x for x in graph.neighbors(v) if graph.nodes()[x]['label'] == 'I'], prod_input)) == 2]
        a2 = [v for v in n2 if len(common_elements([x for x in graph.neighbors(v) if graph.nodes()[x]['label'] == 'I'], prod_input)) == 2]
        if len(a1) != 1:
            raise ValueError('Wrong interior connections for vertices on the line')
        if len(a2) != 1:
            raise ValueError('Wrong interior connections for vertices on the line')
        if not are_connected(graph, [a1[0], c[0]]):
            raise ValueError('Vertices on the line not connected')
        if not are_connected(graph, [a2[0], c[0]]):
            raise ValueError('Vertices on the line not connected')
        return down_layer, zip(n1, n2)
