import unittest

from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p13 import P13
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, get_node_at
from agh_graphs.visualize import visualize_graph_3d
from tests.utils import visualize_tests


class P13Test(unittest.TestCase):
    def test_happy_path(self):
        graph = Graph()

        e1_1, e2_1, e3_1, e4_1 = [gen_name() for _ in range(4)]
        graph.add_node(e1_1, layer=1, position=(0.0, 0.0), label='E')
        graph.add_node(e2_1, layer=1, position=(1.0, 0.0), label='E')
        graph.add_node(e3_1, layer=1, position=(0.5, 0.5), label='E')
        graph.add_node(e4_1, layer=1, position=(0.0, 1.0), label='E')

        graph.add_edge(e1_1, e2_1)
        graph.add_edge(e1_1, e3_1)
        graph.add_edge(e1_1, e4_1)
        graph.add_edge(e2_1, e3_1)
        graph.add_edge(e3_1, e4_1)

        i1_1 = add_interior(graph, e1_1, e2_1, e3_1)
        i2_1 = add_interior(graph, e1_1, e3_1, e4_1)
        graph.nodes[i1_1]['label'] = 'i'
        graph.nodes[i2_1]['label'] = 'i'

        e1_2, e2_2, e3_2, e4_2, e5_2 = [gen_name() for _ in range(5)]
        graph.add_node(e1_2, layer=2, position=(0.0, 0.0), label='E')
        graph.add_node(e5_2, layer=2, position=(0.0, 0.0), label='E')
        graph.add_node(e2_2, layer=2, position=(1.0, 0.0), label='E')
        graph.add_node(e3_2, layer=2, position=(0.5, 0.5), label='E')
        graph.add_node(e4_2, layer=2, position=(0.0, 1.0), label='E')

        graph.add_edge(e1_2, e2_2)
        graph.add_edge(e1_2, e3_2)
        graph.add_edge(e5_2, e4_2)
        graph.add_edge(e5_2, e3_2)
        graph.add_edge(e2_2, e3_2)
        graph.add_edge(e3_2, e4_2)

        i1_2 = add_interior(graph, e1_2, e2_2, e3_2)
        i2_2 = add_interior(graph, e5_2, e3_2, e4_2)

        graph.add_edge(i1_1, i1_2)
        graph.add_edge(i2_1, i2_2)

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        P13().apply(graph, [i1_1, i2_1, i1_2, i2_2])

        # based on test_p12
        # if correct number of nodes and edges
        self.assertEqual(len(graph.nodes()), 12)
        self.assertEqual(len(graph.edges()), 24)

        # if interiors has correct labels, layers and are connected
        self.assertEqual(graph.nodes[i1_1]['label'], 'i')
        self.assertEqual(graph.nodes[i2_1]['label'], 'i')
        self.assertEqual(graph.nodes[i1_1]['layer'], 1)
        self.assertEqual(graph.nodes[i2_1]['layer'], 1)
        self.assertEqual(graph.nodes[i1_2]['label'], 'I')
        self.assertEqual(graph.nodes[i2_2]['label'], 'I')
        self.assertEqual(graph.nodes[i1_2]['layer'], 2)
        self.assertEqual(graph.nodes[i2_2]['layer'], 2)
        self.assertTrue(graph.has_edge(i1_1, i1_2))
        self.assertTrue(graph.has_edge(i2_1, i2_2))

        # if each interior has 3 neighbors on the corresponding layer
        i1_1_neighbors = get_neighbors_at(graph, i1_1, graph.nodes[i1_1]['layer'])
        self.assertEqual(len(i1_1_neighbors), 3)
        i2_1_neighbors = get_neighbors_at(graph, i2_1, graph.nodes[i2_1]['layer'])
        self.assertEqual(len(i2_1_neighbors), 3)
        i1_2_neighbors = get_neighbors_at(graph, i1_2, graph.nodes[i1_2]['layer'])
        self.assertEqual(len(i1_2_neighbors), 3)
        i2_2_neighbors = get_neighbors_at(graph, i2_2, graph.nodes[i2_2]['layer'])
        self.assertEqual(len(i2_2_neighbors), 3)

        # if nodes in lower layer exists and are correctly connected
        new_e1_2 = get_node_at(graph, 2, (0.0, 0.0))
        new_e2_2 = get_node_at(graph, 2, (1.0, 0.0))
        new_e3_2 = get_node_at(graph, 2, (0.5, 0.5))
        new_e4_2 = get_node_at(graph, 2, (0.0, 1.0))
        self.assertIsNotNone(new_e1_2)
        self.assertIsNotNone(new_e2_2)
        self.assertIsNotNone(new_e3_2)
        self.assertIsNotNone(new_e4_2)
        self.assertTrue(graph.has_edge(new_e1_2, new_e2_2))
        self.assertTrue(graph.has_edge(new_e1_2, new_e3_2))
        self.assertTrue(graph.has_edge(new_e1_2, new_e4_2))
        self.assertTrue(graph.has_edge(new_e2_2, new_e3_2))
        self.assertTrue(graph.has_edge(new_e3_2, new_e4_2))

        # if lower interiors connect with all 4 vertices
        all_neighbors = i1_2_neighbors + i2_2_neighbors
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
