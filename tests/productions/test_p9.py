import unittest

from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p9 import P9
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, get_node_at
from agh_graphs.visualize import visualize_graph_3d
from tests.utils import visualize_tests


class P9Test(unittest.TestCase):
    def test_happy_path(self):
        graph = Graph()
        e1 = gen_name()
        e2 = gen_name()
        e3 = gen_name()
        graph.add_node(e1, layer=1, position=(1.0, 2.0), label='E')
        graph.add_node(e2, layer=1, position=(1.0, 1.0), label='E')
        graph.add_node(e3, layer=1, position=(2.0, 1.0), label='E')

        graph.add_edge(e1, e2)
        graph.add_edge(e1, e3)
        graph.add_edge(e2, e3)

        i = add_interior(graph, e1, e2, e3)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        [i1] = P9().apply(graph, [i])

        # if correct number of nodes and edges
        self.assertEqual(len(graph.nodes()), 8)
        self.assertEqual(len(graph.edges()), 13)

        # if cross-layer interior connections
        self.assertEqual(graph.nodes[i]['label'], 'i')
        self.assertTrue(graph.has_edge(i, i1))

        # if new interior has correct label and layer
        self.assertEqual(graph.nodes[i1]['label'], 'I')
        self.assertEqual(graph.nodes[i1]['layer'], graph.nodes[i]['layer'] + 1)

        # if new interior has 3 neighbors
        i1_neighbors = get_neighbors_at(graph, i1, graph.nodes[i1]['layer'])
        self.assertEqual(len(i1_neighbors), 3)

        # if new nodes are in correct positions
        new_e1 = get_node_at(graph, 2, (1.0, 2.0))
        new_e2 = get_node_at(graph, 2, (1.0, 1.0))
        new_e3 = get_node_at(graph, 2, (2.0, 1.0))
        self.assertIsNotNone(new_e1)
        self.assertIsNotNone(new_e2)
        self.assertIsNotNone(new_e3)

        # if each vertex has correct label
        for n in i1_neighbors:
            self.assertEqual(graph.nodes[n]['label'], 'E')

        # if each vertex has correct number of neighbors
        for n in i1_neighbors:
            node_neighbors = get_neighbors_at(graph, n, graph.nodes[n]['layer'])
            self.assertEqual(len(node_neighbors), 3)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
