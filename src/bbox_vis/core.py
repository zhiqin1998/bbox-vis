from collections.abc import Sequence
from itertools import cycle, islice

from PIL import Image, ImageDraw, ImageFont

from ._colors import _DEFAULT_COLORS, _get_text_color, _validate_color
from ._utils import _convert_bbox, _get_font_size, _get_thickness, _validate_bbox


def draw_bbox(
    image: Image.Image,
    bbox: Sequence[float | int],
    color: tuple[int, int, int] | None = None,
    bbox_format: str = "xyxy",
    bbox_is_normalized: bool = False,
    label: str | None = None,
    label_top: bool = True,
    label_color: tuple[int, int, int] | None = None,
    thickness: int | None = None,
    font: ImageFont.ImageFont | None = None,
    font_size: int | None = None,
    label_pad: int = 2,
) -> Image.Image:
    """Draw a bounding box on an image.

    Args:
        image: Image as a PIL Image object
        bbox: [x_min, y_min, x_max, y_max] coordinates
        color: RGB color for the bounding box, use default color palette if None
        bbox_format: Format of the bounding box, one of 'xyxy', 'xywh', or 'cxcywh'
        bbox_is_normalized: Whether the bounding box coordinates are normalized (0 to 1)
        label: Optional label to display on the bounding box, if None, no label will be displayed
        label_top: Whether the label should be displayed at the top of the bounding box or at the bottom, default is True (top)
        label_color: RGB color for the label text, if None, it will be automatically determined based on the box color
        thickness: Thickness of the bounding box lines, if None, it will be automatically determined based on the image size
        font: Font to use for the label text, ImageFont object, if None, the default PIL font will be used
        font_size: Size of the font, if None, it will be automatically determined based on the image size
        label_pad: Padding of the label, default is 2

    Returns:
        Image with the bounding box (and label) drawn on it as a PIL Image object

    """
    image = image.copy()
    draw = ImageDraw.Draw(image)
    bbox = _convert_bbox(
        bbox,
        from_format=bbox_format,
        to_format="xyxy",
        is_normalized=bbox_is_normalized,
        img_size=image.size,
    )
    if color is None:
        color = _DEFAULT_COLORS[0]

    _validate_bbox(bbox)
    _validate_color(color)
    if thickness is None:
        thickness = _get_thickness(image.size)
    draw.rectangle(bbox, width=thickness, outline=color)

    if label is not None:
        image = draw_label(
            image,
            bbox,
            label,
            color,
            label_color,
            label_top,
            thickness,
            font,
            font_size,
            pad=label_pad,
        )

    return image


