import logging
from typing import Literal

from .singleton import Singleton

logger = logging.getLogger(__name__)


class IRegistry[T](Singleton):

    """Non destroyable Generic[T] Singleton used to register and store one type of object."""  # noqa: E501

    __destroyable__: Literal[False] = False

    def __init__(self):
        self.__registry: dict[str, T] = {}

    @classmethod
    def register(cls, name: str, entry: T, *, override: bool = False) -> bool:
        """
        Register an object into this registry.

        Logs a warning when attempting to register an entry that already exits\
            without setting override.

        :param name: name to register the object as
        :type name: str
        :param entry: the object to register
        :type entry: T
        :param override: whether to allow override an existing value, defaults to False
        :type override: bool, optional
        :return: whether registering was successful.
        :rtype: bool
        """
        instance = cls()
        if isinstance(entry, type):
            entryclass = entry.__name__
        else:
            entryclass = entry.__class__.__name__

        if not override and name in instance.__registry:
            # turns out pygame.Surface has no fucking __name__
            obj = instance.__registry[name]
            logger.warning(
                'Registry[%s]: %s[%s] already registered as %s',
                cls.__singleton_key__,
                name,
                entryclass,
                getattr(obj, '__name__', repr(obj)),
            )
            return False
        instance.__registry[name] = entry
        return True

    @classmethod
    def get(cls, name: str) -> T | None:
        """
        Get a registered object by name.

        Logs an error when no entry is found

        :param name: name of an object registered with :func:`~.register`
        :type name: str
        :return: object registered under the key or None if not found
        :rtype: T | None
        """
        instance = cls()
        if not instance.has(name):
            logger.error(
                "Registry[%s]: Failed to load '%s'",
                cls.__singleton_key__,
                name,
            )
            return None
        return instance.__registry[name]

    @classmethod
    def get_typed[U](cls, name: str, expect_type: U) -> U | None:
        """
        Wrap .get with a typing sanity check and support for static type checking.

        :param name: name of an object registered with :func:`~.register`
        :type name: str
        :param expect_type: A subtype of T, the type expected to be returned
        :type expect_type: U
        :raises TypeError: Raised when type does not match the expected type
        :return: object registered under the key or None if not found
        :rtype: U
        """
        res = cls.get(name)
        if res is not None and not isinstance(res, expect_type):
            message = (
                f'expected object of type {expect_type} or None '
                f'but got object of type {type(res)}'
            )
            raise TypeError(message)
        return res

    @classmethod
    def has(cls, name: str) -> bool:
        """
        Whether the registry has an object registered under this key.

        :param name: name of an object registered with :func:`~.register`
        :type name: str
        :return: whether an object with `name` is found
        :rtype: bool
        """
        instance = cls()
        return name in instance.__registry

    @classmethod
    def list(cls) -> list[str]:
        """
        List all objects (name) for which an instance exists.

        :return: list (name) of all registered objects
        :rtype: list[str]
        """
        instance = cls()
        return list(instance.__registry.keys())

    @classmethod
    def clear(cls) -> None:
        """Clear the registry."""
        instance = cls()
        instance.__registry = {}


__all__ = [
    'IRegistry',
]
