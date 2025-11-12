from __future__ import annotations

from collections.abc import Iterable

import pygame

from pg_engine.api import (
    IColliderComponent,
    IGame,
)
from pg_engine.utils import apply_transform


class RectColliderComponent(IColliderComponent):

    """Rectangular shaped collider."""

    def __init__(
        self,
        rect: tuple[int, int, int, int],
        rectmode: str = 'topleft',
        **kw,
    ):
        """
        Initialize the collider.

        :param rect: the (initial) this rectangle uses for collision calculation
        :type rect: tuple[int, int, int, int]
        :param rectmode: pygame position of rectangle\
            (eg. rect.center or rect.topleft), defaults to 'topleft'
        :type rectmode: str, optional
        """
        super().__init__(**kw)
        self.local_rect = pygame.Rect(rect)
        self.layer = float('inf')  # top layer for rendering
        self.rectmode = rectmode

    @property
    def rect(self) -> pygame.Rect:
        """The rectangle representing this collider."""
        res = apply_transform(
            self.origin,
            self.local_rect.topleft,
            self.source.transform.get_world_position(),
        )
        return pygame.Rect(*res, self.local_rect.width, self.local_rect.height)

    # used by pygame itself
    # we don't need full on sprites to do collisions
    def add_internal(self, group: pygame.sprite.Group) -> None:
        """Do noting, Method expected by pygame groups."""

    def get_render_data(
        self,
    ) -> tuple[pygame.Surface, Iterable[int | float], int] | tuple[None, None, None]:
        if not (IGame().debug_mode and self.debug_mode):
            return (None, None, None)
        surf = pygame.Surface(self.rect.size)
        color_collision = (255, 0, 0)
        color_trigger = (0, 0, 255)
        color = color_collision if self.physics else color_trigger
        pygame.draw.rect(surf, color, surf.get_rect(), 3)
        surf.set_colorkey((0, 0, 0))
        return (
            surf,
            self.rect.topleft,
            pygame.BLENDMODE_NONE,
        )

    def _create_collision_mask(self) -> pygame.Mask:
        """
        Calculate the collision mask of this component's source object.

        .. warning::
            currently bugged and fills the entire mask after rotation

        :return: _description_
        :rtype: pygame.Mask
        """
        m = pygame.Mask(self.local_rect.size)
        # BUG: mask rotation fills the entire rect
        m.fill()
        return m

    def scale(self, scale_by: float | Iterable[float]) -> None:
        if isinstance(scale_by, (float, int)):
            scale_by = (scale_by, scale_by)
        self.local_rect = self.local_rect.scale_by(*scale_by)
        self.update_mask()

    @property
    def origin(self) -> tuple[int, int]:
        source = self.local_rect
        res = source.move(tuple(-axis for axis in source.topleft))
        return getattr(res, self.rectmode)

    def update(self, dt: int) -> None:
        pass
