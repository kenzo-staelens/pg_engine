from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod

from .interface_system import ISystem
from .singleton import Singleton


class IAudioSystem(ISystem, Singleton, ABC):

    """
    :py:class:`Singleton` Extension to :py:class:`ISystem` to handle audio.

    :term:`__singleton_key__` = 'AudioSystem'
    """

    __singleton_key__ = 'AudioSystem'

    def __init__(self, loading_root: pathlib.PosixPath):
        """
        Initialize an audio system.

        Systems should refrain from keeping audio files in memory due to (generally)\
        short lived use of the file (eg. hitsounds) yet using relatively large amounts\
        of memory.

        :param loading_root: where to look for audio files
        :type loading_root: pathlib.PosixPath
        """
        super().__init__()
        self.root = loading_root

    @abstractmethod
    def play_audio(self, filename: str) -> None:
        """
        Play an audio file from file.

        :param filename: _description_
        :type filename: str
        """


__all__ = [
    'IAudioSystem',
]
