import functools
import http.server
import json
from pathlib import Path
import subprocess
import threading

from PIL import Image

OUT = Path("out").resolve()
WIDTH, HEIGHT = 800, 640
WHITE = (255, 255, 255)
RED = (190, 45, 30)
GREEN = (30, 165, 75)
BLUE = (40, 105, 200)
CROP = (12, 12, 64, 64)
MASK = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"><path fill="#be2d1e" d="M4 6h24v4H4zm0 8h24v4H4zm0 8h24v4H4z"/></svg>'
BASE = """
html,body { margin:0; background:#fff }
.fixture { position:relative; width:52px;height:52px; margin:12px }
.trigger { box-sizing:border-box; background:#fff; border:3px solid #be2d1e; position:absolute;
  left:8px; top:8px; width:36px;height:36px; margin:0 }
.contents { background:#1ea54b; position:absolute; left:16px; top:16px; width:16px;height:16px }
.vector-dropdown .vector-dropdown-checkbox { cursor:pointer; position:absolute; left:8px; top:8px;
  z-index:1; opacity:0; width:36px;height:36px; margin:0;padding:0 }
.icon { display:block;width:32px;height:32px;background-color:#2869c8;
  mask-repeat:no-repeat;mask-position:center; mask-size:32px 32px }
.icon.png { mask-image:url(mask.png) }
.icon.svg { -webkit-mask-image:url(menu.svg);mask-image:url(menu.svg) }
.logo { display:flex;width:80px;height:32px }
.logo img { display:block;width:32px;height:32px }
.radio-input { position:absolute; margin:0; opacity:0; width:32px;height:32px; z-index:1 }
.radio-icon { position:absolute;box-sizing:border-box; width:32px;height:32px;
  border:6px solid #2869c8; border-radius:50%;background:white }
"""
CASES = {
    "opaque-checkbox": '<input class="trigger" type="checkbox" style="appearance:none">',
    "transparent-checkbox": '<span class="contents"></span><input class="trigger vector-dropdown-checkbox" type="checkbox" style="appearance:none">',
    "transparent-group": '<div style="opacity:0"><div class="contents" style="opacity:1"></div></div>',
    "svg-mask": '<span class="icon svg"></span>',
    "png-mask": '<span class="icon png"></span>',
    "direct-svg": '<img src="menu.svg" width="32" height="32" alt="">',
    "flex-svg-logo": '<a class="logo"><span><img src="menu.svg" width="32" height="32" alt=""></span></a>',
    "radio-decoration": '<input class="radio-input" type="radio"><span class="radio-icon"></span>',
}
SAMPLES = {
    "opaque-checkbox": ((9, 9), RED),
    "transparent-checkbox": ((9, 9), WHITE),
    "transparent-group": ((20, 20), WHITE),
    "svg-mask": ((7, 7), BLUE),
    "png-mask": ((7, 7), BLUE),
    "direct-svg": ((7, 7), RED),
    "flex-svg-logo": ((7, 7), RED),
    "radio-decoration": ((1, 1), WHITE),
}


def measure(path, sample):
    with Image.open(path) as image:
        crop = image.convert("RGB").crop(CROP)
        return crop, {
            "sample": crop.getpixel(sample),
            "white": sum(pixel == WHITE for pixel in crop.getdata()),
            "red": sum(pixel == RED for pixel in crop.getdata()),
            "green": sum(pixel == GREEN for pixel in crop.getdata()),
            "blue": sum(pixel == BLUE for pixel in crop.getdata()),
        }


def main():
    fixtures = OUT / "fixtures"
    fixtures.mkdir()
    (fixtures / "menu.svg").write_text(MASK)
    alpha = Image.new("RGBA", (32, 32))
    for y in (*range(6, 10), *range(14, 18), *range(22, 26)):
        for x in range(4, 28):
            alpha.putpixel((x, y), (*RED, 255))
    alpha.save(fixtures / "mask.png")
    for name, markup in CASES.items():
        (fixtures / f"{name}.html").write_text(
            '<!doctype html><meta charset="utf-8"><style>' + BASE +
            "</style><div class='fixture vector-dropdown'>" + markup + "</div>"
        )
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=fixtures)
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        origin = f"http://127.0.0.1:{server.server_port}"
        jobs = [
            {"url": f"{origin}/{name}.html", "width": WIDTH, "height": HEIGHT, "file": f"{name}.png"}
            for name in CASES
        ]
        (OUT / "jobs.jsonl").write_text("".join(json.dumps(job) + "\n" for job in jobs))
        with (OUT / "foafnaut.log").open("w") as log:
            subprocess.run(
                ["deno", "run", "-A", "--unstable-ffi", "core/tests/browser-wpt/reftest-render.ts",
                 "--native-engine", "engine/libweb-render.so", "--list", str(OUT / "jobs.jsonl"),
                 "--out", str(OUT / "foafnaut")], check=True, stdout=log, stderr=subprocess.STDOUT,
                timeout=120,
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
    for name, (sample, expected) in SAMPLES.items():
        ref, reference = measure(chrome / f"{name}.png", sample)
        actual, foafnaut = measure(OUT / "foafnaut" / f"{name}.png", sample)
        assert reference["sample"] == expected, (name, reference, expected)
        result[name] = {
            "chrome": reference, "foafnaut": foafnaut,
            "changedPixels": sum(a != b for a, b in zip(ref.getdata(), actual.getdata())),
        }
        print(name, result[name], flush=True)
    (OUT / "pixels.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
