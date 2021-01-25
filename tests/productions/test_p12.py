import unittest

from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p12 import P12
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, get_node_at
from agh_graphs.visualize import visualize_graph_3d
from tests.utils import visualize_tests


class P12Test(unittest.TestCase):
    def test_happy_path(self):
        graph = Graph()
        e1 = gen_name()
        e2 = gen_name()
        e3 = gen_name()
        e4 = gen_name()
        e1_1 = gen_name()
        e1_2 = gen_name()
        e1_3 = gen_name()
        e2_1 = gen_name()
        e2_2 = gen_name()
        e2_4 = gen_name()
        e3_5 = gen_name()

        graph.add_node(e1, layer=1, position=(1.0, 1.0), label='E')
        graph.add_node(e2, layer=1, position=(2.0, 2.0), label='E')
        graph.add_node(e3, layer=1, position=(1.0, 2.0), label='E')
        graph.add_node(e4, layer=1, position=(2.0, 1.0), label='E')
        graph.add_node(e1_1, layer=2, position=(1.0, 1.0), label='E')
        graph.add_node(e1_2, layer=2, position=(2.0, 2.0), label='E')
        graph.add_node(e1_3, layer=2, position=(1.0, 2.0), label='E')
        graph.add_node(e2_1, layer=2, position=(1.0, 1.0), label='E')
        graph.add_node(e2_2, layer=2, position=(2.0, 2.0), label='E')
        graph.add_node(e2_4, layer=2, position=(2.0, 1.0), label='E')
        graph.add_node(e3_5, layer=2, position=(2.0, 3.0), label='E')

        graph.add_edge(e1, e2)
        graph.add_edge(e1, e3)
        graph.add_edge(e1, e4)
        graph.add_edge(e2, e3)
        graph.add_edge(e2, e4)
        graph.add_edge(e1_1, e1_2)
        graph.add_edge(e1_1, e1_3)
        graph.add_edge(e1_2, e1_3)
        graph.add_edge(e2_1, e2_2)
        graph.add_edge(e2_1, e2_4)
        graph.add_edge(e2_2, e2_4)
        graph.add_edge(e3_5, e1_2)
        graph.add_edge(e3_5, e1_3)

        i1 = add_interior(graph, e1, e2, e3)
        i2 = add_interior(graph, e1, e2, e4)
        i1_1 = add_interior(graph, e1_1, e1_2, e1_3)
        i2_1 = add_interior(graph, e2_1, e2_2, e2_4)
        i3_1 = add_interior(graph, e3_5, e1_2, e1_3)
        graph.nodes[i1]['label'] = 'i'
        graph.nodes[i2]['label'] = 'i'

        graph.add_edge(i1, i1_1)
        graph.add_edge(i2, i2_1)
        graph.add_edge(i1, i3_1)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        P12().apply(graph, [i1, i2, i1_1, i2_1])

        # if correct number of nodes and edges
        self.assertEqual(len(graph.nodes()), 14)
        self.assertEqual(len(graph.edges()), 30)

        # if interiors has correct labels, layers and are connected
        self.assertEqual(graph.nodes[i1]['label'], 'i')
        self.assertEqual(graph.nodes[i2]['label'], 'i')
        self.assertEqual(graph.nodes[i1_1]['label'], 'I')
        self.assertEqual(graph.nodes[i2_1]['label'], 'I')
        self.assertEqual(graph.nodes[i1]['layer'], 1)
        self.assertEqual(graph.nodes[i2]['layer'], 1)
        self.assertEqual(graph.nodes[i1_1]['layer'], 2)
        self.assertEqual(graph.nodes[i2_1]['layer'], 2)
        self.assertTrue(graph.has_edge(i1, i1_1))
        self.assertTrue(graph.has_edge(i2, i2_1))

        # if each interior has 3 neighbors
        i1_neighbors = get_neighbors_at(graph, i1, graph.nodes[i1]['layer'])
        self.assertEqual(len(i1_neighbors), 3)
        i2_neighbors = get_neighbors_at(graph, i2, graph.nodes[i2]['layer'])
        self.assertEqual(len(i2_neighbors), 3)
        i1_1_neighbors = get_neighbors_at(graph, i1_1, graph.nodes[i1_1]['layer'])
        self.assertEqual(len(i1_1_neighbors), 3)
        i2_1_neighbors = get_neighbors_at(graph, i2_1, graph.nodes[i2_1]['layer'])
        self.assertEqual(len(i2_1_neighbors), 3)

        # if nodes in lower layer exists and are correctly connected
        new_e1 = get_node_at(graph, 2, (1.0, 1.0))
        new_e2 = get_node_at(graph, 2, (2.0, 2.0))
        new_e3 = get_node_at(graph, 2, (1.0, 2.0))
        new_e4 = get_node_at(graph, 2, (2.0, 1.0))
        self.assertIsNotNone(new_e1)
        self.assertIsNotNone(new_e2)
        self.assertIsNotNone(new_e3)
        self.assertIsNotNone(new_e4)
        self.assertTrue(graph.has_edge(new_e1, new_e2))
        self.assertTrue(graph.has_edge(new_e1, new_e3))
        self.assertTrue(graph.has_edge(new_e1, new_e4))
        self.assertTrue(graph.has_edge(new_e2, new_e3))
        self.assertTrue(graph.has_edge(new_e2, new_e4))

        # if lower interiors connect with all 4 vertices
        all_neighbors = i1_1_neighbors + i2_1_neighbors
        all_neighbors = list(dict.fromkeys(all_neighbors))  # remove duplicates
        self.assertEqual(len(all_neighbors), 4)

        # if each vertex has correct label
        for n in all_neighbors:
            self.assertEqual(graph.nodes[n]['label'], 'E')

        # if each vertex has correct number of neighbors (based on neighbour interiors count)
        for n in all_neighbors:
            node_neighbors = get_neighbors_at(graph, n, graph.nodes[n]['layer'])
            i_neighbors = [x for x in node_neighbors if graph.nodes[x]['label'] == 'I']
            if len(i_neighbors) == 1:
                self.assertEqual(len(node_neighbors), 3)
            elif len(i_neighbors) == 2:
                self.assertEqual(len(node_neighbors), 5)
            else:
                self.assertEqual(len(node_neighbors), 7)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
