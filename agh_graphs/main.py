from matplotlib import pyplot
from networkx import Graph

from productions.p1 import P1
from productions.p2 import P2
from utils import gen_name
from visualize import visualize_graph_layer, visualize_graph_3d

productions = [
    P1(),
    P2(),
    # P2(),
    # P2()
]

if __name__ == '__main__':
    layer = 2
    graph = Graph()
    initial_node_name = gen_name()
    graph.add_node(initial_node_name, layer=0, position=(0.5, 0.5), label='E')

    prod_input = [initial_node_name]
    for production in productions:
        prod_input = production.apply(graph, prod_input)

    visualize_graph_3d(graph)
    pyplot.show()

    visualize_graph_layer(graph, layer)
    pyplot.show()
