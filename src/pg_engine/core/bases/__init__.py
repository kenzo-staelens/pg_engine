from .initializer import Initializer
from .lib_abstract import *
from .lib_singleton import Singleton, TRegistry
from .lib_meta import PostInit
from .config import *
from .container import ObjectContainer
from .class_registry import ClassRegistry
from .context import ContextRegistry, Context
from .base_game import BaseGame
from .renderer import BaseRenderer

from .wrappers import *
from .scene import Scene, SceneBuilder
from .camera import Camera2D

for to_register in [
    BaseGame,
    BaseRenderer,
    ContextRegistry,
    SceneBuilder,
    Scene,
    Camera2D,
]:
    Initializer.add_hooks(
        lambda to_register=to_register: ClassRegistry.register(to_register),
        None,
    )

try:
    from .pygame_gui_uimanager import PygameGuiUIManager, PygameGuiRegistry
    Initializer.add_hooks(
        lambda: ClassRegistry.register(PygameGuiUIManager),
        None,
    )
    Initializer.add_hooks(
        lambda: ClassRegistry.register(PygameGuiRegistry),
        PygameGuiRegistry.clear,
    )
except ModuleNotFoundError:
    pass
