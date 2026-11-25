"""Report whole-frame RGB changes, region changes and native box measurements."""
import hashlib
import json
import math
from pathlib import Path
import sys

from PIL import Image, ImageChops, ImageStat

site, output, *roles = sys.argv[1:]
out = Path(output)
fixture = json.loads((out / "fixture.json").read_text())


def pixel_stats(a, b):
    delta = ImageChops.difference(a, b)
    r, g, blue = delta.split()
    mask = ImageChops.lighter(ImageChops.lighter(r, g), blue)
    return {
        "changed_pixels": a.width * a.height - mask.histogram()[0],
        "bbox": mask.getbbox(),
        "mean_abs_rgb": round(sum(ImageStat.Stat(delta).mean) / 3, 5),
    }


def color_bounds(image, color, rect):
    x0, y0, x1, y1 = rect
    points = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if image.getpixel((x, y)) == color]
    if not points:
        return None
    x, y = zip(*points)
    return [min(x), min(y), max(x)+1, max(y)+1]


def gov_geometry(image):
    # Same search-submit background and icon colors as the exact transform replay.
    button = color_bounds(image, (210, 226, 241), fixture["regions"]["search_submit"])
    return {"button": button, "icon": color_bounds(image, (29, 112, 184), button) if button else None}


def read_frame(role, path):
    image = Image.open(path).convert("RGB")
    assert image.size == (1280, 735) and image.getbbox() is not None, role
    assert any(lo != hi for lo, hi in image.getextrema()), (role, "uniform frame")
    return image


def layout_summary(role, image):
    role_out = out / role
    layout = json.loads((role_out / "geometry.json").read_text())
    assert (layout["width"], layout["height"]) == image.size
    boxes = layout["boxes"]
    assert boxes and all(len(box) == 5 and all(math.isfinite(x) for x in box) for box in boxes), role
    visible = sum(w > 0 and h > 0 and x < image.width and y < image.height and x + w > 0 and y + h > 0
                  for _, x, y, w, h in boxes)
    assert visible, role
    runs = layout["glyphRuns"]
    top_runs = [{"text": run["text"], "size": run["size"],
                 "xy": [round(run["glyphs"][0][1], 2), round(run["glyphs"][0][2], 2)]}
                for run in runs if run.get("glyphs") and 0 <= run["glyphs"][0][2] < image.height
                and isinstance(run.get("text"), str) and run["text"].strip()]
    result = json.loads((role_out / "result.json").read_text())
    log = (role_out / "run.log").read_text()
    records = [json.loads(line) for line in log.splitlines() if line.startswith('{"type":"realpages-replay')]
    summaries = [r for r in records if r["type"] == "realpages-replay"]
    assert len(summaries) == 1 and summaries[0]["hits"] > 0, (role, summaries)
    assert hashlib.sha256(image.tobytes()).hexdigest() == result["sha"], role
    return {
        "pixel_sha256": result["sha"],
        "visible_boxes": visible,
        "boxes": len(boxes),
        "links": len(layout["links"]),
        "largest_visible_text": sorted(top_runs, key=lambda r: -r["size"])[:16],
        "replay": summaries[0],
        "missing_urls": sorted({r["url"] for r in records if r["type"] == "realpages-replay-miss"}),
        "render": result,
    }


chrome = read_frame("chrome", out / "chrome.png")
frames = {role: read_frame(role, out / role / "page.png") for role in roles}
summary = {"site": site, "fixture": fixture["id"], "viewport": chrome.size, "frames": {}, "comparisons": {}}
for role, frame in frames.items():
    details = layout_summary(role, frame)
    summary["frames"][role] = details
    for region, coords in fixture["regions"].items():
        frame.crop(coords).save(out / role / (region + ".png"))
for region, coords in fixture["regions"].items():
    chrome.crop(coords).save(out / ("chrome-" + region + ".png"))
if site == "govuk":
    summary["search_submit_geometry"] = {role: gov_geometry(img) for role, img in {"chrome": chrome, **frames}.items()}
comparisons = {(role, "chrome"): (frame, chrome) for role, frame in frames.items()}
if "successor" in frames:
    comparisons[("successor", "baseline")] = (frames["successor"], frames["baseline"])
for (a, b), (one, two) in comparisons.items():
    summary["comparisons"][f"{a}_vs_{b}"] = {
        "page": pixel_stats(one, two),
        **{region: pixel_stats(one.crop(coords), two.crop(coords)) for region, coords in fixture["regions"].items()},
    }
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary["comparisons"], indent=2))
