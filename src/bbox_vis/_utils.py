"""Internal utilities for bbox-vis"""

from collections.abc import Sequence
from functools import lru_cache, wraps

SUPPORTED_BBOX_FORMATS = ("xyxy", "xywh", "cxcywh")


def _validate_bbox(bbox: Sequence[int]) -> None:
    """Validate bounding box format and values.

    Args:
        bbox: List of [x_min, y_min, x_max, y_max] coordinates

    Raises:
        ValueError: If bbox is empty, has wrong length, or has invalid coordinates

    """
    if bbox is None or (hasattr(bbox, "__len__") and len(bbox) == 0):
        raise ValueError("Bounding box cannot be empty")
    if len(bbox) != 4:
        raise ValueError(
            "Bounding box must have exactly 4 coordinates, e.g. [x_min, y_min, x_max, y_max]"
        )
    if bbox[0] > bbox[2] or bbox[1] > bbox[3]:
        raise ValueError(
            "Invalid bounding box coordinates: x_min > x_max or y_min > y_max"
        )


def _convert_bbox(
    bbox: Sequence[float | int],
    img_size: tuple[int, int],
    from_format: str,
    to_format: str = "xyxy",
    is_normalized: bool = False,
) -> list[int]:
    """Convert a bounding box from the given format to the specified format in absolute pixels.

    Supported formats:
        - ``"xyxy"``:  ``[x_min, y_min, x_max, y_max]``
        - ``"xywh"``: ``[x_min, y_min, width, height]``
        - ``"cxcywh"``: ``[x_center, y_center, width, height]``

    Args:
        bbox: Bounding box coordinates expressed in ``bbox_format``
        img_size: Tuple of (width, height) used to denormalize boxes
        from_format: One of ``"xyxy"``, ``"xywh"``, or ``"cxcywh"``
        to_format: One of ``"xyxy"``, ``"xywh"``, or ``"cxcywh"`` (default: ``"xyxy"``)
        is_normalized: Whether the bounding box coordinates are normalized (default: ``False``)

    Returns:
        Bounding box as the specificed ``to_format`` in absolute integer pixels

    Raises:
        ValueError: If ``from_format`` or ``to_format`` is unsupported or ``bbox`` is not 4 values

    """
    f_fmt, t_fmt = from_format.lower(), to_format.lower()
    if f_fmt not in SUPPORTED_BBOX_FORMATS:
        raise ValueError(
            f"Unsupported from_format {from_format!r}. "
            f"Expected one of {SUPPORTED_BBOX_FORMATS}."
        )
    if t_fmt not in SUPPORTED_BBOX_FORMATS:
        raise ValueError(
            f"Unsupported to_format {to_format!r}. "
            f"Expected one of {SUPPORTED_BBOX_FORMATS}."
        )
    if bbox is None or len(bbox) != 4:
        raise ValueError("Bounding box must have exactly 4 coordinates")

    if is_normalized:
        img_width, img_height = img_size[0], img_size[1]
        bbox = [
            bbox[0] * img_width,
            bbox[1] * img_height,
            bbox[2] * img_width,
            bbox[3] * img_height,
        ]

    if f_fmt == "xyxy":
        x_min, y_min, x_max, y_max = bbox
    elif f_fmt == "xywh":
        x_min, y_min, width, height = bbox
        if width < 0 or height < 0:
            raise ValueError("bounding box width and height must be non-negative")
        x_max, y_max = x_min + width, y_min + height
    else:
        x_center, y_center, width, height = bbox
        if width < 0 or height < 0:
            raise ValueError("bounding box width and height must be non-negative")
        x_min = x_center - width / 2
        y_min = y_center - height / 2
        x_max, y_max = x_min + width, y_min + height

    if t_fmt == "xyxy":
        return [round(x_min), round(y_min), round(x_max), round(y_max)]
    elif t_fmt == "xywh":
        width = x_max - x_min
        height = y_max - y_min
        return [round(x_min), round(y_min), round(width), round(height)]
    else:
        width = x_max - x_min
        height = y_max - y_min
        x_center = x_min + width / 2
        y_center = y_min + height / 2
        return [round(x_center), round(y_center), round(width), round(height)]


def _freeze_arguments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Convert any list argument into a tuple automatically
        frozen_args = tuple(tuple(x) if isinstance(x, Sequence) else x for x in args)
        frozen_kwargs = {
            k: tuple(v) if isinstance(v, Sequence) else v for k, v in kwargs.items()
        }
        return func(*frozen_args, **frozen_kwargs)

    return wrapper


@_freeze_arguments
@lru_cache(maxsize=64)
def _get_thickness(image_size: tuple[int, int], min_val: int = 1) -> int:
    """Determine the thickness of the bounding box lines based on the image size

    Args:
        image_size: Size of the image as a tuple of (width, height)
        min_val: Minimum thickness value, default is 1

    Returns:
        Thickness of the bounding box lines
    """
    thickness = max(round(sum(image_size) / 2 * 0.005), min_val)
    return thickness


@_freeze_arguments
@lru_cache(maxsize=64)
def _get_font_size(image_size: tuple[int, int], min_val: int = 6) -> int:
    """Determine the font size based on the image size

    Args:
        image_size: Size of the image as a tuple of (width, height)
        min_val: Minimum font size value, default is 6

    Returns:
        Font size for the text
    """
    font_size = max(round(sum(image_size) / 2 * 0.03), min_val)
    return font_size
