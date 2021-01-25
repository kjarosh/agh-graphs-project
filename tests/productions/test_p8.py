import unittest
from random import choice

from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p1 import P1
from agh_graphs.productions.p2 import P2
from agh_graphs.productions.p8 import P8
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at, find_overlapping_vertices, join_overlapping_vertices, \
    get_node_at, centroid
from agh_graphs.visualize import visualize_graph_3d, visualize_graph_layer
from tests.utils import visualize_tests


class P8Test(unittest.TestCase):

    def testHappyPath(self):
        graph = createCorrectGraph()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'I']
        P8().apply(graph, prod_input)
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        #test if number of nodes and edges is correct
        self.assertEqual(len(graph.nodes()), 11)
        self.assertEqual(len(graph.edges()), 19)

        e1 = get_node_at(graph=graph, layer=1, pos=(1.0, 2.0))
        e2 = get_node_at(graph=graph, layer=1, pos=(3.0, 2.0))
        i1 = get_node_at(graph=graph, layer=1, pos=(2.0, 3.0))
        i2 = get_node_at(graph=graph, layer=1, pos=(2.0, 1.0))
        I1 = get_node_at(graph=graph, layer=2, pos=(1.5, 3.5))
        I2 = get_node_at(graph=graph, layer=2, pos=(2.5, 3.5))
        e3 = get_node_at(graph=graph, layer=2, pos=(1.0, 2.0))
        e4 = get_node_at(graph=graph, layer=2, pos=(3.0, 2.0))
        e5 = get_node_at(graph=graph, layer=2, pos=(2.0, 2.0))
        I3 = get_node_at(graph=graph, layer=2, pos=(1.5, 0.5))
        I4 = get_node_at(graph=graph, layer=2, pos=(2.5, 0.5))

        #check position
        self.assertIsNotNone(e1)
        self.assertIsNotNone(e2)
        self.assertIsNotNone(i1)
        self.assertIsNotNone(i2)
        self.assertIsNotNone(I1)
        self.assertIsNotNone(I2)
        self.assertIsNotNone(e3)
        self.assertIsNotNone(e4)
        self.assertIsNotNone(e5)
        self.assertIsNotNone(I3)
        self.assertIsNotNone(I4)

        #check edges
        # upper layer edges
        self.assertTrue(graph.has_edge(e1, i1))
        self.assertTrue(graph.has_edge(e1, i2))
        self.assertTrue(graph.has_edge(e2, i1))
        self.assertTrue(graph.has_edge(e2, i2))
        self.assertTrue(graph.has_edge(e1, e2))

        # interlayer connections
        self.assertTrue(graph.has_edge(I1, i1))
        self.assertTrue(graph.has_edge(I2, i1))
        self.assertTrue(graph.has_edge(I3, i2))
        self.assertTrue(graph.has_edge(I4, i2))

        # lower layer connections
        self.assertTrue(graph.has_edge(I1, e3))
        self.assertTrue(graph.has_edge(I1, e5))
        self.assertTrue(graph.has_edge(e3, e5))
        self.assertTrue(graph.has_edge(I2, e4))
        self.assertTrue(graph.has_edge(I2, e5))
        self.assertTrue(graph.has_edge(e4, e5))
        self.assertTrue(graph.has_edge(I3, e3))
        self.assertTrue(graph.has_edge(I4, e4))


        #check labels
        self.assertEqual(graph.nodes[e1]['label'], 'E')
        self.assertEqual(graph.nodes[e2]['label'], 'E')
        self.assertEqual(graph.nodes[i1]['label'], 'i')
        self.assertEqual(graph.nodes[i2]['label'], 'i')
        self.assertEqual(graph.nodes[I1]['label'], 'I')
        self.assertEqual(graph.nodes[I2]['label'], 'I')
        self.assertEqual(graph.nodes[e3]['label'], 'E')
        self.assertEqual(graph.nodes[e4]['label'], 'E')
        self.assertEqual(graph.nodes[I3]['label'], 'I')
        self.assertEqual(graph.nodes[I4]['label'], 'I')

    def testOnBiggerGraph(self):
        graph = Graph()
        initial_node_name = gen_name()
        graph.add_node(initial_node_name, layer=0, position=(0.5, 0.5), label='E')

        [i1, i2] = P1().apply(graph, [initial_node_name])
        [i1_1, i1_2] = P2().apply(graph, [i1], orientation=1)
        [i2_1, i2_2] = P2().apply(graph, [i2], orientation=1)

        overlappings = find_overlapping_vertices(graph)
        join_overlapping_vertices(graph, overlappings[0][0], overlappings[0][1], 2)
        join_overlapping_vertices(graph, overlappings[4][0], overlappings[4][1], 2)
        # visualize_graph_layer(graph, 2)

        [i1_1new, i1_2new, i2_1new, i2_2new] = P8().apply(graph, [i1_1, i1_2, i2_1, i2_2])

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        self.assertEqual(len(graph.nodes()), 16)
        self.assertEqual(len(graph.edges()), 37)

        e = get_node_at(graph=graph, layer=0, pos=(0.5, 0.5))
        e1 = get_node_at(graph=graph, layer=1, pos=(0.0, 0.0))
        e2 = get_node_at(graph=graph, layer=1, pos=(1.0, 0.0))
        e3 = get_node_at(graph=graph, layer=1, pos=(1.0, 1.0))
        e4 = get_node_at(graph=graph, layer=1, pos=(0.0, 1.0))
        e5 = get_node_at(graph=graph, layer=2, pos=(0.0, 0.0))
        e6 = get_node_at(graph=graph, layer=2, pos=(1.0, 0.0))
        e7 = get_node_at(graph=graph, layer=2, pos=(1.0, 1.0))
        e8 = get_node_at(graph=graph, layer=2, pos=(0.0, 1.0))
        e9 = get_node_at(graph=graph, layer=2, pos=(0.5, 0.5))

        #check position
        self.assertIsNotNone(e)
        self.assertIsNotNone(e1)
        self.assertIsNotNone(e2)
        self.assertIsNotNone(e3)
        self.assertIsNotNone(e4)
        self.assertIsNotNone(e5)
        self.assertIsNotNone(e6)
        self.assertIsNotNone(e7)
        self.assertIsNotNone(e8)
        self.assertIsNotNone(e9)

        self.assertEqual(graph.nodes[i1_1new]['position'], graph.nodes[i1_1]['position'])
        self.assertEqual(graph.nodes[i1_2new]['position'], graph.nodes[i1_2]['position'])
        self.assertEqual(graph.nodes[i2_1new]['position'], graph.nodes[i2_1]['position'])
        self.assertEqual(graph.nodes[i2_2new]['position'], graph.nodes[i2_2]['position'])

        self.assertEqual(graph.nodes[i1_1new]['layer'], graph.nodes[i1_1]['layer'])
        self.assertEqual(graph.nodes[i1_2new]['layer'], graph.nodes[i1_2]['layer'])
        self.assertEqual(graph.nodes[i2_1new]['layer'], graph.nodes[i2_1]['layer'])
        self.assertEqual(graph.nodes[i2_2new]['layer'], graph.nodes[i2_2]['layer'])

        #check edges

        #zero
        self.assertTrue(graph.has_edge(e, i1))
        self.assertTrue(graph.has_edge(e, i2))

        # first
        self.assertTrue(graph.has_edge(e1, e2))
        self.assertTrue(graph.has_edge(e1, e3))
        self.assertTrue(graph.has_edge(e1, e4))
        self.assertTrue(graph.has_edge(e2, e3))
        self.assertTrue(graph.has_edge(e3, e4))
        self.assertTrue(graph.has_edge(e1, i1))
        self.assertTrue(graph.has_edge(e4, i1))
        self.assertTrue(graph.has_edge(e3, i1))
        self.assertTrue(graph.has_edge(e1, i2))
        self.assertTrue(graph.has_edge(e3, i2))
        self.assertTrue(graph.has_edge(e2, i2))

        #second
        self.assertTrue(graph.has_edge(e5, e6))
        self.assertTrue(graph.has_edge(e5, e9))
        self.assertTrue(graph.has_edge(e5, e8))
        self.assertTrue(graph.has_edge(e6, e7))
        self.assertTrue(graph.has_edge(e7, e9))
        self.assertTrue(graph.has_edge(e7, e8))

        self.assertTrue(graph.has_edge(i1, i1_1new))
        self.assertTrue(graph.has_edge(i1, i1_2new))
        self.assertTrue(graph.has_edge(i2, i2_1new))
        self.assertTrue(graph.has_edge(i2, i2_2new))
        self.assertTrue(graph.has_edge(e9, i1_1new))
        self.assertTrue(graph.has_edge(e9, i1_2new))
        self.assertTrue(graph.has_edge(e9, i2_1new))
        self.assertTrue(graph.has_edge(e9, i2_2new))
        self.assertTrue(graph.has_edge(e6, i2_1new))
        self.assertTrue(graph.has_edge(e6, i2_2new))
        self.assertTrue(graph.has_edge(e8, i1_1new))
        self.assertTrue(graph.has_edge(e8, i1_2new))
        self.assertTrue(graph.has_edge(e7, i1_2new))
        self.assertTrue(graph.has_edge(e7, i2_2new))
        self.assertTrue(graph.has_edge(e5, i1_1new))
        self.assertTrue(graph.has_edge(e5, i2_1new))

        #check labels
        self.assertEqual(graph.nodes[e1]['label'], 'E')
        self.assertEqual(graph.nodes[e2]['label'], 'E')
        self.assertEqual(graph.nodes[e3]['label'], 'E')
        self.assertEqual(graph.nodes[e4]['label'], 'E')
        self.assertEqual(graph.nodes[e5]['label'], 'E')
        self.assertEqual(graph.nodes[e6]['label'], 'E')
        self.assertEqual(graph.nodes[e7]['label'], 'E')
        self.assertEqual(graph.nodes[e8]['label'], 'E')

        self.assertEqual(graph.nodes[i1_1new]['label'], 'I')
        self.assertEqual(graph.nodes[i1_2new]['label'], 'I')
        self.assertEqual(graph.nodes[i2_1new]['label'], 'I')
        self.assertEqual(graph.nodes[i2_2new]['label'], 'I')
        self.assertEqual(graph.nodes[i1]['label'], 'i')
        self.assertEqual(graph.nodes[i2]['label'], 'i')

    def testMissingNode(self):
        graph = createCorrectGraph()
        e4 = get_node_at(graph=graph, layer=2, pos=(3.0, 2.0))
        graph.remove_node(e4)
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'I']
        with self.assertRaises(ValueError):
            P8().apply(graph, prod_input)

    def testMissingEdge(self):
        graph = createCorrectGraph()
        e4 = get_node_at(graph=graph, layer=2, pos=(3.0, 2.0))
        I4 = get_node_at(graph=graph, layer=2, pos=(2.5, 0.5))
        graph.remove_edge(I4, e4)
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'I']
        with self.assertRaises(ValueError):
            P8().apply(graph, prod_input)

    def testWrongLabel(self):
        graph = createCorrectGraph()
        attributes = [y for x, y in graph.nodes(data=True) if y['label'] == 'I']
        attributes[1]['label'] = 'E'
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'I']
        with self.assertRaises(ValueError):
           P8().apply(graph, prod_input)

    def testWrongPosition(self):
        graph = createCorrectGraph()
        e_attributes = [y for x, y in graph.nodes(data=True) if y['label'] == 'E']
        e_attributes[0]['position'] = (1.0, 4.0)
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'I']
        with self.assertRaises(ValueError):
            P8().apply(graph, prod_input)


