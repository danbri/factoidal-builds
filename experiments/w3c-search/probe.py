"""Check the live W3C search form with native X11 keyboard and pointer events."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import parse_qs, urlsplit

from Xlib import display

checker, host, output = map(lambda arg: Path(arg).resolve(), sys.argv[1:4])
mode = sys.argv[4]
query = {"enter": "CSS Grid", "button": "CSS Layout"}[mode]
module = importlib.util.spec_from_file_location("linux_check", checker)
assert module and module.loader, checker
check = importlib.util.module_from_spec(module)
module.loader.exec_module(check)
output.mkdir(parents=True)
log = output / "browser.log"
page = "https://www.w3.org/help/search/"
receipt = {"mode": mode, "query": query, "status": "failed"}
with log.open("w") as stream:
    browser = subprocess.Popen(
        [str(host), "--url", page, "--window-size", "1280x800", "--no-state",
         "--no-splash", "--trace-input"], stdout=stream, stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
    )
    connection = None
    try:
        connection = display.Display()
        def find_window():
            return check.xdotool("search", "--onlyvisible", "--pid", browser.pid,
                                 "--name", "^Search .+ W3C$", check=False).stdout.split()
        xid = int(check.wait_for(browser, "W3C search window", find_window, timeout=55)[0])
        window = connection.create_resource_object("window", xid)
        check.xdotool("windowfocus", "--sync", xid)
        def controls():
            image = check.window_image(window)
            field = check.colour_mask(image, (199, 233, 207)).getbbox()
            button = check.colour_mask(image, (216, 210, 243)).getbbox()
            return (image, field, button) if field and button else None
        before, field, button = check.wait_for(browser, "painted search controls", controls, timeout=35)
        before.save(output / "before.png")
        receipt.update(field=field, button=button)

        def click(box):
            left, top, right, bottom = box
            check.xdotool("mousemove", "--window", xid, (left + right) // 2,
                          (top + bottom) // 2, "click", "1")

        click(field)
        check.xdotool("type", "--clearmodifiers", "--delay", "45", query)
        def dark_pixels(image):
            return sum(max(pixel) < 105 for pixel in image.crop(field).convert("RGB").getdata())
        def painted_query():
            image = check.window_image(window)
            return image if dark_pixels(image) - dark_pixels(before) >= 25 else None
        after = check.wait_for(browser, "painted query text", painted_query, timeout=8)
        after.save(output / "typed.png")
        receipt["darkPixelsAdded"] = dark_pixels(after) - dark_pixels(before)
        if mode == "enter":
            check.xdotool("key", "--clearmodifiers", "Return")
        else:
            click(button)

        def records(kind):
            return [r for r in check.trace_records(log) if r.get("type") == kind]
        handoff = check.wait_for(browser, "W3C form response",
                                 lambda: records("w3c-search-handoff"), timeout=40)
        receipt["handoff"] = handoff
        assert len(handoff) == 1 and handoff[0]["status"] == 302, handoff
        params = parse_qs(urlsplit(handoff[0]["url"]).query, keep_blank_values=True)
        assert params == {"q": [query], "ko": ["-2"], "k1": ["-1"], "search": [""]}, params
        destination = urlsplit(handoff[0]["location"])
        assert destination.scheme == "https" and destination.hostname == "duckduckgo.com", destination
        assert parse_qs(destination.query).get("q") == [f"site:www.w3.org {query}"], destination
        nav = records("native-html-form-navigate")
        assert len(nav) == 1 and nav[0]["method"].lower() == "get" and not nav[0]["blocked"], nav
        assert nav[0]["cause"].startswith("key" if mode == "enter" else "pointer"), nav
        assert any(r["engine"].split()[0] == "native" for r in records("native-html-engine"))
        receipt["navigation"] = nav
        receipt["status"] = "handoff-pass"

        def presented_provider():
            return [r for r in records("native-html-presented")
                    if urlsplit(r.get("url", "")).hostname == "duckduckgo.com"]
        try:
            receipt["providerFrame"] = check.wait_for(browser, "painted provider response",
                                                       presented_provider, timeout=40)[-1]
            check.window_image(window).save(output / "provider.png")
        except RuntimeError as error:
            receipt["providerFrameError"] = str(error)
        receipt["providerResponses"] = records("w3c-search-provider")
    finally:
        if connection:
            connection.close()
        if browser.poll() is None:
            browser.terminate()
            try:
                browser.wait(timeout=8)
            except subprocess.TimeoutExpired:
                browser.kill()
                browser.wait(timeout=5)
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
