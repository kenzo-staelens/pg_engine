from .gameconfig_processor import GameConfigProcessor
from .graphics_processor import GraphicsProcessor

from pg_engine.core.bases import Initializer, ClassRegistry

for to_register in [
    GameConfigProcessor,
    GraphicsProcessor,
]:
    Initializer.add_hooks(
        lambda c=to_register: ClassRegistry.register(c),
        None,
    )

__all__ = [
    'GameConfigProcessor',
    'GraphicsProcessor',
]
