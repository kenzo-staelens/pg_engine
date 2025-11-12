from __future__ import annotations


class IPlugin:
    __plugin_extends__ = None

    def __init_subclass__(cls):
        if cls.__plugin_extends__ is None:
            message = '__plugin_extends__ cannot be None'
            raise ValueError(message)
        super().__init_subclass__()
