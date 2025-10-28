from collections.abc import Iterable


def apply_transform(*transforms: Iterable[int | float]) -> Iterable[int | float]:
    """
    Apply multiple transforms Sequentially.

    :return: result of the sequentially applied transforms
    :rtype: Iterable[int | float]
    """
    return tuple(
        sum(axis)
        for axis in zip(
            *transforms,
            strict=True,
        )
    )


def clip(value: float, min_val: float, max_val: float) -> float:
    """
    Clip a value between minimum and maximum values.

    :param value: the value to clip
    :type value: float
    :param min_val: minimum allowed value
    :type min_val: float
    :param max_val: maximum allowed value
    :type max_val: float
    :return: value if value in domain [min_val, max_val] otherwise whatever is closest
    :rtype: float
    """
    return max(
        min_val,
        min(
            max_val,
            value,
        ),
    )
