"""
This module contains the basic code for productions. You can add your own
production by extending the `Production` class.
"""
from abc import ABC, abstractmethod
from enum import Enum

from networkx import Graph


class ProductionType(Enum):
    layer_creation = 1
    layer_modification = 2


class Production(ABC):
    @abstractmethod
    def get_type(self) -> ProductionType:
        """
        Returns the type of the production: if this production adds a new layer,
        its type should be `ProductionType.layer_creation`, if this production only
        modifies a layer, it should be `ProductionType.layer_modification`.
        """
        pass

    @abstractmethod
    def apply(self, layer: int, graph: Graph) -> None:
        """
        Apply the production on `graph`. The `layer` param tells which layer this
        production should act upon.

        If the production is creating a new layer, it should create the layer
        only from the given layer.

        If the production modifies a layer, the upper layer should be equal to
        the given layer.
        """
        pass

    def __str__(self) -> str:
        return self.__class__.__name__
