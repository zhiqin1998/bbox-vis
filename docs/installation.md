# Installation

## From PyPI

Install the latest released version with pip:

```bash
python -m pip install bbox-vis
```

The package supports Python 3.10 and later. Pillow is installed automatically as a runtime dependency.

## From source

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/zhiqin1998/bbox-vis.git
cd bbox-vis
python -m pip install -e .
```

## Development setup

The project uses [uv](https://docs.astral.sh/uv/) for reproducible development environments:

```bash
uv sync
uv run pytest
```

To build these docs locally:

```bash
uv run --group docs mkdocs serve
```
