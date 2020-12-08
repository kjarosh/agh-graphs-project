"""
This module contains the basic code for productions. You can add your own
production by extending the `Production` class.
"""
from abc import ABC, abstractmethod
from typing import List

from networkx import Graph


class Production(ABC):

    @abstractmethod
    def apply(self, graph: Graph, prod_input: List[str], orientation: int = 0, **kwargs) -> List[str]:
        """
        Apply the production on `graph`.

        `prod_input` is a list of vertexes ids that this production should use.
        It contains ids of `I` or `i` vertexes. Ids of other vertexes (e.g. E)
        can be obtained by checking `I` or `i` neighbours.

        This function should return list of vertexes ids that should be used
        in the next production.
        """
        pass

    def __str__(self) -> str:
        return self.__class__.__name__
