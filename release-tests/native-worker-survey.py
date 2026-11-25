"""Run the packaged Linux Foafnaut on the registered live pages under an X11 display."""
import collections
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from PIL import Image, ImageChops
from Xlib import X, display

binary, lab, out = map(lambda p: Path(p).resolve(), sys.argv[1:4])
shard = int(sys.argv[4])
shards = int(sys.argv[5])
registry = json.loads((lab / "realpages/pages.json").read_text())
specs = registry["pages"][shard::shards]
out.mkdir(parents=True, exist_ok=True)
connection = display.Display()

def xdotool(*args):
    return subprocess.run(["xdotool", *map(str, args)], text=True, capture_output=True, timeout=7)

def window_image(window):
    size = window.get_geometry()
    root = connection.screen().root
    position = root.translate_coords(window, 0, 0)
    screen = root.get_geometry()
    if (position.x < 0 or position.y < 0 or
            position.x + size.width > screen.width or position.y + size.height > screen.height):
        raise RuntimeError(f"Window outside the capture screen at {position.x},{position.y} ({size.width}x{size.height})")
    raster = root.get_image(position.x, position.y, size.width, size.height, X.ZPixmap, 0xffffffff)
    if raster.depth != 24 or len(raster.data) != size.width * size.height * 4:
        raise RuntimeError("Expected 24-bit X11 pixels")
    return Image.frombytes("RGB", (size.width, size.height), raster.data, "raw", "BGRX")

def read_traces(reader):
    while True:
        offset = reader.tell()
        line = reader.readline()
        if not line.endswith("\n"):
            reader.seek(offset)
            break
        if line.startswith("{"):
            try:
                result = json.loads(line)
            except ValueError:
                continue
            if isinstance(result, dict):
                yield result

def capture(spec):
    key = spec["id"]
    if not re.fullmatch("[a-z0-9-]+", key):
        raise ValueError("Invalid registry ID")
    url = spec["url"]
    if url.startswith("lab:"):
        url = (lab / url.removeprefix("lab:")).as_uri()
    width, height = map(int, spec.get("viewport", registry["defaults"]["viewport"]).split("x"))
    budget = registry["defaults"]["budgets"] | spec.get("budgets", {})
    row = dict(id=key, url=url, viewport=[width,height], budget=budget, state="pending")
    log = out / f"{key}.log"
    arguments = [str(binary), "--url", url, "--no-state", "--no-splash", "--perf-summary", "--trace-input"]
    arguments.extend(("--window-size", f"{width}x{height}"))
    single_frame = os.environ.get("SURVEY_RENDER_MODE") == "single"
    if single_frame:
        arguments.append("--single-frame")
    if spec.get("scripts") is False:
        arguments.append("--no-scripts")
    with log.open("w") as output, log.open("r", errors="replace") as reader:
        start = time.monotonic()
        browser = subprocess.Popen(arguments, cwd=binary.parent, stdin=subprocess.DEVNULL,
                                   stdout=output, stderr=subprocess.STDOUT)
        window = None
        base = None
        frame = None
        configured = False
        wheel_at = None
        while_timeout = start + 190
        try:
            while time.monotonic() < while_timeout:
                if browser.poll() is not None:
                    row.update(state="exited", exitCode=browser.returncode)
                    break
                if window is None:
                    found = xdotool("search", "--onlyvisible", "--pid", browser.pid).stdout.split()
                    if found:
                        window = connection.create_resource_object("window", int(found[0]))
                        xdotool("windowfocus", "--sync", window.id)
                        xdotool("windowmove", "--sync", window.id, 0, 0).check_returncode()
                        row["windowMs"] = round((time.monotonic()-start)*1000)
                for trace in read_traces(reader):
                    kind = trace.get("type")
                    if kind == "native-html-engine":
                        row["documentEngine"] = trace["engine"].split()[0]
                    if kind == "native-html-loaded":
                        row["loaded"] = trace
                    if kind == "native-html-frame" and trace.get("presented"):
                        if "initialFrame" not in row:
                            row["initialFrame"] = trace
                        if (trace.get("width"),trace.get("height")) == (width,height):
                            configured = True
                            if frame is None:
                                frame = trace
                    if wheel_at is not None and kind == "native-html-scroll" and trace.get("scroll", 0) > 0:
                        row.setdefault("scrollTrace", trace)
                    if wheel_at is not None and kind == "native-html-input-latency":
                        row.setdefault("inputTrace", []).append(trace)
                        # Single-frame rendering performs a full redraw for scrolling.
                        # Its presented event settles the wheel trace without the
                        # separate fast layered scroll event.
                        if single_frame and trace.get("kind") == "scroll":
                            row.setdefault("scrollTrace", trace)
                if base is None and window is not None and frame is not None:
                    image = window_image(window)
                    if image.size != (width, height):
                        time.sleep(0.1)
                        continue
                    top = min(height-1,(frame.get("layers") or {}).get("top",65))
                    base = image.crop((0,top,width,height))
                    colors = base.getcolors(maxcolors=4)
                    row.update(state="presented", firstFrame=frame,
                               presentedMs=round((time.monotonic()-start)*1000),
                               documentColorsAtLeast=5 if colors is None else len(colors))
                    image.save(out / f"{key}.png")
                    if spec.get("scroll") is False:
                        break
                    xdotool("mousemove", "--window", window.id, width//2, 3*height//4, "click", "5")
                    wheel_at = time.monotonic()
                    while_timeout = wheel_at + 15
                if wheel_at is not None and "scrollTrace" in row:
                    after = window_image(window)
                    crop_top = height - base.height
                    delta = ImageChops.difference(base,after.crop((0,crop_top,width,height)))
                    row.update(scrollObservedMs=round((time.monotonic()-wheel_at)*1000),
                               scrollChangesPixels=delta.getbbox() is not None)
                    after.save(out / f"{key}-scroll.png")
                    break
                time.sleep(0.1)
            if row["state"] == "pending":
                row.update(state="no-target-frame", configured=configured)
        except Exception as error:
            row.update(state="probe-error", error=str(error), configured=configured)
        finally:
            if browser.poll() is None:
                browser.terminate()
                try:
                    browser.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    browser.kill()
                    browser.wait(timeout=5)
            row["elapsedMs"] = round((time.monotonic()-start)*1000)
    return row

rows = []
for spec in specs:
    row = capture(spec)
    rows.append(row)
    print(json.dumps({k:row[k] for k in ("id","state","presentedMs","scrollObservedMs") if k in row}), flush=True)
    (out / "summary.json").write_text(json.dumps(rows, indent=2)+"\n")
print(collections.Counter(row["state"] for row in rows), flush=True)
