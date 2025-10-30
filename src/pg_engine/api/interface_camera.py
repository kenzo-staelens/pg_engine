from abc import ABC, abstractmethod

from .interface_transform import ITransform
from .singleton import Singleton


class ICamera(ITransform, Singleton, ABC):

    """
    Base Class for :term:`Camera`.

    Used by :attr:`IRenderer.apply_camera`

    :term:`__singleton_key__` = 'Camera'
    """

    __singleton_key__ = 'Camera'

    @abstractmethod
    def __init__(self):
        """Initialize the camera."""


__all__ = [
    'ICamera',
]
