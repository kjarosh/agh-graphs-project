import unittest
from random import choice
from networkx import Graph
from matplotlib import pyplot
from agh_graphs.utils import gen_name
from agh_graphs.productions.p7 import P7
from agh_graphs.visualize import visualize_graph_3d
from tests.test_utils import visualize_tests, addTriangle


class P7Test(unittest.TestCase):
    def testCorrectGraph(self):
        graph = createCorrectGraph()
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        # SHOULD MERGE e15 into e14 and e17 into e16
        output = P7().apply(graph, prod_input)

        self.assertEqual(len(graph.nodes()), 15)
        self.assertEqual(len(graph.edges()), 35)
        self.assertEqual(prod_input, output)

        # check 'i' nodes
        self.assertTrue(graph.has_edge('i2', 'I1'))
        self.assertTrue(graph.has_edge('i2', 'I2'))
        self.assertTrue(graph.has_edge('i1', 'I3'))
        self.assertTrue(graph.has_edge('i1', 'I4'))

        # check merged nodes
        self.assertFalse(graph.has_node('e17'))
        self.assertFalse(graph.has_node('e15'))
        self.assertTrue(graph.has_edge('I1', 'e16'))
        self.assertTrue(graph.has_edge('I2', 'e16'))
        self.assertTrue(graph.has_edge('I3', 'e16'))
        self.assertFalse(graph.has_edge('I3', 'e17'))
        self.assertFalse(graph.has_edge('I4', 'e15'))
        self.assertTrue(graph.has_edge('I4', 'e14'))
        self.assertFalse(graph.has_edge('I4', 'e17'))
        self.assertTrue(graph.has_edge('I4', 'e16'))

        # check proper layers
        upper_layer_nodes = ['e01', 'e02', 'e03', 'e04', 'i1', 'i2']
        lower_layer_nodes = ['I1', 'I2', 'I3', 'I4', 'e11', 'e12', 'e13', 'e14', 'e16']

        upper_layer_numbers = \
            list(map(lambda x: x[1]['layer'], filter(lambda x: x[0] in upper_layer_nodes, graph.nodes(data=True))))
        lower_layer_numbers = \
            list(map(lambda x: x[1]['layer'], filter(lambda x: x[0] in lower_layer_nodes, graph.nodes(data=True))))

        self.assertEqual(len(set(upper_layer_numbers)), 1)
        self.assertEqual(len(set(lower_layer_numbers)), 1)

        self.assertEqual(upper_layer_numbers[0] + 1, lower_layer_numbers[0])

        # check the rest of the edges
        self.assertTrue(graph.has_edge('e01', 'i1'))
        self.assertTrue(graph.has_edge('e01', 'i2'))
        self.assertTrue(graph.has_edge('e04', 'i1'))
        self.assertTrue(graph.has_edge('e04', 'i2'))
        self.assertTrue(graph.has_edge('e03', 'i1'))
        self.assertTrue(graph.has_edge('e02', 'i2'))
        self.assertTrue(graph.has_edge('e01', 'e02'))
        self.assertTrue(graph.has_edge('e02', 'e04'))
        self.assertTrue(graph.has_edge('e01', 'e04'))
        self.assertTrue(graph.has_edge('e01', 'e03'))
        self.assertTrue(graph.has_edge('e04', 'e03'))
        self.assertTrue(graph.has_edge('I1', 'e11'))
        self.assertTrue(graph.has_edge('I1', 'e12'))
        self.assertTrue(graph.has_edge('I1', 'e16'))
        self.assertTrue(graph.has_edge('I2', 'e12'))
        self.assertTrue(graph.has_edge('I2', 'e16'))
        self.assertTrue(graph.has_edge('I2', 'e14'))
        self.assertTrue(graph.has_edge('I3', 'e13'))
        self.assertTrue(graph.has_edge('I3', 'e11'))
        self.assertTrue(graph.has_edge('I4', 'e13'))
        self.assertTrue(graph.has_edge('e11', 'e12'))
        self.assertTrue(graph.has_edge('e11', 'e16'))
        self.assertTrue(graph.has_edge('e12', 'e16'))
        self.assertTrue(graph.has_edge('e14', 'e16'))
        self.assertTrue(graph.has_edge('e12', 'e14'))
        self.assertTrue(graph.has_edge('e11', 'e13'))

    def testMissingNodeGraph(self):
        graph = createCorrectGraph()
        node = choice([x for x, y in graph.nodes(data=True) if y['label'] == 'E'])
        graph.remove_node(node)
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        with self.assertRaises(ValueError):
            P7().apply(graph, prod_input)

    def testMissingEdgeGraph(self):
        graph = createCorrectGraph()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        for edge in graph.edges():
            graph.remove_edge(edge[0], edge[1])
            with self.assertRaises(ValueError):
                P7().apply(graph, prod_input)
            graph.add_edge(edge[0], edge[1])

    def testBadInput(self):
        graph = createCorrectGraph()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        attributes = [y for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        attributes[0]['label'] = 'E'
        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()
        with self.assertRaises(ValueError):
            P7().apply(graph, prod_input)


def createCorrectGraph():
    graph = Graph()
    e01 = "e01"
    e02 = "e02"
    e03 = "e03"
    e04 = "e04"
    i1 = "i1"
    i2 = "i2"
    I1 = "I1"
    I2 = "I2"
    I3 = "I3"
    I4 = "I4"
    e11 = "e11"
    e12 = "e12"
    e13 = "e13"
    e14 = "e14"
    e15 = "e15"
    e16 = "e16"
    e17 = "e17"

    graph.add_node(e01, layer=0, position=(0.0, 0.0), label='E')
    graph.add_node(e02, layer=0, position=(0.0, 2.0), label='E')
    graph.add_node(e03, layer=0, position=(2.0, 0.0), label='E')
    graph.add_node(e04, layer=0, position=(2.0, 2.0), label='E')
    graph.add_node(i2, layer=0, position=(0.5, 1.5), label='i')
    graph.add_node(i1, layer=0, position=(1.5, 0.5), label='i')

    graph.add_node(I1, layer=1, position=(0.5, 0.5), label='I')
    graph.add_node(I2, layer=1, position=(0.5, 1.5), label='I')
    graph.add_node(I3, layer=1, position=(1.5, 0.5), label='I')
    graph.add_node(I4, layer=1, position=(1.5, 1.5), label='I')
    graph.add_node(e11, layer=1, position=(0.0, 0.0), label='E')
    graph.add_node(e12, layer=1, position=(0.0, 2.0), label='E')
    graph.add_node(e13, layer=1, position=(2.0, 0.0), label='E')
    graph.add_node(e14, layer=1, position=(2.0, 2.0), label='E')
    graph.add_node(e15, layer=1, position=(2.0, 2.0), label='E')
    graph.add_node(e16, layer=1, position=(1.0, 1.0), label='E')
    graph.add_node(e17, layer=1, position=(1.0, 1.0), label='E')
    # upper layer edges
    graph.add_edge(e01, i1)
    graph.add_edge(e01, i2)
    graph.add_edge(e04, i1)
    graph.add_edge(e04, i2)
    graph.add_edge(e03, i1)
    graph.add_edge(e02, i2)

    graph.add_edge(e01, e02)
    graph.add_edge(e02, e04)
    graph.add_edge(e01, e04)

    graph.add_edge(e01, e03)
    graph.add_edge(e04, e03)

    # interlayer connections
    graph.add_edge(i2, I1)
    graph.add_edge(i2, I2)
    graph.add_edge(i1, I3)
    graph.add_edge(i1, I4)

    # lower layer interior connections
    graph.add_edge(I1, e11)
    graph.add_edge(I1, e12)
    graph.add_edge(I1, e16)

    graph.add_edge(I2, e12)
    graph.add_edge(I2, e16)
    graph.add_edge(I2, e14)

    graph.add_edge(I3, e13)
    graph.add_edge(I3, e17)
    graph.add_edge(I3, e11)

    graph.add_edge(I4, e15)
    graph.add_edge(I4, e17)
    graph.add_edge(I4, e13)

    # lower layer edges connections
    graph.add_edge(e11, e12)
    graph.add_edge(e11, e16)
    graph.add_edge(e12, e16)

    graph.add_edge(e14, e16)
    graph.add_edge(e12, e14)

    graph.add_edge(e11, e13)
    graph.add_edge(e13, e17)
    graph.add_edge(e11, e17)

    graph.add_edge(e15, e13)
    graph.add_edge(e15, e17)

    return graph
