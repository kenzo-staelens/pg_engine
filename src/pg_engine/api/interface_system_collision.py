from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

from .interface_system import ISystem
from .singleton import Singleton

if TYPE_CHECKING:
    from .interface_component_collider import IColliderComponent


class ICollisionSystem(ISystem, Singleton, ABC):

    """
    :py:class:`Singleton` Extension to :py:class:`ISystem` to handle collisions.

    :term:`__singleton_key__` = 'CollisionSystem'
    """

    __singleton_key__ = 'CollisionSystem'

    @abstractmethod
    def get_groups(
            self,
            interraction: frozenset[str],
        ) -> tuple[
            pygame.sprite.Group,
            pygame.sprite.Group,
            bool,
        ]:
        """
        Get Collision Data.

        Gets two spritegroups and a bool indicating whether the\
            collision groups are the same.

        :param interraction: the interraction (set by :func:`~.enable_collision`)
        :type interraction: frozenset[str]
        :return: Collision data
        :rtype: tuple[ pygame.sprite.Group, pygame.sprite.Group, bool, ]
        """

    @abstractmethod
    def add(self, collider_component: IColliderComponent, layer: str) -> None:
        """
        Add a collider to be handled by the system.

        :param collider_component: Component to be added to the system
        :type collider_component: IColliderComponent
        :param layer: collision layer the component should be added into
        :type layer: str
        """

    @abstractmethod
    def enable_collision(self, layer1: str, layer2: str) -> None:
        """
        Enable collisions between two collision layers (interchangeable).

        :param layer1: first layer in the interraction
        :type layer1: str
        :param layer2: second layer in the collision
        :type layer2: str
        """


__all__ = [
    'ICollisionSystem',
]
