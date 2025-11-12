from __future__ import annotations

from abc import ABC, abstractmethod

type SerializableData = int | float | str | bool
type SerializableDict = dict[str, SerializableData] | dict[str, SerializableDict]


class ISerializable(ABC):
    @abstractmethod
    def serialize(self) -> SerializableDict:
        """
        Create a JSON writeable representation of this object.

        :return: JSON writeable representation
        :rtype: SerializableDict
        """

    @abstractmethod
    def from_serialized(self, saved: SerializableDict) -> bool:
        """
        Load from serialized data.

        :param saved: data saved via :func:`serializable`
        :type saved: SerializableDict
        :return: whether loading was successful
        :rtype: bool
        """
