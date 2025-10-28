from __future__ import annotations

import contextlib
import logging
import pathlib
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Iterator
from functools import cached_property
from typing import Any

import pygame

from .class_registry import ClassRegistry
from .lib_meta import PostInit
from .lib_singleton import Singleton, TRegistry

logger = logging.getLogger(__name__)


class Configurable:
    @abstractmethod
    def configure(self, config_data: dict) -> None:
        """
        Perform subclass specific configurations.

        :param config_data: Configuration data
        :type config_data: dict
        """


class TRenderer(Singleton, ABC, Configurable):

    """
    Base class for Renderers.

    :term:`__singleton_key__` = 'Renderer'
    """

    __singleton_key__ = 'Renderer'

    def __init__(self):
        self.uimanager: TUIManager
        self.render_surface: pygame.Surface
        self.size: tuple[int, int]
        #: flag to listen for triggered cache updates
        #: this causes less cache updates when a lot of objects
        #: get created in the same frame
        self.scheduled_update: bool = False

    @abstractmethod
    def render(self) -> None:
        """Render all renderables."""

    @classmethod
    @abstractmethod
    def apply_camera(cls, position: Iterable[int | float]) -> Iterable[int | float]:
        """
        Apply the transformation of :class:`TCamera` onto the rendered view.

        :param position: Position to apply the camera onto
        :type position: Iterable[int  |  float]
        :return: Resulting position after applying the camera
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def clear(self) -> None:
        """Clear the screen."""

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def update_cache(self) -> None:
        """
        Update the internal cache.

        Cache should be updated at most once per frame and should use
        :attr:`~scheduled_update` for that check.
        """


class TRenderable(ABC):

    """Base class for renderable objects."""

    def __init__(self, layer: int, source: TGameObject):
        """
        Initialize the renderable.

        :param layer: Layer this object will be rendered (starting at 0)
        :type layer: int
        :param source: Gameobject this renderable belongs to
        :type source: TGameObject
        """
        self.source = source
        self.layer = layer
        self.render_state = True

    @abstractmethod
    def get_render_data(self) -> tuple[pygame.Surface, Iterable[int | float], int]:
        ...

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def scale(self, scale_by: float | Iterable[float]) -> None:
        """
        Scale the renderable in one or more dimensions.

        :param scale_by: scale equally in all dimensions if float otherwise\
        scale per dimension given in the iterable
        :type scale_by: float | Iterable[float]
        """


class TContainer[T](ABC):

    """Generic container class."""

    @abstractmethod
    def __init__(self):
        """Initialize the container."""

    @abstractmethod
    def add(self, name: str, store: T) -> None:
        """
        Add an object to the container.

        Adding an object should not override existing objects.
        use :func:`~override` for such functionality

        :param name: reference of the stored object in this container
        :type name: str
        :param store: Object to store
        :type store: T
        """

    @abstractmethod
    def override(self, name: str, store: T) -> None:
        """
        Add or override an object to the container.

        :param name: reference of the stored object in this container
        :type name: str
        :param store: Object to store
        :type store: T
        """

    @abstractmethod
    def __delattr__(self, name: str) -> None:
        """
        Delete an object out of this container by name.

        :raises AttributeError: raised when no object with name can be found.
        :param name: name reference of the object to delete
        :type name: str
        """

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        """
        Iterate interface of this container.

        :yield: Iterator of this container;
        :rtype: Iterator[T]
        """

    @abstractmethod
    def get_of_type[U](self, tclass: type[U]) -> list[U]:
        """
        Get all items of type :class:`U` in this container.

        :param tclass: class or superclass of the returned objects.
        :type tclass: type[T]

        :return: list of all objects of type :type:`U`
        :rtype: List[U]
        """

    @abstractmethod
    def by_name(self, name: str) -> T:
        """
        Get an object out of this container by name.

        :raises AttributeError: raised when no object with name can be found
        :param name: name reference of the object to get
        :type name: str
        :return: object found at reference.
        :rtype: T
        """


class TGame(Singleton, ABC, Configurable):

    """
    Base class for Game instances.

    :term:`__singleton_key__` = 'Game'
    """

    __singleton_key__ = 'Game'

    def __init__(self):
        """
        Initialize a game with it's internal components and values.

        ## Requires
        - valid TRenderer instance
        - valid TRendTSystemControllererer instance
        - valid TUIManager instance
        - valid TGameObjectBuilder instance
        - valid TSceneBuilder instance
        - valid TGlobalCamera instance
        """
        self.fps: int = 0
        self._running: bool = False
        self.window_surface: pygame.Surface | None = None
        self.clock: pygame.Clock | None = None

        self.renderer = TRenderer()
        self.system_controller = TSystemController()
        self.uimanager = TUIManager()
        self.objectbuilder = TGameObjectBuilder()
        self.scenebuilder = TSceneBuilder()
        self.camera = TGlobalCamera()

        self.scenes: dict[str, TScene] = {}
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

    def remove_gameobject(self, gameobject: TGameObject) -> None:
        """
        Propagate call to remove_gameobject to all subcomponents.

        By default propagates to
        - systemcontroller
        - all scenes
        - schedules renderer cache update

        :param gameobject: The gameobject to remove
        :type gameobject: TGameObject
        """
        self.system_controller.remove_gameobject(gameobject)
        for scene in self.scenes.values():
            scene.remove_gameobject(gameobject)
        self.renderer.scheduled_update = True

    @abstractmethod
    def spawn(
        self,
        spawn_source: TGameObject,
        scene: str,
        object_config: str,
        post_process: Callable[[TGameObject], None] | None = None,
    ) -> TGameObject:
        """
        Spawn a new gameobject.

        should be called with super. schedules a renderer cache update.

        :param spawn_source: gameobject that is spawning the new entity
        :type spawn_source: TGameObject
        :param scene: scene into which to spawn the new entity
        :type scene: str
        :param object_config: definition of the entity to spawn
        :type object_config: str
        :param post_process: callable that performs postprocessing after\
            the entity is spawned, defaults to None
        :type post_process: Callable[[TGameObject], None] | None, optional
        :return: the spawned gameobject
        :rtype: TGameObject
        """
        self.renderer.scheduled_update = True


class TScene(ABC):

    """
    Base class for scenes.

    :param name: name of the scene
    :type name: str
    """

    def __init__(self, name: str):
        """
        Initialize the scene.

        :param name: name of the scene
        :type name: str
        """
        self.name = name
        self.gameobjects: list[TGameObject] = []
        self.active = False

    @abstractmethod
    def add_gameobject(self, gameobject: TGameObject) -> None:
        """
        Add a gameobject to internal representation.

        :param gameobject: Game object to add.
        :type gameobject: TGameObject
        """

    @abstractmethod
    def remove_gameobject(self, gameobject: TGameObject) -> None:
        """
        Remove a gameobject to internal representation.

        :param gameobject: Game object to remove.
        :type gameobject: TGameObject
        """

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """


