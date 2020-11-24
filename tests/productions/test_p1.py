import unittest

from networkx import Graph

from productions.p1 import P1
from utils import gen_name, get_node_at


class P1Test(unittest.TestCase):
    def test_happy_path(self):
        graph = Graph()
        initial_node = gen_name()
        graph.add_node(initial_node, layer=0, position=(0.5, 0.5), label='E')

        P1().apply(0, graph)

        nodes_data = graph.nodes(data=True)

        self.assertEqual(len(graph.nodes()), 7)
        self.assertEqual(len(graph.edges()), 13)

        # check the initial node
        initial_node_data = nodes_data[initial_node]
        self.assertEqual(initial_node_data['layer'], 0)
        self.assertEqual(initial_node_data['position'], (0.5, 0.5))
        self.assertEqual(initial_node_data['label'], 'e')

        # check other nodes
        vx_bl = get_node_at(graph, 1, (0, 0))
        vx_br = get_node_at(graph, 1, (1, 0))
        vx_tl = get_node_at(graph, 1, (0, 1))
        vx_tr = get_node_at(graph, 1, (1, 1))
        self.assertIsNotNone(vx_bl)
        self.assertIsNotNone(vx_br)
        self.assertIsNotNone(vx_tl)
        self.assertIsNotNone(vx_tr)
        self.assertEqual(nodes_data[vx_bl]['label'], 'E')
        self.assertEqual(nodes_data[vx_br]['label'], 'E')
        self.assertEqual(nodes_data[vx_tl]['label'], 'E')
        self.assertEqual(nodes_data[vx_tr]['label'], 'E')

        vx_i1 = get_node_at(graph, 1, (2 / 3, 1 / 3))
        vx_i2 = get_node_at(graph, 1, (1 / 3, 2 / 3))
        self.assertIsNotNone(vx_i1)
        self.assertIsNotNone(vx_i2)
        self.assertEqual(nodes_data[vx_i1]['label'], 'I')
        self.assertEqual(nodes_data[vx_i2]['label'], 'I')

        self.assertTrue(graph.has_edge(initial_node, vx_i1))
        self.assertTrue(graph.has_edge(initial_node, vx_i2))
        self.assertTrue(graph.has_edge(vx_tl, vx_tr))
        self.assertTrue(graph.has_edge(vx_tr, vx_br))
        self.assertTrue(graph.has_edge(vx_br, vx_bl))
        self.assertTrue(graph.has_edge(vx_bl, vx_tl))
        self.assertTrue(graph.has_edge(vx_bl, vx_tr))
        self.assertTrue(graph.has_edge(vx_i1, vx_bl))
        self.assertTrue(graph.has_edge(vx_i1, vx_br))
        self.assertTrue(graph.has_edge(vx_i1, vx_tr))
        self.assertTrue(graph.has_edge(vx_i2, vx_bl))
        self.assertTrue(graph.has_edge(vx_i2, vx_tl))
        self.assertTrue(graph.has_edge(vx_i2, vx_tr))

    def test_different_position(self):
        graph = Graph()
        graph.add_node(gen_name(), layer=0, position=(2, 2), label='E')

        P1().apply(0, graph)

        # check other nodes
        vx_bl = get_node_at(graph, 1, (0, 0))
        vx_br = get_node_at(graph, 1, (4, 0))
        vx_tl = get_node_at(graph, 1, (0, 4))
        vx_tr = get_node_at(graph, 1, (4, 4))
        self.assertIsNotNone(vx_bl)
        self.assertIsNotNone(vx_br)
        self.assertIsNotNone(vx_tl)
        self.assertIsNotNone(vx_tr)

    def test_wrong_layer(self):
        graph = Graph()
        graph.add_node(gen_name(), layer=1, position=(0.5, 0.5), label='E')

        P1().apply(1, graph)

        self.assertEqual(len(graph.nodes()), 1)

    def test_wrong_label(self):
        graph = Graph()
        graph.add_node(gen_name(), layer=0, position=(0.5, 0.5), label='e')

        P1().apply(0, graph)

        self.assertEqual(len(graph.nodes()), 1)
