from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

import pygame

from .interface_configurable import IConfigurable
from .singleton import Singleton

if TYPE_CHECKING:
    from .interface_uimanager import IUIManager


class IRenderer(Singleton, IConfigurable, ABC):

    """
    Base class for Renderers.

    :term:`__singleton_key__` = 'Renderer'
    """

    __singleton_key__ = 'Renderer'

    def __init__(self):
        self.uimanager: IUIManager
        self.render_surface: pygame.Surface
        self.size: tuple[int, int]
        #: flag to listen for triggered cache updates
        #: this causes less cache updates when a lot of objects
        #: get created in the same frame
        self.scheduled_update: bool = False

    @abstractmethod
    def render(self) -> None:
        """Render all renderables."""

    @classmethod
    @abstractmethod
    def apply_camera(cls, position: Iterable[int | float]) -> Iterable[int | float]:
        """
        Apply the transformation of :class:`ICamera` onto the rendered view.

        :param position: Position to apply the camera onto
        :type position: Iterable[int  |  float]
        :return: Resulting position after applying the camera
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def clear(self) -> None:
        """Clear the screen."""

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def update_cache(self) -> None:
        """
        Update the internal cache.

        Cache should be updated at most once per frame and should use
        :attr:`~scheduled_update` for that check.
        """


__all__ = [
    'IRenderer',
]