def draw_label(
    image: Image.Image,
    bbox: Sequence[float | int],
    label: str,
    fill_color: tuple[int, int, int] | None = None,
    label_color: tuple[int, int, int] | None = None,
    label_top: bool = True,
    thickness: int | None = None,
    font: ImageFont.ImageFont | None = None,
    font_size: int | None = None,
    pad: int = 2,
    bbox_format: str = "xyxy",
    bbox_is_normalized: bool = False,
) -> Image.Image:
    """Draw a label on an image.

    Args:
        image: Image as a PIL Image object
        bbox: [x_min, y_min, x_max, y_max] coordinates
        label: Label to display on the bounding box
        fill_color: RGB color for the label box, use default color palette if None
        label_color: RGB color for the label text, if None, it will be automatically determined based on the box color
        label_top: Whether the label should be displayed at the top of the bounding box or at the bottom, default is True (top)
        thickness: Thickness of the bounding box lines (use for padding calculations), if None, it will be automatically determined based on the image size
        font: Font to use for the label text, ImageFont object, if None, the default PIL font will be used
        font_size: Size of the font, if None, it will be automatically determined based on the image size
        pad: Padding of the label, default is 2
        bbox_format: Format of the bounding box coordinates, default is "xyxy"
        bbox_is_normalized: Whether the bounding box coordinates are normalized (0 to 1), default is False

    Returns:
        Image with the label drawn on it as a PIL Image object

    """
    image = image.copy()
    draw = ImageDraw.Draw(image)

    if thickness is None:
        thickness = _get_thickness(image.size)
    if font is None:
        if font_size is None:
            font_size = _get_font_size(image.size)
        font = ImageFont.load_default(size=font_size)
    if fill_color is None:
        fill_color = _DEFAULT_COLORS[0]
    if label_color is None:
        label_color = _get_text_color(fill_color)

    bbox = _convert_bbox(
        bbox,
        from_format=bbox_format,
        to_format="xyxy",
        is_normalized=bbox_is_normalized,
        img_size=image.size,
    )
    _validate_color(label_color)
    _validate_color(fill_color)
    _validate_bbox(bbox)

    tbox_width, tbox_height = font.getbbox(label)[2:4]
    pad = pad * 2
    tbox_width, tbox_height = tbox_width + pad, tbox_height + pad
    pad += thickness
    x_min, y_min, _, _ = bbox
    if (
        x_min + tbox_width > image.size[0]
    ):  # check if label extend beyond right side of image
        x_min = image.size[0] - tbox_width
    x_min = max(0, x_min)  # check if label extend beyond left side of image
    y_min = max(0, y_min)  # check if label extend beyond top side of image
    if label_top:
        is_fit = y_min >= tbox_height  # label on top fits within image

        draw.rectangle(
            (
                x_min,
                y_min - tbox_height if is_fit else 0,
                x_min + tbox_width + 1,
                y_min + 1 if is_fit else tbox_height + 1,
            ),
            fill=fill_color,
        )
        draw.text(
            (
                x_min + pad // 2,
                y_min - tbox_height + pad // 2 - 1 if is_fit else max(pad // 2 - 1, 0),
            ),
            label,
            fill=label_color,
            font=font,
        )
    else:
        draw.rectangle(
            (x_min, y_min, x_min + tbox_width + 1, y_min + tbox_height + 1),
            fill=fill_color,
        )
        draw.text(
            (x_min + pad // 2, y_min + pad // 2 - 1), label, fill=label_color, font=font
        )

    return image


def draw_multiple_bboxes(
    image: Image.Image,
    bboxes: Sequence[Sequence[float | int]],
    colors: Sequence[tuple[int, int, int]] | tuple[int, int, int] | None = None,
    bbox_format: str = "xyxy",
    bbox_is_normalized: bool = False,
    labels: Sequence[str] | None = None,
    label_top: bool = True,
    label_colors: Sequence[tuple[int, int, int]] | tuple[int, int, int] | None = None,
    thickness: int | None = None,
    font: ImageFont.ImageFont | None = None,
    font_size: int | None = None,
    label_pad: int = 2,
) -> Image.Image:
    """Draw multiple bounding boxes on an image.

    Args:
        image: Image as a PIL Image object
        bboxes: List of bounding boxes, each as a list of [x_min, y_min, x_max, y_max] coordinates
        colors: List of RGB colors for the bounding boxes, use default color palette if None
        bbox_format: Format of the bounding boxes, one of 'xyxy', 'xywh', or 'cxcywh'
        bbox_is_normalized: Whether the bounding box coordinates are normalized (0 to 1)
        labels: Optional list of labels to display on the bounding boxes, if None, no labels will be displayed
        label_top: Whether the labels should be displayed at the top of the bounding boxes or at the bottom, default is True (top)
        label_colors: List of RGB colors for the label, if None, they will be automatically determined based on the box colors
        thickness: Thickness of the bounding box lines, if None, it will be automatically determined based on the image size
        font: Font to use for the label, as an ImageFont object, if None, the default PIL font will be used
        font_size: Size of the font, if None, it will be automatically determined based on the image size
        label_pad: Padding of the label, default is 2

    Returns:
        Image with the bounding boxes (and labels) drawn on it as a PIL Image object

    """
    if isinstance(colors, Sequence) and not isinstance(colors[0], Sequence):
        colors = [colors] * len(bboxes)
    if isinstance(label_colors, Sequence) and not isinstance(label_colors[0], Sequence):
        label_colors = [label_colors] * len(bboxes)
    if colors is None:
        colors = list(islice(cycle(_DEFAULT_COLORS), len(bboxes)))
    if label_colors is None:
        label_colors = [None] * len(bboxes)
    if labels is None:
        labels = [None] * len(bboxes)
    assert len(colors) == len(bboxes), "Length of colors must match length of bboxes"
    assert len(label_colors) == len(bboxes), (
        "Length of label_colors must match length of bboxes"
    )
    assert len(labels) == len(bboxes), "Length of labels must match length of bboxes"

    for bbox, color, label_color, label in zip(
        bboxes, colors, label_colors, labels, strict=True
    ):
        image = draw_bbox(
            image,
            bbox,
            color=color,
            bbox_format=bbox_format,
            bbox_is_normalized=bbox_is_normalized,
            label=label,
            label_top=label_top,
            label_color=label_color,
            label_pad=label_pad,
            thickness=thickness,
            font=font,
            font_size=font_size,
        )
    return image


def draw_multiple_labels(
    image: Image.Image,
    bboxes: Sequence[Sequence[float | int]],
    labels: Sequence[str],
    fill_colors: Sequence[tuple[int, int, int]] | tuple[int, int, int] | None = None,
    label_colors: Sequence[tuple[int, int, int]] | tuple[int, int, int] | None = None,
    label_top: bool = True,
    font: ImageFont.ImageFont | None = None,
    font_size: int | None = None,
    pad: int = 2,
    bbox_format: str = "xyxy",
    bbox_is_normalized: bool = False,
) -> Image.Image:
    """Draw a label on an image.

    Args:
        image: Image as a PIL Image object
        bboxes: List of [x_min, y_min, x_max, y_max] coordinates
        labels: List of labels to display on the bounding boxes
        fill_colors: RGB colors for the label boxes, use default color palette if None
        label_colors: RGB colors for the label text, if None, it will be automatically determined based on the box colors
        label_top: Whether the label should be displayed at the top of the bounding box or at the bottom, default is True (top)
        font: Font to use for the label text, ImageFont object, if None, the default PIL font will be used
        font_size: Size of the font, if None, it will be automatically determined based on the image size
        pad: Padding of the label, default is 2
        bbox_format: Format of the bounding box coordinates, default is "xyxy"
        bbox_is_normalized: Whether the bounding box coordinates are normalized (0 to 1),

    Returns:
        Image with the labels drawn on it as a PIL Image object

    """
    if isinstance(fill_colors, Sequence) and not isinstance(fill_colors[0], Sequence):
        fill_colors = [fill_colors] * len(bboxes)
    if isinstance(label_colors, Sequence) and not isinstance(label_colors[0], Sequence):
        label_colors = [label_colors] * len(bboxes)
    if fill_colors is None:
        fill_colors = list(islice(cycle(_DEFAULT_COLORS), len(bboxes)))
    if label_colors is None:
        label_colors = [None] * len(bboxes)

    assert len(fill_colors) == len(bboxes), (
        "Length of fill_colors must match length of bboxes"
    )
    assert len(label_colors) == len(bboxes), (
        "Length of label_colors must match length of bboxes"
    )
    assert len(labels) == len(bboxes), "Length of labels must match length of bboxes"

    for bbox, label, fill_color, label_color in zip(
        bboxes, labels, fill_colors, label_colors, strict=True
    ):
        image = draw_label(
            image,
            bbox,
            label,
            fill_color=fill_color,
            label_color=label_color,
            label_top=label_top,
            font=font,
            font_size=font_size,
            pad=pad,
            bbox_format=bbox_format,
            bbox_is_normalized=bbox_is_normalized,
        )

    return image
