import pytest
from PIL import Image

from bbox_vis import (
    draw_bbox,
    draw_label,
    draw_multiple_bboxes,
    draw_multiple_labels,
)
from bbox_vis._colors import _DEFAULT_COLORS


@pytest.fixture
def image():
    return Image.new("RGB", (100, 80), "white")


def test_draw_bbox_draws_outline_without_mutating_input(image):
    result = draw_bbox(image, (10, 15, 30, 25), color=(255, 0, 0), thickness=1)

    assert result is not image
    assert image.getpixel((10, 15)) == (255, 255, 255)
    assert result.getpixel((10, 15)) == (255, 0, 0)
    assert result.getpixel((30, 25)) == (255, 0, 0)
    assert result.getpixel((20, 20)) == (255, 255, 255)


@pytest.mark.parametrize(
    ("bbox_format", "bbox"),
    [
        ("xyxy", (10, 15, 30, 25)),
        ("xywh", (10, 15, 20, 10)),
        ("cxcywh", (20, 20, 20, 10)),
    ],
)
def test_draw_bbox_supports_coordinate_formats(image, bbox_format, bbox):
    result = draw_bbox(
        image, bbox, bbox_format=bbox_format, color=(255, 0, 0), thickness=1
    )

    assert result.getpixel((10, 15)) == (255, 0, 0)
    assert result.getpixel((30, 25)) == (255, 0, 0)


def test_draw_bbox_denormalizes_coordinates(image):
    result = draw_bbox(
        image,
        (0.1, 0.25, 0.3, 0.5),
        bbox_is_normalized=True,
        color=(0, 0, 255),
        thickness=1,
    )

    assert result.getpixel((10, 20)) == (0, 0, 255)
    assert result.getpixel((30, 40)) == (0, 0, 255)


@pytest.mark.parametrize(
    "bbox",
    [(), (1, 2, 3), (10, 20, 5, 25), (10, 20, 30, 15)],
)
def test_draw_bbox_rejects_invalid_boxes(image, bbox):
    with pytest.raises(ValueError, match=r"Bounding box|Invalid bounding box"):
        draw_bbox(image, bbox, color=(255, 0, 0))


@pytest.mark.parametrize("color", [(-1, 0, 0), (256, 0, 0), (1, 2), (1, 2, 3.5)])
def test_draw_bbox_rejects_invalid_colors(image, color):
    with pytest.raises(ValueError, match="Color"):
        draw_bbox(image, (10, 10, 20, 20), color=color)


def test_draw_bbox_uses_default_color(image):
    result = draw_bbox(image, (10, 10, 20, 20), thickness=1)

    assert result.getpixel((10, 10)) == _DEFAULT_COLORS[0]


def test_draw_label_draws_top_and_bottom_variants(image):
    top = draw_label(
        image,
        (20, 30, 40, 50),
        "cat",
        fill_color=(255, 0, 0),
        font_size=8,
    )
    bottom = draw_label(
        image,
        (20, 30, 40, 50),
        "cat",
        fill_color=(255, 0, 0),
        label_top=False,
        font_size=8,
    )

    assert top.getpixel((20, 29)) == (255, 0, 0)
    assert bottom.getpixel((20, 30)) == (255, 0, 0)
    assert top != bottom
    assert image.getpixel((20, 30)) == (255, 255, 255)


def test_draw_label_uses_explicit_text_color(image):
    result = draw_label(
        image,
        (20, 30, 40, 50),
        "cat",
        fill_color=(255, 255, 255),
        label_color=(255, 0, 0),
        font_size=8,
    )

    assert any(
        red > green and red > blue for red, green, blue in result.get_flattened_data()
    )


def test_draw_multiple_bboxes_cycles_default_colors(image):
    result = draw_multiple_bboxes(
        image,
        [(10, 10, 20, 20), (30, 10, 40, 20)],
        thickness=1,
    )

    assert result.getpixel((10, 10)) == _DEFAULT_COLORS[0]
    assert result.getpixel((30, 10)) == _DEFAULT_COLORS[1]


def test_draw_multiple_bboxes_accepts_one_color_for_all_boxes(image):
    result = draw_multiple_bboxes(
        image,
        [(10, 10, 20, 20), (30, 10, 40, 20)],
        colors=(0, 0, 255),
        thickness=1,
    )

    assert result.getpixel((10, 10)) == (0, 0, 255)
    assert result.getpixel((30, 10)) == (0, 0, 255)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"colors": [(255, 0, 0)]}, "colors"),
        ({"label_colors": [(255, 0, 0)]}, "label_colors"),
        ({"labels": ["one"]}, "labels"),
    ],
)
def test_draw_multiple_bboxes_requires_matching_lengths(image, kwargs, message):
    with pytest.raises(AssertionError, match=message):
        draw_multiple_bboxes(
            image,
            [(10, 10, 20, 20), (30, 10, 40, 20)],
            **kwargs,
        )


def test_draw_multiple_labels_draws_each_label(image):
    result = draw_multiple_labels(
        image,
        [(10, 20, 30, 40), (50, 20, 70, 40)],
        ["cat", "dog"],
        fill_colors=[(255, 0, 0), (0, 0, 255)],
        font_size=8,
    )

    assert result.getpixel((10, 19)) == (255, 0, 0)
    assert result.getpixel((50, 19)) == (0, 0, 255)


def test_draw_multiple_labels_requires_matching_lengths(image):
    with pytest.raises(AssertionError, match="labels"):
        draw_multiple_labels(
            image,
            [(10, 20, 30, 40), (50, 20, 70, 40)],
            ["cat"],
        )