def createCorrectGraph():
        graph = Graph()
        e1 = gen_name()
        e2 = gen_name()
        i1 = gen_name()
        i2 = gen_name()
        I1 = gen_name()
        I2 = gen_name()
        e3 = gen_name()
        e4 = gen_name()
        e5 = gen_name()
        e6 = gen_name()
        I3 = gen_name()
        I4 = gen_name()

        graph.add_node(e1, layer=1, position=(1.0, 2.0), label='E')
        graph.add_node(e2, layer=1, position=(3.0, 2.0), label='E')

        graph.add_node(i1, layer=1, position=(2.0, 3.0), label='i')
        graph.add_node(i2, layer=1, position=(2.0, 1.0), label='i')

        graph.add_node(I1, layer=2, position=(1.5, 3.5), label='I')
        graph.add_node(I2, layer=2, position=(2.5, 3.5), label='I')

        graph.add_node(e3, layer=2, position=(1.0, 2.0), label='E')
        graph.add_node(e4, layer=2, position=(3.0, 2.0), label='E')
        graph.add_node(e5, layer=2, position=(2.0, 2.0), label='E')

        graph.add_node(I3, layer=2, position=(1.5, 0.5), label='I')
        graph.add_node(I4, layer=2, position=(2.5, 0.5), label='I')

        graph.add_node(e6, layer=2, position=(2.0, 2.0), label='E')

        # upper layer edges
        graph.add_edge(e1, i1)
        graph.add_edge(e1, i2)
        graph.add_edge(e2, i1)
        graph.add_edge(e2, i2)
        graph.add_edge(e1, e2)

        # interlayer connections
        graph.add_edge(I1, i1)
        graph.add_edge(I2, i1)
        graph.add_edge(I3, i2)
        graph.add_edge(I4, i2)

        # lower layer connections
        graph.add_edge(I1, e3)
        graph.add_edge(I1, e5)
        graph.add_edge(e3, e5)
        graph.add_edge(I2, e4)
        graph.add_edge(I2, e5)
        graph.add_edge(e4, e5)
        graph.add_edge(I3, e3)
        graph.add_edge(I3, e6)
        graph.add_edge(e3, e6)
        graph.add_edge(I4, e4)
        graph.add_edge(I4, e6)
        graph.add_edge(e4, e6)
        return graph