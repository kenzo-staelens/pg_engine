from abc import ABC, abstractmethod
from collections.abc import Iterator


class IContainer[T](ABC):

    """Generic container class."""

    @abstractmethod
    def __init__(self):
        """Initialize the container."""

    @abstractmethod
    def add(self, name: str, store: T) -> None:
        """
        Add an object to the container.

        Adding an object should not override existing objects.
        use :func:`~override` for such functionality

        :param name: reference of the stored object in this container
        :type name: str
        :param store: Object to store
        :type store: T
        """

    @abstractmethod
    def override(self, name: str, store: T) -> None:
        """
        Add or override an object to the container.

        :param name: reference of the stored object in this container
        :type name: str
        :param store: Object to store
        :type store: T
        """

    @abstractmethod
    def __delattr__(self, name: str) -> None:
        """
        Delete an object out of this container by name.

        :raises AttributeError: raised when no object with name can be found.
        :param name: name reference of the object to delete
        :type name: str
        """

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        """
        Iterate interface of this container.

        :yield: Iterator of this container;
        :rtype: Iterator[T]
        """

    @abstractmethod
    def get_of_type[U](self, tclass: type[U]) -> list[U]:
        """
        Get all items of type :class:`U` in this container.

        :param tclass: class or superclass of the returned objects.
        :type tclass: type[T]

        :return: list of all objects of type :type:`U`
        :rtype: List[U]
        """

    @abstractmethod
    def by_name(self, name: str) -> T:
        """
        Get an object out of this container by name.

        :raises AttributeError: raised when no object with name can be found
        :param name: name reference of the object to get
        :type name: str
        :return: object found at reference.
        :rtype: T
        """


__all__ = [
    'IContainer',
]
