from abc import ABCMeta


class PostInit(ABCMeta):

    """Metaclass to add an extra __post_init__ initialization step after __init__."""

    def __call__(cls, *args, **kw):
        instance = super().__call__(*args, **kw)  # < runs __new__ and __init__
        instance.__post_init__()
        return instance


__all__ = [
    'PostInit',
]
