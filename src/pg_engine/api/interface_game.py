from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING

import pygame

from .interface_configurable import IConfigurable
from .singleton import Singleton

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .interface_builder_gameobject import IGameObjectBuilder
    from .interface_builder_scene import ISceneBuilder
    from .interface_camera import ICamera
    from .interface_gameobject import IGameObject
    from .interface_renderer import IRenderer
    from .interface_scene import IScene
    from .interface_system_controller import ISystemController
    from .interface_uimanager import IUIManager


class IGame(Singleton, IConfigurable, ABC):

    """
    Base class for Game instances.

    :term:`__singleton_key__` = 'Game'
    """

    __singleton_key__ = 'Game'

    def __init__(self):
        """
        Initialize a game with it's internal components and values.

        ## Requires
        - valid IRenderer instance
        - valid ISystemController instance
        - valid IUIManager instance
        - valid IGameObjectBuilder instance
        - valid ISceneBuilder instance
        - valid IGlobalCamera instance
        """
        self.fps: int = 0
        self._running: bool = False
        self.window_surface: pygame.Surface | None = None
        self.clock: pygame.Clock | None = None

        self.renderer: IRenderer = Singleton.get('Renderer')
        self.system_controller: ISystemController = Singleton.get('SystemController')
        self.uimanager: IUIManager = Singleton.get('UIManager')
        self.objectbuilder: IGameObjectBuilder = Singleton.get('GameObjectBuilder')
        self.scenebuilder: ISceneBuilder = Singleton.get('SceneBuilder')
        self.camera: ICamera = Singleton.get('Camera')

        self.scenes: dict[str, IScene] = {}
        self._active_scene: str = 'default'
        self.debug_mode = False

    @property
    def active_scene(self) -> str:
        """
        Get the name of the current active scene.

        :return: name of the active scene
        :rtype: str
        """
        return self._active_scene

    @active_scene.setter
    def active_scene(self, scene: str) -> None:
        """
        Set the current active scene and perform necessary operations.

        by default triggers :func:`~TUIManager.set_active_scene`

        :param scene: name of the new scene
        :type scene: str
        """
        self.uimanager.set_active_scene(scene)
        self._active_scene = scene

    @property
    @abstractmethod
    def running(self) -> bool:
        """Readonly access to running state."""

    def before_start(self) -> None:
        """
        Perform required actions before game start.

        By default
        - hides all UI elements
        - sets default active scene to 'default' (enabling it's UI)
        - sets state running to True
        - assigns a pygame Clock
        """
        self.uimanager.hide_all()
        self.active_scene = 'default'
        self._running = True
        self.clock = pygame.Clock()

    @abstractmethod
    def cleanup(self) -> None:
        """Perform required cleanup actions after game exists."""

    @abstractmethod
    def gameloop(self) -> None:
        """Primary driver function of running all operations a game performs every frame."""  # noqa: E501

    def run(self) -> None:
        """Entrypoint for a game to start."""
        logger.info('Starting...')
        self.before_start()
        logger.info('Started')
        self.gameloop()
        logger.info('Exiting...')
        self.cleanup()

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the game from running and perform any operations before cleanup.

        Implementations of this method should call :func:`update` of this\
        instance's systems, managers, displays, etc. and handle clock ticking
        """

    def remove_gameobject(self, gameobject: IGameObject) -> None:
        """
        Propagate call to remove_gameobject to all subcomponents.

        By default propagates to
        - systemcontroller
        - all scenes
        - schedules renderer cache update

        :param gameobject: The gameobject to remove
        :type gameobject: IGameObject
        """
        self.system_controller.remove_gameobject(gameobject)
        for scene in self.scenes.values():
            scene.remove_gameobject(gameobject)
        self.renderer.scheduled_update = True

    @abstractmethod
    def spawn(
        self,
        spawn_source: IGameObject,
        scene: str,
        object_config: str,
        post_process: Callable[[IGameObject], None] | None = None,
    ) -> IGameObject:
        """
        Spawn a new gameobject.

        should be called with super. schedules a renderer cache update.

        :param spawn_source: gameobject that is spawning the new entity
        :type spawn_source: IGameObject
        :param scene: scene into which to spawn the new entity
        :type scene: str
        :param object_config: definition of the entity to spawn
        :type object_config: str
        :param post_process: callable that performs postprocessing after\
            the entity is spawned, defaults to None
        :type post_process: Callable[[IGameObject], None] | None, optional
        :return: the spawned gameobject
        :rtype: IGameObject
        """
        self.renderer.scheduled_update = True


__all__ = [
    'IGame',
]
