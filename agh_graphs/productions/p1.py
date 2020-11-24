from networkx import Graph

from agh_graphs.production import Production
from production import ProductionType
from utils import gen_name, add_interior


class P1(Production):
    def get_type(self) -> ProductionType:
        return ProductionType.layer_creation

    def apply(self, layer: int, graph: Graph) -> None:
        if layer != 0:
            # this production makes sense only on layer 0
            return
        if len(graph.nodes()) != 1:
            return

        initial_node, data = list(graph.nodes(data=True))[0]

        if data['label'] != 'E' or data['layer'] != 0:
            return

        # change label
        data['label'] = 'e'

        midx, midy = data['position']
        x = 2 * midx
        y = 2 * midy

        vx_tl = gen_name()
        vx_tr = gen_name()
        vx_bl = gen_name()
        vx_br = gen_name()
        graph.add_node(vx_bl, layer=1, position=(0, 0), label='E')
        graph.add_node(vx_br, layer=1, position=(x, 0), label='E')
        graph.add_node(vx_tl, layer=1, position=(0, y), label='E')
        graph.add_node(vx_tr, layer=1, position=(x, y), label='E')

        graph.add_edge(vx_tl, vx_tr)
        graph.add_edge(vx_tr, vx_br)
        graph.add_edge(vx_br, vx_bl)
        graph.add_edge(vx_bl, vx_tl)
        graph.add_edge(vx_tr, vx_bl)

        i1 = add_interior(graph, vx_tl, vx_tr, vx_bl)
        i2 = add_interior(graph, vx_tr, vx_br, vx_bl)

        graph.add_edge(i1, initial_node)
        graph.add_edge(i2, initial_node)
