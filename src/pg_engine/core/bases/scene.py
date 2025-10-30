from __future__ import annotations

from pg_engine.api import IGameObject, IScene, ISceneBuilder


class SceneBuilder(ISceneBuilder):
    def build(self, name: str, definition: dict | None = None) -> IScene:  # noqa: ARG002
        return self.builder_class(name)


class Scene(IScene):
    def __init__(self, name: str):
        super().__init__(name)

    def add_gameobject(self, gameobject: IGameObject) -> None:
        self.gameobjects.append(gameobject)

    def remove_gameobject(self, gameobject: IGameObject) -> None:
        if gameobject in self.gameobjects:
            self.gameobjects.remove(gameobject)

    def update(self, dt: int) -> None:
        for go in self.gameobjects:
            go.update(dt)
