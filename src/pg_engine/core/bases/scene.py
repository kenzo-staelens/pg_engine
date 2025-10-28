from __future__ import annotations

from .lib_abstract import TGameObject, TScene, TSceneBuilder


class SceneBuilder(TSceneBuilder):
    def build(self, name: str, definition: dict | None = None) -> TScene:  # noqa: ARG002
        return self.builder_class(name)


class Scene(TScene):
    def __init__(self, name: str):
        super().__init__(name)

    def add_gameobject(self, gameobject: TGameObject) -> None:
        self.gameobjects.append(gameobject)

    def remove_gameobject(self, gameobject: TGameObject) -> None:
        if gameobject in self.gameobjects:
            self.gameobjects.remove(gameobject)

    def update(self, dt: int) -> None:
        for go in self.gameobjects:
            go.update(dt)
