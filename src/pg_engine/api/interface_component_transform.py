from abc import ABC, abstractmethod
from collections.abc import Iterable

from .interface_component import IComponent
from .interface_transform import ITransform


class ITransformComponent(ITransform, IComponent, ABC):

    """Base class for translate/rotate components."""

    @abstractmethod
    def get_world_position(self) -> Iterable[int | float]:
        """
        World Position of the transform.

        can be calculated by sequentially applying transforms of parent objects\
            until this object's transform is added.

        :return: Iterable of coordinates e.g. `(x, y)`
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def get_world_rotation(self) -> Iterable[int | float]:
        """
        World Rotation of the transform.

        can be calculated by sequentially applying rotations of parent objects\
            until this object's transform is added.

        :return: Iterable of coordinates e.g. `(angle,)`
        :rtype: Iterable[int | float]
        """


__all__ = [
    'ITransformComponent',
]
