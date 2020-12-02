"""
Utility module.
"""
import math
import uuid

from networkx import Graph


def gen_name():
    return str(uuid.uuid1())


def centroid(a, b, c):
    """
    Returns the centroid of the triangle defined by the given points:
    a, b, and c.
    """
    return tuple(sum(s) / len(s) for s in zip(a, b, c))


def angle_with_x_axis(a: (int, int), b: (int, int)) -> float:
    """
    Returns angle between segment and positive X-axis
    """
    x = b[0] - a[0]
    y = b[1] - a[1]
    return math.degrees(math.atan2(y, x)) % 360


def add_interior(graph: Graph, a_name, b_name, c_name):
    """
    Adds a node which represents the interior of the triangle defined by
    nodes with names: a_name, b_name and c_name.
    """
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


def get_segment_with_lowest_angle(graph, segment_ids):
    segments = []
    for segment in segment_ids:
        pos1 = graph.nodes[segment[0]]['position']
        pos2 = graph.nodes[segment[1]]['position']
        segments.append((pos1, pos2))

    min_angle = angle_with_x_axis(segments[0][0], segments[0][1])
    min_segment_idx = 0
    for i in range(0, len(segments)):
        angle = angle_with_x_axis(segments[i][0], segments[i][1])
        if angle < min_angle:
            min_angle = angle
            min_segment_idx = i
    return segment_ids[min_segment_idx]


def get_neighbors_at(graph: Graph, vertex, layer):
    neighbors = list(graph.neighbors(vertex))
    return [v for v in neighbors if graph.nodes[v]['layer'] == layer]


def add_break_vertex(graph: Graph, segment_ids) -> str:
    (v1, v2) = get_segment_with_lowest_angle(graph, segment_ids)

    layer = graph.nodes[v1]['layer']
    v1_pos = graph.nodes[v1]['position']
    v2_pos = graph.nodes[v2]['position']

    v_x = (v1_pos[0] + v2_pos[0]) / 2
    v_y = (v1_pos[1] + v2_pos[1]) / 2

    v_pos = (v_x, v_y)
    v = gen_name()

    graph.add_node(v, layer=layer, position=v_pos, label='E')

    graph.remove_edge(v1, v2)
    graph.add_edge(v1, v)
    graph.add_edge(v2, v)

    return v
