"""
Utility module for tests.
"""
import os

from networkx import Graph

from agh_graphs.utils import gen_name

visualize_tests = 'VISUALIZE_TESTS' in os.environ and os.environ['VISUALIZE_TESTS'] == 'true'


def addTriangle(graph: Graph, node, attr):
    e1 = gen_name()
    e2 = gen_name()
    e3 = gen_name()
    x = attr['position'][0]
    y = attr['position'][1]
    graph.add_node(e1, layer=attr['layer'], position=(x + 0.5, y + 0.5), label='E')
    graph.add_node(e2, layer=attr['layer'], position=(x, y + 0.5), label='E')
    graph.add_node(e3, layer=attr['layer'], position=(x - 0.5, y - 0.5), label='E')
    graph.add_edge(node, e1)
    graph.add_edge(node, e2)
    graph.add_edge(node, e3)
    return graph