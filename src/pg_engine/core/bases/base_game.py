from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

import pygame

from pg_engine.core.bases.registry import PrefabRegistry

from .lib_abstract import TGame, TGameObject

logger = logging.getLogger(__name__)


class BaseGame(TGame):

    """Minimal implementation of a game object."""

    def before_start(self) -> None:
        super().before_start()

    def cleanup(self) -> None:
        self.system_controller.destroy()
        self.renderer.destroy()
        self.clock = None

    def gameloop(self) -> None:
        while self.running:
            # dt in milliseconds
            dt = self.clock.tick(
                self.fps,
            )
            # triggers update scripts and such
            self.scenes[self.active_scene].update(dt)
            self.system_controller.update(dt)
            self.renderer.update(dt)
            self.uimanager.update(dt)

            self.renderer.render()
            self.uimanager.draw_ui(self.renderer.render_surface)
            pygame.display.update()

    @property
    def running(self) -> bool:
        return self._running

    def stop(self) -> None:
        self._running = False

    def configure(self, config_config: dict[str, Any]) -> None:
        """
        Set several attributes of this instance using :func:`setattr` if provided.

        :param config_config: Config data passed tot this method
        :type config_config: dict[str, Any]
        """
        for key, value in config_config.items():
            setattr(self, key, value)

    def spawn(
        self,
        spawn_source: TGameObject,
        scene: str,
        object_def_name: str,
        post_process: Callable[[TGameObject], None] | None = None,
    ) -> TGameObject:
        if post_process is None:
            def post_process(go: TGameObject) -> TGameObject:
                pass
        object_config = PrefabRegistry.get(object_def_name)
        gameobject = self.objectbuilder.build(object_def_name, object_config)
        gameobject.transform.move(spawn_source.transform.position, True)
        post_process(gameobject)
        gameobject.scene = scene
        self.scenes[scene].add_gameobject(gameobject)
        super().spawn(spawn_source, scene, object_def_name, post_process)
        return gameobject


__all__ = [
    'BaseGame',
]
