#!/usr/bin/env python3
"""Compare the control in the native screenshots, excluding the browser chrome."""

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops


PANEL = (228, 19, 154)


def control_panel(path):
    with Image.open(path) as image:
        rgb = image.convert("RGB")
    width, _ = rgb.size
    points = [
        (index % width, index // width)
        for index, color in enumerate(rgb.getdata())
        if all(abs(actual - expected) <= 3 for actual, expected in zip(color, PANEL))
    ]
    if not points:
        raise ValueError(f"no colored fixture panel in {path}")
    xs, ys = zip(*points)
    bounds = min(xs), min(ys), max(xs) + 1, max(ys) + 1
    if bounds[2] - bounds[0] < 300 or bounds[3] - bounds[1] < 74:
        raise ValueError(f"incomplete fixture panel in {path}: {bounds}")
    return rgb.crop(bounds)


def unequal_pixels(a, b):
    if a.size != b.size:
        raise ValueError(f"fixture crops have different sizes: {a.size}, {b.size}")
    return sum(pixel != (0, 0, 0) for pixel in ImageChops.difference(a, b).getdata())


out = Path(sys.argv[1])
labels = ("wrapped", "reference", "different")
panels = {name: control_panel(out / f"{name}.png") for name in labels}
for name, panel in panels.items():
    panel.save(out / f"{name}-control.png")
wrapped_difference = unequal_pixels(panels["wrapped"], panels["reference"])
different_difference = unequal_pixels(panels["different"], panels["reference"])
result = {
    "pass": wrapped_difference == 0 and different_difference > 0,
    "wrapped_vs_direct_different_pixels": wrapped_difference,
    "negative_control_different_pixels": different_difference,
    "panel_size": panels["wrapped"].size,
}
report = json.dumps(result)
print(report)
(out / "pixel-results.json").write_text(report + "\n")
sys.exit(0 if result["pass"] else 1)