class TProcessor(ABC):

    """Base Class for Processors."""

    # overload doesn't work with classmethods
    @classmethod
    @abstractmethod
    def process(
        cls,
        config: dict[str, Any],
        processor_args: dict[str, str] | None = None,
    ) -> None:
        """
        Process (standardized) incoming configuration data.

        :param config: incoming configuration in standardized
            (ie. dict[str, any]) format
        :type config: dict[str, Any]
        :param processor_args: arguments passed to the concrete implementation,
            defaults to None
        :type processor_args: dict[str, str] | None, optional
        :rtype: None
        """


class TComponent:

    """Base class for components."""

    def __init__(self, source: TGameObject):
        """
        Initialize the component.

        :param source: Gameobject the component belongs to.
        :type source: TGameObject
        """
        self.source = source

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """


class Transformbase(ABC):
    @property
    @abstractmethod
    def position(self) -> Iterable[int | float]:
        """
        Position "component" of the transform.

        :return: Iterable of coordinates e.g. `(x, y)`
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def move(self, move_data: Iterable[int | float], absolute: bool = False) -> None:
        """
        Move this object.

        :param move_data: Iterable of deltas (or coordinates if absolute) to move by.
        :type move_data: Iterable[int  |  float]
        :param absolute: move to the exact given coordinates, defaults to False
        :type absolute: bool, optional
        """

    @property
    @abstractmethod
    def rotation(self) -> Iterable[int | float]:
        """
        Rotation "component" of the transform.

        :return: Iterable of coordinates e.g. `(angle,)`
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def rotate(self, rotation: Iterable[float], absolute: bool = False) -> None:
        """
        Rotate this object.

        :param rotation: Iterable of deltas (or angles if absolute) to rotate by.
        :type move_data: Iterable[int  |  float]
        :param absolute: rotate to the exact given angle, defaults to False
        :type absolute: bool, optional
        """


class TTransformComponent(Transformbase, TComponent):

    """Base class for translate/rotate components."""

    @abstractmethod
    def get_world_position(self) -> Iterable[int | float]:
        """
        World Position of the transform.

        can be calculated by sequentially applying transforms of parent objects\
            until this object's transform is added.

        :return: Iterable of coordinates e.g. `(x, y)`
        :rtype: Iterable[int | float]
        """

    @abstractmethod
    def get_world_rotation(self) -> Iterable[int | float]:
        """
        World Rotation of the transform.

        can be calculated by sequentially applying rotations of parent objects\
            until this object's transform is added.

        :return: Iterable of coordinates e.g. `(angle,)`
        :rtype: Iterable[int | float]
        """


class TGlobalCamera(Transformbase, Singleton, ABC):

    """
    Base Class for :term:`Camera`.

    Used by :attr:`.TRenderer.apply_camera`

    :term:`__singleton_key__` = 'Camera'
    """

    __singleton_key__ = 'Camera'

    @abstractmethod
    def __init__(self):
        """Initialize the camera."""


class TColliderComponent(TComponent, TRenderable, metaclass=PostInit):

    """Base class of components used in collision checks."""

    def __init__(
        self,
        collision_layers: list[str],
        physics: bool,
        # active disable via config; needs game debug mode = true
        debug_mode: bool = True,
        **kw,
    ):
        """
        Initialize the collider.

        :param collision_layers: :term:`collision layers` on which\
            this collider listens.
        :type collision_layers: list[str]
        :param physics: whether this collider is a phyisics collider or a trigger.
        :type physics: bool
        :param debug_mode: whether this collider should render debug data,\
            defaults to True
        :type debug_mode: bool, optional
        """
        super().__init__(**kw)
        self.collision_layers = collision_layers
        self.physics = physics
        self.debug_mode = debug_mode

    @cached_property
    def mask(self) -> pygame.Mask:
        """Attribute looked at by pygame for mask_collision."""
        return self._create_collision_mask()

    @abstractmethod
    def _create_collision_mask(self) -> pygame.Mask:
        """Calculate the collision mask of this component's source object."""

    def update_mask(self) -> None:
        """
        Get rid of the currently cached mask.

        This implementation deletes the currently cached mask attribute such that\
            the engine can lazily recalculate the mask next time it is requested.
        """
        with contextlib.suppress(AttributeError):
            del self.mask

    def __post_init__(self):
        """Add this component to the collision system to be processed on init."""
        system = TCollisionSystem()
        for layer in self.collision_layers:
            system.add(self, layer)


