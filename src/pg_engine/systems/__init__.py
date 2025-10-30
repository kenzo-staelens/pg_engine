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

from .audio_system import AudioSystem

from pg_engine.api.registry import ClassRegistry
from pg_engine.core.bases import Initializer

for to_initialize in [
    AudioSystem,
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
    'AudioSystem',
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
