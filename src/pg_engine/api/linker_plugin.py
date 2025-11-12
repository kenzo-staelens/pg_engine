from __future__ import annotations

from typing import cast, final

from .interface_plugin import IPlugin
from .interface_registry import IRegistry


@final
class PluginRegistry(IRegistry[type[IPlugin]]):
    __singleton_key__ = 'PluginRegistry'


class PluginLinker:
    @staticmethod
    def link_plugin(linkable: type) -> type:
        """
        Link plugins into an existing class.

        :param linkable: Class to link plugins on
        :type linkable: type
        :return: Class with plugins linked
        :rtype: type
        """
        mro = linkable.__mro__
        new_bases: list[type[IPlugin]] = [
            plugin
            for plugin in PluginRegistry.values()
            if any(plugin.__plugin_extends__ == str(t) for t in mro)
        ]
        if not new_bases:
            return linkable
        return type(
            linkable.__name__,
            (*new_bases, *linkable.__bases__),
            cast('dict', linkable.__dict__),
        )


__all__ = [
    'PluginLinker',
    'PluginRegistry',
]
