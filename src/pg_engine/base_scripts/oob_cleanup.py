from pg_engine.core import TScript


class OOBCleanup(TScript):

    """
    Script that handles out of bounds cleanup for objects.

    :term:__exports__ = 'oob_cleanup'
    """

    __exports__ = 'oob_cleanup'

    def __init__(self, bounds: list[tuple[str, str, int]], **kw):
        super().__init__(**kw)
        self.bounds = bounds

    def update(self, dt: int) -> None:
        super().update(dt)
        pos = self.source.transform.get_world_position()
        if any(
            getattr(float, op)(
                pos[bound_idx],
                value,
            )
            for bound_idx, op, value in self.bounds
        ):
            self.source.destroy()
