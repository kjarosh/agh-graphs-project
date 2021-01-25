import unittest

from networkx import Graph

from agh_graphs.productions.p5 import P5
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, get_node_at
from agh_graphs.visualize import visualize_graph_layer, visualize_graph_3d
from matplotlib import pyplot

from tests.utils import visualize_tests


class P5Test(unittest.TestCase):
    # add new nodes on given positions with given layer and label
    def create_nodes(self, graph, _layer, _label, vertex_positions):
        nodes = []
        for x, y in vertex_positions:
            e = gen_name()
            graph.add_node(e, layer=_layer, position=(x, y), label=_label)
            nodes.append(e)
        return nodes

    # add chain edges between given nodes
    # nodes = [a, b, c, a] will result in edges between a, b; b, c; c, a
    def create_edges_chain(self, graph, nodes):
        for i in range(len(nodes) - 1):
            graph.add_edge(nodes[i], nodes[i + 1])

    def test_happy_path(self):
        graph = Graph()
        positions = [(1.0, 1.0), (1.0, 2.0), (1.0, 3.0),
                     (2.0, 3.0), (3.0, 3.0), (2.0, 2.0)]

        [e1, e12, e2, e23, e3, e31] = self.create_nodes(graph, 1, 'E', positions)
        self.create_edges_chain(graph, [e1, e12, e2, e23, e3, e31, e1])

        i = add_interior(graph, e1, e2, e3)

        if visualize_tests:
            pyplot.title("Correct input", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()

        [i1, i3, i2a, i2b] = P5().apply(graph, [i])

        if visualize_tests:
            pyplot.title("Correct output", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()

            pyplot.title("Correct output (layer = 1)", fontsize=16)
            visualize_graph_layer(graph, 1)
            pyplot.show()

            pyplot.title("Correct output (layer = 2)", fontsize=16)
            visualize_graph_layer(graph, 2)
            pyplot.show()

        # if correct number of nodes and edges
        self.assertEqual(len(graph.nodes()), 17)
        self.assertEqual(len(graph.edges()), 34)

        # if cross-layer interior connections
        self.assertEqual(graph.nodes[i]['label'], 'i')
        self.assertTrue(graph.has_edge(i, i1))
        self.assertTrue(graph.has_edge(i, i3))
        self.assertTrue(graph.has_edge(i, i2a))
        self.assertTrue(graph.has_edge(i, i2b))

        # if new interiors has correct labels and layers
        self.assertEqual(graph.nodes[i1]['label'], 'I')
        self.assertEqual(graph.nodes[i3]['label'], 'I')
        self.assertEqual(graph.nodes[i2a]['label'], 'I')
        self.assertEqual(graph.nodes[i2b]['label'], 'I')
        self.assertEqual(graph.nodes[i1]['layer'], graph.nodes[i]['layer'] + 1)
        self.assertEqual(graph.nodes[i3]['layer'], graph.nodes[i]['layer'] + 1)
        self.assertEqual(graph.nodes[i2a]['layer'], graph.nodes[i]['layer'] + 1)
        self.assertEqual(graph.nodes[i2b]['layer'], graph.nodes[i]['layer'] + 1)

        # if each new interior has 3 neighbors
        i1_neighbors = get_neighbors_at(graph, i1, graph.nodes[i1]['layer'])
        self.assertEqual(len(i1_neighbors), 3)
        i3_neighbors = get_neighbors_at(graph, i3, graph.nodes[i3]['layer'])
        self.assertEqual(len(i3_neighbors), 3)
        i2a_neighbors = get_neighbors_at(graph, i2a, graph.nodes[i2a]['layer'])
        self.assertEqual(len(i2a_neighbors), 3)
        i2b_neighbors = get_neighbors_at(graph, i2b, graph.nodes[i2b]['layer'])
        self.assertEqual(len(i2b_neighbors), 3)

        # if new nodes are in correct positions
        new_e1 = get_node_at(graph, 2, (1.0, 1.0))
        new_e12 = get_node_at(graph, 2, (1.0, 2.0))
        new_e2 = get_node_at(graph, 2, (1.0, 3.0))
        new_e23 = get_node_at(graph, 2, (2.0, 3.0))
        new_e3 = get_node_at(graph, 2, (3.0, 3.0))
        new_e31 = get_node_at(graph, 2, (2.0, 2.0))
        self.assertIsNotNone(new_e1)
        self.assertIsNotNone(new_e12)
        self.assertIsNotNone(new_e2)
        self.assertIsNotNone(new_e23)
        self.assertIsNotNone(new_e3)
        self.assertIsNotNone(new_e31)

        # if interiors connect with all new 6 vertices
        all_neighbors = i1_neighbors + i3_neighbors + i2a_neighbors + i2b_neighbors
        all_neighbors = list(dict.fromkeys(all_neighbors))  # remove duplicates
        self.assertEqual(len(all_neighbors), 6)

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
            else:  # 4
                self.assertEqual(len(node_neighbors), 9)

    def test_parent_graph(self):
        graph = Graph()
        positions = [(1.0, 1.0), (1.0, 9.0), (9.0, 1.0), 
                     (9.0, 9.0), (5.0, 5.0), (3.0, 7.0), 
                     (7.0, 7.0), (6.0, 6.0), (4.0, 8.0)]

        [e0a, e1, e0b, e0c, e2, e12, e3, e23, e31] = self.create_nodes(graph, 1, 'E', positions)

        self.create_edges_chain(graph, [e0a, e1, e12, e0a, e2, e12])
        self.create_edges_chain(graph, [e0a, e0b, e2, e23, e0b, e3, e23])
        self.create_edges_chain(graph, [e0b, e0c, e3, e31, e0c, e1, e31])

        i_0a_1_12 = add_interior(graph, e0a, e1, e12)
        i_0a_12_2 = add_interior(graph, e0a, e12, e2)
        i_0a_0b_2 = add_interior(graph, e0a, e0b, e2)
        i_0b_2_23 = add_interior(graph, e0b, e2, e23)
        i_0b_23_3 = add_interior(graph, e0b, e23, e3)
        i_0b_0c_3 = add_interior(graph, e0b, e3, e0c)
        i_0c_1_31 = add_interior(graph, e1, e31, e0c)
        i_0c_3_31 = add_interior(graph, e31, e3, e0c)
        i = add_interior(graph, e1, e2, e3)

        if visualize_tests:
            pyplot.title("Correct subgraph input", fontsize=16)
            visualize_graph_layer(graph, 1)
            pyplot.show()

        [i1, i3, i2a, i2b] = P5().apply(graph, [i])

        if visualize_tests:
            pyplot.title("Correct subgraph output", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()

            pyplot.title("Correct subgraph output (layer=1)", fontsize=16)
            visualize_graph_layer(graph, 1)
            pyplot.show()

            pyplot.title("Correct subgraph output (layer=2)", fontsize=16)
            visualize_graph_layer(graph, 2)
            pyplot.show()

        # if edges are unchanged
        self.assertTrue(graph.has_edge(e0a, e1))
        self.assertTrue(graph.has_edge(e1, e12))
        self.assertTrue(graph.has_edge(e12, e0a))
        self.assertTrue(graph.has_edge(e0a, e2))
        self.assertTrue(graph.has_edge(e2, e12))
        self.assertTrue(graph.has_edge(e0a, e0b))
        self.assertTrue(graph.has_edge(e0b, e2))
        self.assertTrue(graph.has_edge(e2, e23))
        self.assertTrue(graph.has_edge(e23, e0b))
        self.assertTrue(graph.has_edge(e0b, e3))
        self.assertTrue(graph.has_edge(e3, e23))
        self.assertTrue(graph.has_edge(e0b, e0c))
        self.assertTrue(graph.has_edge(e0c, e3))
        self.assertTrue(graph.has_edge(e3, e31))
        self.assertTrue(graph.has_edge(e31, e0c))
        self.assertTrue(graph.has_edge(e0c, e1))
        self.assertTrue(graph.has_edge(e1, e31))

        # if interior links are unchanged
        self.assertTrue(graph.has_edge(i, e1))
        self.assertTrue(graph.has_edge(i, e2))
        self.assertTrue(graph.has_edge(i, e3))
        self.assertTrue(graph.has_edge(i_0a_1_12, e0a))
        self.assertTrue(graph.has_edge(i_0a_1_12, e1))
        self.assertTrue(graph.has_edge(i_0a_1_12, e12))
        self.assertTrue(graph.has_edge(i_0a_12_2, e0a))
        self.assertTrue(graph.has_edge(i_0a_12_2, e12))
        self.assertTrue(graph.has_edge(i_0a_12_2, e2))
        self.assertTrue(graph.has_edge(i_0a_0b_2, e0a))
        self.assertTrue(graph.has_edge(i_0a_0b_2, e0b))
        self.assertTrue(graph.has_edge(i_0a_0b_2, e2))
        self.assertTrue(graph.has_edge(i_0b_2_23, e0b))
        self.assertTrue(graph.has_edge(i_0b_2_23, e2))
        self.assertTrue(graph.has_edge(i_0b_2_23, e23))
        self.assertTrue(graph.has_edge(i_0b_23_3, e0b))
        self.assertTrue(graph.has_edge(i_0b_23_3, e23))
        self.assertTrue(graph.has_edge(i_0b_23_3, e3))
        self.assertTrue(graph.has_edge(i_0b_0c_3, e0b))
        self.assertTrue(graph.has_edge(i_0b_0c_3, e3))
        self.assertTrue(graph.has_edge(i_0b_0c_3, e0c))
        self.assertTrue(graph.has_edge(i_0c_1_31, e1))
        self.assertTrue(graph.has_edge(i_0c_1_31, e31))
        self.assertTrue(graph.has_edge(i_0c_1_31, e0c))
        self.assertTrue(graph.has_edge(i_0c_3_31, e31))
        self.assertTrue(graph.has_edge(i_0c_3_31, e3))
        self.assertTrue(graph.has_edge(i_0c_3_31, e0c))

        # if vertex labels are unchanged
        self.assertEqual(graph.nodes[e0a]['label'], 'E')
        self.assertEqual(graph.nodes[e1]['label'], 'E')
        self.assertEqual(graph.nodes[e0b]['label'], 'E')
        self.assertEqual(graph.nodes[e0c]['label'], 'E')
        self.assertEqual(graph.nodes[e2]['label'], 'E')
        self.assertEqual(graph.nodes[e12]['label'], 'E')
        self.assertEqual(graph.nodes[e3]['label'], 'E')
        self.assertEqual(graph.nodes[e23]['label'], 'E')
        self.assertEqual(graph.nodes[e31]['label'], 'E')

        # if number of neighbors is unchanged
        # if each vertex has correct number of neighbors (based on neighbour interiors count)
        for n in [e0a, e1, e0b, e0c, e2, e12, e3, e23, e31]:
            node_neighbors = get_neighbors_at(graph, n, graph.nodes[n]['layer'])
            i_neighbors = [x for x in node_neighbors if graph.nodes[x]['label'] == 'I' or graph.nodes[x]['label'] == 'i']
            e_neighbors = [x for x in node_neighbors if graph.nodes[x]['label'] == 'E' or graph.nodes[x]['label'] == 'e']
            if len(e_neighbors) == len(i_neighbors):
                self.assertEqual(len(node_neighbors), len(i_neighbors) * 2)
            else:
                self.assertEqual(len(node_neighbors), (len(i_neighbors) * 2) + 1)

        # if vertices position is unchanged
        self.assertEqual(graph.nodes[e0a]['position'], (1.0, 1.0))
        self.assertEqual(graph.nodes[e1]['position'], (1.0, 9.0))
        self.assertEqual(graph.nodes[e0b]['position'], (9.0, 1.0))
        self.assertEqual(graph.nodes[e0c]['position'], (9.0, 9.0))
        self.assertEqual(graph.nodes[e2]['position'], (5.0, 5.0))
        self.assertEqual(graph.nodes[e12]['position'], (3.0, 7.0))
        self.assertEqual(graph.nodes[e3]['position'], (7.0, 7.0))
        self.assertEqual(graph.nodes[e23]['position'], (6.0, 6.0))
        self.assertEqual(graph.nodes[e31]['position'], (4.0, 8.0))

    def test_bad_input_vertex_count(self):
        graph = Graph()
        positions = [(1.0, 1.0), (1.0, 3.0),
                     (2.0, 3.0), (3.0, 3.0), (2.0, 2.0)]

        [e1, e2, e23, e3, e31] = self.create_nodes(graph, 1, 'E', positions)
        self.create_edges_chain(graph, [e1, e2, e23, e3, e31, e1])

        i = add_interior(graph, e1, e2, e3)

        with self.assertRaises(AssertionError):
            [i1, i3, i2a, i2b] = P5().apply(graph, [i])
        self.assertEqual(len(graph.nodes()), 6)
        self.assertEqual(len(graph.edges()), 8)

        if visualize_tests:
            pyplot.title("Vertex missing", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_vertex_position(self):
        graph = Graph()
        positions = [(1.0, 1.0), (1.5, 2.0), (1.0, 3.0),
                     (2.0, 3.0), (3.0, 3.0), (2.0, 2.0)]

        [e1, e12, e2, e23, e3, e31] = self.create_nodes(graph, 1, 'E', positions)
        self.create_edges_chain(graph, [e1, e12, e2, e23, e3, e31, e1])

        i = add_interior(graph, e1, e2, e3)

        with self.assertRaises(AssertionError):
            [i1, i3, i2a, i2b] = P5().apply(graph, [i])
        self.assertEqual(len(graph.nodes()), 7)
        self.assertEqual(len(graph.edges()), 9)

        if visualize_tests:
            pyplot.title("Wrong vertex position", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_vertex_label(self):
        graph = Graph()
        positions = [(1.0, 1.0), (1.0, 2.0), (1.0, 3.0),
                     (2.0, 3.0), (3.0, 3.0)]

        [e1, e12, e2, e23, e3] = self.create_nodes(graph, 1, 'E', positions)
        e31 = gen_name()
        graph.add_node(e31, layer=1, position=(2.0, 2.0), label='e')

        self.create_edges_chain(graph, [e1, e12, e2, e23, e3, e31, e1])

        i = add_interior(graph, e1, e2, e3)

        with self.assertRaises(AssertionError):
            [i1, i3, i2a, i2b] = P5().apply(graph, [i])
        self.assertEqual(len(graph.nodes()), 7)
        self.assertEqual(len(graph.edges()), 9)

        if visualize_tests:
            pyplot.title("Wrong 'e' label", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_i_label(self):
        graph = Graph()
        positions = [(1.0, 1.0), (1.0, 2.0), (1.0, 3.0),
                     (2.0, 3.0), (3.0, 3.0), (2.0, 2.0)]

        [e1, e12, e2, e23, e3, e31] = self.create_nodes(graph, 1, 'E', positions)

        self.create_edges_chain(graph, [e1, e12, e2, e23, e3, e31, e1])

        i = add_interior(graph, e1, e2, e3)
        graph.nodes[i]['label'] = 'i'

        with self.assertRaises(AssertionError):
            [i1, i3, i2a, i2b] = P5().apply(graph, [i])
        self.assertEqual(len(graph.nodes()), 7)
        self.assertEqual(len(graph.edges()), 9)

        if visualize_tests:
            pyplot.title("Wrong 'i' label", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()

    def test_bad_input_edge_link_missing(self):
        graph = Graph()
        positions = [(1.0, 1.0), (1.0, 2.0), (1.0, 3.0),
                     (2.0, 3.0), (3.0, 3.0), (2.0, 2.0)]

        [e1, e12, e2, e23, e3, e31] = self.create_nodes(graph, 1, 'E', positions)

        self.create_edges_chain(graph, [e1, e12, e2, e23, e3, e31])

        i = add_interior(graph, e1, e2, e3)

        with self.assertRaises(AssertionError):
            [i1, i3, i2a, i2b] = P5().apply(graph, [i])
        self.assertEqual(len(graph.nodes()), 7)
        self.assertEqual(len(graph.edges()), 8)

        if visualize_tests:
            pyplot.title("Edge link missing", fontsize=16)
            visualize_graph_3d(graph)
            pyplot.show()
