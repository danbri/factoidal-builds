"""Check the native X11 keyboard and button paths for a FrogFind-shaped GET form."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread
from urllib.parse import parse_qs, urlsplit

from Xlib import display

check_path = Path(sys.argv[1]) / "check-linux-browser.py"
spec = importlib.util.spec_from_file_location("check_linux_browser", check_path)
assert spec and spec.loader, check_path
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
colour_mask, trace_records = check.colour_mask, check.trace_records
wait_for, window_image, xdotool = check.wait_for, check.window_image, check.xdotool

BROWSER = Path(sys.argv[2]).resolve()
LIBRARY = Path(sys.argv[3]).resolve()
OUT = Path(sys.argv[4]).resolve()
BACKEND = sys.argv[5]
CASE = sys.argv[6]
QUERY = {"enter": "Lean 4 CSS", "button": "Foafnaut + WPT"}[CASE]
OUT.mkdir(parents=True, exist_ok=True)
HOME_TITLE = "FrogFind!"
RESULT_TITLE = "Local search received"
INPUT = (199, 233, 207)
BUTTON = (216, 210, 243)
RESULT = (19, 88, 167)
source = Path(sys.argv[7]).read_text()
assert source.count("</head>") == 1
# Only the two paint colours are changed, so X11 can locate the two controls.
FORM = source.replace("</head>", """<style>
  input[type=text] {background-color:#c7e9cf !important}
  input[type=submit] {background-color:#d8d2f3 !important}
</style></head>""")

class Fixture(BaseHTTPRequestHandler):
    def do_GET(self):
        target = urlsplit(self.path)
        if target.path != "/":
            self.send_error(404)
            return
        args = parse_qs(target.query)
        if args:
            self.server.queries.append({"raw":target.query, "args":args})
            markup = f"<title>{RESULT_TITLE}</title><h1>{RESULT_TITLE}</h1><div style='width:240px;height:80px;background:#1358a7'></div>"
        else:
            markup = FORM
        content = markup.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(("127.0.0.1",0),Fixture)
server.queries = []
Thread(target=server.serve_forever,daemon=True).start()
url = f"http://127.0.0.1:{server.server_port}/"
flags = ["--wasm-engine"] if BACKEND == "wasm" else ["--native-engine",str(LIBRARY)]
assert BACKEND in {"native","wasm"},BACKEND
record = {"backend":BACKEND,"submission":CASE,"queries":server.queries,"status":"fail"}
log_path = OUT/"browser.log"
with TemporaryDirectory() as cwd, log_path.open("w") as log:
    browser = subprocess.Popen([str(BROWSER), "--url",url,"--no-state","--no-splash","--trace-input",*flags],
                               cwd=cwd,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL)
    connection = None
    try:
        connection = display.Display()
        result = wait_for(browser,HOME_TITLE,lambda:xdotool("search","--onlyvisible","--pid",browser.pid,
                            "--name","^"+HOME_TITLE+"$",check=False).stdout.split())
        xid = int(result[0])
        window = connection.create_resource_object("window", xid)
        xdotool("windowfocus","--sync",xid)

        def controls():
            image = window_image(window)
            boxes = [colour_mask(image,rgb).getbbox() for rgb in (INPUT,BUTTON)]
            return (image,boxes) if all(boxes) else None

        image, (field, button) = wait_for(browser,"painted input and submit controls",controls)
        image.save(OUT/"before.png")

        def click(box):
            left,top,right,bottom = box
            xdotool("mousemove","--window",xid,(left+right)//2,(top+bottom)//2,"click","1")

        click(field)
        xdotool("type","--clearmodifiers","--delay","50",QUERY)
        def typed():
            image = window_image(window)
            return image if image.crop(field).tobytes() != before.crop(field).tobytes() else None
        before = image
        try:
            after_type = wait_for(browser,"input repaint after typing",typed,timeout=5)
            record["typedPixelsChanged"] = True
        except RuntimeError:
            if browser.poll() is not None:
                raise
            after_type = window_image(window)
            record["typedPixelsChanged"] = False
        after_type.save(OUT/"typed.png")
        if CASE == "enter":
            xdotool("key","--clearmodifiers","Return")
        else:
            click(button)
        wait_for(browser,"submitted query",lambda:server.queries,timeout=25)
        assert len(server.queries) == 1 and server.queries[0]["args"] == {"q":[QUERY]}, server.queries

        def outcome():
            image = window_image(window)
            name = xdotool("getwindowname",xid).stdout.strip()
            return image if name==RESULT_TITLE and colour_mask(image,RESULT).getbbox() else None

        wait_for(browser,"painted search result",outcome).save(OUT/"result.png")
        engine_traces = [row["engine"].split()[0] for row in trace_records(log_path)
                         if row.get("type") == "native-html-engine"]
        assert engine_traces and set(engine_traces)=={BACKEND},engine_traces
        record["status"]="pass"
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
        server.shutdown()
        server.server_close()
        (OUT/"receipt.json").write_text(json.dumps(record,indent=2)+"\n")
