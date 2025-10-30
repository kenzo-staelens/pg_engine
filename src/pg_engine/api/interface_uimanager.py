from abc import ABC, abstractmethod
from typing import Any

import pygame

from .interface_configurable import IConfigurable
from .singleton import Singleton


class IUIManager(Singleton, IConfigurable, ABC):

    """
    Base class for handling UI operations and objects.

    written in the style of pygame_gui uimanager

    :term:`__singleton_key__` = 'UIManager'
    """

    __singleton_key__ = 'UIManager'

    @abstractmethod
    def __init__(self):
        self.manager: Any
        self.size: tuple[int, int]

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def draw_ui(self, render_surface: pygame.Surface) -> None:
        """
        Render the ui on the screen.

        :param render_surface: Pygame surface to render onto
        :type render_surface: pygame.Surface
        """

    @abstractmethod
    def process_events(self, event: pygame.Event) -> bool:
        """
        Process an event.

        :param event: pygame event or gui event (which extends the preceding)
        :type event: pygame.Event
        :return: whether the event was consumed
        :rtype: bool
        """
        return False

    @abstractmethod
    def set_visual_debug_mode(self, state: bool) -> None:
        """
        Enable or disable visual UI debugging.

        :param state: state to set
        :type state: bool
        """

    @abstractmethod
    def set_active_scene(self, scene: str) -> None:
        """
        Enable the UI of the active scene and disable all others.

        :param scene: scene to change UI for
        :type scene: str
        """

    @abstractmethod
    def hide_all(self) -> None:
        """Hide all UI elements/scenes."""


__all__ = [
    'IUIManager',
]
