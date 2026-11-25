import collections
import functools
import http.server
import json
from pathlib import Path
import subprocess
import threading

from PIL import Image


OUT = Path("out").resolve()
WIDTH, HEIGHT = 800, 630
RED, GREEN = (183, 50, 33), (26, 177, 71)
GRID = ".list{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}"
COLUMN = ".flow{display:flex;flex-direction:column}.media{flex:none}"
CASES = {
    "block-control": (".card{width:320px}", [(16, 180)]),
    "grid-explicit-width-control": (GRID + ".card{width:320px}", [(16, 180), (336, 180)]),
    "grid-equal-tracks": (GRID, [(16, 180), (336, 180)]),
    "grid-border-box": (
        GRID + ".card{width:320px;box-sizing:border-box;margin-left:5%;padding-inline:10%}",
        [(72, 144), (392, 144)],
    ),
    "grid-column": (GRID + COLUMN, [(16, 180), (336, 180)]),
    "grid-unequal-tracks": (
        ".list{width:576px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr)}",
        [(16, 108), (208, 216)],
    ),
}
STYLE = """
html, body {margin: 0; padding: 0; background: white;}
.list {width: 640px;}
.placeholder {display: block; position: relative; padding-bottom: 56.25%;}
img {display: block; width: 100%; height: 100%; position: absolute; inset: 0; object-fit: cover;}
.marker {height: 12px; background: rgb(26, 177, 71);}
"""
CARD = """
<div class="card"><div class="flow">
  <div class="media"><span class="placeholder"><img width="240" height="135" src="image.png" alt=""></span></div>
  <div class="marker"></div>
</div></div>
"""


def measure(path, x):
    with Image.open(path) as png:
        rgb = png.convert("RGB")
        assert rgb.size == (WIDTH, HEIGHT), rgb.size
        rows = collections.defaultdict(list)
        for y in range(rgb.height):
            pixel = rgb.getpixel((x, y))
            if pixel in (RED, GREEN):
                rows[pixel].append(y)
        return {
            name: [min(rows[color]), max(rows[color])] if rows[color] else None
            for name, color in (("image", RED), ("below_image", GREEN))
        }


def main():
    fixtures = OUT / "fixtures"
    fixtures.mkdir()
    Image.new("RGB", (240, 135), RED).save(fixtures / "image.png")
    for name, (rules, samples) in CASES.items():
        (fixtures / f"{name}.html").write_text("<!doctype html><meta charset=utf-8><style>" + STYLE + rules + "</style>" + "<div class=list>" + CARD * len(samples) + "</div>")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=fixtures)
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        origin = f"http://127.0.0.1:{server.server_port}"
        jobs = [{"url": f"{origin}/{name}.html", "width": WIDTH, "height": HEIGHT, "file": f"{name}.png"} for name in CASES]
        (OUT / "jobs.jsonl").write_text("".join(json.dumps(job) + "\n" for job in jobs))
        with (OUT / "foafnaut.log").open("w") as log:
            subprocess.run(["deno", "run", "-A", "--unstable-ffi", "core/tests/browser-wpt/reftest-render.ts",
                            "--native-engine", "engine/libweb-render.so", "--list", str(OUT / "jobs.jsonl"),
                            "--out", str(OUT / "foafnaut")], check=True, stdout=log, stderr=subprocess.STDOUT, timeout=150)
        chrome = OUT / "chrome"
        chrome.mkdir()
        for name in CASES:
            with (chrome / f"{name}.log").open("w") as log:
                subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                                "--force-device-scale-factor=1", f"--window-size={WIDTH},{HEIGHT}", "--hide-scrollbars",
                                f"--screenshot={chrome / (name + '.png')}", f"{origin}/{name}.html"],
                               check=True, stdout=log, stderr=subprocess.STDOUT, timeout=45)
        server.shutdown()
    result = {}
    print("| Fixture | Sample x | Chrome image and marker | Foafnaut image and marker |")
    print("| --- | --- | --- | --- |")
    for name, (_, samples) in CASES.items():
        result[name] = []
        for x, height in samples:
            reference = measure(chrome / f"{name}.png", x)
            actual = measure(OUT / "foafnaut" / f"{name}.png", x)
            expected = {"image": [0, height - 1], "below_image": [height, height + 11]}
            assert reference == expected, (name, x, reference)
            result[name].append({"x": x, "chrome": reference, "foafnaut": actual})
            print(f"| {name} | {x} | {list(reference.values())} | {list(actual.values())} |")
    (OUT / "geometry.json").write_text(json.dumps(result, indent=2) + "\n")
    for name in CASES:
        assert all(sample["chrome"] == sample["foafnaut"] for sample in result[name]), name


if __name__ == "__main__":
    main()
