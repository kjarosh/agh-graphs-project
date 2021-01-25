import unittest

from matplotlib import pyplot
from networkx import Graph
from math import isclose

from agh_graphs.productions.p1 import P1
from agh_graphs.productions.p2 import P2
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, get_node_at
from agh_graphs.visualize import visualize_graph_3d
from tests.utils import visualize_tests

eps = 1e-6


class P2Test(unittest.TestCase):
    def test_happy_path(self):
        graph = Graph()
        e1 = gen_name()
        e2 = gen_name()
        e3 = gen_name()
        graph.add_node(e1, layer=0, position=(1.0, 2.0), label='E')
        graph.add_node(e2, layer=0, position=(1.0, 1.0), label='E')
        graph.add_node(e3, layer=0, position=(2.0, 1.0), label='E')

        graph.add_edge(e1, e2)
        graph.add_edge(e1, e3)
        graph.add_edge(e2, e3)

        i = add_interior(graph, e1, e2, e3)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        [i1, i2] = P2().apply(graph, [i])

        self.assertIsNotNone(get_node_at(graph, 1, (1.0, 2.0)))
        self.assertIsNotNone(get_node_at(graph, 1, (1.0, 1.0)))
        self.assertIsNotNone(get_node_at(graph, 1, (2.0, 1.0)))
        self.assertIsNotNone(get_node_at(graph, 1, (1.5, 1.0)))

        (i1_x, i1_y) = graph.nodes[i1]['position']
        (i2_x, i2_y) = graph.nodes[i2]['position']
        self.assertTrue(isclose(i1_x, 1.166666, rel_tol=eps))
        self.assertTrue(isclose(i1_y, 1.333333, rel_tol=eps))
        self.assertTrue(isclose(i2_x, 1.5, rel_tol=eps))
        self.assertTrue(isclose(i2_y, 1.333333, rel_tol=eps))

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

    def test_integrity(self):
        graph = Graph()
        initial_node_name = gen_name()
        graph.add_node(initial_node_name, layer=0, position=(0.5, 0.5), label='E')

        [i1, i2] = P1().apply(graph, [initial_node_name])
        [i1_1, i1_2] = P2().apply(graph, [i1])
        [i2_1, i2_2] = P2().apply(graph, [i2])
        [i3_1, i3_2] = P2().apply(graph, [i1_1])

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        [i4_1, i4_2] = P2().apply(graph, [i1_2])

        self.check_graph_integrity(graph, i1, 'i')
        self.check_graph_integrity(graph, i2, 'i')
        self.check_graph_integrity(graph, i1_1, 'i')
        self.check_graph_integrity(graph, i1_2, 'i')
        self.check_graph_integrity(graph, i2_1, 'I')
        self.check_graph_integrity(graph, i2_2, 'I')
        self.check_graph_integrity(graph, i3_1, 'I')
        self.check_graph_integrity(graph, i3_2, 'I')
        self.check_graph_integrity(graph, i4_1, 'I')
        self.check_graph_integrity(graph, i4_2, 'I')

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

    def check_graph_integrity(self, graph, i_node_id, expected_label):
        i_node_data = graph.nodes[i_node_id]
        i_node_layer = i_node_data['layer']

        self.assertEqual(i_node_data['label'], expected_label)

        neighbors = get_neighbors_at(graph, i_node_id, i_node_layer)
        self.assertEqual(len(neighbors), 3)
        for n_id in neighbors:
            self.assertEqual(graph.nodes[n_id]['label'], 'E')
            n_expected_neighbors = [x for x in neighbors if x != n_id]
            n_neighbors = get_neighbors_at(graph, n_id, i_node_layer)
            for expected_neighbor in n_expected_neighbors:
                self.assertTrue(expected_neighbor in n_neighbors)
