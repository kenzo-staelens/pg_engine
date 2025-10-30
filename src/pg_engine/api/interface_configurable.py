from abc import ABC, abstractmethod


class IConfigurable(ABC):
    @abstractmethod
    def configure(self, config_data: dict) -> None:
        """
        Perform subclass specific configurations.

        :param config_data: Configuration data
        :type config_data: dict
        """


__all__ = [
    'IConfigurable',
]
