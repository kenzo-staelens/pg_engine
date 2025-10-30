from __future__ import annotations

from typing import final

import pygame

from .interface_gameobject import IGameObject
from .interface_registry import IRegistry
from .interface_script import IScript


@final
class ClassRegistry(IRegistry[type]):
    __singleton_key__ = 'ClassRegistry'

    @classmethod
    def register(cls, entry: type, *, override: bool = False) -> bool:
        return super().register(entry.__name__, entry, override=override)


@final
class AssetRegistry(IRegistry[pygame.Surface]):
    __singleton_key__ = 'AssetRegistry'


@final
class ScriptRegistry(IRegistry[IScript]):
    __singleton_key__ = 'ScriptRegistry'


@final
class ObjectRegistry(IRegistry[IGameObject]):
    __singleton_key__ = 'ObjectRegistry'


@final
class PrefabRegistry(IRegistry[dict]):
    __singleton_key__ = 'PrefabRegistry'


class UIRegistry[UI_T](IRegistry[UI_T]):
    __singleton_key__ = 'UIRegistry'


__all__ = [
    'AssetRegistry',
    'ClassRegistry',
    'ObjectRegistry',
    'PrefabRegistry',
    'ScriptRegistry',
    'UIRegistry',
]
