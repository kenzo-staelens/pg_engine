from __future__ import annotations

import logging

import pygame
from pygame_gui.core import UIContainer, UIElement

from pg_engine.api import IGame, IUIManager
from pg_engine.core import Context
from pg_engine.core.loaders import UILoader

logger = logging.getLogger(__name__)


class PygameGuiUILoader(UILoader[UIElement]):

    """Implementation of :class:`UILoader` to load pygame_gui UIs."""

    def init_scenes(self) -> None:
        manager = IUIManager().manager
        for scene in IGame().scenes:
            container = UIContainer(
                manager=manager,
                relative_rect=pygame.Rect(0, 0, *IUIManager().size),
            )
            self.register_loaded(scene, container)

    @classmethod
    def create_ui_object(
        cls,
        name: str,  # noqa: ARG003
        object_class: type[UIElement],
        relative_rect: pygame.Rect,
        anchors: dict,
        definition: dict,
    ) -> UIElement:
        manager = IUIManager().manager
        # pygamegui needs the parent object *now* for calculating position
        # based on anchors -> lazy not allowed though you can sequence the ui without
        # circular dependencies
        logger.critical('%s %s %s %s', object_class, relative_rect, anchors, definition)
        with Context(evaluate_lazy=True):
            return object_class(
                relative_rect=relative_rect,
                manager=manager,
                anchors=anchors,
                **definition,
            )
