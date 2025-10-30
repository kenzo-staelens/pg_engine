from .yaml_loader import YamlLoader
from .sprite_loader import SpriteLoader
from .script_loader import ScriptLoader
from .game_config_loader import GameConfigLoader
from .ui_loader import UILoader
from .game_object_loader import GameObjectLoader, GameObjectBuilder
from .spritesheet import SpriteSheet
from .lazy_proxy import Proxy

from pg_engine.core.bases import Initializer, ClassRegistry

for to_register in [
    GameConfigLoader,
    GameObjectBuilder,
    GameObjectLoader,
    ScriptLoader,
    SpriteLoader,
    YamlLoader,
]:
    Initializer.add_hooks(
        lambda c=to_register: ClassRegistry.register(c),
        None,
    )

__all__ = [
    'GameConfigLoader',
    'GameObjectBuilder',
    'GameObjectLoader',
    'Proxy',
    'ScriptLoader',
    'SpriteLoader',
    'SpriteSheet',
    'UILoader',
    'YamlLoader',
]
