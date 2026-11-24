#!/usr/bin/env python3
"""Exercise a relocated Foafnaut package on a real X11 window in Xvfb."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image, ImageChops
from Xlib import X, display, protocol


FIRST = "Foafnaut window test - first"
SECOND = "Foafnaut window test - second"
LIVE_URL = "https://example.org/"
LINK_RGB = (21, 128, 54)
PAGES = {
    "/first": (FIRST, "#c43b32", '<p><a style="color:#158036" href="/second">Read the next page</a></p>'),
    "/second": (SECOND, "#286db3", "<p>The link opened this document.</p>"),
}


class Fixture(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.requests.append(self.path)
        if self.path not in PAGES:
            self.send_error(404)
            return
        title, colour, body = PAGES[self.path]
        html = (f"<!doctype html><html><head><title>{title}</title></head><body>"
                f"<h1>{title}</h1><div style='width:210px;height:44px;background-color:{colour}'></div>"
                f"{body}</body></html>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)

    def log_message(self, *args):
        pass


def xdotool(*args, check=True):
    return subprocess.run(["xdotool", *map(str, args)], text=True, capture_output=True, check=check, timeout=10)


def wait_for(browser, label, call, timeout=170):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if browser.poll() is not None:
            raise RuntimeError(f"Browser exited with status {browser.returncode} while waiting for {label}")
        result = call()
        if result:
            return result
        time.sleep(0.15)
    raise RuntimeError(f"Timed out waiting for {label}")


def window_image(window):
    size = window.get_geometry()
    data = window.get_image(0, 0, size.width, size.height, X.ZPixmap, 0xffffffff)
    if data.depth != 24 or len(data.data) != size.width * size.height * 4:
        raise RuntimeError("The X11 window probe requires a 24-bit Xvfb screen with 32-bit pixels")
    return Image.frombytes("RGB", (size.width, size.height), data.data, "raw", "BGRX")


def colour_mask(image, rgb, tolerance=4):
    channels = [band.point([255 if abs(value-centre) <= tolerance else 0 for value in range(256)])
                for band, centre in zip(image.split(), rgb)]
    return ImageChops.darker(ImageChops.darker(channels[0], channels[1]), channels[2])


def trace_records(log):
    for line in log.read_text(errors="replace").splitlines():
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except ValueError:
                continue


def run(binary, evidence, record):
    server = ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
    server.requests = []
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    with tempfile.TemporaryDirectory(prefix="foafnaut-working-") as work, (evidence / "browser.log").open("w") as log:
        started = time.monotonic()
        browser = subprocess.Popen([str(binary), "--url", base + "/first", "--no-state", "--no-splash", "--perf-summary"],
                                   cwd=work, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        x = None
        try:
            x = display.Display()
            record["stage"] = "mapped window"

            def find_window():
                result = xdotool("search", "--onlyvisible", "--all", "--pid", browser.pid,
                                 "--name", "^" + re.escape(FIRST) + "$", check=False)
                return int(result.stdout.splitlines()[0]) if result.stdout.strip() else None

            xid = wait_for(browser, FIRST, find_window)
            window = x.create_resource_object("window", xid)
            xdotool("windowfocus", "--sync", xid)
            record["windowId"] = xid

            def snapshot(title, rgb, filename):
                def painted():
                    if xdotool("getwindowname", xid).stdout.strip() != title:
                        return None
                    image = window_image(window)
                    count = colour_mask(image, rgb).histogram()[255]
                    return (image, count) if count >= 1500 else None
                image, count = wait_for(browser, f"{title} title and page-colour pixels", painted)
                image.save(evidence / filename)
                record["pages"].append(dict(title=title, screenshot=filename, width=image.width, height=image.height,
                                            matchedPixels=count, rgb=rgb, sinceLaunchMs=round((time.monotonic()-started)*1000)))
                return image

            record["stage"] = "first HTML page"
            first = snapshot(FIRST, (196, 59, 50), "first.png")
            if os.environ.get("FOAFNAUT_DIAGNOSTIC_FIRST_PAINT_ONLY") == "1":
                def presented():
                    for row in trace_records(evidence / "browser.log"):
                        if row.get("type") == "native-html-frame" and row.get("presented"):
                            return row
                    return None
                frame = wait_for(browser, "first presented frame trace", presented)
                record.update(status="pass", stage="first presentation", firstFrame=frame)
                return
            # Click the actual coloured link text. Its position depends on layout, font and scale.
            link = colour_mask(first, LINK_RGB, 12)
            bounds = link.getbbox()
            if not bounds or link.histogram()[255] < 15:
                raise RuntimeError("The first window has no drawn link text in its authored colour")
            # The link may contain spaces. Pick a coloured pixel near its centre.
            cx, cy = (bounds[0] + bounds[2])//2, (bounds[1] + bounds[3])//2
            px, py = min(((xx, yy) for yy in range(bounds[1], bounds[3]) for xx in range(bounds[0], bounds[2])
                          if link.getpixel((xx, yy))), key=lambda xy: (xy[0]-cx)**2 + (xy[1]-cy)**2)
            record["stage"] = "native pointer and link navigation"
            xdotool("mousemove", "--window", xid, px, py, "click", "1")
            snapshot(SECOND, (40, 109, 179), "second.png")
            if "/second" not in server.requests:
                raise RuntimeError("The link never fetched the second HTTP document")
            record["linkClick"] = [px, py]
            record["stage"] = "native history shortcut"
            xdotool("key", "--clearmodifiers", "alt+Left")
            snapshot(FIRST, (196, 59, 50), "back.png")
            record["stage"] = "address entry and live HTTPS page"
            xdotool("key", "--clearmodifiers", "ctrl+l")
            xdotool("type", "--clearmodifiers", "--delay", 20, LIVE_URL)
            xdotool("key", "Return")

            def live_page():
                if xdotool("getwindowname", xid).stdout.strip() != "Example Domain":
                    return None
                image = window_image(window)
                # Text in the document portion, outside the address bar and tabs. The two
                # authored fixture colours must have gone from the displayed document.
                body = image.crop((0, 120, image.width, image.height))
                histogram = body.convert("L").histogram()
                ink = sum(histogram[:150])
                if (ink < 100 or sum(histogram[200:]) < body.width*body.height//4 or
                        colour_mask(body,(196,59,50)).histogram()[255] > 100):
                    return None
                return image, ink

            live, ink = wait_for(browser, "live Example Domain title and rendered text", live_page, timeout=100)
            live.save(evidence / "live.png")
            record["live"] = dict(url=LIVE_URL, title="Example Domain", screenshot="live.png", documentInkPixels=ink)
            record["stage"] = "native resize"
            xdotool("windowsize", xid, 680, 460)
            def reflowed():
                return any(row.get("type") == "native-html-frame" and row.get("presented") and
                           row.get("width") == 680 and row.get("height") == 460
                           for row in trace_records(evidence / "browser.log")) and live_page()
            resized, _ = wait_for(browser, "presented frame for resized live document", reflowed)
            resized.save(evidence / "resized.png")
            record["stage"] = "window manager close"
            message = protocol.event.ClientMessage(window=xid, client_type=x.intern_atom("WM_PROTOCOLS"),
                                                   data=(32, [x.intern_atom("WM_DELETE_WINDOW"), X.CurrentTime, 0, 0, 0]))
            window.send_event(message, event_mask=0)
            x.flush()
            rc = browser.wait(timeout=40)
            if rc:
                raise RuntimeError(f"Browser exited with status {rc} after window close")
        finally:
            if browser.poll() is None:
                browser.terminate()
                try:
                    browser.wait(timeout=6)
                except subprocess.TimeoutExpired:
                    browser.kill()
                    browser.wait()
            if x:
                x.close()
            server.shutdown()
            server.server_close()
            record["httpRequests"] = server.requests
    record["stage"] = "engine frame and worker evidence"
    records = list(trace_records(evidence / "browser.log"))
    frames = [row for row in records if row.get("type") == "native-html-frame" and row.get("presented")]
    summary = next((row for row in records if row.get("type") == "native-html-perf-summary"), {})
    if not frames or summary.get("present") != "window" or summary.get("inputEventsDropped") != 0:
        raise RuntimeError("Missing successful window presents or the input queue dropped events")
    expected = "native" if binary.with_name("libweb-render.so").is_file() else "wasm"
    if summary.get("compileBackend") != expected or not any(row.get("compiledIn") == "worker" for row in frames):
        raise RuntimeError(f"Expected a presented document from the {expected} worker")
    if not any(row.get("width") == 680 and row.get("height") == 460 for row in frames):
        raise RuntimeError("The renderer did not present a frame for the resized window")
    record.update(presentedFrames=len(frames), worker=expected, firstFrame=frames[0],
                  vulkanDriver=os.environ.get("VK_DRIVER_FILES"), sdlDriver=os.environ.get("SDL_VIDEODRIVER"),
                  inputEventsDropped=summary["inputEventsDropped"], stage="complete", status="pass")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    binary, evidence = args.binary.resolve(), args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    record = dict(format="foafnaut-linux-window-smoke-v1", status="fail", stage="package identity",
                  display=os.environ.get("DISPLAY"), pages=[])
    try:
        record["sourceCommit"] = json.loads(binary.with_name("BUILD-INFO.json").read_text())["commitFull"]
        with binary.open("rb") as stream:
            record["executableSha256"] = hashlib.file_digest(stream, "sha256").hexdigest()
        run(binary, evidence, record)
    except Exception as error:
        record["error"] = str(error)
        raise
    finally:
        (evidence / "window-smoke.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"Foafnaut window, HTTP link, history, HTTPS page, resize and close passed. Evidence in {evidence}")


if __name__ == "__main__":
    main()
