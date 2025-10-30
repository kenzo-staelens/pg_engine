from contextvars import ContextVar, Token
from typing import Any, final

from pg_engine.api import IRegistry


@final
class ContextRegistry(IRegistry[ContextVar]):

    """
    Singleton class to centralize context var access.

    :term:`__singleton_key__` = 'Context'
    """

    __singleton_key__ = 'Context'

    @classmethod
    def get_context(cls, ctx: str) -> Any | None:  # noqa: ANN401
        """
        Get a contextvar by name.

        :param ctx: name of the contextvar
        :type ctx: str
        :return: value stored in the contextvar or none if not found
        :rtype: Any | None
        """
        if not cls.has(ctx):
            return None
        ctxvar: ContextVar = cls.get(ctx)  # get contextvar
        return ctxvar.get()  # get value from context


class Context:

    """Context manager for wrapping code execution with a context var."""

    def __init__(self, **contexts: dict[str, Any]):
        self.tokens: list[tuple[ContextVar, Token]] = []
        self.contexts = contexts

    def __enter__(self):
        for context, value in self.contexts.items():
            if not ContextRegistry.has(context):
                ContextRegistry.register(context, ContextVar(context, default=None))
            ctx = ContextRegistry.get(context)
            token = ctx.set(value)
            self.tokens.append((ctx, token))

    def __exit__(self, *args):  # exception/exc types ignored
        for ctx, token in self.tokens:
            ctx.reset(token)
