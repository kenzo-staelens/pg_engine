from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface_gameobject import IGameObject


class IScene(ABC):

    """
    Base class for scenes.

    :param name: name of the scene
    :type name: str
    """

    def __init__(self, name: str):
        """
        Initialize the scene.

        :param name: name of the scene
        :type name: str
        """
        self.name = name
        self.gameobjects: list[IGameObject] = []
        self.active = False

    @abstractmethod
    def add_gameobject(self, gameobject: IGameObject) -> None:
        """
        Add a gameobject to internal representation.

        :param gameobject: Game object to add.
        :type gameobject: IGameObject
        """

    @abstractmethod
    def remove_gameobject(self, gameobject: IGameObject) -> None:
        """
        Remove a gameobject to internal representation.

        :param gameobject: Game object to remove.
        :type gameobject: IGameObject
        """

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """


__all__ = [
    'IScene',
]
