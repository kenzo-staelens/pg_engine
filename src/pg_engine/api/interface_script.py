from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface_component import IComponent
    from .interface_gameobject import IGameObject


class IScript:

    """
    Base class for user defined scrips.

    should be part of a dedicated component type.

    :term:__exports__ is used by :class:`ScriptLoader`
    """

    __exports__ = None

    def __init__(self, source: IComponent):
        """
        Initialize script values.

        :param source: component this script belongs to
        :type source: IComponent
        """
        self._source: IGameObject = source.source

    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @property
    def source(self) -> IGameObject:
        """Proxy for bypassing this script's component source."""
        return self._source


__all__ = [
    'IScript',
]
