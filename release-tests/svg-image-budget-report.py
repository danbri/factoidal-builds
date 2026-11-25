import json
from pathlib import Path
import sys

out = Path(sys.argv[1])
results = {}
print("| Page | Arm | Whole replay s | Page load and raster ms | Compile-only render ms | Peak RSS MiB |")
print("|---|---|---:|---:|---:|---:|")
for page in ("w3c", "bbc", "wiki-mobile", "w3c-flexbox"):
    rows = {}
    for arm in ("a1", "b1", "b2", "a2"):
        key = f"{page}-{arm}"
        log = (out / f"{key}.log").read_text().splitlines()
        draw, = [json.loads(line.removeprefix("__done ")) for line in log if line.startswith("__done ")]
        phase, = [json.loads(line) for line in log if line.startswith('{"type":"reftest-time"')]
        assert draw["status"] == "ok" and draw["file"] == phase["file"] == f"{key}.png", draw
        assert (out / draw["file"]).stat().st_size
        elapsed, rss = (out / f"{key}.time").read_text().split()
        rows[arm] = {"elapsedSeconds": float(elapsed), "rssKiB": int(rss),
                     "draw": draw, "compileOnly": phase}
        print(f"| {page} | {arm} | {elapsed} | {draw['ms']} | {phase['ms']} | {int(rss)/1024:.1f} |")
    results[page] = {"arms": rows, "matchingRaster": len({r["draw"]["sha"] for r in rows.values()}) == 1}
(out / "report.json").write_text(json.dumps(results, indent=2) + "\n")
print()
print("The replay uses the same native CPU path and includes an extra compile-only render measurement.")
