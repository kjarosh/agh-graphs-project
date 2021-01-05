import unittest

from networkx import Graph

from agh_graphs.derivations.derivation_a import DerivationA
from agh_graphs.utils import gen_name, centroid


class DerivationATest(unittest.TestCase):

    def test_if_output_correct(self):
        graph = Graph()
        initial_node_name = gen_name()
        graph.add_node(initial_node_name, layer=0, position=(0.5, 0.5), label='E')
        bottom_left, bottom_right, top_left, top_right = (0, 0), (1, 0), (0, 1), (1, 1)
        DerivationA().run(graph, [bottom_left, bottom_right, top_left, top_right])

        # check number of nodes and edges
        self.assertEqual(len(graph.nodes()), 13)
        self.assertEqual(len(graph.edges()), 26)

        # check layer, labels and positions of nodes
        # layer 0
        self.assertEqual(len(self.find_nodes(graph, layer=0, label='e', position=(0.5, 0.5))), 1)
        e0 = self.find_nodes(graph, layer=0, label='e', position=(0.5, 0.5))[0]

        # layer 1
        i_left_pos = centroid(bottom_left, top_left, top_right)
        i_right_pos = centroid(bottom_left, bottom_right, top_right)
        self.assertEqual(len(self.find_nodes(graph, layer=1, label='i', position=i_left_pos)), 1)
        i1_left = self.find_nodes(graph, layer=1, label='i', position=i_left_pos)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=1, label='i', position=i_right_pos)), 1)
        i1_right = self.find_nodes(graph, layer=1, label='i', position=i_right_pos)[0]

        self.assertEqual(len(self.find_nodes(graph, layer=1, label='E', position=bottom_left)), 1)
        e1_bl = self.find_nodes(graph, layer=1, label='E', position=bottom_left)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=1, label='E', position=bottom_right)), 1)
        e1_br = self.find_nodes(graph, layer=1, label='E', position=bottom_right)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=1, label='E', position=top_left)), 1)
        e1_tl = self.find_nodes(graph, layer=1, label='E', position=top_left)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=1, label='E', position=top_right)), 1)
        e1_tr = self.find_nodes(graph, layer=1, label='E', position=top_right)[0]

        # layer 2
        self.assertEqual(len(self.find_nodes(graph, layer=2, label='I', position=i_left_pos)), 1)
        i2_left = self.find_nodes(graph, layer=2, label='I', position=i_left_pos)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=2, label='I', position=i_right_pos)), 1)
        i2_right = self.find_nodes(graph, layer=2, label='I', position=i_right_pos)[0]

        self.assertEqual(len(self.find_nodes(graph, layer=2, label='E', position=bottom_left)), 1)
        e2_bl = self.find_nodes(graph, layer=2, label='E', position=bottom_left)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=2, label='E', position=bottom_right)), 1)
        e2_br = self.find_nodes(graph, layer=2, label='E', position=bottom_right)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=2, label='E', position=top_left)), 1)
        e2_tl = self.find_nodes(graph, layer=2, label='E', position=top_left)[0]
        self.assertEqual(len(self.find_nodes(graph, layer=2, label='E', position=top_right)), 1)
        e2_tr = self.find_nodes(graph, layer=2, label='E', position=top_right)[0]

        # check edges
        # edges between layers
        self.assertTrue(graph.has_edge(e0, i1_left))
        self.assertTrue(graph.has_edge(e0, i1_right))

        self.assertTrue(graph.has_edge(i1_left, i2_left))
        self.assertTrue(graph.has_edge(i1_right, i2_right))

        # interior - E
        # layer 1
        self.assertTrue(graph.has_edge(i1_left, e1_bl))
        self.assertTrue(graph.has_edge(i1_left, e1_tl))
        self.assertTrue(graph.has_edge(i1_left, e1_tr))
        self.assertTrue(graph.has_edge(i1_right, e1_bl))
        self.assertTrue(graph.has_edge(i1_right, e1_br))
        self.assertTrue(graph.has_edge(i1_right, e1_tr))

        # layer 2
        self.assertTrue(graph.has_edge(i2_left, e2_bl))
        self.assertTrue(graph.has_edge(i2_left, e2_tl))
        self.assertTrue(graph.has_edge(i2_left, e2_tr))
        self.assertTrue(graph.has_edge(i2_right, e2_bl))
        self.assertTrue(graph.has_edge(i2_right, e2_br))
        self.assertTrue(graph.has_edge(i2_right, e2_tr))

        # E - E
        # layer 1
        self.assertTrue(graph.has_edge(e1_bl, e1_br))
        self.assertTrue(graph.has_edge(e1_bl, e1_tl))
        self.assertTrue(graph.has_edge(e1_tr, e1_br))
        self.assertTrue(graph.has_edge(e1_tr, e1_tl))
        self.assertTrue(graph.has_edge(e1_bl, e1_tr))

        # layer 2
        self.assertTrue(graph.has_edge(e2_bl, e2_br))
        self.assertTrue(graph.has_edge(e2_bl, e2_tl))
        self.assertTrue(graph.has_edge(e2_tr, e2_br))
        self.assertTrue(graph.has_edge(e2_tr, e2_tl))
        self.assertTrue(graph.has_edge(e2_bl, e2_tr))

    def find_nodes(self, graph, layer, label, position=None):
        nodes = [n for n in graph.nodes() if graph.nodes[n]['layer'] == layer
                and graph.nodes[n]['label'] == label
                and (position is None or graph.nodes[n]['position'] == position)]
        return nodes
