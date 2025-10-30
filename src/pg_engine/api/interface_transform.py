from abc import ABC, abstractmethod
from collections.abc import Iterable


class ITransform(ABC):
    @property
    @abstractmethod
    def position(self) -> Iterable[int | float]:
        """
        Position "component" of the transform.

        :return: Iterable of coordinates e.g. `(x, y)`
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def move(self, move_data: Iterable[int | float], absolute: bool = False) -> None:
        """
        Move this object.

        :param move_data: Iterable of deltas (or coordinates if absolute) to move by.
        :type move_data: Iterable[int  |  float]
        :param absolute: move to the exact given coordinates, defaults to False
        :type absolute: bool, optional
        """

    @property
    @abstractmethod
    def rotation(self) -> Iterable[int | float]:
        """
        Rotation "component" of the transform.

        :return: Iterable of coordinates e.g. `(angle,)`
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def rotate(self, rotation: Iterable[float], absolute: bool = False) -> None:
        """
        Rotate this object.

        :param rotation: Iterable of deltas (or angles if absolute) to rotate by.
        :type move_data: Iterable[int  |  float]
        :param absolute: rotate to the exact given angle, defaults to False
        :type absolute: bool, optional
        """


__all__ = [
    'ITransform',
]
