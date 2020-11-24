"""
Module responsible for production evaluation. Based on the given productions
and initial graph, the productions are applied and the resulting graph is created.
"""
import logging

import networkx
from networkx import Graph

from production import Production, ProductionType


class Evaluator:
    layer: int = 0
    creation_productions: [Production]
    modification_productions: [Production]
    graph: Graph

    def __init__(self, productions: [Production], graph: Graph) -> None:
        super().__init__()

        self.creation_productions = []
        self.modification_productions = []
        for production in productions:
            if production.get_type() == ProductionType.layer_creation:
                self.creation_productions.append(production)
            elif production.get_type() == ProductionType.layer_modification:
                self.modification_productions.append(production)
        self.graph = graph

    def evaluate_next_layer(self):
        logging.info('Evaluating next layer from layer {}'.format(self.layer))

        logging.debug('Applying creation productions')
        self.apply_productions(self.creation_productions)
        logging.debug('Applying modification productions')
        self.apply_productions(self.modification_productions)
        self.layer += 1

    def apply_productions(self, productions: [Production]):
        i = 0
        while True:
            i += 1
            logging.debug('Applying productions ({})'.format(i))

            old_graph = self.graph.copy()
            for production in productions:
                production.apply(self.layer, self.graph)
            if networkx.is_isomorphic(old_graph, self.graph):
                break
