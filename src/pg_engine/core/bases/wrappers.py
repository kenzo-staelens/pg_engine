from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import cast


def parameterized[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorate a decorator to handle passing arguments or leaving bare.

    allows use of both

    .. code-block:: python

       @my_decorator
       def func():
           ...

    and

    .. code-block:: python

       @my_decorator(param=value)
       def func():
           ...

    :param func: The decorator being modified.
    :type func: Callable
    :return: Augmented decorator
    :rtype: Callable
    """
    @functools.wraps(func)
    def wrapper(fn: Callable | None = None, **kw) -> Callable:
        if fn is None:
            return functools.partial(func, **kw)
        return cast('Callable[P, T]', func(fn, **kw))
    return wrapper


def one_shot[**P, T](oneshot_fn: Callable[P, T]) -> Callable[P, T]:
    """
    Modify decorator behavior targeting unbound class methods.

    Decorators decorated with this method should only be applied on unbound\
        class methods. Such decorators can then modify the class of the method\
        they're discarded upon performing their function

    ## example:
        :func:`listen`

    :param oneshot_fn: The decorator being decorated
    :type oneshot_fn: _type_
    :return: the decorated decorator
    :rtype: Callable
    """

    class OneshotWrapper:
        def __init__(self, fn: Callable | None = None, **kwargs):
            self.fn = fn
            self.kwargs = kwargs
            functools.update_wrapper(
                cast('Callable', self),
                cast('Callable', fn),
            )

        def __set_name__(self, owner: type, name: str) -> None:
            # HACK: run the oneshot_fn decorator once then forget
            # it ever got used to wrap the method `fn`

            # this results in removing a lot of overhead
            # for methods that get called repeatedly
            # but only need to get initialized once
            oneshot_fn(self.fn, owner, **self.kwargs)
            setattr(owner, name, self.fn)

    # we don't know if the wrapped method is parameterized
    # just assume it is; if not it will just as if parameterized was never used
    @functools.wraps(oneshot_fn)
    @parameterized
    def wrapper(fn: Callable, **kw) -> OneshotWrapper:
        return OneshotWrapper(fn, **kw)
    return wrapper


def throttled[T, **P](delay: float) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorate a function call with a rate limit.

    :param delay: minimum delay between calls in (real time) seconds
    :type delay: float
    :return: the wrapped method
    :rtype: Callable[[Callable[P, T]], Callable[P, T]]
    """
    start = time.time() - delay

    def throttled_wrapper(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kw: P.kwargs) -> T | None:
            nonlocal start
            now = time.time()
            if now - start < delay:
                return None
            start = time.time()
            return func(*args, **kw)
        return wrapper
    return throttled_wrapper


__all__ = [
    'one_shot',
    'parameterized',
    'throttled',
]
