"""
bbox-vis: A simple bounding box visualization tool based on Pillow
"""

from __future__ import annotations

from importlib.metadata import version

from .core import draw_bbox, draw_label, draw_multiple_bboxes, draw_multiple_labels

__version__ = version(__name__)

__all__ = (
    "__version__",
    "draw_bbox",
    "draw_label",
    "draw_multiple_bboxes",
    "draw_multiple_labels",
)

__author__ = "Zhi Qin Tan"
__email__ = "zhiqin1998@hotmail.com"
