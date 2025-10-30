from __future__ import annotations

import contextlib
from abc import ABC, abstractmethod
from functools import cached_property

import pygame

from .interface_component import IComponent
from .interface_renderable import IRenderable
from .interface_system_collision import ICollisionSystem
from .post_init import PostInit


class IColliderComponent(IComponent, IRenderable, ABC, metaclass=PostInit):

    """Base class of components used in collision checks."""

    def __init__(
        self,
        collision_layers: list[str],
        physics: bool,
        # active disable via config; needs game debug mode = true
        debug_mode: bool = True,
        **kw,
    ):
        """
        Initialize the collider.

        :param collision_layers: :term:`collision layers` on which\
            this collider listens.
        :type collision_layers: list[str]
        :param physics: whether this collider is a phyisics collider or a trigger.
        :type physics: bool
        :param debug_mode: whether this collider should render debug data,\
            defaults to True
        :type debug_mode: bool, optional
        """
        super().__init__(**kw)
        self.collision_layers = collision_layers
        self.physics = physics
        self.debug_mode = debug_mode

    @cached_property
    def mask(self) -> pygame.Mask:
        """Attribute looked at by pygame for mask_collision."""
        return self._create_collision_mask()

    @abstractmethod
    def _create_collision_mask(self) -> pygame.Mask:
        """Calculate the collision mask of this component's source object."""

    def update_mask(self) -> None:
        """
        Get rid of the currently cached mask.

        This implementation deletes the currently cached mask attribute such that\
            the engine can lazily recalculate the mask next time it is requested.
        """
        with contextlib.suppress(AttributeError):
            del self.mask

    def __post_init__(self):
        """Add this component to the collision system to be processed on init."""
        system = ICollisionSystem()
        for layer in self.collision_layers:
            system.add(self, layer)


__all__ = [
    'IColliderComponent',
]
