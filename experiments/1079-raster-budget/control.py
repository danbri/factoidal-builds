from contextlib import contextmanager
from functools import partial
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
from threading import Thread
from zipfile import ZipFile

from PIL import Image, ImageDraw

root = Path.cwd()
out = root / "out"
site = out / "synthetic-inputs"
assets = site / "assets"
assets.mkdir(parents=True)
digest = lambda data: sha256(data).hexdigest()
engines = {role: root / f"{role}-engine/libweb-render.so" for role in ("baseline", "candidate")}


def asset(i):
    return f"{i:02}.png"


def color(i):
    return (40 + 3*i, 70, 170)


for i in range(48):
    img = Image.new("RGB", (610, 360), (238, 242, 255))
    draw = ImageDraw.Draw(img)
    for y in range(0, 360, 7):
        for x in range(0, 610, 7):
            if (x//7+y//7+i) % 2 == 0:
                draw.rectangle((x, y, x+6, y+6), (42+i, 116, 104))
    draw.rectangle((0, 0, 15, 15), color(i))
    img.save(assets / asset(i), compress_level=6)
(assets / "vector.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="90" height="90"><rect width="90" height="90" fill="orange"/></svg>')


def fixture(name, sources, shown, *, prefix="assets", vector=False):
    tags = []
    for row, i in enumerate(sources):
        pos = shown.get(row)
        left, top = pos if pos is not None else (0, 720+row*140)
        ident = f"source-{i:02}"
        tags.append(f'<img alt="{ident}" src="/{prefix}/{asset(i)}" style="left:{left}px;top:{top}px">')
    if vector:
        tags.append('<img alt="vector" src="/assets/vector.svg" style="left:0;top:10000px">')
    path = site / f"{name}.html"
    path.write_text('''<!doctype html><meta charset="utf-8"><style>
        html,body {margin:0;background:white}
        img {position:absolute;display:block;width:244px;height:144px}
        </style>''' + "\n".join(tags))


first = {i: (i%2*250, i//2*150) for i in range(4)}
displaced = {i+4: xy for i, xy in first.items()}
all_sources = list(range(48))
fixture("under", [0, 1], {0: (0, 0), 1: (250, 0)})
fixture("fair", all_sources, first)
fixture("offscreen", all_sources, displaced)
fixture("duplicate", [0] + all_sources, {0: (0, 0), 1: (250, 0), 2: (0, 150), 3: (250, 150), 4: (0, 300)})
fixture("vector", all_sources, first, vector=True)
fixture("late", all_sources, first, prefix="late-assets")


class Handler(SimpleHTTPRequestHandler):
    early = False
    def do_GET(self):
        if self.path.startswith("/late-assets/"):
            if self.early and self.path.rsplit("/", 1)[1] not in (asset(0), asset(1)):
                self.send_error(404)
                return
            self.path = self.path.replace("/late-assets/", "/assets/", 1)
        super().do_GET()
    def log_message(self, form, *args):
        pass


@contextmanager
def serve():
    handler = partial(Handler, directory=site)
    with ThreadingHTTPServer(("127.0.0.1",0), handler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}"
        finally:
            server.shutdown()
            thread.join()


def render(role, prefix, jobs, capture=None):
    directory = out / prefix / role
    directory.mkdir(parents=True)
    job_input = directory / "jobs.jsonl"
    job_input.write_text("".join(json.dumps(dict(url=url,width=w,height=h,file=f"{case}.png"))+'\n'
                                 for case, url, w, h in jobs))
    command = ["deno", "run", "--no-config", "--no-npm", "--unstable-ffi", "-A"]
    env = dict(os.environ)
    if capture:
        env["REALPAGES_REPLAY"] = str(capture)
        env["REFTEST_TIME"] = "1"
        command += ["--preload", "core/labs/demos/foafnaut/realpages/replay.ts"]
    command += ["core/tests/browser-wpt/reftest-render.ts", "--native-engine", str(engines[role]),
                "--list", str(job_input), "--out", str(directory)]
    with (directory / "renderer.log").open("w") as log:
        subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=520)
    done = [json.loads(line.removeprefix("__done ")) for line in (directory / "renderer.log").read_text().splitlines()
            if line.startswith("__done ")]
    assert len(done) == len(jobs) and all(row["status"] == "ok" for row in done), (role, prefix, done)
    return directory


capture = root / "capture/bbc-uk-with-photos.zip"
with ZipFile(capture) as replay:
    manifest = json.loads(replay.read("manifest.json"))
    entries = {entry["url"]: entry for entry in manifest["entries"] if entry.get("body")}
    raw_html = replay.read(entries["https://www.bbc.co.uk/news"]["body"])
(out / "bbc-inputs.json").write_text(json.dumps({"archiveSha256":digest(capture.read_bytes()),"originalHtmlSha256":digest(raw_html)},indent=2))
bbc_jobs = [("bbc","https://www.bbc.co.uk/news",1280,735)]
for repeat, order in ((1, ("baseline","candidate")),(2,("candidate","baseline"))):
    for role in order:
        render(role,f"bbc-{repeat}",bbc_jobs,capture)

cases = ("under","fair","offscreen","duplicate","vector")
with serve() as url:
    for role in engines:
        render(role,"synthetic",[(case,f"{url}/{case}.html",510,480) for case in cases])
        Handler.early = True
        render(role,"early",[("late",f"{url}/late.html",510,480)])
        Handler.early = False
        render(role,"late",[("late",f"{url}/late.html",510,480)])

(out / "synthetic-source-sha256.json").write_text(json.dumps({
    str(path.relative_to(site)):digest(path.read_bytes()) for path in sorted(site.rglob("*")) if path.is_file()
},indent=2))
