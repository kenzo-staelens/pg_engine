from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface_gameobject import IGameObject


class IComponent(ABC):

    """Base class for components."""

    def __init__(self, source: IGameObject):
        """
        Initialize the component.

        :param source: Gameobject the component belongs to.
        :type source: IGameObject
        """
        self.source = source

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """


__all__ = [
    'IComponent',
]
