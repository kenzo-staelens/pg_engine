from abc import ABC, abstractmethod


class IBuilder[T](ABC):

    """Generic class used to build other objects of type T."""

    def __init__(
        self,
        builder_class: type[T] | None = None,
        builder_kw: dict | None = None,
    ):
        """
        Initialize the builder.

        :param builder_class: Class which gets used to create objects, defaults to None
        :type builder_class: type[T] | None, optional
        :param builder_kw: keyword args for the builder_class, defaults to None
        :type builder_kw: dict | None, optional
        :raises ValueError: raised when the provided builder is None
        """
        if builder_class is None:
            raise ValueError
        self.builder_class = builder_class
        self.builder_kw: dict = builder_kw or {}

    @abstractmethod
    def build(self, name: str, definition: dict | None = None) -> T:
        """
        Build an object using `builder_class` as class to pass the definition to.

        :param name: name of the object to build
        :type name: str
        :param definition: blueprint of the object to build, defaults to None
        :type definition: dict | None, optional
        :return: the built object
        :rtype: T
        """


__all__ = [
    'IBuilder',
]
