from typing import final

from .lib_singleton import TRegistry


@final
class ClassRegistry(TRegistry[type]):
    __singleton_key__ = 'ClassRegistry'

    @classmethod
    def register(cls, entry: type, *, override: bool = False) -> bool:
        return super().register(entry.__name__, entry, override=override)
