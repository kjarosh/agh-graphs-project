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
    Returns angle (0-180) between segment and positive X-axis
    """
    x = b[0] - a[0]
    y = b[1] - a[1]
    return math.degrees(math.atan2(y, x)) % 180


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


def sort_vertices_by_coordinates(graph: Graph, vertices: [str]):
    """
    Returns list of vertices sorted by x coordinate and then y coordinate.
    """
    def key(item):
        return graph.nodes()[item]['position']

    return sorted(vertices, key=key)


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
                pos_a = node_a_data['position']
                pos_b = node_b_data['position']
                if is_close(pos_a, pos_b):
                    overlapping.append((node_a_id, node_b_id))
    return overlapping


def join_overlapping_vertices(graph: Graph, vertex1, vertex2, layer):
    """
    Joins two vertices by moving all edges from `vertex2` to `vertex1`,
    then it removes `vertex2`.

    'vertex1', 'vertex2' - vertices to join, should be overlapping

    Returns vertex1 if joined.
    Returns None if vertices are not overlapping.
    """

    v1_pos = graph.nodes()[vertex1]['position']
    v2_pos = graph.nodes()[vertex2]['position']

    if is_close(v1_pos, v2_pos):
        vertex1_neighbors = get_neighbors_at(graph, vertex1, layer)
        vertex2_neighbors = get_neighbors_at(graph, vertex2, layer)

        for vertex2_neighbor in vertex2_neighbors:
            if vertex2_neighbor not in vertex1_neighbors:
                graph.add_edge(vertex1, vertex2_neighbor)
        graph.remove_node(vertex2)
        return vertex1

    return None


def get_common_neighbors(graph: Graph, v1: str, v2: str, on_layer: int = None) -> [str]:
    """
    Returns common neighbors of vertexes `v1` and `v2` that are on layer `on_layer`

    If `on_layer` is `None` (default) all common neighbors are returned.
    """
    neighbors1 = set(graph.neighbors(v1))
    neighbors2 = set(graph.neighbors(v2))
    common = neighbors1 & neighbors2
    if on_layer:
        return [v for v in common if graph.nodes[v]['layer'] == on_layer]
    else:
        return list(common)


def get_vertex_between(graph, v1, v2, layer=None, label=None):
    """
    Returns the node between `v1` and `v2` on layer `layer` with
    label `label`. Returns `None` if not found.

    Parameters `layer` or `label` may be `None`, and they are not
    taken into account when searching then.
    """
    (v1_x, v1_y) = graph.nodes[v1]['position']
    (v2_x, v2_y) = graph.nodes[v2]['position']
    desired_position = ((v1_x + v2_x) / 2, (v1_y + v2_y) / 2)
    neighbors = [n for n in graph.neighbors(v1)
                 if n in graph.neighbors(v2)
                 and (layer is None or graph.nodes[n]['layer'] == layer)
                 and (label is None or graph.nodes[n]['label'] == label)
                 and is_close(graph.nodes[n]['position'], desired_position)]
    if len(neighbors) != 1:
        return None
    return neighbors[0]


def is_close(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return math.isclose(x1, x2) and math.isclose(y1, y2)
