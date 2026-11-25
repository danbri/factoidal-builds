import functools
import http.server
import json
from pathlib import Path
import re
import subprocess
import threading
from zipfile import ZipFile

from PIL import Image, ImageChops

OUT = Path("out").resolve()
WIDTH, HEIGHT = 800, 640
STYLE = """
html,body {margin:0;background:white;color:black;font-size:16px}
.fixture {margin:12px;width:650px}
.mw-logo {display:flex;height:100%;align-items:center}
.mw-logo-container {float:left;max-width:120px}
.mw-logo-container img {width:100%}
.mw-logo-wordmark {display:block;margin:0 auto}
.mw-logo-tagline {display:block;margin:5px auto 0}
.vector-header-start {display:flex;align-items:center;gap:20px}
.mw-header {display:grid;grid-template-columns:200px 1fr;grid-template-areas:"headerStart headerEnd";height:50px}
.vector-header-start {grid-area:headerStart}
.vector-header-end {grid-area:headerEnd}
.menu {flex:none;width:32px;height:32px}
"""
WORDMARK = '<img class="mw-logo-wordmark" src="wordmark.svg" style="width:8.75em;height:1.375em" alt="Wikipedia">'
TAGLINE = '<img class="mw-logo-tagline" src="tagline.svg" width="140" height="11" style="width:8.75em;height:.6875em" alt="The Free Encyclopedia">'
LOGO = '<a href="page" class="mw-logo"><span class="mw-logo-container">' + WORDMARK + TAGLINE + '</span></a>'
CASES = {
    "wordmark-direct": '<img src="wordmark.svg" width="140" height="22" alt="">',
    "wordmark-unclipped": '<img src="wordmark-unclipped.svg" width="140" height="22" alt="">',
    "tagline-direct": '<img src="tagline.svg" width="140" height="11" alt="">',
    "tagline-unclipped": '<img src="tagline-unclipped.svg" width="140" height="11" alt="">',
    "wordmark-em": WORDMARK,
    "simple-flex": LOGO,
    "nested-flex": '<div class="vector-header-start"><span class="menu"></span>' + LOGO + '</div>',
    "grid-header": '<header class="mw-header"><div class="vector-header-start"><span class="menu"></span>' +
                   LOGO + '</div><div class="vector-header-end"></div></header>',
}


def measure(path):
    with Image.open(path) as image:
        crop = image.convert("RGB").crop((0, 0, 320, 100))
        diff = ImageChops.difference(crop, Image.new("RGB", crop.size, (255, 255, 255)))
        ink = [(x, y) for y in range(crop.height) for x in range(crop.width) if max(diff.getpixel((x, y))) > 64]
        return {
            "inkPixels": len(ink),
            "inkBounds": [min(x for x, y in ink), min(y for x, y in ink),
                          max(x for x, y in ink), max(y for x, y in ink)] if ink else None,
        }


def main():
    fixtures = OUT / "fixtures"
    fixtures.mkdir()
    capture = next(Path("capture").rglob("desktop-wikipedia-www-20261124.zip"))
    with ZipFile(capture) as archive:
        entries = json.loads(archive.read("manifest.json"))["entries"]
        for name in ("wordmark", "tagline"):
            entry, = (e for e in entries if e["url"].endswith(f"wikipedia-{name}-en-25.svg"))
            svg = archive.read(entry["body"]).decode()
            reduced, edits = re.subn(r' clip-path="url\(#[^"]+\)"', "", svg)
            assert edits == 1, (name, edits)
            (fixtures / f"{name}.svg").write_text(svg)
            (fixtures / f"{name}-unclipped.svg").write_text(reduced)
    for name, markup in CASES.items():
        (fixtures / f"{name}.html").write_text(
            '<!doctype html><meta charset="utf-8"><style>' + STYLE +
            "</style><div class='fixture'>" + markup + "</div>"
        )

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=fixtures)
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        origin = f"http://127.0.0.1:{server.server_port}"
        jobs = [{"url": f"{origin}/{name}.html", "width": WIDTH, "height": HEIGHT, "file": f"{name}.png"} for name in CASES]
        (OUT / "jobs.jsonl").write_text("".join(json.dumps(job) + "\n" for job in jobs))
        with (OUT / "foafnaut.log").open("w") as log:
            subprocess.run(
                ["deno", "run", "-A", "--unstable-ffi", "core/tests/browser-wpt/reftest-render.ts",
                 "--native-engine", "engine/libweb-render.so", "--list", str(OUT / "jobs.jsonl"),
                 "--out", str(OUT / "foafnaut")], check=True, stdout=log, stderr=subprocess.STDOUT, timeout=150,
            )
        chrome = OUT / "chrome"
        chrome.mkdir()
        for name in CASES:
            with (chrome / f"{name}.log").open("w") as log:
                subprocess.run(
                    ["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                     "--force-device-scale-factor=1", f"--window-size={WIDTH},{HEIGHT}", "--hide-scrollbars",
                     f"--screenshot={chrome / (name + '.png')}", f"{origin}/{name}.html"],
                    check=True, stdout=log, stderr=subprocess.STDOUT, timeout=45,
                )
        server.shutdown()
    result = {}
    for name in CASES:
        reference = measure(chrome / f"{name}.png")
        actual = measure(OUT / "foafnaut" / f"{name}.png")
        assert reference["inkPixels"] > 10, (name, reference)
        result[name] = {"chrome": reference, "foafnaut": actual}
        print(name, result[name], flush=True)
    (OUT / "logo.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
