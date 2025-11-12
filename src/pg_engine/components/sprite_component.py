from collections.abc import Iterable, Sequence

import pygame

from pg_engine.api import (
    IComponent,
    IRenderable,
    IRenderer,
)
from pg_engine.api.registry import AssetRegistry
from pg_engine.utils import apply_transform


class SpriteComponent(IComponent, IRenderable):
    def __init__(
        self,
        asset: str,
        layer: int,
        rectmode: str = 'topleft',
        scaled: float | Sequence[float] | None = None,
        **kw,
    ):
        """
        Create a renderable sprite.

        :param asset: Asset to render with
        :type asset: str
        :param layer: layer to render on (from IRenderable)
        :type layer: int
        :param rectmode: origin of rendering, defaults to 'topleft'
        :type rectmode: str, optional
        :param scaled: whether to scale the incoming asset and to what size, defaults to None
        :type scaled: float | Iterable[float] | None, optional
        """  # noqa: E501
        IComponent.__init__(self, **kw)
        IRenderable.__init__(self, layer, **kw)
        self.asset: pygame.surface.Surface | None = AssetRegistry.get(asset)
        self.rectmode = rectmode
        if scaled is not None:
            self.scale(scaled)

    def get_render_data(
        self,
    ) -> tuple[pygame.Surface, Iterable[int | float], int] | tuple[None, None, None]:
        if not self.render_state or not self.asset:
            return (None, None, None)
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

    def scale(self, scale_by: float | Sequence[float]) -> None:
        self.asset = pygame.transform.scale_by(self.asset, scale_by)
        IRenderer().scheduled_update = True

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
        source = self.asset.get_rect() if self.asset else pygame.rect.Rect(0, 0, 0, 0)
        res = source.move(tuple(-axis for axis in source.topleft))
        return tuple(getattr(res, self.rectmode))

    def update(self, dt: int) -> None:
        pass
