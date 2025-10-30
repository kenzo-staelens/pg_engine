from __future__ import annotations

import logging
from collections.abc import Callable
from enum import Enum
from queue import Queue

import pygame

from pg_engine.api import (
    IEventSystem,
    IGame,
    IGameObject,
    IScene,
    IScript,
    PostInit,
    Singleton,
)
from pg_engine.core.bases import one_shot

logger = logging.getLogger(__name__)

NOTIFY = pygame.event.custom_type()
logger.debug("Registered event type 'NOTIFY' as %d", NOTIFY)

# there's one more debug log in here but it tends to spam during gamedev
# should be manually turned on
logger.setLevel(logging.INFO)


class Scope(Enum):
    LOCAL = 1
    BROADCAST_SCENE = 2
    BROADCAST = 3


class ListenerContainer:

    """Container to handle finding event listeners by scope, target and event."""

    def __init__(self):
        # NOTE: it's generally more performant to
        # work int -> separation_by_object -> callable
        # because pygame generates a lot of events we'll likely never listen for
        # the sooner these are filtered out the less work we have to do
        # when we have an event we actually listen for we'll at least
        # likely have a record that listens to it making the work useful
        self.listeners: dict[int, dict[IGameObject, list[Callable]]] = {}
        self.broadcast_listeners: dict[int, dict[IScene | None, list[Callable]]] = {}

    @staticmethod
    def _add_listener_to(
        evt_type: int,
        listener: object,
        method: Callable,
        listener_dict: dict[int, dict[object, list[Callable]]],
    ) -> None:
        """
        Categorize a listener into buckets.

        :param evt_type: event type this callable listens to
        :type evt_type: int
        :param listener: object owning the listener
        :type listener: object
        :param method: the listener callable
        :type method: Callable
        :param listener_dict: bucket to categorize the listener into
        :type listener_dict: dict[int, dict[object, list[Callable]]]
        """
        evt_type_dict = listener_dict.get(evt_type, {})
        if evt_type not in listener_dict:
            listener_dict[evt_type] = evt_type_dict
        listener_methods = evt_type_dict.get(listener, [])
        if listener not in evt_type_dict:
            if hasattr(listener, 'source'):
                listener = listener.source
            evt_type_dict[listener] = listener_methods
        listener_methods.append(method)

    def add_listener(
        self,
        evt_type: int,
        listener: IGameObject,
        method: Callable,
    ) -> None:
        """
        Add a listener to the internal :attr:`listeners` bucket.

        :param evt_type: Event type the method listens for
        :type evt_type: int
        :param listener: the object owning the listener
        :type listener: IGameObject
        :param method: the listener callable
        :type method: Callable
        """
        self._add_listener_to(evt_type, listener, method, self.listeners)

    def add_broadcast(
        self,
        evt_type: int,
        scene: IScene | None,
        method: Callable,
    ) -> None:
        """
        Add a listener to the internal :attr:`broadcast_listeners` bucket.

        :param evt_type: Event type the method listens for
        :type evt_type: int
        :param listener: the object owning the listener
        :type listener: IGameObject
        :param method: the listener callable
        :type method: Callable
        """
        self._add_listener_to(evt_type, scene, method, self.broadcast_listeners)

    @staticmethod
    def _read_listener(
            event: pygame.Event,
            listener_dict: dict[int, dict[object, list[Callable]]],
            listener_target: object | None,
        ) -> list[Callable]:
        return listener_dict.get(event.type, {}).get(listener_target, [])

    def get_listeners(
            self,
            event: pygame.Event,
        ) -> list[Callable]:
        defined_listener = event.dict.get('listener')
        # by scene
        if defined_listener is None:
            return self._read_listener(event, self.broadcast_listeners, None)
        if isinstance(defined_listener, IScene):
            # broadcast scene
            listener = defined_listener.name
            return self._read_listener(event, self.broadcast_listeners, listener)
        if isinstance(defined_listener, IGameObject):
            return self._read_listener(event, self.listeners, defined_listener)

        # other cannot determine
        message = f'cannot search listeners for type {defined_listener.__class__}'
        raise NotImplementedError(message)

    def remove_gameobject(self, gameobject: IGameObject) -> None:
        for listenerdict in self.listeners.values():
            if gameobject in listenerdict:
                del listenerdict[gameobject]
        for broadcastdict in self.broadcast_listeners.values():
            for scene, by_scene_list in broadcastdict.items():
                # filter by owning object
                broadcastdict[scene] = [
                    x for x in by_scene_list if x.__self__ is not gameobject
                ]


class SystemEventQueue(Singleton):
    __singleton_key__ = 'SystemEventQueue'

    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def get(self) -> list[pygame.Event]:
        return [self.queue.get() for _ in range(self.queue.qsize())]

    def put(self, event: pygame.Event) -> None:
        self.queue.put(event)


