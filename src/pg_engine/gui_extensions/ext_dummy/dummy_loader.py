from __future__ import annotations

from typing import Any, final

import pygame

from pg_engine.core.loaders import UILoader


class DummyUILoader(UILoader[Any]):

    """Dummy class for when no UI extensions are available."""

    @classmethod
    def create_ui_object(
        cls,
        name: str,
        object_class: type,
        relative_rect: pygame.Rect,
        anchors: dict,
        definition: dict,
    ) -> Any:  # noqa: ANN401
        pass

    @classmethod
    def init_scenes(cls) -> None:
        pass

    @final
    def load(self) -> dict[str, Any]:  # noqa: PLR6301
        return {}
