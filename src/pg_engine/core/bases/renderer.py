from collections.abc import Iterable

import pygame

from pg_engine.api import ICamera, IGame, IGameObject, IRenderable, IRenderer
from pg_engine.utils import apply_transform

from .config import TRendererConfig


class BaseRenderer(IRenderer):
    def __init__(self):
        super().__init__()
        self.cache: dict[IGameObject, list[IRenderable]] = {}
        self.cached_scene = None

    def update(self, dt: int) -> None:
        pass

    def render(self) -> None:
        self.update_cache()
        self.clear()
        for render_obj in self.cache:
            # pos is parenthesised here because it captures an iterable; could be tuple
            surface, (pos), mode = render_obj.get_render_data()
            if not surface:
                continue
            self.render_surface.blit(
                surface,
                tuple(self.apply_camera(pos)),
                special_flags=mode,
            )

    @classmethod
    def apply_camera(cls, position: Iterable[int | float]) -> Iterable[int | float]:
        return apply_transform(
            position,
            (-axis for axis in ICamera().position),
        )

    def clear(self) -> None:
        self.render_surface.fill((0, 0, 0))

    def configure(self, renderer_config: TRendererConfig) -> None:
        self.render_surface = pygame.display.set_mode(
            **renderer_config['display_mode'],
        )
        self.size = renderer_config['display_mode']['size']

    def update_cache(self) -> None:
        scene_name = IGame().active_scene
        if self.cached_scene == scene_name and not self.scheduled_update:
            return
        self.cache: list[IRenderable] = []
        scene = IGame().scenes[scene_name]
        for gameobject in scene.gameobjects:
            renderable = gameobject.components.get_of_type(IRenderable)
            if not renderable:
                continue
            self.cache += renderable
        self.cached_scene = scene_name
        self.cache.sort(key=lambda x: x.layer)


__all__ = [
    'BaseRenderer',
]
