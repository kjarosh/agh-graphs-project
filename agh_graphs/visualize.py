"""
Module responsible for visualization of the graph.
"""

import networkx
import numpy as np
from networkx import Graph

from agh_graphs.utils import find_overlapping_vertices, pull_vertices_apart, pull_vertex_towards_neighbors


def visualize_graph_layer(graph: Graph, layer: int):
    graph = graph.copy()

    __pull__overlapping_vertices_apart(graph, 0.05)

    to_remove = []
    for node, data in graph.nodes(data=True):
        if data['layer'] != layer:
            to_remove.append(node)

    graph.remove_nodes_from(to_remove)

    colors = [__get_color(d) for n, d in graph.nodes(data=True)]
    networkx.draw(
        graph,
        networkx.get_node_attributes(graph, 'position'),
        labels=networkx.get_node_attributes(graph, 'label'),
        node_color=colors,
        with_labels=True)


def visualize_graph_3d(graph: Graph):
    graph = graph.copy()

    __pull__overlapping_vertices_apart(graph, 0.05)
    colors = [__get_color(d) for n, d in graph.nodes(data=True)]
    networkx.draw(
        graph,
        __project_nodes(graph.nodes(data=True)),
        labels=networkx.get_node_attributes(graph, 'label'),
        node_color=colors,
        with_labels=True)


def __get_color(node_data):
    if node_data['label'] in {'e', 'E'}:
        return '#5081bd'

    if node_data['label'] in {'i', 'I'}:
        return '#c0504d'

    return 'red'


def __project_node(nodes_data, focus_on_layer=2):
    """
    Perform a 3D perspective projection on the node.
    """
    a = np.array([
        nodes_data['position'][0],
        nodes_data['position'][1],
        nodes_data['layer']
    ]).reshape(3, 1)

    # camera rotation
    rx, ry, rz = (-1.6, 0, -0.9)
    # camera position
    c = np.array([-4, -3, focus_on_layer - 4]).reshape(3, 1)

    mx = np.array([
        [1, 0, 0],
        [0, np.cos(rx), np.sin(rx)],
        [0, -np.sin(rx), np.cos(rx)],
    ])
    my = np.array([
        [np.cos(ry), 0, -np.sin(ry)],
        [0, 1, 0],
        [np.sin(ry), 0, np.cos(ry)],
    ])
    mz = np.array([
        [np.cos(rz), np.sin(rz), 0],
        [-np.sin(rz), np.cos(rz), 0],
        [0, 0, 1],
    ])

    d = mx.dot(my).dot(mz).dot(a - c).reshape(3)

    return (
        d[0] / d[2],
        d[1] / d[2],
    )


def __project_nodes(nodes):
    return {n: __project_node(d) for n, d in nodes}


def __pull_overlapping_vertices_towards_neighbors(graph: Graph, factor: float):
    overlapping = find_overlapping_vertices(graph)

    to_pull_apart = set()
    for a, b in overlapping:
        to_pull_apart.add(a)
        to_pull_apart.add(b)

    for n in to_pull_apart:
        pull_vertex_towards_neighbors(graph, n, factor)


def __pull__overlapping_vertices_apart(graph: Graph, factor: float):
    overlapping = find_overlapping_vertices(graph)

    for a, b in overlapping:
        pull_vertices_apart(graph, a, b, factor)
