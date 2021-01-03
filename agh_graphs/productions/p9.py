from typing import List

from networkx import Graph

from agh_graphs.production import Production
from agh_graphs.utils import gen_name, add_interior, get_neighbors_at


class P9(Production):

    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        # Production based on P2
        self.__check_prod_input(graph, prod_input)

        [i] = prod_input
        i_data = graph.nodes[i]
        i_data['label'] = 'i'
        i_layer = i_data['layer']
        new_layer = i_layer + 1

        i_neighbors = get_neighbors_at(graph, i, i_layer)

        # create new 'E' nodes in the next layer
        new_e1 = gen_name()
        new_e2 = gen_name()
        new_e3 = gen_name()

        e1_pos = graph.nodes[i_neighbors[0]]['position']
        e2_pos = graph.nodes[i_neighbors[1]]['position']
        e3_pos = graph.nodes[i_neighbors[2]]['position']

        graph.add_node(new_e1, layer=new_layer, position=e1_pos, label='E')
        graph.add_node(new_e2, layer=new_layer, position=e2_pos, label='E')
        graph.add_node(new_e3, layer=new_layer, position=e3_pos, label='E')

        # create edges between new 'E' nodes
        graph.add_edge(new_e1, new_e2)
        graph.add_edge(new_e2, new_e3)
        graph.add_edge(new_e3, new_e1)

        # create new 'I' node and edges between new 'I' nodes and new 'E' nodes
        i1 = add_interior(graph, new_e1, new_e2, new_e3)

        # create edges between new 'I' node and parent 'i' node
        graph.add_edge(i1, i)

        return [i1]

    @staticmethod
    def __check_prod_input(graph, prod_input):
        if len(prod_input) != 1:
            raise ValueError('wrong number of interiors')
        i_node_id = prod_input[0]
        i_node_data = graph.nodes[i_node_id]
        i_node_layer = i_node_data['layer']

        if i_node_data['label'] != 'I':
            raise ValueError("wrong interior label") 

        neighbors = get_neighbors_at(graph, i_node_id, i_node_layer)
        if len(neighbors) != 3:
            raise ValueError("interior with wrong number of edges")

        for n_id in neighbors:
            if graph.nodes[n_id]['label'] != 'E':
                raise ValueError("wrong vertex label")
            n_expected_neighbors = [x for x in neighbors if x != n_id]
            n_neighbors = get_neighbors_at(graph, n_id, i_node_layer)
            for expected_neighbor in n_expected_neighbors:
                if expected_neighbor not in n_neighbors:
                    raise ValueError("missing edge between vertices")
