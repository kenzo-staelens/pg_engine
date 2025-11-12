from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod

from .interface_system import ISystem
from .singleton import Singleton


class ISaveSystem(ISystem, Singleton, ABC):

    """
    Base Class for :term:`EventSystem`.

    :term:`__singleton_key__` = 'EventSystem'
    """

    __singleton_key__ = 'SaveSystem'

    @abstractmethod
    def save_state(self) -> bool:
        """
        Save the current game state.

        :return: whether saving was successful
        :rtype: bool
        """

    @abstractmethod
    def load_from_save(self, path: pathlib.PosixPath) -> None:
        """
        Load and populate a previously saved gamestate.

        :param path: Path to load from
        :type path: pathlib.PosixPath
        """
