# bbox-vis

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

A simple bounding box visualization tool based on Pillow

Read the [documentation](https://bbox-vis.readthedocs.io/) for installation, usage examples, and the API reference.

## Installation

```bash
python -m pip install bbox_vis
```

From source:
```bash
git clone https://github.com/zhiqin1998/bbox-vis
cd bbox-vis
python -m pip install .
```

## Usage

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

See the [usage guide](https://bbox-vis.readthedocs.io/usage/) for more examples, including multiple boxes and normalized coordinates.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/zhiqin1998/bbox-vis/workflows/CI/badge.svg
[actions-link]:             https://github.com/zhiqin1998/bbox-vis/actions
[pypi-link]:                https://pypi.org/project/bbox-vis/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/bbox-vis
[pypi-version]:             https://img.shields.io/pypi/v/bbox-vis
<!-- prettier-ignore-end -->
