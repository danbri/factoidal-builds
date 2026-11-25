"""Measure the authored invalid and valid border colors in a stable page crop."""

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops


PANEL = (228, 19, 154)
INVALID = (213, 43, 53)
VALID = (17, 119, 66)


def near(pixel, expected):
    return all(abs(a - b) <= 3 for a, b in zip(pixel, expected))


def read_panel(path):
    with Image.open(path) as image:
        rgb = image.convert("RGB")
    points = [
        (index % rgb.width, index // rgb.width)
        for index, color in enumerate(rgb.getdata())
        if near(color, PANEL)
    ]
    if not points:
        raise ValueError(f"fixture panel absent in {path}")
    xs, ys = zip(*points)
    bounds = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    if bounds[2] - bounds[0] != 336 or bounds[3] - bounds[1] != 140:
        raise ValueError(f"unexpected fixture panel bounds in {path}: {bounds}")
    return bounds, rgb.crop(bounds)


def count(image, color):
    return sum(near(pixel, color) for pixel in image.getdata())


out = Path(sys.argv[1])
before_bounds, before = read_panel(out / "before.png")
after_bounds, after = read_panel(out / "after.png")
before.save(out / "before-control.png")
after.save(out / "after-control.png")
changed = sum(pixel != (0, 0, 0) for pixel in ImageChops.difference(before, after).getdata())
border_transition = sum(
    near(old, INVALID) and near(new, VALID)
    for old, new in zip(before.getdata(), after.getdata())
)
result = {
    "pass": before_bounds == after_bounds and border_transition >= 800
    and count(before, VALID) == 0 and count(after, INVALID) == 0,
    "bounds": {"before": before_bounds, "after": after_bounds},
    "different_pixels": changed,
    "red_to_green_pixels": border_transition,
    "before": {"invalid_red_pixels": count(before, INVALID), "valid_green_pixels": count(before, VALID)},
    "after": {"invalid_red_pixels": count(after, INVALID), "valid_green_pixels": count(after, VALID)},
}
report = json.dumps(result)
print(report)
(out / "pixel-results.json").write_text(report + "\n")
sys.exit(0 if result["pass"] else 1)
