"""Sample the actual native worker during the initial Wikipedia layout."""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

lab, engine, out = map(Path, sys.argv[1:4])
case = sys.argv[4]
size, url = {
    "wp-us": ("1280x800", "https://en.wikipedia.org/wiki/United_States"),
    "m-us": ("412x860", "https://en.wikipedia.org/wiki/United_States?useskin=minerva"),
}[case]
host = lab / "run_html.ts"
text = host.read_text()
anchor = '          if(worker?.alive){({layers:nextLayers,workerMs}=await worker.compileLayers(request.source,sentWidth,sentHeight,request.options));bandMs=workerMs;}'
assert text.count(anchor) == 1
prefix = """          if(frameNumber===0)console.log(JSON.stringify({
            type:"wiki-first-worker",width:sentWidth,height:sentHeight,worker:!!worker?.alive}));
"""
host.write_text(text.replace(anchor, prefix + anchor))
out.mkdir(exist_ok=True)

def capture(name, sample):
    log = out / f"{name}.log"
    shot = out / f"{name}.png"
    args = [
        "deno", "run", "--no-check", "--no-config", "--no-npm", "--node-modules-dir=none",
        "--unstable-webgpu", "--unstable-ffi", "-A", "--preload", str(lab / "realpages/replay.ts"),
        str(host), "--native-engine", str(engine), "--offscreen", "--offscreen-size", size + "@1",
        "--no-state", "--be-liberal-in-what-we-accept", "--perf-summary", "--watch-sweep", "10",
        "--shot", str(shot), "--shot-at-end", "--url", url,
    ]
    sampler = None
    rows = []
    with log.open("w") as stream, subprocess.Popen(args, cwd=lab, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, bufsize=1) as browser:
        for line in browser.stdout:
            print(line, end="", file=stream)
            if not line.startswith("{"):
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            rows.append(row)
            if row.get("type") == "wiki-first-worker" and sample and sampler is None:
                assert row["worker"] and f'{row["width"]}x{row["height"]}' == size, row
                sampler = subprocess.Popen(["sudo", "sample", str(browser.pid), "8", "2",
                                            "-file", str(out / "initial.sample")])
        assert browser.wait() == 0, log
    if sample:
        assert sampler is not None and sampler.wait(timeout=20) == 0, log
    frame = next(row for row in rows if row.get("type") == "native-html-frame" and row.get("presented"))
    loaded = next(row for row in rows if row.get("type") == "native-html-loaded")
    replay = [row for row in rows if row.get("type") == "realpages-replay"][-1]
    assert loaded["url"] == url and loaded["links"] > 10000 and replay["hits"] > 15, (loaded, replay)
    assert frame["compiledIn"] == "worker" and frame["workerMs"] >= 8000, frame
    return {"first": frame, "loaded": loaded, "replay": replay,
            "terminalPng": hashlib.sha256(shot.read_bytes()).hexdigest()}

try:
    controls = {"plain": capture("plain", False), "sampled": capture("sampled", True)}
finally:
    host.write_text(text)

# Count inclusively, once per group per stack. Across groups the counts overlap.
groups = {
    "layout": ("Rendering_Layout_", "Rendering_LayoutTask_"),
    "selector matching": ("matchEntry", "matchGroupedEntry", "DOM_Selectors"),
    "cascade": ("Generated_styled", "CSS_compute"),
    "style application": ("Rendering_CSS_apply",),
    "text shaping": ("SfntShape_", "shapeKept", "bitmapOutline"),
    "SVG raster": ("SVGRaster", "rasterFast", "vectorPicture"),
    "image decode": ("storeIn", "decodeWith", "pageStore"),
    "serialization": ("packScene", "BatchedRender", "frameReply", "sceneJson", "Json_compress"),
}
ancestors = []
counts = collections.Counter()
for line in (out / "initial.sample").read_text().partition("Call graph:")[2].split("Total number in stack")[0].splitlines():
    item = re.match(r"^([ +!|:-]*)(\d+)\s+(\S+)", line)
    if not item:
        continue
    depth, count, symbol = len(item[1]), int(item[2]), item[3]
    while ancestors and ancestors[-1][0] >= depth:
        ancestors.pop()
    parent = ancestors[-1][1] if ancestors else set()
    matched = {name for name, names in groups.items() if any(key in symbol for key in names)}
    for name in matched - parent:
        counts[name] += count
    ancestors.append((depth, parent | matched))
assert counts["layout"] or counts["cascade"], counts
report = {"case":case, "arms":controls, "inclusiveSamples":dict(counts),
          "sameTerminalPng": controls["plain"]["terminalPng"] == controls["sampled"]["terminalPng"]}
(out / "profile.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
