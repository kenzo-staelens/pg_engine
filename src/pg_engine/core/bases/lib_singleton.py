from __future__ import annotations

import logging
import weakref
from typing import ClassVar, Literal, Self, final

logger = logging.getLogger(__name__)


class Singleton:

    """
    Class to manage and create singleton objects.

    This class should, in almost all cases be inherited to create singleton classes\
        while still functioning as a Registry (do not confuse with :class:`TRegistry`\
        though they have a similar API.)

    :term:`__singleton_key__` key under which an instance can be directly requested\
        from the singleton class

    :term:`__destroyable__` whether the singleton can be destroyed, defaults to True.

    For all intents and purposes one cannot feasibly create an instance from Singleton\
    as an error gets thrown when :term:`__singleton_key__` is not set
    """

    _instances: ClassVar = {}
    __singleton_key__ = None
    __destroyable__ = True

    @final
    @classmethod
    def destroy(cls) -> None:
        """
        Destroy a singleton instance.

        If :term:`__destroyable__` is set to false log a warning instead.
        """
        logger.debug(
            'Singleton: Destroying %s',
            cls.__name__,
        )
        if cls.__destroyable__ and cls.__singleton_key__ in Singleton._instances:
            del Singleton._instances[cls.__singleton_key__]
            return
        logger.warning(
            "Singleton: '%s' is not destroyable.",
            cls.__name__,
        )

    @final
    def __new__(cls, *args, **kw) -> Self:
        """
        Return an existing singleton (by :term:`__singleton_key__`) or create a new one.

        :return: an instance of the Singleton (sub)class
        :rtype: Self
        """
        if cls.__singleton_key__ is None:
            logger.error(
                'Singleton[%s]: __singleton_key__ cannot be None',
                cls.__name__,
            )
            return None
        if cls.__singleton_key__ not in cls._instances:
            instance = super().__new__(cls)
            instance.__init__(*args, **kw)
            Singleton._instances[cls.__singleton_key__] = instance
        return weakref.proxy(Singleton._instances[cls.__singleton_key__])

    @classmethod
    def get(cls, name: str, default: Singleton | None = None) -> Singleton | None:
        """
        Get a Singleton instance by it's name.

        :param name: name of the singleton, this is it's :term:`__singleton_key__`
        :type name: str
        :param default: Default to return if no instance found, defaults to None
        :type default: Singleton | None, optional
        :return: instance of a singleton or the default
        :rtype: Singleton | None
        """
        inst = cls._instances.get(name)
        if inst:
            return inst
        return default

    @classmethod
    def list(cls) -> list[str]:
        """
        List all singletons (name) for which an instance exists.

        :return: list (name) of all instantiated singletons
        :rtype: list[str]
        """
        return list(cls._instances.keys())

    @classmethod
    def clear(cls) -> None:
        """Discard internal registry of instantiated singletons."""
        cls._instances.clear()


class TRegistry[T](Singleton):

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
    'Singleton',
    'TRegistry',
]
