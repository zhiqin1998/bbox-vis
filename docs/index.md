# bbox-vis

**bbox-vis** is a small Python library for drawing bounding boxes and labels on [Pillow](https://python-pillow.org/) images.

It is designed for computer vision workflows where you want to inspect detections quickly without changing the source image.
Every drawing function returns a copy of the input image.

## Highlights

- Draw one or many bounding boxes.
- Add labels above or below boxes.
- Accept `xyxy`, `xywh`, and `cxcywh` coordinates.
- Accept normalized coordinates in the `[0, 1]` range.
- Use explicit RGB colors or the built-in color palette.
- Automatically choose a contrasting label text color.

## Quick example

```python
from PIL import Image

from bbox_vis import draw_bbox

image = Image.new("RGB", (400, 300), "white")
annotated = draw_bbox(
    image,
    (50, 40, 250, 200),
    color=(255, 0, 0),
    label="object",
)
annotated.save("annotated.png")
```

Continue with the [installation instructions](installation.md), see the [usage guide](usage.md), or browse the [API reference](api.md).
