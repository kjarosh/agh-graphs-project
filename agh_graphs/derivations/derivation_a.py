from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p1 import P1
from agh_graphs.productions.p12 import P12
from agh_graphs.productions.p9 import P9
from agh_graphs.utils import gen_name
from agh_graphs.visualize import visualize_graph_layer, visualize_graph_3d


class DerivationA:

    def __init__(self, visualize=False):
        self.visualize = visualize

    def run(self, graph, p1_positions):
        assert len(graph.nodes()) == 1
        initial_node_name = list(graph.nodes())[0]
        self.visualize_if_enabled(graph)

        [i1, i2] = P1().apply(graph, [initial_node_name], positions=p1_positions)
        self.visualize_if_enabled(graph)

        [i1_] = P9().apply(graph, [i1])
        self.visualize_if_enabled(graph)

        [i2_] = P9().apply(graph, [i2])
        self.visualize_if_enabled(graph)

        [] = P12().apply(graph, [i1, i2, i1_, i2_])
        self.visualize_if_enabled(graph)

        if self.visualize:
            visualize_graph_layer(graph, 0)
            pyplot.show()

            visualize_graph_layer(graph, 1)
            pyplot.show()

            visualize_graph_layer(graph, 2)
            pyplot.show()

    def visualize_if_enabled(self, graph):
        if self.visualize:
            visualize_graph_3d(graph)
            pyplot.show()


if __name__ == '__main__':
    graph = Graph()
    graph.add_node(gen_name(), layer=0, position=(0.5, 0.5), label='E')
    p1_positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
    DerivationA(visualize=True).run(graph, p1_positions)
