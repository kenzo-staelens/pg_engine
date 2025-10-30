from __future__ import annotations

import pathlib
from collections.abc import Callable
from functools import partial
from typing import Any

import yaml
from yaml.nodes import Node

from pg_engine.api import (
    ILoader,
    IRegistry,
)
from pg_engine.core import (
    ClassRegistry,
    Context,
    ContextRegistry,
)

from .lazy_proxy import Proxy

BASE_PATH = pathlib.Path(__file__).parent.parent.parent.parent


def get_factory_method(registry: IRegistry, proxy: str) -> Callable:
    """
    Create a factory method for lazy loader.

    :param registry: registry to load from
    :type registry: IRegistry
    :param proxy: name of the object being proxied
    :type proxy: str
    :return: factory method used by :class:`Proxy`
    :rtype: Callable
    """
    def factory_method[T]() -> T:
        return registry.get(proxy)
    return factory_method


class ConsumeRefs(yaml.Loader):

    """
    Extra anchors consumer.

    helper class for consuming references created by YamlLoader
    or any other yaml like loader that passes the extra_anchors context.

    This is because if a loader would instantiate a new loader or load an extra file
    all references would be lost.
    """

    def compose_node(
        self,
        node: Node | None,
        index: int,
    ) -> Node | None:
        anchors = ContextRegistry.get_context('extra_anchors')
        if anchors:
            # load self refs over given anchors
            self.anchors = anchors | self.anchors
        return super().compose_node(node, index)


class YamlConstructors(ConsumeRefs):
    def __init__(self, stream: yaml._ReadStream, root: None = None):
        super().__init__(stream)
        self.root = root

    def include(self, node: Node) -> dict:
        """
        Include another file's content into this file.

        .. code-block:: yaml

           !include path/to/included/file.yml

        :param node: String node containing the path of the included file
        :type node: Node
        :return: yaml loaded content of the included file
        :rtype: dict
        :raises RuntimeError: raised when including without a root
        """
        if not self.root:
            message = 'Cannot Include without a root'
            raise RuntimeError(message)

        filename = self.construct_scalar(node)
        with open(self.root / filename) as stream:
            return yaml.load(
                stream,
                partial(YamlConstructors, root=self.root),  # noqa: S506
            )

    def lazy(self, node: Node) -> Proxy:
        """
        Load a reference as lazy loadable.

        .. code-block:: yaml

           !lazy
           target_registry: __singleton_key__ of a registry
           proxies: name of the object as it appears or will appear in the registry

        :param node: Mapping in the above format
        :type node: Node
        :return: :class:`~.base_library.core.loaders.Proxy` for lazy evaluation
        :rtype: :class:`~.base_library.core.loaders.Proxy`
        """
        mapping = self.construct_mapping(node)
        reg: IRegistry = ClassRegistry.get(mapping['target_registry'])()
        factory = get_factory_method(reg, mapping['proxies'])

        return Proxy(factory)

    def calc(self, node: Node) -> int | float:
        """
        Perform math within a yaml file.

        !! USES EVAL

        ## Mapping format

        .. code-block:: yaml

           !calc
           values:
             - value
             - value
             - ...
           formula: formula in python fstring format

           example_three: !calc
             values:
               - 1
               - 2
             formula: "{}+{}"


        :param node: Mapping in the above format
        :type node: Node
        :return: calculation result
        :rtype: int | float
        """
        mapping = self.construct_mapping(node, deep=True)
        formula = mapping['formula'].format(*mapping['vars'])
        return eval(formula)  # noqa: S307
        # game config data is assumed to be safe
        # if not then the developer of this game shouldn't have to go through here
        # in the first place

    def classget(self, node: None) -> type:
        """
        Get a class in the :class:`ClassRegistry`.

        .. code-block:: yaml

           !classget RegisteredClassWithNoArgs

        :param node: String node containing the registered name of a class
        :type node: None
        :return: Class as found in the registry
        :rtype: type
        """
        initnode = self.construct_scalar(node)
        return ClassRegistry.get(initnode)

    def classinit(self, node: Node) -> Any:  # noqa: ANN401
        """
        Initialize a class in the :class:`ClassRegistry`.

        ## Mapping format

        .. code-block:: yaml

           !classinit
             type: RegisteredClassWithArgs
             args:
               args: to_pass

        :param node: String node containing the registered name of a class
        :type node: None
        :return: Class as found in the registry
        :rtype: type
        """
        if isinstance(node, yaml.nodes.MappingNode):
            initnode = self.construct_mapping(node, deep=True)
            cls = ClassRegistry.get(initnode['type'])
            return cls(**initnode['args'])
        if isinstance(node, yaml.nodes.ScalarNode):
            initnode = self.construct_scalar(node)
            return ClassRegistry.get(initnode)()
        return None


YamlConstructors.add_constructor('!include', YamlConstructors.include)
YamlConstructors.add_constructor('!lazy', YamlConstructors.lazy)
YamlConstructors.add_constructor('!calc', YamlConstructors.calc)
YamlConstructors.add_constructor('!classinit', YamlConstructors.classinit)
YamlConstructors.add_constructor('!classget', YamlConstructors.classget)


class YamlLoader(ILoader):

    """Base class for loaders that load in a yaml file format."""

    def __init__(
        self,
        filename: str,
        root: pathlib.PosixPath,
        registry: IRegistry,
        useref: str | list[str] | None = None,
    ):
        """
        Initialize the loader.

        :param filename: Filename/path to load from
        :type filename: str
        :param root: Filename/path search configurations in
        :type root: str
        :param registry: registry this loader stores loaded objects into,\
            defaults to None
        :type registry: IRegistry
        :param useref: file or files to use as anchor references, defaults to None
        :type useref: str | list[str] | None, optional
        """
        super().__init__(filename, root, registry)
        if isinstance(useref, str):
            useref = [useref]
        self.useref = useref or []

    def load(self) -> dict[str, Any]:
        """
        Load data from a file, optionally using external references.

        :return: loaded data in standardized dict[str, any] format
        :rtype: dict[str, Any]
        """
        with open(self.root / self.filename) as f:
            loader = YamlConstructors(f, root=self.root)
            anchors = {}
            for ref in self.useref:
                anchors |= self._load_refs(ref, loader)
            with Context(extra_anchors=anchors, include_fileroot=str(self.root)):
                return loader.get_single_data()

    def _load_refs(self, ref_path: str, loader: ConsumeRefs) -> dict[str, Node]:
        """
        Load raw yaml references from another file.

        :param ref_path: file path
        :type ref_path: str
        :param loader: Loader to use while loading references
        :type loader: ConsumeRefs
        :return: raw references as used by :class:`yaml.Loader` subclasses
        :rtype: dict[str, Node]
        """
        with open(self.root / ref_path) as f:
            new_loader = loader.__class__(f, root=self.root)
        new_loader.get_event()
        if not new_loader.check_event(yaml.events.StreamEndEvent):
            new_loader.get_event()
            new_loader.compose_node(None, None)
        anchors = new_loader.anchors
        new_loader.dispose()
        return anchors
