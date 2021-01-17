import unittest
from random import choice
from networkx import Graph
from matplotlib import pyplot
from agh_graphs.productions.p7 import P7
from agh_graphs.visualize import visualize_graph_3d
from tests.test_utils import visualize_tests


class P7Test(unittest.TestCase):
    def testCorrectGraph(self):
        graph = createCorrectGraph()
        print(graph.nodes(data=True))

        original_positions = dict(map(lambda x: (x[0], x[1]['position']), graph.nodes(data=True)))

        if visualize_tests:
            visualize_graph_3d(graph)
            pyplot.show()

        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        output = P7().apply(graph, prod_input)

        self.assertEqual(len(graph.nodes()), 15)
        self.assertEqual(len(graph.edges()), 35)

        self.assertEqual(output, [])

        for node in nodes_after_merge():
            self.assertTrue(graph.has_node(node))

        for node in set(required_nodes()) - set(nodes_after_merge()):
            self.assertFalse(graph.has_node(node))

        for edge in edges_after_merge():
            self.assertTrue(graph.has_edge(edge[0], edge[1]))

        for edge in set(required_edges()) - set(edges_after_merge()):
            self.assertFalse(graph.has_edge(edge[0], edge[1]))

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

        after_merge_positions = dict(map(lambda x: (x[0], x[1]['position']), graph.nodes(data=True)))

        for node, position in after_merge_positions.items():
            self.assertTrue(position, original_positions[node])

    def testMissingNodeGraph(self):
        for node in required_nodes():
            graph = createCorrectGraph()
            graph.remove_node(node)
            prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']

            if visualize_tests:
                visualize_graph_3d(graph)
                pyplot.show()

            with self.assertRaises(ValueError):
                P7().apply(graph, prod_input)

        for node in not_required_nodes():
            graph = createCorrectGraph()
            graph.remove_node(node)
            prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
            P7().apply(graph, prod_input)

    def testMissingEdgeGraph(self):
        for edge in required_edges():
            graph = createCorrectGraph()
            graph.remove_edge(edge[0], edge[1])
            prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']

            if visualize_tests:
                visualize_graph_3d(graph)
                pyplot.show()

            with self.assertRaises(ValueError):
                P7().apply(graph, prod_input)

        for edge in not_required_edges():
            graph = createCorrectGraph()
            graph.remove_edge(edge[0], edge[1])
            prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']

            if visualize_tests:
                visualize_graph_3d(graph)
                pyplot.show()

            P7().apply(graph, prod_input)

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

    def testBadPosition(self):
        merger_nodes = ['e15', 'e14', 'e16', 'e17']
        for node in merger_nodes:
            graph = createCorrectGraph()
            prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']

            node = list(filter(lambda x: x[0] == node, graph.nodes(data=True)))[0]
            node[1]['position'] = (1000.0, 1000.0)

            with self.assertRaises(ValueError):
                P7().apply(graph, prod_input)





def required_nodes():
    return [
        'e01', # Doesn't care if this node exist or not
        'e04', # Doesn't care if this node exist or not
        'i1',
        'i2',
        'I1',
        'I2',
        'I3',
        'I4',
        'e11',
        'e14',
        'e15',
        'e16',
        'e17']


def not_required_nodes():
    return ['e02', 'e03', 'e12', 'e13']


def nodes_after_merge():
    # SHOULD MERGE e15 into e14 and e17 into e16
    return ['e01',
            'e04',
            'i1',
            'i2',
            'I1',
            'I2',
            'I3',
            'I4',
            'e11',
            'e14',
            'e16',
            'e02',
            'e03',
            'e12',
            'e13']


def required_edges():
    return [
        ('e01', 'i1'),  # Tests don't care if this edge is in the original graph
        ('e01', 'i2'),  # Tests don't care if this edge is in the original graph
        ('e04', 'i1'),  # Tests don't care if this edge is in the original graph
        ('e04', 'i2'),  # Tests don't care if this edge is in the original graph
        ('e01', 'e04'), # Tests don't care if this edge is in the original graph
        ('i2', 'I1'),
        ('i2', 'I2'),
        ('i1', 'I3'),
        ('i1', 'I4'),
        ('I1', 'e11'),
        ('I1', 'e16'),
        ('I2', 'e16'),
        ('I2', 'e14'),
        ('I3', 'e17'),
        ('I3', 'e11'),
        ('I4', 'e15'),
        ('I4', 'e17'),
        ('e11', 'e16'),
        ('e14', 'e16'),
        ('e11', 'e17'),
        ('e15', 'e17')]

