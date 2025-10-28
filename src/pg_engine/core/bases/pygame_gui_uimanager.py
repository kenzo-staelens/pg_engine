from typing import final

import pygame
import pygame_gui

from .config import TUImanagerConfig
from .lib_abstract import TGame, TUIManager
from .registry import UIRegistry


@final
class PygameGuiRegistry(UIRegistry[pygame_gui.core.UIElement]):
    ...


class PygameGuiUIManager(TUIManager):
    def __init__(self):
        self.manager: pygame_gui.UIManager
        self.size: tuple[int, int]

    def update(self, dt: int) -> None:
        self.manager.update(dt / 1000)

    def draw_ui(self, render_surface: pygame.Surface) -> None:
        self.manager.draw_ui(render_surface)

    def process_events(self, event: pygame.Event) -> bool:
        return self.manager.process_events(event)

    def set_visual_debug_mode(self, state: bool) -> None:
        self.manager.set_visual_debug_mode(state)

    def configure(self, ui_config: TUImanagerConfig) -> None:
        """
        Configure the window resolution for this a :class:`pygame_gui.UIManager`.

        :param ui_config: configuration dictionary
        :type ui_config: TUImanagerConfig
        """
        self.manager = pygame_gui.UIManager(**ui_config)
        self.size = ui_config['window_resolution']

    def set_active_scene(self, scene: str) -> None:  # noqa: PLR6301
        UIRegistry.get(TGame().active_scene).hide()
        UIRegistry.get(scene).show()

    def hide_all(self) -> None:  # noqa: PLR6301
        for scene in TGame().scenes:
            UIRegistry.get(scene).hide()
