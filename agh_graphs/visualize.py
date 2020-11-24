"""
Module responsible for visualization of the graph.
"""
import networkx
from matplotlib import pyplot
from networkx import Graph


def __get_color(node_data):
    if node_data['label'] in {'e', 'E'}:
        return '#5081bd'

    if node_data['label'] in {'i', 'I'}:
        return '#c0504d'

    return 'red'


def visualize_graph_layer(graph: Graph, layer: int):
    filtered_graph = graph.copy()

    to_remove = []
    for node, data in filtered_graph.nodes(data=True):
        if data['layer'] != layer:
            to_remove.append(node)

    filtered_graph.remove_nodes_from(to_remove)

    colors = [__get_color(d) for n, d in filtered_graph.nodes(data=True)]
    networkx.draw(
        filtered_graph,
        networkx.get_node_attributes(filtered_graph, 'position'),
        labels=networkx.get_node_attributes(filtered_graph, 'label'),
        node_color=colors,
        with_labels=True)
    return pyplot.show()
