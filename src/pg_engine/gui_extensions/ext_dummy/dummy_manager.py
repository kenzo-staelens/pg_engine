from __future__ import annotations

import pygame

from pg_engine.api import IUIManager


class DummyUIManager(IUIManager):

    """Dummy class for when no UI extensions are available."""

    def __init__(self):
        super().__init__()

    def draw_ui(self, render_surface: pygame.Surface) -> None:
        pass

    def hide_all(self) -> None:
        pass

    def process_events(self, event: pygame.event.Event) -> bool:  # noqa: ARG002, PLR6301
        return False

    def set_active_scene(self, scene: str) -> None:
        pass

    def set_visual_debug_mode(self, state: bool) -> None:
        pass

    def update(self, dt: int) -> None:
        pass

    def configure(self, config_data: dict) -> None:
        pass
