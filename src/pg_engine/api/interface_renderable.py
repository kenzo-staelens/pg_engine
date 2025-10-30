from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .interface_gameobject import IGameObject


class IRenderable(ABC):

    """Base class for renderable objects."""

    def __init__(self, layer: int, source: IGameObject):
        """
        Initialize the renderable.

        :param layer: Layer this object will be rendered (starting at 0)
        :type layer: int
        :param source: Gameobject this renderable belongs to
        :type source: IGameObject
        """
        self.source = source
        self.layer = layer
        self.render_state = True

    @abstractmethod
    def get_render_data(self) -> tuple[pygame.Surface, Iterable[int | float], int]:
        ...

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def scale(self, scale_by: float | Iterable[float]) -> None:
        """
        Scale the renderable in one or more dimensions.

        :param scale_by: scale equally in all dimensions if float otherwise\
        scale per dimension given in the iterable
        :type scale_by: float | Iterable[float]
        """


__all__ = [
    'IRenderable',
]
