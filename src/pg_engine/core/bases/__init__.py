from .initializer import Initializer
from .config import *
from .container import ObjectContainer
from .context import ContextRegistry, Context
from .base_game import BaseGame
from .renderer import BaseRenderer

from .wrappers import *
from .scene import Scene, SceneBuilder
from .camera import Camera2D

from pg_engine.api.registry import ClassRegistry

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
