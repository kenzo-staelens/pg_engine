from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface_gameobject import IGameObject


class ISystem(ABC):

    """Base class of systems managed by :py:class:`ISystemController`."""

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def remove_gameobject(self, gameobject: IGameObject) -> None:
        """
        Remove a gameobject from this system's processing.

        :param gameobject: The gameobject to remove
        :type gameobject: IGameObject
        """

    @abstractmethod
    def get_sequence_hooks(self) -> Iterable[Callable[[int], None]]:
        """
        Get this system's hooks which should be called by :class:`ISystemController`.

        :return: This system's callables taking `dt` and handle a part of the engine.
        :rtype: Iterable[Callable[[int], None]]
        """


__all__ = [
    'ISystem',
]
