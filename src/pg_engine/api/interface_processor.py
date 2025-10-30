from abc import ABC, abstractmethod
from typing import Any


class IProcessor(ABC):

    """Base Class for Processors."""

    # overload doesn't work with classmethods
    @classmethod
    @abstractmethod
    def process(
        cls,
        config: dict[str, Any],
        processor_args: dict[str, str] | None = None,
    ) -> None:
        """
        Process (standardized) incoming configuration data.

        :param config: incoming configuration in standardized
            (ie. dict[str, any]) format
        :type config: dict[str, Any]
        :param processor_args: arguments passed to the concrete implementation,
            defaults to None
        :type processor_args: dict[str, str] | None, optional
        :rtype: None
        """


__all__ = [
    'IProcessor',
]
