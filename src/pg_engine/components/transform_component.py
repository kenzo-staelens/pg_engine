from __future__ import annotations

import functools
import math
from abc import abstractmethod
from collections.abc import Iterable

from pg_engine.core import TTransformComponent
from pg_engine.utils import apply_transform


# NOTE: math might need an extra check to be sure
class TransformComponent(TTransformComponent):
    def get_world_rotation(self) -> Iterable[int | float]:
        reference = self.rotation_reference
        return tuple(apply_transform(reference, self.rotation))

    def get_world_position(self) -> Iterable[int, int]:
        with_rotation = self._rotate_coordinate(
            self.position_reference,
            self.get_world_rotation(),
        )
        return tuple(apply_transform(with_rotation, self.position))

    @property
    @abstractmethod
    def rotation_reference(self) -> Iterable[int | float]:
        """
        Rotation relative to parent object.

        :return: the relative rotation as an iterable of angles\
            e.g. (angle,)
        :rtype: Iterable[int | float]
        """

    @property
    @abstractmethod
    def position_reference(self) -> Iterable[int | float]:
        """
        Position relative to parent object.

        :return: the relative rotation as an iterable of axes\
            e.g. (x, y)
        :rtype: Iterable[int | float]
        """

    @staticmethod
    @abstractmethod
    def _rotate_coordinate(
        coordinate: Iterable[int | float],
        angle: Iterable[int | float],
    ) -> Iterable[int | float]:
        """
        Calculate a coordinate rotated around (0,0) by an angle.

        :param coordinate: Coordinate point to rotate.
        :type coordinate: tuple[int, int]
        :param angle: The angle to rotate by.
        :type angle: tuple[int]
        :return: The point rotated around (0,0).
        :rtype: tuple[int, int]
        """


class TransformComponent2D(TransformComponent):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        angle: int = 0,
        **kw,
    ):
        """
        Initialize a 2D transform.

        Additionally takes arguments taken by :class:TransformComponent

        :param x: W position, defaults to 0
        :type x: int, optional
        :param y: Y position, defaults to 0
        :type y: int, optional
        :param angle: rotation angle in degrees, defaults to 0
        :type angle: int, optional
        """
        super().__init__(**kw)
        self.x = x
        self.y = y
        self.angle = angle

    # --- REQUIRED PROPERTIES ---
    @property
    def position(self) -> Iterable[int | float]:
        return (self.x, self.y)

    @property
    def rotation(self) -> Iterable[int | float]:
        return (self.angle,)

    # --- CALCULATION PROPERTIES ---
    @property
    def rotation_reference(self) -> Iterable[int | float]:
        if self.source.parent:
            return self.source.parent.transform.get_world_rotation()
        return (0,)

    @property
    def position_reference(self) -> Iterable[int | float]:
        if self.source.parent:
            return self.source.parent.transform.get_world_position()
        return (0, 0)

    # --- TRANSFORMATIONS ---
    def move(self, move_data: tuple[int, int], absolute: bool = False) -> None:
        if absolute:
            self.x, self.y = move_data
            return
        self.x += move_data[0]
        self.y += move_data[1]

    def rotate(self, rotation: tuple[int], absolute: bool = False) -> None:
        if absolute:
            self.angle = rotation[0]  # incoming tuple
            return
        self.angle += rotation[0]

    @staticmethod
    @functools.lru_cache(maxsize=16)
    def _rotate_coordinate(
        coordinate: tuple[int, int],
        angle: tuple[int],
    ) -> tuple[int, int]:
        rad = math.radians(angle[0])
        rotation = (math.cos(rad) + math.sin(rad) * 1j)
        complex_coordinate = coordinate[0] + coordinate[1] * 1j
        rotated = (rotation * complex_coordinate)
        return rotated.real, rotated.imag