class EventSystem(IEventSystem):
    def __init__(self):
        super().__init__()
        self.event_hooks: ListenerContainer = ListenerContainer()

    def update(self, _: int) -> None:
        self._eventloop()

    def update_system(self, _: int) -> None:
        self._eventloop(SystemEventQueue())

    def _eventloop(self, event_source: SystemEventQueue | None = None) -> None:
        if event_source is None:
            event_source = pygame.event
        for event in event_source.get():
            if event.type == pygame.QUIT:
                IGame().stop()
            if IGame().uimanager.process_events(event):
                # event processed by pygame_gui are not our
                # responsibility
                continue
            for hook in self.event_hooks.get_listeners(event):
                hook(event)

    @classmethod
    def send(
        cls,
        event_type: int,
        targets: list[IGameObject] | None,
        data: dict | None = None,
        system: bool = False,
    ) -> None:
        if data is None:
            data = {}
        if targets is None:
            event = pygame.event.Event(event_type, data)
            pygame.event.post(event)
            return
        for target in targets:
            extra_data = data | {'listener': target}
            # apparently pygame doesn't like "type=..." parameter
            event = pygame.event.Event(event_type, **extra_data)
            if not system:
                pygame.event.post(event)
                continue
            SystemEventQueue().put(event)

    @classmethod
    def broadcast_scene(
        cls,
        event_type: int,
        scene_name: str,
        data: dict | None = None,
        system: bool = False,
    ) -> None:
        scene = IGame().scenes.get(scene_name)
        cls.send(event_type, targets=[scene], data=data, system=system)

    @classmethod
    def broadcast(cls, event_type: int, data: dict | None = None) -> None:
        cls.send(event_type, targets=None, data=data)

    def register_event_hook(
            self,
            event_type: int,
            listener: IGameObject | None,
            hook: Callable[[pygame.Event], None],
        ) -> None:
        logger.debug(
            'EventSystem: Registering event hook [%s(%d)] -> %s',
            pygame.event.event_name(event_type),
            event_type,
            hook.__name__,
        )
        self.event_hooks.add_listener(event_type, listener, hook)

    def register_broadcast_hook(
        self,
        event_type: int,
        scene: IScene | None,
        hook: Callable[[pygame.Event], None],
    ) -> None:
        self.event_hooks.add_broadcast(event_type, scene, hook)

    def remove_gameobject(self, gameobject: IGameObject) -> None:
        self.event_hooks.remove_gameobject(gameobject)

    def get_sequence_hooks(self) -> list[Callable[[int], None]]:
        return [self.update]


class EventListenerMeta(PostInit):

    """
    Metaclass to define event listeners.

    adds a boolean key :term:`__create_event_listeners__` to the created class\
        which stores all event hooks this class should create upon initializing

    Additionally copies all entries of :term:`__create_event_listeners__`\
        of parent classes

    skips the above mentioned operation if classvar\
        :term:`__create_listener_list__` is set to False
    """

    def __new__(meta, name: str, bases: tuple[type, ...], attrs: dict[str]):
        if (
            # HACK: root class should not have a __create_event_listeners__
            # but all of it's first decendents should define it
            # additionally their children *should* inherit the attribute
            any(base.__dict__.get('__create_listener_list__') for base in bases)
            and '__create_event_listeners__' not in attrs
        ):
            attrs['__create_event_listeners__'] = []
        for base in bases:
            if '__create_event_listeners__' not in attrs:
                break
            if '__create_event_listeners__' in base.__dict__:
                attrs['__create_event_listeners__'] += base.__create_event_listeners__
        attrs['__create_listener_list__'] = True
        return super().__new__(meta, name, bases, attrs)


class EventListener(metaclass=EventListenerMeta):
    # HACK: this classvar only exists here for typehinting purposes
    __create_event_listeners__: list

    def __post_init__(self):
        """Register event listener hooks on object initialization."""
        for listener in self.__create_event_listeners__:
            sys = IEventSystem()
            evt_type, scope, fn_name = listener
            # it's hard to have the name wrong unless you forget to functools.wrap
            fn: Callable = getattr(self, fn_name)
            match scope:
                case Scope.BROADCAST:
                    sys.register_broadcast_hook(evt_type, None, fn)
                case Scope.BROADCAST_SCENE:
                    sys.register_broadcast_hook(evt_type, self.scene, fn)
                case Scope.LOCAL:
                    sys.register_event_hook(evt_type, self, fn)

    @property
    def scene(self) -> IScene:
        return self.source.scene


# BUG: inheriting and changing a collider breaks listening for that collider
@one_shot
def listen(
    fn: Callable[[IScript, pygame.Event], None],
    owner: type[EventListener],
    /,
    event_type: int,
    scope: Scope,
) -> Callable[[int], None]:
    """
    Decorate event listener methods.

    Due to technical limitations this decorator should be the first decorator used
    parameters `fn` and `owner` get passed through decorators wrapping this decorator

    .. code-block:: python

       @listen(event_type = ..., scope = ...)
       @other_decorators
       def event_listener_method(self, event: pygame.Event) -> None:
           ...

    .. warning::
        inheriting existing listener methods causes only the first defined to be called\
        including with super calls
    """
    owner.__create_event_listeners__.append((event_type, scope, fn.__name__))
