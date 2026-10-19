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
