import functools
import logging
from abc import abstractmethod
from collections.abc import Callable

import pygame

from pg_engine.api import (
    IColliderComponent,
    ICollisionSystem,
    IEventSystem,
    IGame,
    IGameObject,
    IScript,
)

from .event_system import EventListener, Scope, listen

logger = logging.getLogger(__name__)

COLLISION = pygame.event.custom_type()
TRIGGER = pygame.event.custom_type()

IS_PHYSICS = {
    COLLISION: True,
    TRIGGER: False,
}

logger.debug("Registered event type 'COLLISION' as %d", COLLISION)
logger.debug("Registered event type 'TRIGGER' as %d", TRIGGER)


class CollisionScript(IScript, EventListener):

    """
    Minimal (dumb) collision script base.

    Must be inherited and have it's :term:__export__ set
    """

    __exports__ = None

    @abstractmethod
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.store_phys = self.source.transform.position

    def update(self, dt: int) -> None:
        super().update(dt)
        self.store_phys = self.source.transform.position

    @listen(event_type=COLLISION, scope=Scope.LOCAL)
    def on_collision(self, event: pygame.Event) -> None:  # noqa: ARG002
        """
        Collision event listener hook.

        resets the position of this script's source to the last known position\
            when a collision occurs.

        :param event: pygame collision event
        :type event: pygame.Event
        """
        self.source.transform.move(self.store_phys, True)


class CollisionSystem(ICollisionSystem):
    def __init__(self):
        """
        Initialize the collision system.

        contains:
        - dictionary to separate collision layers for more efficient processing
        - a set of interractions to track
        """
        super().__init__()
        self.collision_layers: dict[str, list[IColliderComponent]] = {}
        self.interractions: set[frozenset[str]] = set()

    def update(self, dt: int) -> None:
        pass

    def handle_collisions(self, dt: int, event_type: int) -> None:
        """
        Handle collisions of type given by event_type.

        this method is used in this class's :func:`.get_sequence_hooks`

        :param dt: milliseconds since last frame
        :type dt: int
        :param event_type: type of collision
        :type event_type: int
        """
        for interraction in self.interractions:
            g1, g2, self_group = self.get_groups(
                interraction,
                IS_PHYSICS.get(event_type, False),
            )
            system_event = IS_PHYSICS.get(event_type, False)
            # there are reasons to shortcut
            # remove a sprite from a group
            # by setting killa or killb to true
            # currently not implemented
            collisions: dict[
                IColliderComponent,
                list[IColliderComponent],
            ] = pygame.sprite.groupcollide(
                g1, g2,
                False, False,
                pygame.sprite.collide_mask,
            )

            for g1_sprite, g2_sprites in collisions.items():
                for g2_sprite in g2_sprites:
                    backing_g1 = g1_sprite.source
                    backing_g2 = g2_sprite.source
                    if backing_g1 is backing_g2:
                        continue  # no collide self if multple colliders on object
                    self._create_collision_event(
                        event_type,
                        g1_sprite,
                        g2_sprite,
                        dt,
                        system_event,
                    )
                    if self_group:
                        continue  # would otherwise duplicate events on same layer
                    self._create_collision_event(
                        event_type,
                        g2_sprite,
                        g1_sprite,
                        dt,
                        system_event,
                    )

    @staticmethod
    def _create_collision_event(
        event_type: int,
        target: IColliderComponent,
        collides_with: list[IColliderComponent],
        dt: int,
        is_system_event: bool = False,
    ) -> None:
        """
        Fire a collision event to be processed by the event system.

        :param event_type: Event for the collision type `COLLISION` or `TRIGGER`
        :type event_type: int
        :param target: target to send the event to
        :type target: IColliderComponent
        :param collides_with: source of the event
        :type collides_with: list[IColliderComponent]
        :param dt: milliseconds since last frame, added to event data
        :type dt: int
        :param is_system_event: is a system event, defaults to False
        :type is_system_event: bool, optional
        """
        send_data = [
            event_type,
            [target.source],
            {
                'collides': collides_with.source,
                'dt': dt,
            },
        ]
        IEventSystem().send(*send_data, system=is_system_event)

    def get_groups(self, interraction: frozenset[str], physics: bool) -> tuple[
        pygame.sprite.Group,
        pygame.sprite.Group,
        bool,
    ]:
        is_self_collision = False
        if len(interraction) == 1:
            is_self_collision = True
            interraction = tuple(interraction) * 2
        groups = []
        active_scene = IGame().active_scene
        for layer in interraction:
            group = pygame.sprite.Group(
                [
                    collider
                    for collider in self.collision_layers.get(layer, [])
                    if collider.physics == physics
                    and active_scene == collider.source.scene
                ],
            )
            groups.append(group)
        return *groups, is_self_collision

    def add(self, collider_component: IColliderComponent, layer: str) -> None:
        layer_data = self.collision_layers.get(layer, [])
        if not layer_data:
            self.collision_layers[layer] = layer_data
        layer_data.append(collider_component)

    def enable_collision(self, layer1: str, layer2: str) -> None:
        self.interractions.add(
            frozenset((layer1, layer2)),
        )

    def remove_gameobject(self, gameobject: IGameObject) -> None:
        for layer, colliders in self.collision_layers.items():
            self.collision_layers[layer] = [
                collider for collider in colliders if collider.source != gameobject
            ]

    def get_sequence_hooks(self) -> list[Callable[[int], None]]:
        return [
            functools.partial(self.handle_collisions, event_type=COLLISION),
            functools.partial(self.handle_collisions, event_type=TRIGGER),
        ]
