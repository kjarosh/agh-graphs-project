from matplotlib import pyplot
from networkx import Graph

from agh_graphs.productions.p1 import P1
from agh_graphs.productions.p12 import P12
from agh_graphs.productions.p13 import P13
from agh_graphs.productions.p2 import P2
from agh_graphs.productions.p6 import P6
from agh_graphs.productions.p9 import P9
from agh_graphs.utils import gen_name
from agh_graphs.visualize import visualize_graph_3d, visualize_graph_layer


def derive_e():
    g = Graph()
    initial_node_name = gen_name()
    g.add_node(initial_node_name, layer=0, position=(0.5, 0.5), label='E')

    # Layer 1
    [a1, a2] = P1().apply(g, [initial_node_name])

    # Layer 2
    [b3, b2] = P2().apply(g, [a1], orientation=1)
    [b4, b1] = P2().apply(g, [a2], orientation=1)
    P6().apply(g, [a1, a2, b1, b2, b3, b4])

    # Layer 3
    [c3, c2] = P2().apply(g, [b1], orientation=1)
    [i11, c1] = P2().apply(g, [b2])
    [i13, i12] = P2().apply(g, [b3], orientation=1)
    [i14, c4] = P2().apply(g, [b4])
    P12().apply(g, [b3, b4, i13, i14])
    P12().apply(g, [b1, b4, c3, c4])
    P12().apply(g, [b2, b1, c1, c2])
    P13().apply(g, [b2, b3, i11, i12])

    # Layer 4
    [new_i11] = P9().apply(g, [i11])
    [new_i12] = P9().apply(g, [i12])
    [new_i13] = P9().apply(g, [i13])
    [new_i14] = P9().apply(g, [i14])
    [i22, d1] = P2().apply(g, [c1], orientation=1)
    [d3, d2] = P2().apply(g, [c2], orientation=1)
    [d4, d5] = P2().apply(g, [c3], orientation=2)
    [i25, d6] = P2().apply(g, [c4], orientation=2)
    P12().apply(g, [i12, i13, new_i12, new_i13])
    P12().apply(g, [i13, i14, new_i13, new_i14])
    P12().apply(g, [i14, c4, new_i14, i25])
    P12().apply(g, [i11, c1, new_i11, i22])
    P12().apply(g, [c2, c3, d3, d4])
    P6().apply(g, [c1, c2, d1, d2, d3, i22])
    P6().apply(g, [c3, c4, d4, d5, d6, i25])
    P13().apply(g, [i11, i12, new_i11, new_i12])
    i11 = new_i11
    i12 = new_i12
    i13 = new_i13
    i14 = new_i14

    # Layer 5
    [new_i11] = P9().apply(g, [i11])
    [new_i12] = P9().apply(g, [i12])
    [new_i13] = P9().apply(g, [i13])
    [new_i14] = P9().apply(g, [i14])
    [new_i22] = P9().apply(g, [i22])
    [new_i25] = P9().apply(g, [i25])
    [i21, e1] = P2().apply(g, [d1])
    [e3, e2] = P2().apply(g, [d2], orientation=1)
    [i23, e4] = P2().apply(g, [d3])
    [i24, e5] = P2().apply(g, [d4])
    [e7, e6] = P2().apply(g, [d5], orientation=1)
    [i26, e8] = P2().apply(g, [d6])
    P12().apply(g, [i12, i13, new_i12, new_i13])
    P12().apply(g, [i13, i14, new_i13, new_i14])
    P12().apply(g, [i11, i22, new_i11, new_i22])
    P12().apply(g, [i14, i25, new_i14, new_i25])
    P12().apply(g, [i22, d1, new_i22, i21])
    P12().apply(g, [i25, d6, new_i25, i26])
    P12().apply(g, [d2, d3, e3, e4])
    P12().apply(g, [d1, d2, e1, e2])
    P12().apply(g, [d4, d5, e5, e6])
    P12().apply(g, [d5, d6, e7, e8])
    P6().apply(g, [d3, d4, e4, e5, i23, i24])
    P13().apply(g, [d3, i22, new_i22, i23])
    P13().apply(g, [d4, i25, i24, new_i25])
    P13().apply(g, [i11, i12, new_i11, new_i12])
    i11 = new_i11
    i12 = new_i12
    i13 = new_i13
    i14 = new_i14
    i22 = new_i22
    i25 = new_i25

    # Layer 6
    [new_i11] = P9().apply(g, [i11])
    [new_i12] = P9().apply(g, [i12])
    [new_i13] = P9().apply(g, [i13])
    [new_i14] = P9().apply(g, [i14])
    [new_i21] = P9().apply(g, [i21])
    [new_i22] = P9().apply(g, [i22])
    [new_i23] = P9().apply(g, [i23])
    [new_i24] = P9().apply(g, [i24])
    [new_i25] = P9().apply(g, [i25])
    [new_i26] = P9().apply(g, [i26])
    P12().apply(g, [i12, i13, new_i12, new_i13])
    P12().apply(g, [i13, i14, new_i13, new_i14])
    P12().apply(g, [i11, i22, new_i11, new_i22])
    P12().apply(g, [i14, i25, new_i14, new_i25])
    P12().apply(g, [i21, i22, new_i21, new_i22])
    P12().apply(g, [i25, i26, new_i25, new_i26])
    [i31, i41] = P2().apply(g, [e1], orientation=1)
    [i42, f1] = P2().apply(g, [e2], orientation=1)
    [i43, f2] = P2().apply(g, [e3], orientation=2)
    [i32, i44] = P2().apply(g, [e4], orientation=2)
    [i33, i45] = P2().apply(g, [e5], orientation=1)
    [i46, f3] = P2().apply(g, [e6], orientation=1)
    [i47, f4] = P2().apply(g, [e7], orientation=2)
    [i34, i48] = P2().apply(g, [e8], orientation=2)
    P6().apply(g, [e1, e2, f1, i41, i42, i31])
    P6().apply(g, [e3, e4, f2, i43, i44, i32])
    P6().apply(g, [e5, e6, f3, i45, i46, i33])
    P6().apply(g, [e7, e8, f4, i47, i48, i34])
    P12().apply(g, [e2, e3, i42, i43])
    P12().apply(g, [e4, e5, i44, i45])
    P12().apply(g, [e6, e7, i46, i47])
    P12().apply(g, [i21, e1, new_i21, i31])
    P12().apply(g, [i23, e4, new_i23, i32])
    P12().apply(g, [i24, e5, new_i24, i33])
    P12().apply(g, [i26, e8, new_i26, i34])
    P13().apply(g, [i22, i23, new_i22, new_i23])
    P13().apply(g, [i23, i24, new_i23, new_i24])
    P13().apply(g, [i24, i25, new_i24, new_i25])
    P13().apply(g, [i11, i12, new_i11, new_i12])
    i11 = new_i11
    i12 = new_i12
    i13 = new_i13
    i14 = new_i14
    i21 = new_i21
    i22 = new_i22
    i23 = new_i23
    i24 = new_i24
    i25 = new_i25
    i26 = new_i26

    # Layer 7
    [new_i11] = P9().apply(g, [i11])
    [new_i12] = P9().apply(g, [i12])
    [new_i13] = P9().apply(g, [i13])
    [new_i14] = P9().apply(g, [i14])
    [new_i21] = P9().apply(g, [i21])
    [new_i22] = P9().apply(g, [i22])
    [new_i23] = P9().apply(g, [i23])
    [new_i24] = P9().apply(g, [i24])
    [new_i25] = P9().apply(g, [i25])
    [new_i26] = P9().apply(g, [i26])
    [new_i31] = P9().apply(g, [i31])
    [new_i32] = P9().apply(g, [i32])
    [new_i33] = P9().apply(g, [i33])
    [new_i34] = P9().apply(g, [i34])
    [new_i41] = P9().apply(g, [i41])
    [new_i42] = P9().apply(g, [i42])
    [new_i43] = P9().apply(g, [i43])
    [new_i44] = P9().apply(g, [i44])
    [new_i45] = P9().apply(g, [i45])
    [new_i46] = P9().apply(g, [i46])
    [new_i47] = P9().apply(g, [i47])
    [new_i48] = P9().apply(g, [i48])
    P12().apply(g, [i12, i13, new_i12, new_i13])
    P12().apply(g, [i13, i14, new_i13, new_i14])
    P12().apply(g, [i11, i22, new_i11, new_i22])
    P12().apply(g, [i14, i25, new_i14, new_i25])
    P12().apply(g, [i21, i22, new_i21, new_i22])
    P12().apply(g, [i25, i26, new_i25, new_i26])
    P12().apply(g, [i21, i31, new_i21, new_i31])
    P12().apply(g, [i23, i32, new_i23, new_i32])
    P12().apply(g, [i24, i33, new_i24, new_i33])
    P12().apply(g, [i26, i34, new_i26, new_i34])
    P12().apply(g, [i31, i41, new_i31, new_i41])
    P12().apply(g, [i31, i42, new_i31, new_i42])
    P12().apply(g, [i32, i43, new_i32, new_i43])
    P12().apply(g, [i32, i44, new_i32, new_i44])
    P12().apply(g, [i33, i45, new_i33, new_i45])
    P12().apply(g, [i33, i46, new_i33, new_i46])
    P12().apply(g, [i34, i47, new_i34, new_i47])
    P12().apply(g, [i34, i48, new_i34, new_i48])
    P12().apply(g, [i42, i43, new_i42, new_i43])
    P12().apply(g, [i44, i45, new_i44, new_i45])
    P12().apply(g, [i46, i47, new_i46, new_i47])
    [i52, i51] = P2().apply(g, [f1], orientation=1)
    [i54, i53] = P2().apply(g, [f2], orientation=1)
    [i56, i55] = P2().apply(g, [f3], orientation=1)
    [i58, i57] = P2().apply(g, [f4], orientation=1)
    P12().apply(g, [i41, f1, new_i41, i51])
    P12().apply(g, [i43, f2, new_i43, i53])
    P12().apply(g, [i45, f3, new_i45, i55])
    P12().apply(g, [i47, f4, new_i47, i57])
    P13().apply(g, [i22, i23, new_i22, new_i23])
    P13().apply(g, [i23, i24, new_i23, new_i24])
    P13().apply(g, [i24, i25, new_i24, new_i25])
    P13().apply(g, [i11, i12, new_i11, new_i12])
    P13().apply(g, [i42, f1, new_i42, i52])
    P13().apply(g, [i44, f2, new_i44, i54])
    P13().apply(g, [i46, f3, new_i46, i56])
    P13().apply(g, [i48, f4, new_i48, i58])

    return g


if __name__ == '__main__':
    graph = derive_e()

    visualize_graph_3d(graph)
    pyplot.show()

    visualize_graph_layer(graph, 7)
    pyplot.show()
