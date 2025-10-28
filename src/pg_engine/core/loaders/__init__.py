from .yaml_loader import YamlLoader
from .sprite_loader import SpriteLoader
from .script_loader import ScriptLoader
from .game_config_loader import GameConfigLoader
from .ui_loader import UILoader, DummyUIManager, DummyUILoader
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
    DummyUIManager,
    DummyUILoader,
]:
    Initializer.add_hooks(
        lambda c=to_register: ClassRegistry.register(c),
        None,
    )

__all__ = [
    'DummyUILoader',
    'DummyUIManager',
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

try:
    from .pygame_gui_loader import PygameGuiUILoader
    Initializer.add_hooks(
        lambda: ClassRegistry.register(PygameGuiUILoader),
        None,
    )
    __all__ += ['PygameGuiUILoader']
except ModuleNotFoundError:
    pass
