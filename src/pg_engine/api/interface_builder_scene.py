from .interface_builder import IBuilder
from .interface_scene import IScene
from .singleton import Singleton


class ISceneBuilder(IBuilder[IScene], Singleton):

    """
    Typed :class:`Singleton` for building :class:`IScene` instances.

    :term:`__singleton_key__` = 'SceneBuilder'
    """

    __singleton_key__ = 'SceneBuilder'


__all__ = [
    'ISceneBuilder',
]
