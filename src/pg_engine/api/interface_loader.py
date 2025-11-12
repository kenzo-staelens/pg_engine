from __future__ import annotations

import logging
import pathlib
from abc import ABC, abstractmethod
from typing import Any

from .interface_registry import IRegistry
from .registry import ClassRegistry

logger = logging.getLogger(__name__)


class ILoader(ABC):

    """Base class for data loaders loading data from a file."""

    def __init__(
        self,
        filename: str,
        root: pathlib.PosixPath,
        registry: IRegistry | str | None = None,
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
        self.root = root
        self.registry: IRegistry | None = None
        if isinstance(registry, IRegistry):
            self.registry: IRegistry = registry
        elif isinstance(registry, str):
            self.registry: IRegistry = ClassRegistry.get(registry)

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
        registry: type[IRegistry] | IRegistry | None = None,
    ) -> bool:
        """
        Register a loaded object into this loader's registry.

        :param name: name to store the object as
        :type name: str
        :param loaded: the loaded object
        :type loaded: object
        :param registry: another registry to store into instead, defaults to None
        :type registry: IRegistry | None, optional
        :return: whether storing was successful
        :rtype: bool
        """
        if registry:
            return registry.register(name, loaded)
        if self.registry:
            return self.registry.register(name, loaded)
        logger.warning("Attempted to register '%s' with no registry", name)
        return False


__all__ = [
    'ILoader',
]
