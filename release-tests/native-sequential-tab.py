"""Drive default sequential focus with native X11 keys and verify visible focus events."""
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
<meta charset=utf-8><title>Native sequential Tab</title>
<style>
html, body {margin:0; height:100%; background:#e9ecf1}
#status, #key {position:absolute; top:20px; width:32px; height:12px}
#status {left:24px; background:#b0a5c0}
#key {left:64px; background:#c7b296}
#a {display:block; position:absolute; top:70px; left:80px; width:160px;
  height:28px; padding:0; border:0; background:#b4d9ed}
</style>
<div id=status></div><div id=key></div>
<a id=a href="#a">First in tree, default tabindex</a>
<button id=two tabindex=2>Second priority</button>
<div style="display:none"><button tabindex=1>Hidden</button></div>
<button tabindex=1 disabled>Disabled</button>
<div inert><button tabindex=1>Inert</button></div>
<button id=one tabindex=1>First priority</button>
<input id=b type=text value=Search>
<button tabindex=-1>Negative</button>
<button id=c>Last in tree</button>
<script>
const status = document.getElementById('status');
const key = document.getElementById('key');
const one = document.getElementById('one');
for (const [id, color] of [['one', '#23b45a'], ['two', '#d2376e'], ['a', '#3778be'],
                          ['b', '#915422'], ['c', '#156d68']]) {
  document.getElementById(id).addEventListener('focus', () => { status.style.backgroundColor = color; });
}
let first = true;
let cancel = true;
document.addEventListener('keydown', event => {
  if (event.key !== 'Tab') return;
  if (first) {
    first = false;
    key.style.backgroundColor = '#b12f45';
  }
  if (event.target === one && !event.shiftKey && cancel) {
    cancel = false;
    event.preventDefault();
    key.style.backgroundColor = '#290f92';
  }
});
status.style.backgroundColor = '#7125a3';
</script>
"""
INITIAL = (113, 37, 163)
FOCUSED = {"one": (35, 180, 90), "two": (210, 55, 110), "a": (55, 120, 190),
           "b": (145, 84, 34), "c": (21, 109, 104)}
KEY_RECEIVED = (177, 47, 69)
KEY_CANCELLED = (41, 15, 146)
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
    shift = conn.keysym_to_keycode(XK.string_to_keysym("Shift_L"))
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
                                if shot.getpixel((32, row)) == INITIAL and shot.getpixel((225, row+60)) == (180, 217, 237):
                                    return (shot, row-20)
                            return None

                        before, origin = wait_for(proc, initial, 150, "initial fixture colours")
                        before.save(OUT / f"{LABEL}-unfocused.png")

                        def key(code, reverse=False):
                            if reverse:
                                xtest.fake_input(conn, X.KeyPress, shift)
                            xtest.fake_input(conn, X.KeyPress, code)
                            xtest.fake_input(conn, X.KeyRelease, code)
                            if reverse:
                                xtest.fake_input(conn, X.KeyRelease, shift)
                            conn.sync()

                        def focus_color(shot):
                            return shot.getpixel((32, origin+25))

                        def key_color(shot):
                            return shot.getpixel((72, origin+25))

                        def snap(stage, focus, received):
                            latest = None
                            def visible():
                                nonlocal latest
                                latest = image()
                                if focus_color(latest) == focus and key_color(latest) == received:
                                    return latest
                                return None
                            try:
                                shot = wait_for(proc, visible, 20, stage)
                            except RuntimeError:
                                if latest is not None:
                                    latest.save(OUT / f"{LABEL}-{stage}-last.png")
                                    report[stage] = {"focus": focus_color(latest), "key": key_color(latest)}
                                raise
                            shot.save(OUT / f"{LABEL}-{stage}.png")
                            report[stage] = {"focus": focus, "key": received}

                        key(esc)
                        address_fill = before.getpixel((650, 45))
                        wait_for(proc, lambda: True if image().getpixel((650, 45)) != address_fill else None,
                                 20, "address field leaving focus")
                        key(tab)
                        if LABEL == "baseline":
                            snap("keydown-without-default-focus", INITIAL, KEY_RECEIVED)
                            time.sleep(1)
                            if focus_color(image()) != INITIAL:
                                raise RuntimeError("baseline unexpectedly advanced focus after key delivery")
                            return

                        snap("first-positive", FOCUSED["one"], KEY_RECEIVED)
                        key(tab)
                        snap("cancelled-tab", FOCUSED["one"], KEY_CANCELLED)
                        time.sleep(.35)
                        if focus_color(image()) != FOCUSED["one"]:
                            raise RuntimeError("cancelled Tab advanced focus")
                        for stage, control in [("second-positive", "two"), ("tree-link", "a"),
                                               ("tree-input", "b"), ("tree-button", "c")]:
                            key(tab)
                            snap(stage, FOCUSED[control], KEY_CANCELLED)
                        for stage, control in [("reverse-input", "b"), ("reverse-link", "a"),
                                               ("reverse-positive", "two")]:
                            key(tab, reverse=True)
                            snap(stage, FOCUSED[control], KEY_CANCELLED)
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
