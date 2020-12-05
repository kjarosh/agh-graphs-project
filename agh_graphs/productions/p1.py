from typing import List

from networkx import Graph

from agh_graphs.production import Production
from utils import gen_name, add_interior


class P1(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0) -> List[str]:
        [initial_node_id] = prod_input
        initial_node_data = graph.nodes[initial_node_id]

        if initial_node_data['layer'] != 0:
            raise ValueError('bad layer')

        if initial_node_data['label'] != 'E':
            raise ValueError('bad label')

        # change label
        initial_node_data['label'] = 'e'

        midx, midy = initial_node_data['position']
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

        if orientation % 2 == 1:
            [vx_bl, vx_br, vx_tr, vx_tl] = [vx_br, vx_tr, vx_tl, vx_bl]

        graph.add_edge(vx_tl, vx_tr)
        graph.add_edge(vx_tr, vx_br)
        graph.add_edge(vx_br, vx_bl)
        graph.add_edge(vx_bl, vx_tl)
        graph.add_edge(vx_tr, vx_bl)

        i1 = add_interior(graph, vx_tl, vx_tr, vx_bl)
        i2 = add_interior(graph, vx_tr, vx_br, vx_bl)

        graph.add_edge(i1, initial_node_id)
        graph.add_edge(i2, initial_node_id)

        return [i1, i2]
