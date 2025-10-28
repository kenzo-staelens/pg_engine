from typing import final

import pygame

from pg_engine.core.bases import TScript

from .class_registry import ClassRegistry
from .lib_abstract import TGameObject
from .lib_singleton import TRegistry


# predefined registries for ease of access
@final
class AssetRegistry(TRegistry[pygame.Surface]):
    __singleton_key__ = 'AssetRegistry'


@final
class ScriptRegistry(TRegistry[TScript]):
    __singleton_key__ = 'ScriptRegistry'


@final
class ObjectRegistry(TRegistry[TGameObject]):
    __singleton_key__ = 'ObjectRegistry'


@final
class PrefabRegistry(TRegistry[dict]):
    __singleton_key__ = 'PrefabRegistry'


class UIRegistry[UI_T](TRegistry[UI_T]):
    __singleton_key__ = 'UIRegistry'


__all__ = [
    'AssetRegistry',
    'ClassRegistry',
    'ObjectRegistry',
    'PrefabRegistry',
    'ScriptRegistry',
    'UIRegistry',
]
