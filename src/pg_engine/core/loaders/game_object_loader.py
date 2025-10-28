from __future__ import annotations

import logging
import sys

from pg_engine.core import (
    ClassRegistry,
    TComponent,
    TComponentConfig,
    TGame,
    TGameObject,
    TGameObjectBuilder,
    TGameObjectConfig,
)
from pg_engine.core.bases.registry import PrefabRegistry
from pg_engine.core.exit_codes import ExitCodes

from .yaml_loader import YamlLoader

logger = logging.getLogger(__name__)


class GameObjectBuilder(TGameObjectBuilder):
    def build(self, name: str, definition: TGameObjectConfig) -> TGameObject:
        scene = definition.get('scene')
        if isinstance(scene, bool) or scene is None:
            scene = 'default'
        if not isinstance(scene, str):
            raise TypeError
        go = self.builder_class(
            scene=scene,
            name=name,
            **self.builder_kw,
        )
        ComponentBuilder.attach_components(go, definition.get('components', []))
        TGame().scenes[scene].add_gameobject(go)
        return go


class ComponentBuilder:

    """Helper class for constructing and adding components to a gameobject."""

    @classmethod
    def attach_components(
        cls,
        gameobject: TGameObject,
        components: list[TComponentConfig],
    ) -> None:
        """
        Attach one or more components to a gameobject from definition.

        .. note::
            The :attr:`TComponent.source` is set during creation of the component.

        :param gameobject: Gameobject to attach to
        :type gameobject: TGameObject
        :param components: list of component definitions
        :type components: list[TComponentConfig]
        """
        for component_def in components:
            refname, component = cls.create_component(component_def, gameobject)
            gameobject.components.add(refname, component)

    @classmethod
    def create_component(
        cls,
        component_def: TComponentConfig,
        game_object: TGameObject | None = None,
    ) -> tuple[str, TComponent]:
        """
        Construct a gameobject from definition.

        :param component_def: Blueprint of the component
        :type component_def: TComponentConfig
        :param game_object: game object to use as source parameter, defaults to None
        :type game_object: TGameObject | None, optional
        :return: name (from refname) or type of the component and the constructed component
        :rtype: tuple[str, TComponent]
        """  # noqa: E501
        c_type = component_def['type']
        refname = component_def.get('refname', c_type)
        args = component_def['args'] or {}
        component_class: type[TComponent] | None = ClassRegistry.get(c_type)
        if not component_class:
            logger.critical(
                'Component[%s]: Could not find registry entry',
                c_type,
            )
            sys.exit(ExitCodes.EXIT_CODE_NO_REGISTRY)
        try:
            component = component_class(**args, source=game_object)
        except Exception:
            logger.exception('An error occured while constructing a component')
            sys.exit(ExitCodes.EXIT_CODE_FATAL_CONSTRUCT)
        else:
            return refname, component


class GameObjectLoader(YamlLoader):

    """Specialized loader for loading and constructing gameobjects from configurations."""  # noqa: E501

    def load(self) -> dict[str, TGameObject]:
        """
        Load gameobjects from a yaml file.

        :return: Returns a processable dictionary containing constructed gameobjects.
        :rtype: dict[str, TGameObject]
        """
        data: dict[str, TGameObjectConfig] = super().load()
        loaded = {}
        for name, definition in data.items():
            if definition.get('prefab'):
                del definition['prefab']
                self.register_loaded(name, definition, registry=PrefabRegistry)
                continue
            game_object = TGame().objectbuilder.build(
                name=name,
                definition=definition,
            )
            self.register_loaded(name, game_object)
            loaded[name] = game_object
        return loaded
