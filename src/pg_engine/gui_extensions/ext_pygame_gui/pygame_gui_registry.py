from typing import final

import pygame_gui

from pg_engine.api.registry import UIRegistry


@final
class PygameGuiRegistry(UIRegistry[pygame_gui.core.UIElement]):
    ...
