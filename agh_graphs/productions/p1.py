from typing import List

from networkx import Graph

from agh_graphs.production import Production
from agh_graphs.utils import gen_name, add_interior


class P1(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        [initial_node_id] = prod_input
        initial_node_data = graph.nodes[initial_node_id]

        if initial_node_data['layer'] != 0:
            raise ValueError('bad layer')

        if initial_node_data['label'] != 'E':
            raise ValueError('bad label')

        positions = self.__get_positions(kwargs['positions'] if 'positions' in kwargs else None)

        # change label
        initial_node_data['label'] = 'e'

        vx_tl = gen_name()
        vx_tr = gen_name()
        vx_bl = gen_name()
        vx_br = gen_name()
        graph.add_node(vx_bl, layer=1, position=positions[0], label='E')
        graph.add_node(vx_br, layer=1, position=positions[1], label='E')
        graph.add_node(vx_tl, layer=1, position=positions[2], label='E')
        graph.add_node(vx_tr, layer=1, position=positions[3], label='E')

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

    def __get_positions(self, positions):
        if positions is None:
            return [
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),
            ]
        if type(positions) != list:
            raise ValueError('positions should be a list')
        if len(positions) < 4:
            raise ValueError('too few positions')
        if len(positions) > 4:
            raise ValueError('too many positions')
        for pos in positions:
            if type(pos) != tuple or len(pos) != 2:
                raise ValueError('positions should be tuples of length = 2')
        return positions
