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
RED, GREEN, BLUE = (183, 50, 33), (26, 177, 71), (35, 81, 186)
CASES = {
    "block": "",
    "column": ".flow{display:flex;flex-direction:column}.media{flex:none}",
    "percentage-column": ".wrap,.promo,.flow{height:100%}.flow{display:flex;flex-direction:column}.media{flex:none}",
    "grid": ".list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-areas:'large large small small' 'large large foot foot';gap:8px}.large{grid-area:large}.small{grid-area:small}.foot{grid-area:foot}",
}
CASES["grid-percentage-column"] = CASES["grid"] + CASES["percentage-column"]
STYLE = """
html, body {margin: 0; padding: 0; background: white;}
.list {width: 648px; margin: 0; padding: 0; list-style: none;}
.large {width: 320px;}
.wrap {box-sizing: border-box; padding-bottom: 8px;}
.promo {position: relative;}
.inner {position: relative; overflow: hidden;}
.image-wrap {overflow: hidden; transform: translateZ(0) scale(1);}
.placeholder {display: block; position: relative; padding-bottom: 56.25%; background: rgb(238, 238, 238);}
img {display: block; width: 100%; height: 100%; position: absolute; inset: 0; overflow: hidden; object-fit: cover;}
.marker {height: 12px; background: rgb(26, 177, 71);}
.end {height: 10px; background: rgb(35, 81, 186);}
.small,.foot {min-height: 24px;}
"""
MARKUP = """
<ul class="list"><li class="large"><div class="wrap"><div class="promo"><div class="flow">
  <div class="media"><div class="inner"><div class="image-wrap"><span class="placeholder"><picture>
    <img width="240" height="135" src="image.png" alt="">
  </picture></span></div></div></div>
  <div class="marker"></div>
</div></div></div></li><li class="small"></li><li class="foot"></li></ul>
<div class="end"></div>
"""


def measure(path):
    with Image.open(path) as png:
        rgb = png.convert("RGB")
        assert rgb.size == (WIDTH, HEIGHT), rgb.size
        rows = collections.defaultdict(list)
        for y in range(rgb.height):
            pixel = rgb.getpixel((16, y))
            if pixel in (RED, GREEN, BLUE):
                rows[pixel].append(y)
        return {
            name: [min(rows[color]), max(rows[color])] if rows[color] else None
            for name, color in (("image", RED), ("below_image", GREEN), ("below_grid", BLUE))
        }


def main():
    fixtures = OUT / "fixtures"
    fixtures.mkdir()
    Image.new("RGB", (240, 135), RED).save(fixtures / "image.png")
    for name, rules in CASES.items():
        (fixtures / f"{name}.html").write_text("<!doctype html><meta charset=utf-8><style>" + STYLE + rules + "</style>" + MARKUP)
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
    print("| Fixture | Chrome image, marker, end | Foafnaut image, marker, end |")
    print("| --- | --- | --- |")
    for name in CASES:
        reference = measure(chrome / f"{name}.png")
        actual = measure(OUT / "foafnaut" / f"{name}.png")
        assert reference["image"] == [0, 179] and reference["below_image"] == [180, 191], (name, reference)
        result[name] = {"chrome": reference, "foafnaut": actual}
        print(f"| {name} | {list(reference.values())} | {list(actual.values())} |")
    (OUT / "geometry.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
