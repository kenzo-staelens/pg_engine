"""Groups exit codes in a single file to help prevent exit code collision."""

from enum import IntEnum


class ExitCodes(IntEnum):
    EXIT_CODE_INVALID_CONFIG = 1
    EXIT_CODE_INVALID_KEYS = 2
    EXIT_CODE_INVALID_OBJECT = 3
    EXIT_CODE_NO_REGISTRY = 4
    EXIT_CODE_FATAL_CONSTRUCT = 5
    EXIT_CODE_LOAD_SPRITESHEET = 6
