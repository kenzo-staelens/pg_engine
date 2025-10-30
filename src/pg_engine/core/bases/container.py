import logging
from collections.abc import Iterator
from types import NoneType

from pg_engine.api import IComponent, IContainer

logger = logging.getLogger(__name__)


class ObjectContainer[T](IContainer[T]):

    """
    Generic[T] instantiable container class.

    :attr:`_t` exists for logging purposes and should be the type\
        of objects in this container
    """

    _t = NoneType

    def __init__(self, source: object = None):
        self.__source_object = source
        self.container: dict[str, T] = {}
        self._t: type  # the type of T

    def add(self, name: str, store: T) -> None:
        if name in self.container:
            logger.error(
            "%s[%s] already has '%s'",
                self.__source_object,
                self._t.__name__,
                name,
            )
            return
        self.container[name] = store

    def override(self, name: str, store: T) -> None:
        self.container[name] = store

    def __delattr__(self, name: str) -> None:
        if name in self.container:
            del self.container[name]
            return
        logger.error(
            "%s[%s] has no '%s'",
            self.__class__.__name__,
            self._t.__name__,
            name,
        )

    def __iter__(self) -> Iterator[T]:
        return iter(self.container.values())

    def get_of_type[U](self, tclass: type[U]) -> list[U]:
        return [c for c in self.container.values() if isinstance(c, tclass)]

    def by_name(self, name: str) -> T | None:
        return self.container.get(name)


class ComponentContainer(ObjectContainer[IComponent]):

    """Type narrowed container for :class:`IComponent`."""

    def __init__(self, source: object):
        super().__init__(source)
        self._t = IComponent
