from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from .registry import ClassRegistry

if TYPE_CHECKING:
    from .interface_registry import IRegistry


class ILoader(ABC):

    """Base class for data loaders loading data from a file."""

    def __init__(
        self,
        filename: str,
        root: pathlib.PosixPath,
        registry: str | None = None,
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
        self.registry = None
        self.root = root
        if registry is not None:
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
        registry: IRegistry | None = None,
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
        return self.registry.register(name, loaded)


__all__ = [
    'ILoader',
]