class TSystem:

    """Base class of systems managed by :py:class:`TSystemController`."""

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def remove_gameobject(self, gameobject: TGameObject) -> None:
        """
        Remove a gameobject from this system's processing.

        :param gameobject: The gameobject to remove
        :type gameobject: TGameObject
        """

    @abstractmethod
    def get_sequence_hooks(self) -> Iterable[Callable[[int], None]]:
        """
        Get this system's hooks which should be called by :py:class:`TSystemController`.

        :return: This system's callables taking `dt` and handle a part of the engine.
        :rtype: Iterable[Callable[[int], None]]
        """


class TCollisionSystem(TSystem, Singleton):

    """
    :py:class:`Singleton` Extension to :py:class:`TSystem` to handle collisions.

    :term:`__singleton_key__` = 'CollisionSystem'
    """

    __singleton_key__ = 'CollisionSystem'

    @abstractmethod
    def get_groups(
            self,
            interraction: frozenset[str],
        ) -> tuple[
            pygame.sprite.Group,
            pygame.sprite.Group,
            bool,
        ]:
        """
        Get Collision Data.

        Gets two spritegroups and a bool indicating whether the\
            collision groups are the same.

        :param interraction: the interraction (set by :func:`~.enable_collision`)
        :type interraction: frozenset[str]
        :return: Collision data
        :rtype: tuple[ pygame.sprite.Group, pygame.sprite.Group, bool, ]
        """

    @abstractmethod
    def add(self, collider_component: TColliderComponent, layer: str) -> None:
        """
        Add a collider to be handled by the system.

        :param collider_component: Component to be added to the system
        :type collider_component: TColliderComponent
        :param layer: collision layer the component should be added into
        :type layer: str
        """

    @abstractmethod
    def enable_collision(self, layer1: str, layer2: str) -> None:
        """
        Enable collisions between two collision layers (interchangeable).

        :param layer1: first layer in the interraction
        :type layer1: str
        :param layer2: second layer in the collision
        :type layer2: str
        """


