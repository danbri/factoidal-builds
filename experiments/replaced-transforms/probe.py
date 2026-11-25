import functools
import http.server
import json
from pathlib import Path
import subprocess
import threading

from PIL import Image


OUT = Path("out").resolve()
WIDTH, HEIGHT = 800, 630
RED = (183, 50, 33)
STYLE = """
html,body{margin:0;background:white}
.control{position:relative;width:50px;height:50px}
img{display:block}
.control.block{height:auto}
.control.block>img{height:50px}
.control>img,.control>svg{width:100%;height:100%}
.absolute>*{position:absolute;top:0;left:0}
.scaled>*{transform:scale(.4)}
.origin>*{transform-origin:top left}
.marker{height:7px;background:rgb(26,177,71)}
"""
SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="27" height="27" viewBox="0 0 50 50">'
       '<rect width="50" height="50" fill="#b73221"/></svg>')
IMAGE = '<img width="50" height="50" src="image.png" alt="">'
CASES = {
    "positioned-svg-control": ("absolute", SVG, [0, 0, 49, 49]),
    "positioned-svg-scale": ("absolute scaled", SVG, [15, 15, 34, 34]),
    "positioned-svg-origin": ("absolute scaled origin", SVG, [0, 0, 19, 19]),
    "positioned-png-scale": ("absolute scaled", IMAGE, [15, 15, 34, 34]),
    "block-png-scale": ("block scaled", IMAGE, [15, 15, 34, 34]),
}


def measure(path):
    with Image.open(path) as png:
        rgb = png.convert("RGB")
        assert rgb.size == (WIDTH, HEIGHT), rgb.size
        red = [(x, y) for y in range(70) for x in range(70) if rgb.getpixel((x, y)) == RED]
        bounds = [min(x for x, _ in red), min(y for _, y in red),
                  max(x for x, _ in red), max(y for _, y in red)] if red else None
        green = [y for y in range(70) if rgb.getpixel((5, y)) == (26, 177, 71)]
        return {"icon": bounds, "marker": green}


def main():
    fixtures = OUT / "fixtures"
    fixtures.mkdir()
    Image.new("RGB", (240, 135), RED).save(fixtures / "image.png")
    for name, (classes, markup, _) in CASES.items():
        page = f'<!doctype html><meta charset=utf-8><style>{STYLE}</style><div class="control {classes}">{markup}</div><div class="marker"></div>'
        (fixtures / f"{name}.html").write_text(page)
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
    for name, (_, _, expected) in CASES.items():
        reference = measure(chrome / f"{name}.png")
        actual = measure(OUT / "foafnaut" / f"{name}.png")
        assert reference == {"icon": expected, "marker": list(range(50, 57))}, (name, reference)
        result[name] = {"chrome": reference, "foafnaut": actual}
        print(name, reference, actual)
    (OUT / "geometry.json").write_text(json.dumps(result, indent=2) + "\n")
    assert all(row["chrome"] == row["foafnaut"] for row in result.values()), result


if __name__ == "__main__":
    main()
