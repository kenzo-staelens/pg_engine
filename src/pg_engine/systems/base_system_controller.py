from collections.abc import Callable

from pg_engine.api import (
    ICollisionSystem,
    IEventSystem,
    IGameObject,
    ISystemController,
)


class BaseSystemController(ISystemController):
    def __init__(self):
        super().__init__()
        self.collision_system = ICollisionSystem()
        self.event_system = IEventSystem()
        self.sequence_hooks: list[Callable] = self.get_sequence_hooks()

    def update(self, dt: int) -> None:
        for hook in self.sequence_hooks:
            hook(dt)
            self.event_system.update_system(dt)

    def remove_gameobject(self, gameobject: IGameObject) -> None:
        self.event_system.remove_gameobject(gameobject)
        self.collision_system.remove_gameobject(gameobject)

    def get_sequence_hooks(self) -> list[Callable]:
        return [
            *self.event_system.get_sequence_hooks(),
            *self.collision_system.get_sequence_hooks(),
        ]
