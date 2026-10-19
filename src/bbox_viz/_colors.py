import numbers
from collections.abc import Sequence
from functools import lru_cache

from ._utils import _freeze_arguments

_DEFAULT_COLORS = [
    (0, 114, 189),
    (217, 83, 25),
    (237, 177, 32),
    (126, 47, 142),
    (119, 172, 48),
    (77, 190, 238),
    (162, 20, 47),
    (76, 76, 76),
    (153, 153, 153),
    (255, 0, 0),
    (255, 128, 0),
    (191, 191, 0),
    (0, 255, 0),
    (0, 0, 255),
    (170, 0, 255),
    (85, 85, 0),
    (85, 170, 0),
    (85, 255, 0),
    (170, 85, 0),
    (170, 170, 0),
    (170, 255, 0),
    (255, 85, 0),
    (255, 170, 0),
    (255, 255, 0),
    (0, 85, 128),
    (0, 170, 128),
    (0, 255, 128),
    (85, 0, 128),
    (85, 85, 128),
    (85, 170, 128),
    (85, 255, 128),
    (170, 0, 128),
    (170, 85, 128),
    (170, 170, 128),
    (170, 255, 128),
    (255, 0, 128),
    (255, 85, 128),
    (255, 170, 128),
    (255, 255, 128),
    (0, 85, 255),
    (0, 170, 255),
    (0, 255, 255),
    (85, 0, 255),
    (85, 85, 255),
    (85, 170, 255),
    (85, 255, 255),
    (170, 0, 255),
    (170, 85, 255),
    (170, 170, 255),
    (170, 255, 255),
    (255, 0, 255),
    (255, 85, 255),
    (255, 170, 255),
    (85, 0, 0),
    (128, 0, 0),
    (170, 0, 0),
    (212, 0, 0),
    (255, 0, 0),
    (0, 43, 0),
    (0, 85, 0),
    (0, 128, 0),
    (0, 170, 0),
    (0, 212, 0),
    (0, 255, 0),
    (0, 0, 43),
    (0, 0, 85),
    (0, 0, 128),
    (0, 0, 170),
    (0, 0, 212),
    (0, 0, 255),
    (0, 0, 0),
    (36, 36, 36),
    (73, 73, 73),
    (109, 109, 109),
    (146, 146, 146),
    (182, 182, 182),
    (219, 219, 219),
    (0, 114, 189),
    (80, 183, 189),
]


@_freeze_arguments
@lru_cache(maxsize=64)
def _validate_color(color: Sequence[int]) -> tuple[int, int, int]:
    """Validate a RGB color sequence and normalize it to a tuple of ints.

    Args:
        color: RGB color sequence to validate

    Returns:
        The color as a tuple

    Raises:
        ValueError: If color is not a valid RGB sequence

    """
    if not hasattr(color, "__len__") or len(color) != 3:
        raise ValueError("Color must be a sequence of 3 integers (RGB)")
    # numbers.Integral also admits numpy integer scalars, e.g. colors
    # sampled from image pixels (np.uint8)
    if not all(isinstance(c, numbers.Integral) and 0 <= c <= 255 for c in color):
        raise ValueError("Color values must be integers between 0 and 255")
    r, g, b = (int(c) for c in color)
    return (r, g, b)


@_freeze_arguments
@lru_cache(maxsize=64)
def _get_text_color(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """Assign white or black text color based on the box color

    Args:
        color: RGB color for the bounding box

    Returns:
        RGB color for the text
    """
    color = _validate_color(color)
    txt_color = (0, 0, 0) if sum(color) / 3 > 80 else (255, 255, 255)
    return txt_color
