"""Compare native first layout with the exact baseline and candidate."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

lab, baseline, candidate, out = map(Path, sys.argv[1:5])
case = sys.argv[5]
size, url = {
    "wp-us": ("1280x800", "https://en.wikipedia.org/wiki/United_States"),
    "m-us": ("412x860", "https://en.wikipedia.org/wiki/United_States?useskin=minerva"),
}[case]
host = lab / "run_html.ts"
out.mkdir(exist_ok=True)

def capture(name, engine):
    log = out / f"{name}.log"
    shot = out / f"{name}.png"
    args = [
        "deno", "run", "--no-check", "--no-config", "--no-npm", "--node-modules-dir=none",
        "--unstable-webgpu", "--unstable-ffi", "-A", "--preload", str(lab / "realpages/replay.ts"),
        str(host), "--native-engine", str(engine), "--offscreen", "--offscreen-size", size + "@1",
        "--no-state", "--be-liberal-in-what-we-accept", "--perf-summary", "--watch-sweep", "5",
        "--shot", str(shot), "--shot-at-end", "--url", url,
    ]
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
        assert browser.wait() == 0, log
    frame = next(row for row in rows if row.get("type") == "native-html-frame" and row.get("presented"))
    loaded = next(row for row in rows if row.get("type") == "native-html-loaded")
    replay = [row for row in rows if row.get("type") == "realpages-replay"][-1]
    assert loaded["url"] == url and loaded["links"] > 10000 and replay["hits"] > 15, (loaded, replay)
    assert frame["compiledIn"] == "worker" and frame["workerMs"] > 0, frame
    return {"first": frame, "loaded": loaded, "replay": replay,
            "terminalPng": hashlib.sha256(shot.read_bytes()).hexdigest()}

arms = {}
for name, engine in (("a1", baseline), ("b1", candidate), ("b2", candidate), ("a2", baseline)):
    arms[name] = capture(name, engine)
report = {"case": case, "arms": arms,
          "sameTerminalPng": len({r["terminalPng"] for r in arms.values()}) == 1}
(out / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
assert report["sameTerminalPng"], case
