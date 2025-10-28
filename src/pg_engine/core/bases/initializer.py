from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar, final

import pygame

from .lib_singleton import Singleton


@final
class Initializer:

    """
    Internal manager for adding init and quit hooks.

    Init and quit hooks will be called upon use of
    pg_engine.init() and pg_engine.quit() in the style of pygame init/quit.
    """

    __hooks__: ClassVar = []

    @classmethod
    def add_hooks(cls, init_hook: Callable, quit_hook: Callable | None) -> None:
        """
        Add init or quit hook.

        A common use case is registering classes into :class:`ClassRegistry`\
            and clearing that registry on exit

        :param init_hook: initializer hook
        :type init_hook: Callable
        :param quit_hook: Corresponding exit hook to the init hook
        :type quit_hook: Callable | None
        """
        if quit_hook is None:
            def quit_hook() -> None:
                return None
        cls.__hooks__.append((init_hook, quit_hook))

    @classmethod
    def init(cls) -> None:
        """Call all registered init hooks."""
        pygame.init()
        for hook, _ in cls.__hooks__:
            hook()

    @classmethod
    def quit(cls) -> None:
        """Call all registered init hooks."""
        for _, hook in cls.__hooks__:
            hook()
        Singleton.clear()
        pygame.quit()


__all__ = [
    'Initializer',
]
