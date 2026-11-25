from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import subprocess
from threading import Thread

from PIL import Image


@contextmanager
def serve(directory):
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}"
        finally:
            server.shutdown()
            thread.join()


def marker(path):
    with Image.open(path) as img:
        pixels = img.convert("RGB")
        rows = [y for y in range(120) if pixels.getpixel((10, y)) == (0, 128, 255)]
    assert len(rows) == 20 and rows == list(range(rows[0], rows[0] + 20)), (path, rows)
    return rows[0]


root = Path.cwd()
fixtures = root / "out/fixtures"
fixtures.mkdir(parents=True)
cases = ("block", "grid", "nested")
for case in cases:
    style = """
        html, body { margin: 0; background: white; }
        main { width: 320px; height: 180px; position: relative; }
        main.grid { display: grid; grid-template-columns: repeat(2, 160px); }
        .item { position: relative; }
        .panel { position: absolute; top: 0; left: 0; width: 160px; }
        .pad { padding-top: 50%; }
        .marker { height: 20px; background: #0080ff; }
    """
    panel = '<div class="panel"><div class="pad"><div class="marker"></div></div></div>'
    item = f'<div class="item">{panel if case == "nested" else ""}</div>'
    document = f"""<!doctype html><meta charset="utf-8"><style>{style}</style>
        <main class="{"block" if case == "block" else "grid"}">{item}{"" if case == "nested" else panel}</main>"""
    (fixtures / f"{case}.html").write_text(document)

rows = {}
with serve(fixtures) as url:
    jobs = root / "out/jobs.jsonl"
    jobs.write_text("".join(json.dumps({"url": f"{url}/{case}.html", "width": 320,
                                        "height": 180, "file": f"{case}.png"}) + "\n"
                            for case in cases))
    for role in ("baseline", "candidate"):
        out = root / "out" / role
        out.mkdir()
        with (out / "renderer.log").open("w") as log:
            subprocess.run(["deno", "run", "--no-config", "--no-npm", "--unstable-ffi", "-A",
                            "core/tests/browser-wpt/reftest-render.ts",
                            "--native-engine", str(root / f"{role}-engine/libweb-render.so"),
                            "--list", str(jobs), "--out", str(out)], stdout=log, stderr=subprocess.STDOUT,
                           check=True, timeout=90)
        rows[role] = {case: marker(out / f"{case}.png") for case in cases}
    out = root / "out/chrome"
    out.mkdir()
    for case in cases:
        with (out / f"{case}.log").open("w") as log:
            subprocess.run(["google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--window-size=320,180", "--force-device-scale-factor=1",
                            f"--screenshot={out / (case + '.png')}", f"{url}/{case}.html"],
                           stdout=log, stderr=subprocess.STDOUT, check=True, timeout=30)
    rows["chrome"] = {case: marker(out / f"{case}.png") for case in cases}

(root / "out/comparison.json").write_text(json.dumps(rows, indent=2) + "\n")
print("| Case | Baseline marker y | Candidate marker y | Chrome marker y |")
print("| --- | ---: | ---: | ---: |")
for case in cases:
    print(f"| {case} | {rows['baseline'][case]} | {rows['candidate'][case]} | {rows['chrome'][case]} |")
assert rows["chrome"] == {name: 80 for name in cases}, rows
assert rows["baseline"] == rows["chrome"], rows
assert rows["candidate"] == rows["chrome"], rows
