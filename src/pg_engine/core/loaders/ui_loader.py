from __future__ import annotations

import importlib
import logging
from abc import ABC, abstractmethod
from types import ModuleType
from typing import Any, final

import pygame

from pg_engine.core import TUIManager, UIConfig

from .yaml_loader import YamlLoader

logger = logging.getLogger(__name__)


class TUIContainer:

    """Type hinting based on pygame_gui."""

    @abstractmethod
    def add_element(self, ui_element: Any) -> None:  # noqa: ANN401
        ...


class UILoader[T](YamlLoader, ABC):
    @classmethod
    def _validate_configs(cls, element: str, config: UIConfig) -> bool:
        """
        Verify whether required keys are available in a UI configuration.

        logs a warning for optional but encouraged missing keys
        logs an error for missing required keys and returns false

        :param element: name of the ui element being loaded
        :type element: str
        :param config: Configuration data of the ui element
        :type config: UIConfig
        :return: whether the configuration is valid
        :rtype: bool
        """
        valid = True
        for key in ('anchors', 'args'):
            if key not in config:
                logger.warning(
                    "UIConfig: missing configuration key '%s' on '%s'",
                    key,
                    element,
                )
        for key in ('classpath', 'size', 'offset'):
            if key not in config:
                valid = False
                logger.error(
                    "UIConfig: missing configuration key '%s' on '%s'",
                    key,
                    element,
                )
        return valid

    @classmethod
    @abstractmethod
    def init_scenes(cls) -> None:
        """Construct and initialize scene objects from scenes in :class:`TGame`."""

    @classmethod
    @abstractmethod
    def create_ui_object(
        cls,
        name: str,
        object_class: type,
        relative_rect: pygame.Rect,
        anchors: dict,
        definition: dict,
    ) -> T:
        """
        Create and register UI objects.

        .. note::
            The api of this method is *heavily* inspired by pygame_gui

        :param name: reference name of the ui element
        :type name: str
        :param object_class: class to construct the element with
        :type object_class: type
        :param relative_rect: location and position of the ui element
        :type relative_rect: pygame.Rect
        :param anchors: anchoring information of the ui element
        :type anchors: dict
        :param definition: any other args/kwargs passed to the object_class
        :type definition: dict
        :return: An instance of a ui element
        :rtype: T
        """

    def load(self) -> dict[str, T]:
        data: dict[str, UIConfig] = super().load() or {}
        loaded = {}
        self.init_scenes()
        for key, conf in data.items():
            if not self._validate_configs(key, conf or {}):
                continue

            module_name, class_name = conf['classpath'].rsplit('.', 1)
            module: ModuleType = importlib.import_module(module_name)
            object_class: type[T] = getattr(module, class_name)

            try:
                relative_rect = pygame.rect.Rect(conf['offset'] + conf['size'])
            except TypeError:
                logger.exception(
                    "UIElement: Failed to construct relative_rect on '%s'",
                    key,
                )
                continue

            anchors = conf.get('anchors')
            kw = conf.get('args', {}) or {}

            try:
                ui_object = self.create_ui_object(
                    # key,
                    object_class,
                    relative_rect,
                    anchors,
                    kw,
                )
                self.register_loaded(key, ui_object)
                if 'parent' in conf:
                    container: TUIContainer = self.registry.get(conf['parent'])
                    container.add_element(ui_object)

            except Exception:
                # yes we can use generic exception, we do not know what errors
                # can occur in external lib constructing anything it contains
                logger.exception(
                    "UIElement: Failed to construct '%s'",
                    key,
                )
                continue

            loaded[key] = ui_object
        return loaded


class DummyUIManager(TUIManager):

    """Dummy class for when no UI extensions are available."""

    def __init__(self):
        super().__init__()

    def draw_ui(self, render_surface: pygame.Surface) -> None:
        pass

    def hide_all(self) -> None:
        pass

    def process_events(self, event: pygame.Event) -> bool:  # noqa: ARG002, PLR6301
        return False

    def set_active_scene(self, scene: str) -> None:
        pass

    def set_visual_debug_mode(self, state: bool) -> None:
        pass

    def update(self, dt: int) -> None:
        pass


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
