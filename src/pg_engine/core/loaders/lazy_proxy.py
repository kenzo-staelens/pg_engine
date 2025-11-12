import logging
from collections.abc import Callable
from typing import Any

from lazy_object_proxy import Proxy as _Proxy

from pg_engine.core import ContextRegistry

logger = logging.getLogger(__name__)


class env_cached_property:  # noqa: N801 no, because it's a decorator

    """
    Lazy proxy based on :func:`lazy_object_proxy.utils.cached_property`.

    Additionally skips caching if 'evaluate lazy' context variable is\
        explicity set to false
    """

    def __init__(self, func: Callable):
        """
        Proxy a method.

        .. code-block:: python

           @env_cached_property
           def method(...):
               ...

        :param func: the method being decorated
        :type func: Callable
        """
        self.func = func

    def __get__(self, instance: Any, _: Any) -> Any:  # noqa: ANN401
        """
        Access a property and cache the result.

        This method caches the value as soon as it's being accessed except when\
        'evaluate_lazy' context is False, in which case no caching occurs

        :param instance: Instance being accessed
        :type instance: Any
        :param _: Owner class (unused)
        :type _: Any
        :return: cached value or current value if not yet cached
        :rtype: Any
        """
        if instance is None:
            return self
        value = self.func(instance)
        if ContextRegistry.get_context('evaluate_lazy') != False:  # noqa: E712 True default for None
            if not hasattr(self.func, '__name__'):
                logger.warning('Nameless functions not supported')
                return value
            instance.__dict__[self.func.__name__] = value
        return value


# small patch to proxy to keep context
class Proxy(_Proxy):

    """Patched lazy object proxy to use custom cached proxy."""

    @env_cached_property
    def __wrapped__(self):  # noqa: PLW3201 inherited from _Proxy
        if ContextRegistry.get_context('evaluate_lazy') == False:  # noqa: E712 True default for None
            return None
        return super().__wrapped__
