"""Measure an external X11 click and the first document pixels it changes."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time

from Xlib import X, display, protocol
from Xlib.ext import xtest

binary = Path(os.environ["FOAFNAUT_APP"]).resolve()
layout = sys.argv[1]
out = Path("out").resolve()
out.mkdir(exist_ok=True)
conn = display.Display()
root = conn.screen().root
now = time.monotonic
source_colour = (20, 120, 190)
target_colour = (210, 80, 40)


def fixture(directory):
    for name, colour in [("source", source_colour), ("result", target_colour)]:
        html = f"""<!doctype html><title>{name}</title>
        <a href="result.html" style="display:block;width:800px;height:540px;
        background:rgb({colour[0]},{colour[1]},{colour[2]})">{name}</a>"""
        (directory / f"{name}.html").write_text(html)


def pixel(x, y):
    data = root.get_image(x, y, 1, 1, X.ZPixmap, 0xffffffff)
    if data.depth != 24 or len(data.data) != 4:
        raise RuntimeError("Expected a 24-bit Xvfb display with 32-bit pixels")
    return tuple(data.data[2::-1])


def capture(proc, path, events):
    with path.open("w") as log:
        for line in proc.stdout:
            stamp = now()
            log.write(line)
            log.flush()
            events.put((stamp, line))


def run(label, url, cache):
    result = {"label": label, "layout": layout}
    gate = out / f"{label}.gate.jsonl"
    args = [str(binary), "--url", url,
            "--window-size", "1600x1000", "--no-state", "--no-splash",
            "--follow-links", "--trace-input", "--perf-summary", "--gate-trace", str(gate)]
    if layout == "single":
        args.append("--single-frame")
    start = now()
    proc = subprocess.Popen(args, cwd=binary.parent, env={**os.environ, "MESA_SHADER_CACHE_DIR": str(cache)},
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    events = queue.Queue()
    reader = threading.Thread(target=capture, args=(proc, out / f"{label}.log", events), daemon=True)
    reader.start()
    window = first_frame = sent = visible = dispatched = source_visible = None
    next_lookup = 0
    summary = None
    try:
        while now() - start < 170 and visible is None:
            if proc.poll() is not None:
                raise RuntimeError(f"browser exited {proc.returncode} before target paint")
            while not events.empty():
                stamp, line = events.get_nowait()
                if line.startswith("Input SDL kind=2") and sent is not None:
                    dispatched = stamp
                if not line.startswith("{"):
                    continue
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get("type") == "native-html-frame" and event.get("frame") == 1:
                    first_frame = stamp
                    first_host_ms = event["t"]
            if window is None and now() >= next_lookup:
                next_lookup = now() + .1
                lookup = subprocess.run(["xdotool", "search", "--onlyvisible", "--pid", str(proc.pid)],
                                        capture_output=True, text=True, timeout=2)
                if lookup.stdout.strip():
                    window = conn.create_resource_object("window", int(lookup.stdout.split()[0]))
                    window.configure(x=0, y=0)
                    window.set_input_focus(X.RevertToParent, X.CurrentTime)
                    conn.sync()
            if window is not None:
                pos = root.translate_coords(window, 0, 0)
                colour = pixel(pos.x + 420, pos.y + 300)
                if colour == source_colour and source_visible is None:
                    source_visible = now()
                if first_frame is not None and sent is None:
                    xtest.fake_input(conn, X.MotionNotify, x=pos.x + 240, y=pos.y + 300)
                    sent = now()
                    xtest.fake_input(conn, X.ButtonPress, 1)
                    xtest.fake_input(conn, X.ButtonRelease, 1)
                    conn.sync()
                if sent is not None and colour == target_colour:
                    visible = now()
            time.sleep(.01)
        if visible is None:
            raise RuntimeError("Timed out waiting for clicked document pixels")
        msg = protocol.event.ClientMessage(window=window, client_type=conn.intern_atom("WM_PROTOCOLS"),
                  data=(32, [conn.intern_atom("WM_DELETE_WINDOW"), X.CurrentTime, 0, 0, 0]))
        window.send_event(msg)
        conn.flush()
        proc.wait(timeout=30)
        reader.join(timeout=5)
        for line in (out / f"{label}.log").read_text().splitlines():
            if line.startswith('{"type":"native-html-perf-summary"'):
                summary = json.loads(line)
        if proc.returncode or summary is None or not gate.is_file():
            raise RuntimeError(f"incomplete host summary or trace, exit {proc.returncode}")
        result["maxBlockedMs"] = summary["gpu"]["maxBlockedMs"]
        result["maxPumpGapMs"] = summary["pumpGapAfterFirstFrameMs"]["max"]
        result["maxInFlight"] = summary["gpu"]["maxInFlight"]
        result["dropped"] = summary["inputEventsDropped"]
        asks = [json.loads(line) for line in gate.read_text().splitlines()]
        host_click_ms = first_host_ms + (sent - first_frame) * 1000
        result["observedClickDuringAskMs"] = max((ask["blocked"] for ask in asks
            if ask.get("ev") == "ask" and ask["asked"] <= host_click_ms <= ask["asked"] + ask["blocked"]), default=0)
        if dispatched is None or result["dropped"]:
            raise RuntimeError("missing SDL button trace or dropped native input")
    except Exception as error:
        result["error"] = str(error)
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        reader.join(timeout=5)
        def ms(a, b):
            return round((b - a) * 1000, 1) if a is not None and b is not None else None
        result.update(firstFrameLogMs=ms(start, first_frame), firstSourcePixelsMs=ms(start, source_visible),
                      frameLogToInjectionMs=ms(first_frame, sent), clickToSDLLogMs=ms(sent, dispatched),
                      clickToResultPixelsMs=ms(sent, visible))
        (out / f"{label}.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result), flush=True)
    return result


with tempfile.TemporaryDirectory() as tmp:
    directory = Path(tmp)
    fixture(directory)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(directory)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/source.html"
    rows = []
    try:
        for pair in [1, 2]:
            cache = directory / f"cache-{pair}"
            cache.mkdir()
            for state in ["fresh", "reused"]:
                rows.append(run(f"{layout}-{pair}-{state}", url, cache))
    finally:
        server.shutdown()
        server.server_close()
if any("error" in row for row in rows):
    sys.exit(1)
