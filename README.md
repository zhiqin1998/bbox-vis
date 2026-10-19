# bbox-viz

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

A simple bounding box visualization tool based on Pillow

Read the [documentation](https://bbox-viz.readthedocs.io/) for installation, usage examples, and the API reference.

## Installation

```bash
python -m pip install bbox_viz
```

From source:
```bash
git clone https://github.com/zhiqin1998/bbox-viz
cd bbox-viz
python -m pip install .
```

## Usage

```python
from PIL import Image

from bbox_viz import draw_bbox

image = Image.new("RGB", (400, 300), "white")
annotated = draw_bbox(
    image,
    (50, 40, 250, 200),
    color=(255, 0, 0),
    label="object",
)
annotated.save("annotated.png")
```

See the [usage guide](https://bbox-viz.readthedocs.io/en/latest/usage/) for more examples, including multiple boxes and normalized coordinates.

## Example with a public dataset

The example below draws annotations from the [COCO 2017 validation
set](https://cocodataset.org/#download), using image `397133`
(`000000397133.jpg`). COCO stores boxes as `(x, y, width, height)`, so pass
`bbox_format="xywh"`:

```python
from pathlib import Path

from PIL import Image

from bbox_viz import draw_multiple_bboxes

image = Image.open(Path("docs/assets/coco-397133.jpg"))

# Ground-truth COCO annotations for image 397133.
bboxes = [
    (217.62, 240.54, 38.99, 57.75),    # bottle
    (1.00, 240.24, 346.63, 186.76),    # dining table
    (388.66, 69.92, 109.41, 277.62),   # person
    (135.57, 249.43, 22.32, 28.79),    # knife
]

annotated = draw_multiple_bboxes(
    image,
    bboxes,
    bbox_format="xywh",
    labels=["bottle", "dining table", "person", "knife"],
    thickness=3,
)
annotated.save("coco-397133-annotated.jpg")
```

![Original COCO image](docs/assets/coco-397133.jpg)

*Original image from COCO image `397133`.*

![COCO image with bounding boxes](docs/assets/coco-397133-annotated.jpg)

*The same image rendered with `bbox-viz` and the COCO ground-truth boxes.*

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/zhiqin1998/bbox-viz/workflows/CI/badge.svg
[actions-link]:             https://github.com/zhiqin1998/bbox-viz/actions
[pypi-link]:                https://pypi.org/project/bbox-viz/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/bbox-viz
[pypi-version]:             https://img.shields.io/pypi/v/bbox-viz
<!-- prettier-ignore-end -->
