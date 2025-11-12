"""Groups exit codes in a single file to help prevent exit code collision."""

from collections.abc import Callable
from enum import IntEnum


def int_generator(start: int = 0) -> Callable[[], int]:
    gen_start = start - 1

    def generator() -> int:
        nonlocal gen_start
        gen_start += 1
        return gen_start
    return generator


exit_code_generator = int_generator(1)


class ExitCodes(IntEnum):
    EXIT_CODE_INVALID_CONFIG = exit_code_generator()
    EXIT_CODE_INVALID_KEYS = exit_code_generator()
    EXIT_CODE_INVALID_OBJECT = exit_code_generator()
    EXIT_CODE_NO_REGISTRY = exit_code_generator()
    EXIT_CODE_FATAL_CONSTRUCT = exit_code_generator()
    EXIT_CODE_LOAD_SPRITESHEET = exit_code_generator()


__all__ = [
    'ExitCodes',
    'exit_code_generator',
]
