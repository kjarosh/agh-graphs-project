import unittest
from random import choice
from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p6 import P6
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at
from agh_graphs.visualize import visualize_graph_3d

class P6Test(unittest.TestCase):
    def testCorrectGraph(self):
        graph = createCorrectGraph()
        prod_input = [x for x,y in graph.nodes(data=True) if y['label']=='i' or y['label'] == 'I']
        [] = P6().apply(graph, prod_input)
        self.assertEqual(len(graph.nodes()), 11)
        self.assertEqual(len(graph.edges()), 19)

    def testLargerGraph(self):
        e1 = gen_name()
        graph = createCorrectGraph()
        node, attr = choice(list(graph.nodes(data=True)))
        # print(attr['layer'],type(random_node))
        graph.add_node(e1,layer = attr['layer'],position = attr['position'],label = 'E')
        prod_input = [x for x,y in graph.nodes(data=True) if y['label']=='i' or y['label'] == 'I']
        [] = P6().apply(graph, prod_input)
        self.assertEqual(len(graph.nodes()), 12)
        self.assertEqual(len(graph.edges()), 19)

    def testMissingNodeGraph(self):
        graph = createCorrectGraph()
        node = choice([x for x,y in graph.nodes(data=True) if y['label']=='E'])
        graph.remove_node(node)
        prod_input = [x for x,y in graph.nodes(data=True) if y['label']=='i' or y['label'] == 'I']
        with self.assertRaises(ValueError):
            P6().apply(graph, prod_input)

    def testMissingEdgeGraph(self):
        graph = createCorrectGraph()
        edge = choice([x for x in graph.edges()])
        graph.remove_edge(edge[0],edge[1])
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        with self.assertRaises(ValueError):
            P6().apply(graph, prod_input)

    def testBadInput(self):
        graph = createCorrectGraph()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        attributes = [y for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        attributes[0]['label'] = 'E'
        with self.assertRaises(ValueError):
            P6().apply(graph, prod_input)

    def testBadCoordinates(self):
        graph = createCorrectGraph()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        e_attributes = [y for x, y in graph.nodes(data=True) if y['label'] == 'E']
        e_attributes[0]['position'] = (4.0,4.0)
        with self.assertRaises(ValueError):
            P6().apply(graph, prod_input)

    def testOutputLabels(self):
        graph = createCorrectGraph()
        prod_input = [x for x, y in graph.nodes(data=True) if y['label'] == 'i' or y['label'] == 'I']
        [] = P6().apply(graph, prod_input)
        i_nodes = [x for x, y in graph.nodes(data=True) if y['label'] == 'i']
        I_nodes = [x for x, y in graph.nodes(data=True) if y['label'] == 'I']
        e_nodes = [x for x, y in graph.nodes(data=True) if y['label'] == 'E']

        self.assertEqual(len(i_nodes), 2)
        self.assertEqual(len(I_nodes), 4)
        self.assertEqual(len(e_nodes), 5)

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
    I3 = gen_name()
    I4 = gen_name()
    e6 = gen_name()
    e7 = gen_name()
    e8 = gen_name()
    graph.add_node(e1, layer=1, position=(1.0, 2.0), label='E')
    graph.add_node(e2, layer=1, position=(3.0, 2.0), label='E')
    graph.add_node(i2, layer=1, position=(2.0, 1.0), label='i')
    graph.add_node(i1, layer=1, position=(2.0, 3.0), label='i')
    graph.add_node(I1, layer=2, position=(1.5, 3.5), label='I')
    graph.add_node(I2, layer=2, position=(2.5, 3.5), label='I')
    graph.add_node(e3, layer=2, position=(1.0, 2.0), label='E')
    graph.add_node(e4, layer=2, position=(3.0, 2.0), label='E')
    graph.add_node(e5, layer=2, position=(2.0, 2.0), label='E')
    graph.add_node(I3, layer=2, position=(1.5, 0.5), label='I')
    graph.add_node(I4, layer=2, position=(2.5, 0.5), label='I')
    graph.add_node(e6, layer=2, position=(1.0, 2.0), label='E')
    graph.add_node(e7, layer=2, position=(3.0, 2.0), label='E')
    graph.add_node(e8, layer=2, position=(2.0, 2.0), label='E')
    # upper layer edges
    graph.add_edge(e1, i1)
    graph.add_edge(e1, i2)
    graph.add_edge(e2, i1)
    graph.add_edge(e2, i2)
    graph.add_edge(e1, e2)
    # interlayer connections
    graph.add_edge(i1, I1)
    graph.add_edge(i1, I2)
    graph.add_edge(i2, I3)
    graph.add_edge(i2, I4)
    # lower layer connections
    graph.add_edge(I1, e3)
    graph.add_edge(I1, e5)
    graph.add_edge(e3,e5)
    graph.add_edge(I2, e4)
    graph.add_edge(I2, e5)
    graph.add_edge(e4, e5)
    graph.add_edge(I3, e6)
    graph.add_edge(I3, e8)
    graph.add_edge(e6, e8)
    graph.add_edge(I4, e7)
    graph.add_edge(I4, e8)
    graph.add_edge(e7, e8)
    return graph