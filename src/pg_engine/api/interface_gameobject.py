from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .interface_game import IGame

if TYPE_CHECKING:
    from .interface_component import IComponent
    from .interface_component_transform import ITransformComponent
    from .interface_container import IContainer
    from .interface_scene import IScene


class IGameObject(ABC):
    def __init__(self, scene: IScene, name: str):
        """
        Initialize the gameobject.

        :param scene: scene this gameobject belongs to
        :type scene: str
        :param name: name of this gameobject
        :type name: str
        """
        self.scene: str = scene
        self.name = name
        self.components: IContainer[IComponent]
        self.parent: IGameObject | None = None
        #: used to determine whether this object has already been destroyed
        #: during event processing and should still be handled or not
        self.exists = True

    def destroy(self) -> None:
        """Remove this gameobject from the game and set it's :attr:`~exists` flag to false."""  # noqa: E501
        IGame().remove_gameobject(self)
        self.exists = False

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @property
    @abstractmethod
    def transform(self) -> ITransformComponent:
        """
        Get this Game object's transform component or create a default if none exists.

        :return: this game object's transform component
        :rtype: ITransformComponent
        """


__all__ = [
    'IGameObject',
]
