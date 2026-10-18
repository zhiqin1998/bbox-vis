# Contributing to bbox-vis

See the [Scientific Python Developer Guide][spc-dev-intro] for a detailed
description of best practices for developing scientific packages.

[spc-dev-intro]: https://learn.scientific-python.org/development/

## Prerequisites

Install [uv](https://docs.astral.sh/uv/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

```bash
git clone https://github.com/zhiqin1998/bbox-vis
cd bbox-vis
uv sync
```

This installs the package in editable mode along with all dev dependencies, and
creates a `uv.lock` lockfile for reproducible installs.

## Pre-commit

Pre-commit runs the following checks on each commit:

- Code quality checks (trailing whitespace, merge conflicts, large files, etc.)
- Linting and auto-fixing with [ruff](https://docs.astral.sh/ruff/)
- Code formatting with [ruff format](https://docs.astral.sh/ruff/formatter/)

Install the pre-commit hooks so these run automatically on each commit:

```bash
uv run pre-commit install
```

You can also run them manually:

```bash
uv run pre-commit run --all-files
```

## Testing
Recommend to run all tests before committing

```bash
uv run pytest
```

With coverage:

```bash
uv run pytest --cov=bbox_vis
```

## Type checking

```bash
uv run ty check
```

## Publishing documentation

Documentation is built and published by the `CD` workflow when a release is published, or when the workflow is
manually dispatched. The workflow first runs a strict MkDocs build and then
triggers a Read the Docs build through its API.

To configure this workflow, create a Read the Docs API token and add it to the
repository as an Actions secret named `RTD_API_TOKEN`. The Read the Docs
project slug must be `bbox-vis`.

## Building

To verify the package builds correctly:

```bash
uv build
```

## Adding dependencies

- Runtime: `uv add <package>`
- Dev: `uv add --group dev <package>`
- Test: `uv add --group test <package>`
- Lint: `uv add --group lint <package>`

## About `uv.lock`

The `uv.lock` file is committed to the repository to ensure reproducible
installs. CI uses `uv sync --locked` to verify the lockfile is up to date. If
you change dependencies, run `uv lock` to update it.
