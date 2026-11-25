from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

out = Path(sys.argv[1])
case, mode = sys.argv[2:]

def records(path):
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except ValueError:
                continue

runs = []
for rep in ("run1", "run2"):
    row, = json.loads((out / rep / "summary.json").read_text())
    assert row["state"] == "presented" and row["documentColorsAtLeast"] >= 2, row
    assert row["firstFrame"]["engine"]["backend"] == "native", row
    trace = list(records(out / rep / f"{case}.log"))
    first = row["firstFrame"]["t"]
    trace = [r for r in trace if r.get("t", float("inf")) <= first]
    phases = {r["phase"]: round(r["t"], 2) for r in trace
              if r["type"] == "startup-document-phase"}
    assert phases["prepare-enter"] <= phases["script-resources-ready"] <= first, phases
    if case == "desktop-bbc-news":
        assert phases["script-start"] <= phases["script-ready"], phases
    wires = defaultdict(lambda: {"count":0, "fetchMs":0, "engineMs":0, "statuses": Counter()})
    for r in trace:
        if r["type"] == "startup-sync-wire":
            group = wires[f'{r["host"]} {r["transfer"]}']
            group["count"] += 1
            group["fetchMs"] += r["fetchMs"]
            group["engineMs"] += r["engineMs"]
            group["statuses"][str(r["status"])] += 1
    runs.append({"run":rep, "windowMs":row["windowMs"], "presentedMs":row["presentedMs"],
                 "layoutMs":row["firstFrame"]["layoutMs"], "graphicsMs":row["firstFrame"]["sessionMs"],
                 "phases":phases, "wires":dict(wires), "scrollChangesPixels":row.get("scrollChangesPixels")})
report = {"case":case, "mode":mode, "runs":runs}
(out / "report.json").write_text(json.dumps(report, indent=2)+"\n")
print("```json", json.dumps(report, indent=2), "```", sep="\n")
