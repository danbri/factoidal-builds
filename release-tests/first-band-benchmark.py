import hashlib
import json
import os
from pathlib import Path
from statistics import median
import subprocess
import sys

lab, baseline, candidate, data, out = map(Path, sys.argv[1:])
out.mkdir(exist_ok=True)
cases = [
    ("mdn", "developer.mozilla.org/mdn-display-20261115.zip",
     "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/display", "1280x800", True),
    ("mdn-static", "developer.mozilla.org/mdn-display-20261115.zip",
     "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/display", "1280x800", False),
    ("wiki-mobile", "en.wikipedia.org/m-us-20261115.zip",
     "https://en.wikipedia.org/wiki/United_States?useskin=minerva", "412x860", True),
    ("govuk", "desktop-govuk.zip", "https://www.gov.uk/", "1280x800", True),
    ("w3c", "desktop-w3c-home.zip", "https://www.w3.org/", "1280x800", True),
    ("govuk-static", "desktop-govuk.zip", "https://www.gov.uk/", "1280x800", False),
    ("w3c-static", "desktop-w3c-home.zip", "https://www.w3.org/", "1280x800", False),
    ("hn-static", "news.ycombinator.com/hn-20261115.zip", "https://news.ycombinator.com/", "1280x800", False),
]

def read_records(path):
    result = []
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("{"):
            try:
                result.append(json.loads(line))
            except ValueError:
                continue
    return result

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def capture(case, arm, engine):
    name, archive, url, size, scripts = case
    run = out / f"{name}-{arm}"
    run.mkdir()
    cache = run / "cache"
    cache.mkdir()
    (run / "runtime").mkdir(mode=0o700)
    shot, log, rss = (run / f"frame.{ext}" for ext in ("png", "log", "rss"))
    argv = [
        "/usr/bin/time", "-f", "%M", "-o", str(rss),
        "deno", "run", "--no-check", "--no-config", "--no-npm", "--node-modules-dir=none",
        "--unstable-webgpu", "--unstable-ffi", "-A", "--preload", str(lab / "realpages/replay.ts"),
        str(lab / "run_html.ts"), "--native-engine", str(engine), "--offscreen",
        "--offscreen-size", size + "@1", "--no-state", "--be-liberal-in-what-we-accept",
        "--perf-summary", "--scroll-sweep", "--idle-checks-only", "--shot", str(shot), "--shot-at-end",
        "--url", url,
    ]
    if not scripts:
        argv.append("--no-scripts")
    env = {**os.environ, "REALPAGES_REPLAY": str(data / archive),
           "XDG_CACHE_HOME": str(cache), "XDG_RUNTIME_DIR": str(run / "runtime")}
    # One software driver setting across all arms, with each process starting cold.
    with log.open("w") as stream:
        subprocess.run(argv, cwd=lab, env=env, stdout=stream, stderr=subprocess.STDOUT,
                       timeout=200, check=True)
    records = read_records(log)
    renderer = [r for r in records if r.get("type") == "native-html-engine"]
    assert any(r.get("engine", "").startswith(f"native {engine}") for r in renderer), renderer
    frames = [r for r in records if r.get("type") == "native-html-frame" and r.get("presented")]
    first = frames[0]
    if name == "wiki-mobile":
        loads = [r for r in records if r.get("type") == "native-html-loaded" and r.get("url") == url]
        assert loads and max(r["links"] for r in loads) > 1000, (url, loads, log)
    assert f'{first["width"]}x{first["height"]}' == size, first
    wheel = sorted(r["ms"] for r in records if r.get("type") == "native-html-input-latency" and r.get("kind") == "scroll")
    shifts = [r for r in records if r.get("type") == "native-html-scroll" and r.get("presented")]
    assert wheel and shifts and shot.stat().st_size, log
    last_position = None
    for row in records:
        if row.get("type") == "native-html-frame" and row.get("presented") and "layers" in row:
            last_position = row["layers"]["bandTop"] + row["layers"]["offset"]
        elif row.get("type") == "native-html-scroll" and row.get("presented") and row.get("exact"):
            last_position = row["scroll"]
    requested = shifts[-1]["scroll"]
    if not scripts:
        assert last_position == requested, (last_position, shifts[-1])
    replay = next((r for r in reversed(records) if r.get("type") == "realpages-replay"), {})
    return {
        "firstMs": first["t"], "firstLayoutMs": first["layoutMs"], "firstGraphicsMs": first["sessionMs"],
        "rows": first["layers"]["bandHeight"], "rssKiB": int(rss.read_text().strip()),
        "scrollCount": len(wheel), "scrollP50Ms": median(wheel), "scrollP95Ms": wheel[(95*len(wheel)+99)//100-1],
        "lastScroll": last_position, "lastRequested": requested, "clamped": sum(not row["exact"] for row in shifts),
        "frames": len(frames), "pixels": digest(shot), "replay": replay,
    }

def pixel_delta(left, right, size):
    width, height = map(int, size.split("x"))
    def rgba(path):
        pixels = subprocess.check_output(
            ["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgba", "-"]
        )
        if len(pixels) != width * height * 4:
            raise ValueError(f"Unexpected RGBA size in {path}: {len(pixels)}")
        return pixels

    a, b = rgba(left), rgba(right)
    changed = 0
    max_channel_delta = 0
    bounds = [width, height, 0, 0]
    for i in range(0, len(a), 4):
        if a[i:i + 4] == b[i:i + 4]:
            continue
        x, y = (i // 4) % width, (i // 4) // width
        changed += 1
        bounds = [min(bounds[0], x), min(bounds[1], y), max(bounds[2], x), max(bounds[3], y)]
        max_channel_delta = max(max_channel_delta, *(abs(a[j] - b[j]) for j in range(i, i + 4)))
    return {"changedPixels": changed, "boundsInclusive": bounds if changed else None,
            "maxChannelDelta": max_channel_delta}

for case in cases:
    if os.environ.get("BENCHMARK_CASE") not in (None, case[0]):
        continue
    name, archive, _, size, scripts = case
    run = {}
    for arm, engine in (("a1", baseline), ("b1", candidate), ("b2", candidate), ("a2", baseline)):
        record = capture(case, arm, engine)
        run[arm] = record
        print(json.dumps({"case": name, "arm": arm, **record}), flush=True)
    report = {"case": name, "archiveSha256": digest(data / archive), "arms": run}
    report["sameTerminalPng"] = len({(r["lastScroll"], r["pixels"]) for r in run.values()}) == 1
    report["pixelComparisons"] = {}
    for first, second in (("a1", "a2"), ("b1", "b2"), ("a1", "b1"), ("a2", "b2")):
        if run[first]["lastScroll"] == run[second]["lastScroll"]:
            report["pixelComparisons"][f"{first}:{second}"] = pixel_delta(
                out / f"{name}-{first}/frame.png", out / f"{name}-{second}/frame.png", size
            )
    (out / f"{name}.json").write_text(json.dumps(report, indent=2) + "\n")
    if not scripts:
        assert report["sameTerminalPng"], report