class TEventSystem(TSystem, Singleton):

    """
    Base Class for :term:`EventSystem`.

    :term:`__singleton_key__` = 'EventSystem'
    """

    __singleton_key__ = 'EventSystem'

    @abstractmethod
    def update_system(self, dt: int) -> None:
        """
        Handle system events separate from game events.

        :param dt: milliseconds since last frame
        :type dt: int
        """

    @classmethod
    @abstractmethod
    def send(
        cls,
        event_type: int,
        targets: list[TGameObject] | None,
        data: dict | None = None,
        system: bool = False,
    ) -> None:
        """
        Send an event to one or more specified targets.

        :param event_type: type of the event in pygame
        :type event_type: int
        :param targets: list of gameobjects with scope :attr:`Scope.LOCAL`\
            that receive the event
        :type targets: list[TGameObject] | None
        :param data: metadata for the event, defaults to None
        :type data: dict | None, optional
        :param system: is a system event, defaults to False
        :type system: bool, optional
        """

    @classmethod
    @abstractmethod
    def broadcast_scene(
        cls,
        event_type: int,
        scene_name: str,
        data: dict | None = None,
        system: bool = False,
    ) -> None:
        """
        Broadcast an event to scope :attr:`Scope.BROADCAST` listeners.

        :param event_type: type of the event in pygame
        :type event_type: int
        :param scene_name: target scene to send the event to
        :type scene_name: str
        :param data: metadata for the event, defaults to None
        :type data: dict | None, optional
        :param system: is a system event, defaults to False
        :type system: bool, optional
        """

    @classmethod
    @abstractmethod
    def broadcast(
        cls,
        event_type: int,
        data: dict | None = None,
        system: bool = False,
    ) -> None:
        """
        Broadcast an event to scope :attr:`Scope.BROADCAST` listeners.

        :param event_type: type of the event in pygame
        :type event_type: int
        :param data: metadata for the event, defaults to None
        :type data: dict | None, optional
        :param system: is a system event, defaults to False
        :type system: bool, optional
        """

    @abstractmethod
    def register_event_hook(
        self,
        event_type: int,
        listener: TGameObject | None,
        hook: Callable[[pygame.Event], None],
    ) -> None:
        """
        Register a callable to listen to events of scope :attr:`Scope.LOCAL`.

        :param event_type: event type the callable listens to
        :type event_type: int
        :param listener: listener owning this event hook
        :type listener: TGameObject | None
        :param hook: the callable functioning as eventlistener
        :type hook: Callable[[pygame.Event], None]
        """

    @abstractmethod
    def register_broadcast_hook(
        self,
        event_type: int,
        scene: TScene | None,
        hook: Callable[[pygame.Event], None],
    ) -> None:
        """
        Register a callable to listen to scope :attr:`Scope.BROADCAST_SCENE` and :attr:`Scope.BROADCAST`.

        :param event_type: event type the callable listens to
        :type event_type: int
        :param scene: the scene this hook resides in or None for :attr:`Scope.BROADCAST`
        :param hook: the callable functioning as eventlistener
        :type hook: Callable[[pygame.Event], None]
        """  # noqa: E501