def not_required_edges():
    return [
        ('e03', 'i1'),
        ('e02', 'i2'),
        ('e01', 'e02'),
        ('e02', 'e04'),
        ('e01', 'e03'),
        ('e04', 'e03'),
        ('I1', 'e12'),
        ('I2', 'e12'),
        ('I3', 'e13'),
        ('I4', 'e13'),
        ('e11', 'e12'),
        ('e12', 'e16'),
        ('e12', 'e14'),
        ('e11', 'e13'),
        ('e13', 'e17'),
        ('e15', 'e13'),
    ]

def edges_after_merge():
    # SHOULD MERGE e15 into e14 and e17 into e16
    return [
        ('e01', 'i1'),
        ('e01', 'i2'),
        ('e04', 'i1'),
        ('e04', 'i2'),
        ('e01', 'e04'),
        ('i2', 'I1'),
        ('i2', 'I2'),
        ('i1', 'I3'),
        ('i1', 'I4'),
        ('I1', 'e11'),
        ('I1', 'e16'),
        ('I2', 'e16'),
        ('I2', 'e14'),
        ('I3', 'e16'),
        ('I3', 'e11'),
        ('I4', 'e14'),
        ('I4', 'e16'),
        ('e11', 'e16'),
        ('e14', 'e16'),
        ('e03', 'i1'),
        ('e02', 'i2'),
        ('e01', 'e02'),
        ('e02', 'e04'),
        ('e01', 'e03'),
        ('e04', 'e03'),
        ('I1', 'e12'),
        ('I2', 'e12'),
        ('I3', 'e13'),
        ('I4', 'e13'),
        ('e11', 'e12'),
        ('e12', 'e16'),
        ('e12', 'e14'),
        ('e11', 'e13'),
        ('e13', 'e16'),
        ('e14', 'e13')]

def createCorrectGraph():
    graph = Graph()
    e01 = "e01"
    e02 = "e02"  # not required
    e03 = "e03"  # not required
    e04 = "e04"
    i1 = "i1"
    i2 = "i2"
    I1 = "I1"
    I2 = "I2"
    I3 = "I3"
    I4 = "I4"
    e11 = "e11"
    e12 = "e12"  # not required
    e13 = "e13"  # not required
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

    graph.add_node(I1, layer=1, position=(0.25, 1), label='I')
    graph.add_node(I2, layer=1, position=(1.4, 2), label='I')
    graph.add_node(I3, layer=1, position=(0.75, 0), label='I')
    graph.add_node(I4, layer=1, position=(1.6, 1), label='I')
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
    graph.add_edge(e03, i1)  # not required
    graph.add_edge(e02, i2)  # not required

    graph.add_edge(e01, e02)  # not required
    graph.add_edge(e02, e04)  # not required
    graph.add_edge(e01, e04)

    graph.add_edge(e01, e03)  # not required
    graph.add_edge(e04, e03)  # not required

    # interlayer connections
    graph.add_edge(i2, I1)
    graph.add_edge(i2, I2)
    graph.add_edge(i1, I3)
    graph.add_edge(i1, I4)

    # lower layer interior connections
    graph.add_edge(I1, e11)
    graph.add_edge(I1, e12)  # not required
    graph.add_edge(I1, e16)

    graph.add_edge(I2, e12)  # not required
    graph.add_edge(I2, e16)
    graph.add_edge(I2, e14)

    graph.add_edge(I3, e13)  # not required
    graph.add_edge(I3, e17)
    graph.add_edge(I3, e11)

    graph.add_edge(I4, e15)
    graph.add_edge(I4, e17)
    graph.add_edge(I4, e13)  # not required

    # lower layer edges connections
    graph.add_edge(e11, e12)  # not required
    graph.add_edge(e11, e16)
    graph.add_edge(e12, e16)  # not required

    graph.add_edge(e14, e16)
    graph.add_edge(e12, e14)  # not required

    graph.add_edge(e11, e13)  # not required
    graph.add_edge(e13, e17)  # not required
    graph.add_edge(e11, e17)

    graph.add_edge(e15, e13)  # not required
    graph.add_edge(e15, e17)

    return graph
