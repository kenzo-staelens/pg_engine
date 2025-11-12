from collections.abc import Callable, Sequence
from typing import cast

from pg_engine.api import IScript


class OOBCleanup(IScript):

    """
    Script that handles out of bounds cleanup for objects.

    :term:__exports__ = 'oob_cleanup'
    """

    __exports__ = 'oob_cleanup'

    def __init__(self, bounds: list[tuple[str, int]], **kw):
        super().__init__(**kw)
        self.bounds = bounds

    def update(self, dt: int) -> None:
        super().update(dt)
        pos = cast('Sequence[int]', self.source.transform.get_world_position())
        for bound_idx, (op, value) in enumerate(self.bounds):
            operation = cast(
                'Callable[[float, int], bool]',
                getattr(float, op),
            )
            if operation(pos[bound_idx], value):
                self.source.destroy()
                break
