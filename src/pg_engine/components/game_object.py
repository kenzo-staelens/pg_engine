from __future__ import annotations

from functools import cached_property

from pg_engine.core.bases.container import ComponentContainer
from pg_engine.core.bases.lib_abstract import (
    TGameObject,
    TScene,
    TTransformComponent,
)


class GameObject(TGameObject):
    def __init__(
        self,
        scene: TScene,
        name: str,
        transform_class: type[TTransformComponent],
    ):
        """
        Initialize the gameobject.

        :param scene: scene this gameobject belongs to
        :type scene: TScene
        :param name: name of this gameobject
        :type name: str
        :param transform_class: class of the transform component to default to
        :type transform_class: type[TTransformComponent]
        """
        super().__init__(scene, name)
        self.components = ComponentContainer(self)
        self._transform_class = transform_class

    def __str__(self):
        return self.name

    def update(self, dt: int) -> None:
        for component in self.components:
            component.update(dt)

    @cached_property
    def transform(self) -> TTransformComponent:
        comps = self.components.get_of_type(TTransformComponent)
        if not comps:
            transform = self._transform_class(source=self)
            self.components.add('transform', transform)
            return transform
        return comps[0]
