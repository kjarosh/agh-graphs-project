"""
Utility module.
"""
import functools
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
    Returns angle (0-360) between segment and positive X-axis
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


def add_break(graph: Graph, segment_ids: [(str, str)]) -> str:
    """
    You probably don't want to use this method anymore. Use add_break_in_segment instead.

    Adds a node that breaks proper segment.
    Proper segment is a segment with the smallest angle with positive x-axis.

    `segment_ids` - list of tuples. Each tuple consists of two vertexes ids that represents a segment. This means
    that there has to be an edge between these vertexes.

    Returns id of newly created vertex.
    """
    segment_to_break = get_segment_with_smallest_angle(graph, segment_ids)
    return add_break_in_segment(graph, segment_to_break)


def add_break_in_segment(graph: Graph, segment: (str, str)) -> str:
    """
    Adds a node that breaks given segment.

    Returns id of newly created vertex.
    """
    (v1, v2) = segment
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


def get_node_at(graph, layer, pos):
    nodes = [x for x, y in graph.nodes(data=True) if
             y['position'] == pos and y['layer'] == layer]
    if len(nodes) == 0:
        return None
    if len(nodes) > 1:
        raise RuntimeError(
            'Multiple nodes with the given position: {}'.format(nodes))
    return nodes[0]


def sort_segments_by_angle(graph: Graph, segment_ids: [(str, str)], desc: bool = False):
    """
    Returns list of segment ids sorted by angle with positive x-axis.
    If `desc` is set to true the order will be descending.
    """
    segments = {}
    for segment in segment_ids:
        pos1 = graph.nodes[segment[0]]['position']
        pos2 = graph.nodes[segment[1]]['position']
        segments[segment] = (pos1, pos2)

    def key(item):
        return angle_with_x_axis(item[1][0], item[1][1])

    sorted_segment_ids = [k for k, v in sorted(segments.items(), key=key)]

    if desc:
        sorted_segment_ids.reverse()
    return sorted_segment_ids


def get_segment_with_smallest_angle(graph, segment_ids):
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
    """
    Returns neighbors of the given `vertex` that lies on the layer `layer`.
    """
    neighbors = list(graph.neighbors(vertex))
    return [v for v in neighbors if graph.nodes[v]['layer'] == layer]


def get_vertex_pull(graph: Graph, vertex: str):
    """
    Return the average vector calculated from edges of the vertex.
    """
    positions = graph.nodes(data='position')
    (x, y) = positions[vertex]
    (x_pull, y_pull) = (0.0, 0.0)
    n_count = 0
    for neighbor in graph.neighbors(vertex):
        n_count += 1
        (n_x, n_y) = positions[neighbor]
        x_pull += n_x - x
        y_pull += n_y - y

    x_pull /= n_count
    y_pull /= n_count

    return x_pull, y_pull


def pull_vertex_towards_neighbors(graph: Graph, vertex: str, factor: float):
    """
    Change the position of the vertex in the direction of its
    edges by the given factor.
    """
    positions = graph.nodes(data='position')
    (x, y) = positions[vertex]
    (x_pull, y_pull) = get_vertex_pull(graph, vertex)

    x_pull *= factor
    y_pull *= factor

    graph.nodes()[vertex]['position'] = (x + x_pull, y + y_pull)


def pull_vertices_apart(graph: Graph, vertex_a: str, vertex_b: str, factor: float):
    """
    Change the position of the vertices in the opposite direction obtained from
    their edges so that distance between them is equal to the given parameter.
    """
    positions = graph.nodes(data='position')
    (a_x, a_y) = positions[vertex_a]
    (b_x, b_y) = positions[vertex_b]

    (a_pull_x, a_pull_y) = get_vertex_pull(graph, vertex_a)
    (b_pull_x, b_pull_y) = get_vertex_pull(graph, vertex_b)

    (dir_x, dir_y) = (b_pull_x - a_pull_x, b_pull_y - a_pull_y)
    dir_x *= factor / 2
    dir_y *= factor / 2

    graph.nodes()[vertex_a]['position'] = (a_x - dir_x, a_y - dir_y)
    graph.nodes()[vertex_b]['position'] = (b_x + dir_x, b_y + dir_y)


def find_overlapping_vertices(graph: Graph):
    def compare(a, b):
        a = a[1]
        b = b[1]
        if a['layer'] != b['layer']:
            return b['layer'] - a['layer']

        xpos = a['position']
        ypos = b['position']
        if xpos[0] != ypos[0]:
            return ypos[0] - xpos[0]

        return ypos[1] - xpos[1]

    sorted_nodes = sorted(graph.nodes(data=True), key=functools.cmp_to_key(compare))

    buckets = []

    bucket = []
    last_layer = -1
    last_x = 0
    for node_id, node_data in sorted_nodes:
        layer = node_data['layer']
        (x, y) = node_data['position']

        if layer != last_layer or not math.isclose(last_x, x):
            if len(bucket) >= 2:
                buckets.append(bucket)

            bucket = [(node_id, node_data)]
        else:
            bucket.append((node_id, node_data))

        last_layer = layer
        last_x = x

    overlapping = []
    for bucket in buckets:
        for node_a_id, node_a_data in bucket:
            for node_b_id, node_b_data in bucket:
                if node_a_id == node_b_id:
                    continue
                (a_x, a_y) = node_a_data['position']
                (b_x, b_y) = node_b_data['position']
                if math.isclose(a_x, b_x) and math.isclose(a_y, b_y):
                    overlapping.append((node_a_id, node_b_id))
    return overlapping