class TSystemController(Singleton, ABC):

    """
    Base Class for :term:`SystemController`.

    keeps track and schedules operations for all instances of :py:class:`TSystem`

    :term:`__singleton_key__` = 'SystemController'
    """

    __singleton_key__ = 'SystemController'

    def __init__(self):
        """
        Initialize the systemcontroller.

        Minimally requires a collision_system and event_system.
        """
        super().__init__()
        self.collision_system: TCollisionSystem
        self.event_system: TEventSystem

    @abstractmethod
    def update(self) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def remove_gameobject(self, gameobject: TGameObject) -> None:
        """
        Propagate call to :func:`~.TSystem.remove_gameobject` to all systems.

        :param gameobject: The gameobject to remove
        :type gameobject: TGameObject
        """

    @abstractmethod
    def get_sequence_hooks(self) -> list[Callable[[int], None]]:
        """
        Get all systems' hooks which should be called by instances of this class.

        :return: The systems' callables taking `dt` and handle a part of the engine.
        :rtype: Iterable[Callable[[int], None]]
        """


class TGameObject:
    def __init__(self, scene: TScene, name: str):
        """
        Initialize the gameobject.

        :param scene: scene this gameobject belongs to
        :type scene: TScene
        :param name: name of this gameobject
        :type name: str
        """
        self.scene: TScene = scene
        self.name = name
        self.components: TContainer[TComponent]
        self.parent: TGameObject | None = None
        #: used to determine whether this object has already been destroyed
        #: during event processing and should still be handled or not
        self.exists = True

    def destroy(self) -> None:
        """Remove this gameobject from the game and set it's :attr:`~exists` flag to false."""  # noqa: E501
        TGame().remove_gameobject(self)
        self.exists = False

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @property
    @abstractmethod
    def transform(self) -> TTransformComponent:
        """
        Get this Game object's transform component or create a default if none exists.

        :return: this game object's transform component
        :rtype: TTransformComponent
        """


class TLoader(ABC):

    """Base class for data loaders loading data from a file."""

    def __init__(
        self,
        filename: str,
        root: pathlib.PosixPath,
        registry: str | None = None,
    ):
        """
        Initialize the loader.

        :param filename: file to load from
        :type filename: str
        :param root: root to start searching in
        :type root: PosixPath

        :param registry: registry this loader stores loaded objects into,\
            defaults to None
        :type registry: str | None, optional
        """
        self.filename: str = filename
        self.registry = None
        self.root = root
        if registry is not None:
            self.registry: TRegistry = ClassRegistry.get(registry)

    @abstractmethod
    def load(self) -> dict[str, Any]:
        """
        Entrypoint for loading.

        :return: loaded data in standardized dict[str, any] format
        :rtype: dict[str, Any]
        """

    def register_loaded(
        self,
        name: str,
        loaded: object,
        registry: TRegistry | None = None,
    ) -> bool:
        """
        Register a loaded object into this loader's registry.

        :param name: name to store the object as
        :type name: str
        :param loaded: the loaded object
        :type loaded: object
        :param registry: another registry to store into instead, defaults to None
        :type registry: TRegistry | None, optional
        :return: whether storing was successful
        :rtype: bool
        """
        if registry:
            return registry.register(name, loaded)
        return self.registry.register(name, loaded)


