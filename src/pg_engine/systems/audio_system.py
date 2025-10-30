from typing import Any

import pygame
from cachetools.func import ttl_cache

from pg_engine.api import (
    IAudioSystem,
)


class AudioSystem(IAudioSystem):

    """Bare bones audio system."""

    def __init__(self, channels: list[str], **kw):
        """
        Initialize the audiosystem with a set of channels.

        :param channels: channel names this system should create
        :type channels: list[str]
        """
        super().__init__(**kw)
        self.channels = {
            channel: pygame.mixer.Channel(i)
            for i, channel in enumerate(channels)
        }

    def play_audio(
        self,
        filename: str,
        channel: str | None = None,
        play_args: dict[str, Any] | None = None,
    ) -> None:
        """
        Play audio from a file.

        uses :py.func:`pygame.mixer.Sound.play` when no channel selected

        otherwise uses :py.func:`pygame.mixer.Channel.queue`

        :param filename: File to find the audio in.
        :type filename: str
        :param channel: Channel to play/queue audio in, defaults to None
        :type channel: str | None, optional
        :param play_args: Arguments passed to play, defaults to None
        :type play_args: dict[str, Any] | None, optional
        """
        sound = self._find_sound(filename)
        if channel and channel in self.channels:
            self.channels[channel].queue(sound)
        else:
            sound.play(**(play_args or {}))

    @ttl_cache(maxsize=8, ttl=60)
    def _find_sound(self, filename: str) -> pygame.mixer.Sound:
        """
        Cache layer to keep audio files generally short lived but accessible.

        maximum store of 8 sounds with 60 seconds ttl.

        :param filename: filename to search
        :type filename: str
        :return: Sound object of the audio file
        :rtype: pygame.mixer.Sound
        """
        return pygame.mixer.Sound(self.root / filename)
