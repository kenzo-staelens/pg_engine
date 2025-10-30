from collections.abc import Iterable

from pg_engine.api import ICamera


class Camera2D(ICamera):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        angle: int = 0,
    ):
        """
        Initialize a 2D camera.

        :param x: initial x position, defaults to 0
        :type x: int, optional
        :param y: initial y position, defaults to 0
        :type y: int, optional
        :param angle: initial angle, defaults to 0
        :type angle: int, optional
        """
        self.x = x
        self.y = y
        self._rotation = angle

    @property
    def position(self) -> tuple[int | float]:
        return (self.x, self.y)

    @property
    def rotation(self) -> Iterable[int | float]:
        return (self._rotation,)

    def move(self, move_data: Iterable[int | float], absolute: bool = False) -> None:
        if absolute:
            self.x, self.y = move_data
            return
        self.x += move_data[0]
        self.y += move_data[1]

    def rotate(self, rotation: Iterable[int | float], absolute: bool = False) -> None:
        if absolute:
            self._rotation = rotation[0]
        self._rotation += rotation[0]
