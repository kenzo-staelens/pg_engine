from collections.abc import Iterable

import pygame

from pg_engine.core import TComponent, TRenderable, TRenderer
from pg_engine.core.bases.registry import AssetRegistry
from pg_engine.utils import apply_transform


class SpriteComponent(TComponent, TRenderable):
    def __init__(
        self,
        asset: str,
        layer: int,
        rectmode: str = 'topleft',
        **kw,
    ):
        TComponent.__init__(self, **kw)
        TRenderable.__init__(self, layer, **kw)
        self.asset = AssetRegistry.get(asset)
        self.rectmode = rectmode

    def get_render_data(self) -> tuple[pygame.Surface, Iterable[int | float], int]:
        if not self.render_state:
            return (None,) * 3
        surface = pygame.transform.rotate(
            self.asset,
            self.source.transform.get_world_rotation()[0],
        )

        pos = apply_transform(
            self.origin,
            self.asset.get_rect().topleft,
            self.source.transform.get_world_position(),
        )
        return (
            surface,
            pos,
            pygame.BLENDMODE_NONE,
        )

    def scale(self, scale_by: float | Iterable[float]) -> None:
        self.asset = pygame.transform.scale_by(self.asset, scale_by)
        TRenderer().scheduled_update = True

    @property
    def origin(self) -> tuple[int, int]:
        """
        Source position of where to start a transform.

        ## Examples
        (x, y, w, h) with rectmode 'center' returns (w/2, h/2)

        (x, y, w, h) with rectmode 'topleft' returns (0, 0)

        (x, y, w, h) with rectmode 'bottomright' returns (w, h)


        :return: starting coordinate relative to (0, 0) by rectmode
        :rtype: tuple[int, int]
        """
        source = self.asset.get_rect()
        res = source.move(tuple(-axis for axis in source.topleft))
        return tuple(getattr(res, self.rectmode))

    def update(self, dt: int) -> None:
        pass
