from matplotlib import pyplot
from networkx import Graph

from evaluate import Evaluator
from productions.p1 import P1
from utils import gen_name
from visualize import visualize_graph_layer, visualize_graph_3d

productions = [
    P1()
]

if __name__ == '__main__':
    layer = 1
    graph = Graph()
    graph.add_node(gen_name(), layer=0, position=(0.5, 0.5), label='E')

    evaluator = Evaluator(productions, graph)
    for i in range(layer):
        evaluator.evaluate_next_layer()

    visualize_graph_3d(graph)
    pyplot.show()

    visualize_graph_layer(graph, layer)
    pyplot.show()
