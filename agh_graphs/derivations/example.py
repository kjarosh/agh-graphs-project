"""
This is an example derivation.
If you want to test something you can use it.
It's better to copy-paste this file as `test.py` in order
not to accidentally commit this file.
"""
from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p1 import P1
from agh_graphs.productions.p2 import P2
from agh_graphs.utils import gen_name
from agh_graphs.visualize import visualize_graph_layer, visualize_graph_3d

if __name__ == '__main__':
    graph = Graph()
    initial_node_name = gen_name()
    graph.add_node(initial_node_name, layer=0, position=(0.5, 0.5), label='E')

    [i1, i2] = P1().apply(graph, [initial_node_name])
    [i1_1, i1_2] = P2().apply(graph, [i1])
    [i2_1, i2_2] = P2().apply(graph, [i2])
    [i3_1, i3_2] = P2().apply(graph, [i1_1])

    visualize_graph_3d(graph)
    pyplot.show()

    visualize_graph_layer(graph, 2)
    pyplot.show()
