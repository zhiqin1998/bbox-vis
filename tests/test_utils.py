import pytest

from bbox_viz._colors import _get_text_color, _validate_color
from bbox_viz._utils import (
    _convert_bbox,
    _get_font_size,
    _get_thickness,
    _validate_bbox,
)


@pytest.mark.parametrize(
    ("bbox", "from_format", "to_format", "expected"),
    [
        ((10, 20, 30, 40), "xyxy", "xywh", [10, 20, 20, 20]),
        ((10, 20, 20, 20), "xywh", "cxcywh", [20, 30, 20, 20]),
        ((20, 30, 20, 20), "cxcywh", "xyxy", [10, 20, 30, 40]),
    ],
)
def test_convert_bbox_between_formats(bbox, from_format, to_format, expected):
    assert _convert_bbox(bbox, (100, 80), from_format, to_format) == expected


def test_convert_bbox_denormalizes_and_rounds():
    assert _convert_bbox(
        (0.105, 0.25, 0.305, 0.5),
        (100, 80),
        "xyxy",
        is_normalized=True,
    ) == [10, 20, 30, 40]


@pytest.mark.parametrize("bbox_format", ["bad", ""])
def test_convert_bbox_rejects_unsupported_format(bbox_format):
    with pytest.raises(ValueError, match="Unsupported"):
        _convert_bbox((1, 2, 3, 4), (100, 80), bbox_format)


def test_convert_bbox_rejects_negative_dimensions():
    with pytest.raises(ValueError, match="non-negative"):
        _convert_bbox((1, 2, -3, 4), (100, 80), "xywh")


@pytest.mark.parametrize("bbox", [None, (), (1, 2, 3)])
def test_validate_bbox_rejects_missing_coordinates(bbox):
    with pytest.raises(ValueError, match="Bounding box"):
        _validate_bbox(bbox)


@pytest.mark.parametrize("color", [(0, 0), (256, 0, 0), (0, 1, "2")])
def test_validate_color_rejects_invalid_rgb_values(color):
    with pytest.raises(ValueError, match="Color"):
        _validate_color(color)


def test_validate_color_returns_normalized_integer_tuple():
    assert _validate_color([1, 2, 3]) == (1, 2, 3)


def test_get_text_color_chooses_contrasting_color():
    assert _get_text_color((0, 0, 0)) == (255, 255, 255)
    assert _get_text_color((255, 255, 255)) == (0, 0, 0)


def test_image_size_helpers_have_minimums():
    assert _get_thickness((1, 1)) == 1
    assert _get_font_size((1, 1)) == 6
