import unittest

from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p2 import P2
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at
from agh_graphs.visualize import visualize_graph_3d
from tests.test_utils import visualize_tests


class P2Test(unittest.TestCase):
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

        [i1, i2] = P2().apply(graph, [i])

        self.assertEqual(len(graph.nodes()), 10)
        self.assertEqual(len(graph.edges()), 19)

        self.assertEqual(graph.nodes[i]['label'], 'i')
        self.assertTrue(graph.has_edge(i, i1))
        self.assertTrue(graph.has_edge(i, i2))

        self.assertEqual(graph.nodes[i1]['label'], 'I')
        self.assertEqual(graph.nodes[i2]['label'], 'I')
        self.assertEqual(graph.nodes[i1]['layer'], graph.nodes[i]['layer'] + 1)
        self.assertEqual(graph.nodes[i2]['layer'], graph.nodes[i]['layer'] + 1)

        i1_neighbors = get_neighbors_at(graph, i1, graph.nodes[i1]['layer'])
        self.assertEqual(len(i1_neighbors), 3)
        i2_neighbors = get_neighbors_at(graph, i2, graph.nodes[i2]['layer'])
        self.assertEqual(len(i2_neighbors), 3)

        common_neighbors = [x for x in i1_neighbors if x in i2_neighbors]

        for n in i1_neighbors:
            if n not in common_neighbors:
                self.assertEqual(graph.nodes[n]['label'], 'E')
                self.assertEqual(len(get_neighbors_at(graph, n, graph.nodes[i1]['layer'])), 3)

        for n in i2_neighbors:
            if n not in common_neighbors:
                self.assertEqual(graph.nodes[n]['label'], 'E')
                self.assertEqual(len(get_neighbors_at(graph, n, graph.nodes[i2]['layer'])), 3)

        for c_neighbor in common_neighbors:
            self.assertEqual(graph.nodes[c_neighbor]['label'], 'E')
            self.assertEqual(len(get_neighbors_at(graph, c_neighbor, graph.nodes[i1]['layer'])), 5)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_i_label(self):
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
        graph.nodes[i]['label'] = 'i'

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        with self.assertRaises(AssertionError):
            P2().apply(graph, [i])

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_links(self):
        graph = Graph()
        e1 = gen_name()
        e2 = gen_name()
        e3 = gen_name()
        graph.add_node(e1, layer=1, position=(1.0, 2.0), label='E')
        graph.add_node(e2, layer=1, position=(1.0, 1.0), label='E')
        graph.add_node(e3, layer=1, position=(2.0, 1.0), label='E')

        graph.add_edge(e1, e2)
        graph.add_edge(e1, e3)

        i = add_interior(graph, e1, e2, e3)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        with self.assertRaises(AssertionError):
            P2().apply(graph, [i])

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_vertex_label(self):
        graph = Graph()
        e1 = gen_name()
        e2 = gen_name()
        e3 = gen_name()
        graph.add_node(e1, layer=1, position=(1.0, 2.0), label='X')
        graph.add_node(e2, layer=1, position=(1.0, 1.0), label='E')
        graph.add_node(e3, layer=1, position=(2.0, 1.0), label='E')

        graph.add_edge(e1, e2)
        graph.add_edge(e1, e3)

        i = add_interior(graph, e1, e2, e3)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        with self.assertRaises(AssertionError):
            P2().apply(graph, [i])

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_vertex_count(self):
        graph = Graph()
        e1 = gen_name()
        e2 = gen_name()
        e3 = gen_name()
        graph.add_node(e1, layer=1, position=(1.0, 2.0), label='I')
        graph.add_node(e2, layer=1, position=(1.0, 1.0), label='E')
        graph.add_node(e3, layer=1, position=(2.0, 1.0), label='E')

        graph.add_edge(e1, e2)
        graph.add_edge(e1, e3)
        graph.add_edge(e2, e3)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        with self.assertRaises(AssertionError):
            P2().apply(graph, [e1])

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
