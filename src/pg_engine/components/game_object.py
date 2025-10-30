from __future__ import annotations

from functools import cached_property

from pg_engine.api import (
    IGameObject,
    IScene,
    ITransformComponent,
)
from pg_engine.core.bases.container import ComponentContainer


class GameObject(IGameObject):
    def __init__(
        self,
        scene: IScene,
        name: str,
        transform_class: type[ITransformComponent],
    ):
        """
        Initialize the gameobject.

        :param scene: scene this gameobject belongs to
        :type scene: IScene
        :param name: name of this gameobject
        :type name: str
        :param transform_class: class of the transform component to default to
        :type transform_class: type[ITransformComponent]
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
    def transform(self) -> ITransformComponent:
        comps = self.components.get_of_type(ITransformComponent)
        if not comps:
            transform = self._transform_class(source=self)
            self.components.add('transform', transform)
            return transform
        return comps[0]
