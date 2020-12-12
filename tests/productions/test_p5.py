import unittest

from networkx import Graph

from productions.p5 import P5
from utils import gen_name, add_interior, get_neighbors_at, get_node_at


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

        [i1, i3, i2a, i2b] = P5().apply(graph, [i])

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
        positions = [(1.0, 1.0), (1.0, 2.0), (1.0, 3.0),
                     (2.0, 3.0), (3.0, 3.0), (2.0, 2.0),
                     (0.0, 0.0), (0.0, 2.0)]

        [e1, e12, e2, e23, e3, e31, e0a, e0b] = self.create_nodes(graph, 1, 'E', positions)
        self.create_edges_chain(graph, [e1, e12, e2, e23, e3, e31, e1])
        self.create_edges_chain(graph, [e1, e0a, e0b, e1])

        i = add_interior(graph, e1, e2, e3)

        [i1, i3, i2a, i2b] = P5().apply(graph, [i])

        # check if parent_graph external links and vertices are unchanged
        self.assertTrue(graph.has_edge(e0a, e1))
        self.assertTrue(graph.has_edge(e0b, e1))
        self.assertTrue(graph.has_edge(e0a, e0b))
        self.assertEqual(graph.nodes[e0a]['label'], 'E')
        self.assertEqual(graph.nodes[e0b]['label'], 'E')
        self.assertEqual(len(get_neighbors_at(graph, e0a, graph.nodes[e0a]['layer'])), 2)
        self.assertEqual(len(get_neighbors_at(graph, e0b, graph.nodes[e0b]['layer'])), 2)
        self.assertEqual(graph.nodes[e0a]['position'], (0.0, 0.0))
        self.assertEqual(graph.nodes[e0b]['position'], (0.0, 2.0))

        # check if production graph is unchanged
        # if edges are unchanged
        self.assertTrue(graph.has_edge(e1, e12))
        self.assertTrue(graph.has_edge(e12, e2))
        self.assertTrue(graph.has_edge(e2, e23))
        self.assertTrue(graph.has_edge(e23, e3))
        self.assertTrue(graph.has_edge(e3, e31))
        self.assertTrue(graph.has_edge(e31, e1))
        self.assertTrue(graph.has_edge(i, e1))
        self.assertTrue(graph.has_edge(i, e2))
        self.assertTrue(graph.has_edge(i, e3))

        # if labels are unchanged
        self.assertEqual(graph.nodes[e1]['label'], 'E')
        self.assertEqual(graph.nodes[e12]['label'], 'E')
        self.assertEqual(graph.nodes[e2]['label'], 'E')
        self.assertEqual(graph.nodes[e23]['label'], 'E')
        self.assertEqual(graph.nodes[e3]['label'], 'E')
        self.assertEqual(graph.nodes[e31]['label'], 'E')

        # if number of neighbors is unchanged
        self.assertEqual(len(get_neighbors_at(graph, e1, graph.nodes[e1]['layer'])), 5)
        self.assertEqual(len(get_neighbors_at(graph, e12, graph.nodes[e1]['layer'])), 2)
        self.assertEqual(len(get_neighbors_at(graph, e2, graph.nodes[e1]['layer'])), 3)
        self.assertEqual(len(get_neighbors_at(graph, e23, graph.nodes[e1]['layer'])), 2)
        self.assertEqual(len(get_neighbors_at(graph, e3, graph.nodes[e1]['layer'])), 3)
        self.assertEqual(len(get_neighbors_at(graph, e31, graph.nodes[e1]['layer'])), 2)
        self.assertEqual(len(get_neighbors_at(graph, i, graph.nodes[i]['layer'])), 3)

        # if vertices position is unchanged
        self.assertEqual(graph.nodes[e1]['position'], (1.0, 1.0))
        self.assertEqual(graph.nodes[e12]['position'], (1.0, 2.0))
        self.assertEqual(graph.nodes[e2]['position'], (1.0, 3.0))
        self.assertEqual(graph.nodes[e23]['position'], (2.0, 3.0))
        self.assertEqual(graph.nodes[e3]['position'], (3.0, 3.0))
        self.assertEqual(graph.nodes[e31]['position'], (2.0, 2.0))

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
