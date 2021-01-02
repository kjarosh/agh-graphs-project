from typing import List

from networkx import Graph
from agh_graphs.production import Production
from agh_graphs.utils import get_neighbors_at, join_overlapping_vertices, get_common_neighbors

from agh_graphs.visualize import visualize_graph_3d
from matplotlib import pyplot


def common_elements(list1, list2):
    return list(set(list1).intersection(list2))


def is_triangle(graph, vertices):
    for v1, v2 in [(vertices[i], vertices[j])
                   for i in range(len(vertices))
                   for j in range(i + 1, len(vertices))]:
        if not graph.has_edge(v1, v2):
            return False
    return True


class P7(Production):
    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        layer, to_merge = self.__check_prod_input(graph, prod_input)

        visualize_graph_3d(graph)
        pyplot.show()
        for v1, v2 in to_merge:
            join_overlapping_vertices(graph, v1, v2, layer)

        visualize_graph_3d(graph)
        pyplot.show()

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
                if len(neighbours) != 3:
                    raise ValueError('Wrong number of neighbours of an interior vertex')
                for n in neighbours:
                    if graph.nodes()[n]['label'] != "E":
                        raise ValueError('Vertex does not have "E" label')
                if not is_triangle(graph, neighbours):
                    raise ValueError('Neighbours of an interior vertex are not a triangle')

            common_neighbors = get_common_neighbors(graph, interior_nodes[0], interior_nodes[1],
                                                    layer_num)
            if len(common_neighbors) != 2:
                raise ValueError('Interiors do not have 2 common neighbors')

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

        if len(n1) != 3:
            raise ValueError('There are not exactly 3 unique vertices')
        if len(n2) != 3:
            raise ValueError('There are not exactly 3 unique vertices')

        n1_pos = [graph.nodes()[n]['position'] for n in n1]
        n2_pos = [graph.nodes()[n]['position'] for n in n2]
        n1 = [n for n in n1 for pos in n2_pos if graph.nodes()[n]['position'] == pos]
        n2 = [n for n in n2 for pos in n1_pos if graph.nodes()[n]['position'] == pos]
        if len(n1) != 2:
            raise ValueError('There are not exactly 2 vertices with the same position')
        if len(n2) != 2:
            raise ValueError('There are not exactly 2 vertices with the same position')
        return down_layer, zip(n1, n2)


def createCorrectGraph():
    graph = Graph()
    e01 = "e01"
    e02 = "e02"
    e03 = "e03"
    e04 = "e04"
    i1 = "i1"
    i2 = "i2"
    I1 = "I1"
    I2 = "I2"
    I3 = "I3"
    I4 = "I4"
    e11 = "e11"
    e12 = "e12"
    e13 = "e13"
    e14 = "e14"
    e15 = "e15"
    e16 = "e16"
    e17 = "e17"

    graph.add_node(e01, layer=0, position=(0.0, 0.0), label='E')
    graph.add_node(e02, layer=0, position=(0.0, 2.0), label='E')
    graph.add_node(e03, layer=0, position=(2.0, 0.0), label='E')
    graph.add_node(e04, layer=0, position=(2.0, 2.0), label='E')
    graph.add_node(i2, layer=0, position=(0.5, 1.5), label='i')
    graph.add_node(i1, layer=0, position=(1.5, 0.5), label='i')

    graph.add_node(I1, layer=1, position=(0.5, 0.5), label='I')
    graph.add_node(I2, layer=1, position=(0.5, 1.5), label='I')
    graph.add_node(I3, layer=1, position=(1.5, 0.5), label='I')
    graph.add_node(I4, layer=1, position=(1.5, 1.5), label='I')
    graph.add_node(e11, layer=1, position=(0.0, 0.0), label='E')
    graph.add_node(e12, layer=1, position=(0.0, 2.0), label='E')
    graph.add_node(e13, layer=1, position=(2.0, 0.0), label='E')
    graph.add_node(e14, layer=1, position=(2.0, 2.0), label='E')
    graph.add_node(e15, layer=1, position=(2.0, 2.0), label='E')
    graph.add_node(e16, layer=1, position=(1.0, 1.0), label='E')
    graph.add_node(e17, layer=1, position=(1.0, 1.0), label='E')
    # upper layer edges
    graph.add_edge(e01, i1)
    graph.add_edge(e01, i2)
    graph.add_edge(e04, i1)
    graph.add_edge(e04, i2)
    graph.add_edge(e03, i1)
    graph.add_edge(e02, i2)

    graph.add_edge(e01, e02)
    graph.add_edge(e02, e04)
    graph.add_edge(e01, e04)

    graph.add_edge(e01, e03)
    graph.add_edge(e04, e03)

    # interlayer connections
    graph.add_edge(i2, I1)
    graph.add_edge(i2, I2)
    graph.add_edge(i1, I3)
    graph.add_edge(i1, I4)

    # lower layer interior connections
    graph.add_edge(I1, e11)
    graph.add_edge(I1, e12)
    graph.add_edge(I1, e16)

    graph.add_edge(I2, e12)
    graph.add_edge(I2, e16)
    graph.add_edge(I2, e14)

    graph.add_edge(I3, e13)
    graph.add_edge(I3, e17)
    graph.add_edge(I3, e11)

    graph.add_edge(I4, e15)
    graph.add_edge(I4, e17)
    graph.add_edge(I4, e13)

    # lower layer edges connections
    graph.add_edge(e11, e12)
    graph.add_edge(e11, e16)
    graph.add_edge(e12, e16)

    graph.add_edge(e14, e16)
    graph.add_edge(e12, e14)

    graph.add_edge(e11, e13)
    graph.add_edge(e13, e17)
    graph.add_edge(e11, e17)

    graph.add_edge(e15, e13)
    graph.add_edge(e15, e17)

    return graph


if __name__ == '__main__':
    graph = createCorrectGraph()
    prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
    [] = P7().apply(graph, prod_input)
