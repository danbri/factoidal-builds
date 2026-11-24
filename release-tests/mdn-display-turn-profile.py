import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

lab, engine, snapshot, out = map(Path, sys.argv[1:])
host = lab / "run_html.ts"
source = host.read_text()
anchor = '          scriptDone=(scriptCall("scriptSession","",{action:"advance",session:script.session,'
assert source.count(anchor) == 1
fingerprint = (3154, 1419073, 282, 5, 1, 7, "17:2 19:1 33:4")
command = [
    "deno", "run", "--no-check", "--no-config", "--no-npm", "--node-modules-dir=none",
    "--unstable-webgpu", "--unstable-ffi", "-A", "--preload", str(lab / "realpages/replay.ts"),
    str(host), "--native-engine", str(engine), "--offscreen", "--offscreen-size", "1280x800@1",
    "--no-state", "--be-liberal-in-what-we-accept", "--perf-summary",
    "--scroll-sweep", "--idle-checks-only", "--shot-at-end",
    "--url", "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/display",
]

def capture(arm, profile):
    marker = '          if(script.turn.startMore===true)trace("mdn-profile-advance",{session:script.session});\n'
    host.write_text(source.replace(anchor, marker + anchor) if profile else source)
    output, shot, stacks = (out / f"{arm}.{suffix}" for suffix in ("log", "png", "sample"))
    received, sampled = [], None
    with output.open("w") as log, (out / f"{arm}.sampler.log").open("w") as sampler_log, subprocess.Popen(
        command + ["--shot", str(shot)], cwd=lab, env={**os.environ, "REALPAGES_REPLAY": str(snapshot)},
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
    ) as proc:
        for line in proc.stdout:
            log.write(line)
            if not line.startswith("{"):
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            received.append(row)
            if profile and sampled is None and row.get("type") == "mdn-profile-advance":
                sampled = subprocess.Popen(
                    ["sudo", "-n", "sample", str(proc.pid), "2", "2", "-file", str(stacks)],
                    stdout=sampler_log, stderr=subprocess.STDOUT,
                )
        assert proc.wait() == 0, output
    if profile:
        assert sampled is not None and sampled.wait() == 0 and stacks.stat().st_size, output
    turns = [r for r in received if r.get("type") == "native-html-script" and r.get("cause") == "timers"]
    keys = ("clock", "instructions", "jobs", "tasks", "layouts", "reads", "readOps")
    target = [r for r in turns if tuple(r.get(k) for k in keys) == fingerprint]
    assert len(target) == 1 and target[0]["leanMs"] >= 2000, turns
    if profile:
        start = next(r for r in received if r.get("type") == "mdn-profile-advance")
        following = next(r for r in turns if r["t"] >= start["t"])
        assert following == target[0] and following["t"] - start["t"] >= 2000, (start, following)
    scroll = [r["ms"] for r in received if r.get("type") == "native-html-input-latency" and r.get("kind") == "scroll"]
    assert len(scroll) == 20 and shot.stat().st_size, (scroll, output)
    return {"turn": target[0], "scrollP95Ms": sorted(scroll)[18], "pixelsSha256": hashlib.sha256(shot.read_bytes()).hexdigest()}

groups = {
    "VM interpreter": ("L4Factoidal_JS_vmLoop", "L4Factoidal_JS_VM_"),
    "forced layout": ("WebDocument_readAnswer", "WebDocument_layout"),
    "layout tree": ("Rendering_Layout_",),
    "cascade": ("Rendering_Generated_styled", "Rendering_CSS_computeAll"),
    "selector matching": ("Rendering_CSS_match", "DOM_Selectors"),
    "text shaping": ("SfntShape_", "WebDocument_shapeKept", "bitmapOutline"),
    "native dispatch": ("web_document_call", "WebScripts_scriptSession"),
}

def stacks(path):
    nested, tally = [], collections.Counter()
    in_graph = False
    for line in path.read_text().splitlines():
        if line.startswith("Call graph:"):
            in_graph = True
            continue
        if line.startswith("Total number"):
            break
        if not in_graph:
            continue
        item = re.match(r"^([ +!|:-]*)(\d+)\s+(\S+)", line)
        if not item:
            continue
        depth, count, symbol = len(item[1]), int(item[2]), item[3]
        while nested and nested[-1][0] >= depth:
            nested.pop()
        active = nested[-1][1] if nested else set()
        here = {name for name, prefixes in groups.items() if any(p in symbol for p in prefixes)}
        for name in here - active:
            tally[name] += count
        nested.append((depth, active | here))
    assert tally["layout tree"] or tally["cascade"] or tally["VM interpreter"], path
    return dict(tally)

try:
    control = capture("control", False)
    sampled = capture("sampled", True)
finally:
    host.write_text(source)
report = {"control": control, "sampled": sampled,
          "sameScreenshot": control["pixelsSha256"] == sampled["pixelsSha256"],
          "inclusiveSamples": stacks(out / "sampled.sample")}
(out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
