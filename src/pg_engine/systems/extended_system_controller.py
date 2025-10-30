import itertools
from collections.abc import Callable

from pg_engine.api import (
    IGameObject,
    ISystem,
)

from .base_system_controller import BaseSystemController


class ExtendedSystemController(BaseSystemController):

    """System Controller with ability to dynamically link more systems."""

    def __init__(self, extended_systems: dict[str, ISystem] | None = None):
        """
        Initialize system controller with extra systems.

        :param extended_systems: Extra systems added, defaults to None
        :type extended_systems: dict[str, ISystem] | None, optional
        """
        self.extended_systems = extended_systems or {}
        super().__init__()

    def update(self, dt: int) -> None:
        super().update(dt)
        for system in self.extended_systems.values():
            system.update(dt)

    def remove_gameobject(self, gameobject: IGameObject) -> None:
        for system in self.extended_systems.values():
            system.remove_gameobject(gameobject)

    def get_sequence_hooks(self) -> list[Callable]:
        extended_hooks = list(itertools.chain(
            system.get_sequence_hooks()
            for system in self.extended_systems.values()
        ))
        return super().get_sequence_hooks() + extended_hooks
