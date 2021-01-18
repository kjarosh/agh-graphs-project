from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p1 import P1
from agh_graphs.productions.p2 import P2
from agh_graphs.productions.p9 import P9
from agh_graphs.productions.p10 import P10
from agh_graphs.utils import gen_name
from agh_graphs.visualize import visualize_graph_layer, visualize_graph_3d


def derive_b():
    graph = Graph()
    initial_node_name = gen_name()
    graph.add_node(initial_node_name, layer=0, position=(0.5, 0.5), label='E')

    visualize_graph_3d(graph)
    pyplot.show()

    [i1, i2] = P1().apply(graph, [initial_node_name])

    visualize_graph_3d(graph)
    pyplot.show()

    [i1_1, i1_2] = P2().apply(graph, [i1], orientation=1)
    [i2_1] = P9().apply(graph, [i2])

    visualize_graph_3d(graph)
    pyplot.show()

    P10().apply(graph, [i1_1, i1_2, i2_1])

    visualize_graph_3d(graph)
    pyplot.show()

    return graph


if __name__ == '__main__':

    graph = derive_b()
