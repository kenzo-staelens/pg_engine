from .interface_builder import IBuilder
from .interface_gameobject import IGameObject
from .singleton import Singleton


class IGameObjectBuilder(IBuilder[IGameObject], Singleton):

    """
    Typed :class:`Singleton` for building :class:`IGameObject` instances.

    :term:`__singleton_key__` = 'GameObjectBuilder'
    """

    __singleton_key__ = 'GameObjectBuilder'


__all__ = [
    'IGameObjectBuilder',
]