class Builder[T]:

    """Generic class used to build other objects of type T."""

    def __init__(
        self,
        builder_class: type[T] | None = None,
        builder_kw: dict | None = None,
    ):
        """
        Initialize the builder.

        :param builder_class: Class which gets used to create objects, defaults to None
        :type builder_class: type[T] | None, optional
        :param builder_kw: keyword args for the builder_class, defaults to None
        :type builder_kw: dict | None, optional
        :raises ValueError: raised when the provided builder is None
        """
        if builder_class is None:
            raise ValueError
        self.builder_class = builder_class
        self.builder_kw: dict = builder_kw or {}

    @abstractmethod
    def build(self, name: str, definition: dict | None = None) -> T:
        """
        Build an object using `builder_class` as class to pass the definition to.

        :param name: name of the object to build
        :type name: str
        :param definition: blueprint of the object to build, defaults to None
        :type definition: dict | None, optional
        :return: the built object
        :rtype: T
        """


class TGameObjectBuilder(Builder[TGameObject], Singleton):

    """
    Typed :class:`Singleton` for building :class:`TGameObject` instances.

    :term:`__singleton_key__` = 'GameObjectBuilder'
    """

    __singleton_key__ = 'GameObjectBuilder'


class TSceneBuilder(Builder[TScene], Singleton):

    """
    Typed :class:`Singleton` for building :class:`TScene` instances.

    :term:`__singleton_key__` = 'SceneBuilder'
    """

    __singleton_key__ = 'SceneBuilder'


class TScript:

    """
    Base class for user defined scrips.

    should be part of a dedicated component type.

    :term:__exports__ is used by :class:`ScriptLoader`
    """

    __exports__ = None

    def __init__(self, source: TComponent):
        """
        Initialize script values.

        :param source: component this script belongs to
        :type source: TComponent
        """
        self._source: TGameObject = source.source

    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @property
    def source(self) -> TGameObject:
        """Proxy for bypassing this script's component source."""
        return self._source


class TUIManager(Singleton, ABC, Configurable):

    """
    Base class for handling UI operations and objects.

    written in the style of pygame_gui uimanager

    :term:`__singleton_key__` = 'UIManager'
    """

    __singleton_key__ = 'UIManager'

    @abstractmethod
    def __init__(self):
        self.manager: Any
        self.size: tuple[int, int]

    @abstractmethod
    def update(self, dt: int) -> None:
        """
        Update method passed throughout the entire engine called once per frame.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """

    @abstractmethod
    def draw_ui(self, render_surface: pygame.Surface) -> None:
        """
        Render the ui on the screen.

        :param render_surface: Pygame surface to render onto
        :type render_surface: pygame.Surface
        """

    @abstractmethod
    def process_events(self, event: pygame.Event) -> bool:
        """
        Process an event.

        :param event: pygame event or gui event (which extends the preceding)
        :type event: pygame.Event
        :return: whether the event was consumed
        :rtype: bool
        """
        return False

    @abstractmethod
    def set_visual_debug_mode(self, state: bool) -> None:
        """
        Enable or disable visual UI debugging.

        :param state: state to set
        :type state: bool
        """

    @abstractmethod
    def set_active_scene(self, scene: str) -> None:
        """
        Enable the UI of the active scene and disable all others.

        :param scene: scene to change UI for
        :type scene: str
        """

    @abstractmethod
    def hide_all(self) -> None:
        """Hide all UI elements/scenes."""


__all__ = [
    'Builder',
    'TColliderComponent',
    'TCollisionSystem',
    'TComponent',
    'TContainer',
    'TEventSystem',
    'TGame',
    'TGameObject',
    'TGameObjectBuilder',
    'TGlobalCamera',
    'TLoader',
    'TProcessor',
    'TRenderable',
    'TRenderer',
    'TScene',
    'TSceneBuilder',
    'TScript',
    'TSystem',
    'TSystemController',
    'TTransformComponent',
    'TUIManager',
]
