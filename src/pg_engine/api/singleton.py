from __future__ import annotations

import logging
import weakref
from typing import ClassVar, Self, final

logger = logging.getLogger(__name__)


class Singleton:

    """
    Class to manage and create singleton objects.

    This class should, in almost all cases be inherited to create singleton classes\
        while still functioning as a Registry (do not confuse with :class:`IRegistry`\
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


__all__ = [
    'Singleton',
]


__all__ = [
    'Singleton',
]
