"""
Utility module.
"""
import uuid

from networkx import Graph


def gen_name():
    return str(uuid.uuid1())


def centroid(a, b, c):
    return tuple(sum(s) / len(s) for s in zip(a, b, c))


def add_interior(graph: Graph, a_name, b_name, c_name):
    node_positions = graph.nodes(data='position')
    node_layers = graph.nodes(data='layer')
    a_pos = node_positions[a_name]
    b_pos = node_positions[b_name]
    c_pos = node_positions[c_name]

    layer = node_layers[a_name]
    if layer != node_layers[b_name] or layer != node_layers[c_name]:
        raise RuntimeError('Nodes lay on different layers')

    i_name = gen_name()
    i_pos = centroid(a_pos, b_pos, c_pos)

    graph.add_node(i_name, layer=layer, position=i_pos, label='I')
    graph.add_edge(i_name, a_name)
    graph.add_edge(i_name, b_name)
    graph.add_edge(i_name, c_name)

    return i_name


def get_node_at(graph, layer, pos):
    nodes = [x for x, y in graph.nodes(data=True) if
             y['position'] == pos and y['layer'] == layer]
    if len(nodes) == 0:
        return None
    if len(nodes) > 1:
        raise RuntimeError(
            'Multiple nodes with the given position: {}'.format(nodes))
    return nodes[0]
