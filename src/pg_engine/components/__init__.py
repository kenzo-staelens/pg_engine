from .transform_component import (
    TransformComponent2D,
)
from .script_component import ScriptComponent
from .sprite_component import SpriteComponent
from .rect_collider_component import RectColliderComponent
from .game_object import GameObject

from pg_engine.core.bases import ClassRegistry, Initializer

for to_initialize in [
    RectColliderComponent,
    ScriptComponent,
    TransformComponent2D,
    SpriteComponent,
    GameObject,
]:
    Initializer.add_hooks(
        lambda c=to_initialize: ClassRegistry.register(c),
        None,
    )

__all__ = [
    # 'ColliderComponent',
    'GameObject',
    'RectColliderComponent',
    'ScriptComponent',
    'SpriteComponent',
    'TransformComponent2D',
]
