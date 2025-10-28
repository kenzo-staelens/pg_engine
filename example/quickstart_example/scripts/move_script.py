import pygame

from pg_engine.core import TScript
from pg_engine.systems import (
    EventListener,
    Scope,
    listen,
)


class MoveScript(TScript, EventListener):
    __exports__ = 'move_script'

    def __init__(self, step: int, **kw):
        super().__init__(**kw)
        self.step = step

    @listen(event_type=pygame.KEYDOWN, scope=Scope.BROADCAST)
    def listen_movement(self, event: pygame.event.Event) -> None:
        match event.key:
            case pygame.K_LEFT:
                self.source.transform.move((-self.step, 0))
            case pygame.K_RIGHT:
                self.source.transform.move((self.step, 0))
            case pygame.K_UP:
                self.source.transform.move((0, -self.step))
            case pygame.K_DOWN:
                self.source.transform.move((0, self.step))


__all__ = [
    'MoveScript',
]
