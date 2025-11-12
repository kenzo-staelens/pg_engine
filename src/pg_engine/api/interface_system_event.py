from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import pygame

from .interface_system import ISystem
from .singleton import Singleton

if TYPE_CHECKING:
    from .interface_gameobject import IGameObject
    from .interface_scene import IScene


class IEventSystem(ISystem, Singleton, ABC):

    """
    Base Class for :term:`EventSystem`.

    :term:`__singleton_key__` = 'EventSystem'
    """

    __singleton_key__ = 'EventSystem'

    @abstractmethod
    def update_system(self, dt: int) -> None:
        """
        Handle system events separate from game events.

        :param dt: milliseconds since last frame
        :type dt: int
        """

    @classmethod
    @abstractmethod
    def send(
        cls,
        event_type: int,
        targets: list[IGameObject] | None,
        data: dict[str, Any] | None = None,
        system: bool = False,
    ) -> None:
        """
        Send an event to one or more specified targets.

        :param event_type: type of the event in pygame
        :type event_type: int
        :param targets: list of gameobjects with scope :attr:`Scope.LOCAL`\
            that receive the event
        :type targets: list[IGameObject] | None
        :param data: metadata for the event, defaults to None
        :type data: dict | None, optional
        :param system: is a system event, defaults to False
        :type system: bool, optional
        """

    @classmethod
    @abstractmethod
    def broadcast_scene(
        cls,
        event_type: int,
        scene_name: str,
        data: dict | None = None,
        system: bool = False,
    ) -> None:
        """
        Broadcast an event to scope :attr:`Scope.BROADCAST` listeners.

        :param event_type: type of the event in pygame
        :type event_type: int
        :param scene_name: target scene to send the event to
        :type scene_name: str
        :param data: metadata for the event, defaults to None
        :type data: dict | None, optional
        :param system: is a system event, defaults to False
        :type system: bool, optional
        """

    @classmethod
    @abstractmethod
    def broadcast(
        cls,
        event_type: int,
        data: dict | None = None,
        system: bool = False,
    ) -> None:
        """
        Broadcast an event to scope :attr:`Scope.BROADCAST` listeners.

        :param event_type: type of the event in pygame
        :type event_type: int
        :param data: metadata for the event, defaults to None
        :type data: dict | None, optional
        :param system: is a system event, defaults to False
        :type system: bool, optional
        """

    @abstractmethod
    def register_event_hook(
        self,
        event_type: int,
        listener: Any,  # noqa: ANN401
        hook: Callable[[pygame.event.Event], None],
    ) -> None:
        """
        Register a callable to listen to events of scope :attr:`Scope.LOCAL`.

        :param event_type: event type the callable listens to
        :type event_type: int
        :param listener: listener owning this event hook
        :type listener: IGameObject | None
        :param hook: the callable functioning as eventlistener
        :type hook: Callable[[pygame.event.Event], None]
        """

    @abstractmethod
    def register_broadcast_hook(
        self,
        event_type: int,
        scene: IScene | None,
        hook: Callable[[pygame.event.Event], None],
    ) -> None:
        """
        Register a callable to listen to scope :attr:`Scope.BROADCAST_SCENE` and :attr:`Scope.BROADCAST`.

        :param event_type: event type the callable listens to
        :type event_type: int
        :param scene: the scene this hook resides in or None for :attr:`Scope.BROADCAST`
        :param hook: the callable functioning as eventlistener
        :type hook: Callable[[pygame.event.Event], None]
        """  # noqa: E501


__all__ = [
    'IEventSystem',
]
