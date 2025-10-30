from . import exit_codes
from .bases import *
from . import loaders
from .loaders import GameConfigLoader
from . import processors
from pg_engine.api import registry

for reg in [
    registry.ScriptRegistry,
    registry.AssetRegistry,
    registry.ObjectRegistry,
    registry.UIRegistry,
    registry.ClassRegistry,
    registry.PrefabRegistry,
]:
    Initializer.add_hooks(  # noqa: F405
        lambda c=reg: registry.ClassRegistry.register(c),
        reg.clear,
    )
