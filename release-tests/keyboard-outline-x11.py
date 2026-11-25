"""Replay keyboard and pointer focus through X11 and inspect the visible pixels."""
import functools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image
from Xlib import X, XK, display
from Xlib.ext import xtest


FIXTURE = """<!doctype html>
<meta charset=utf-8><title>Keyboard outline fixture</title>
<style>
html, body {margin:0; height:100%; background:#e9ecf1}
#status {position:absolute; top:20px; left:24px; width:32px; height:12px; background:#b0a5c0}
#a, #b, #c {display:block; position:absolute; box-sizing:border-box; left:80px;
  width:160px; height:28px; padding:0 4px; border:0; color:#111111; font-size:16px}
#a {top:70px; background:#b4d9ed}
#b {top:130px; background:#efcf86}
#c {top:190px; background:#bbddb7; outline:none}
</style>
<div id=status></div>
<a id=a href="#a">Next page</a>
<input type=text id=b value="Search">
<button id=c>Author override</button>
<script>
const a = document.getElementById('a');
const status = document.getElementById('status');
a.addEventListener('click', e => e.preventDefault());
for (const [id, color] of [['a', '#23b45a'], ['b', '#d2376e'], ['c', '#3778be']]) {
  document.getElementById(id).addEventListener('focus', () => { status.style.backgroundColor = color; });
}
status.style.backgroundColor = "#7125a3";
</script>
"""
BG = (233, 236, 241)
INITIAL = (113, 37, 163)
FOCUSED = {"a": (35, 180, 90), "b": (210, 55, 110), "c": (55, 120, 190)}
FILL = {"a": (180, 217, 237), "b": (239, 207, 134), "c": (187, 221, 183)}
Y = {"a": 70, "b": 130, "c": 190}
NO_RING = [BG] * 4
RING = [(0, 0, 0), (255, 255, 255)] * 2
LABEL, ENGINE, LAB = sys.argv[1:]
OUT = Path("out")
REPORT = OUT / f"{LABEL}.json"


def wait_for(proc, fn, seconds, description):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"browser exited {proc.returncode} before {description}")
        result = fn()
        if result is not None:
            return result
        time.sleep(.04)
    raise RuntimeError(f"timed out waiting for {description}")


def main():
    conn = display.Display()
    root = conn.screen().root
    tab = conn.keysym_to_keycode(XK.string_to_keysym("Tab"))
    esc = conn.keysym_to_keycode(XK.string_to_keysym("Escape"))
    report = {}
    try:
        with tempfile.TemporaryDirectory() as tmp, (OUT / f"{LABEL}.log").open("w") as log:
            (Path(tmp) / "index.html").write_text(FIXTURE)
            serve = functools.partial(SimpleHTTPRequestHandler, directory=tmp)
            with ThreadingHTTPServer(("127.0.0.1", 0), serve) as http:
                server = threading.Thread(target=http.serve_forever, daemon=True)
                server.start()
                args = [
                    "deno", "run", "--no-check", "--no-config", "--no-npm", "--node-modules-dir=none",
                    "--unstable-webgpu", "--unstable-ffi", "-A", f"{LAB}/run_html.ts",
                    "--native-engine", ENGINE, "--url", f"http://127.0.0.1:{http.server_port}/",
                    "--window-size", "800x500", "--no-state", "--no-splash", "--trace-input",
                    "--no-spare-engine-worker",
                ]
                with subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT) as proc:
                    try:
                        def lookup():
                            result = subprocess.run(
                                ["xdotool", "search", "--onlyvisible", "--pid", str(proc.pid)],
                                capture_output=True, text=True, timeout=2,
                            )
                            if result.stdout.strip():
                                return conn.create_resource_object("window", int(result.stdout.split()[0]))
                            return None

                        window = wait_for(proc, lookup, 150, "visible browser window")
                        window.configure(x=0, y=0)
                        window.set_input_focus(X.RevertToParent, X.CurrentTime)
                        conn.sync()

                        def image():
                            area = window.get_geometry()
                            spot = root.translate_coords(window, 0, 0)
                            frame = root.get_image(spot.x, spot.y, area.width, area.height, X.ZPixmap, 0xffffffff)
                            if frame.depth != 24 or len(frame.data) != area.width * area.height * 4:
                                raise RuntimeError("expected packed Xvfb 24-bit display pixels")
                            return Image.frombytes("RGB", (area.width, area.height), frame.data, "raw", "BGRX")

                        def initial():
                            shot = image()
                            for row in range(16, min(240, shot.height - 215)):
                                if shot.getpixel((32, row)) == INITIAL and shot.getpixel((225, row+60)) == FILL["a"]:
                                    return (shot, row-20)
                            return None

                        before, origin = wait_for(proc, initial, 150, "initial fixture colours")
                        before.save(OUT / f"{LABEL}-unfocused.png")

                        def key(code):
                            xtest.fake_input(conn, X.KeyPress, code)
                            xtest.fake_input(conn, X.KeyRelease, code)
                            conn.sync()

                        def edge_samples(shot, which):
                            top = origin + Y[which]
                            return [shot.getpixel(point) for point in [(241, top+14), (240, top+14),
                                                                       (180, top-2), (180, top-1)]]

                        for which in Y:
                            top = origin + Y[which]
                            if before.getpixel((239, top+14)) != FILL[which] or edge_samples(before, which) != NO_RING:
                                raise RuntimeError(f"unfocused {which} border or backdrop mismatch")

                        def snap(stage, which, draw_ring=False):
                            expected = {control: NO_RING for control in Y}
                            if draw_ring and LABEL == "candidate":
                                expected[which] = RING
                            latest = None

                            def visible():
                                nonlocal latest
                                shot = image()
                                marker = shot.getpixel((32, origin+25))
                                samples = {control: edge_samples(shot, control) for control in Y}
                                latest = (shot, marker, samples)
                                if marker == FOCUSED[which] and samples == expected:
                                    return shot
                                return None

                            try:
                                shot = wait_for(proc, visible, 20, f"{stage} marker and outline")
                            except RuntimeError as error:
                                if latest is not None:
                                    shot, marker, samples = latest
                                    shot.save(OUT / f"{LABEL}-{stage}-last.png")
                                    report[stage] = {"marker": marker, "edges": samples, "expected": expected}
                                raise error
                            shot.save(OUT / f"{LABEL}-{stage}.png")
                            if shot.getpixel((230, origin + Y[which] + 14)) != FILL[which]:
                                raise RuntimeError(f"{stage}: inner colour changed")
                            report[stage] = expected

                        key(esc)
                        for stage, which in [("tab-link", "a"), ("tab-input", "b"), ("tab-override", "c")]:
                            key(tab)
                            snap(stage, which, draw_ring=which != "c")

                        spot = root.translate_coords(window, 0, 0)
                        xtest.fake_input(conn, X.MotionNotify, x=spot.x+135, y=spot.y+origin+Y["a"]+14)
                        xtest.fake_input(conn, X.ButtonPress, 1)
                        xtest.fake_input(conn, X.ButtonRelease, 1)
                        conn.sync()
                        snap("pointer-link", "a")
                    finally:
                        if proc.poll() is None:
                            proc.terminate()
                            try:
                                proc.wait(8)
                            except subprocess.TimeoutExpired:
                                proc.kill()
                                proc.wait()
                http.shutdown()
    finally:
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
        conn.close()


if __name__ == "__main__":
    main()
