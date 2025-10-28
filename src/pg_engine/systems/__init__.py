from .base_system_controller import BaseSystemController
from .event_system import (
    EventSystem,
    Scope,
    listen,
    EventListener,
    SystemEventQueue,
    NOTIFY,
)
from .collision_system import (
    COLLISION,
    TRIGGER,
    CollisionSystem,
    CollisionScript,
)

from pg_engine.core.bases import ClassRegistry, Initializer

for to_initialize in [
    BaseSystemController,
    EventSystem,
    CollisionSystem,
    SystemEventQueue,
]:
    Initializer.add_hooks(
        lambda c=to_initialize: ClassRegistry.register(c),
        None,
    )

__all__ = [
    # custom events
    'COLLISION',
    'NOTIFY',
    'TRIGGER',

    # classes
    'BaseSystemController',
    'CollisionScript',
    'CollisionSystem',
    'EventListener',
    'EventSystem',
    'Scope',
    'SystemEventQueue',

    # decorators
    'listen',
]
