from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING

from .singleton import Singleton

if TYPE_CHECKING:
    from .interface_gameobject import IGameObject
    from .interface_system_collision import ICollisionSystem
    from .interface_system_event import IEventSystem


class ISystemController(Singleton, ABC):

    """
    Base Class for :term:`SystemController`.

    keeps track and schedules operations for all instances of :class:`ISystem`

    :term:`__singleton_key__` = 'SystemController'
    """

    __singleton_key__ = 'SystemController'

    def __init__(self):
        """
        Initialize the systemcontroller.

        Minimally requires a collision_system and event_system.
        """
        super().__init__()
        self.collision_system: ICollisionSystem
        self.event_system: IEventSystem

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
        Propagate call to :func:`~ISystem.remove_gameobject` to all systems.

        :param gameobject: The gameobject to remove
        :type gameobject: IGameObject
        """

    @abstractmethod
    def get_sequence_hooks(self) -> list[Callable[[int], None]]:
        """
        Get all systems' hooks which should be called by instances of this class.

        :return: The systems' callables taking `dt` and handle a part of the engine.
        :rtype: Iterable[Callable[[int], None]]
        """


__all__ = [
    'ISystemController',
]
