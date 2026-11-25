from collections import Counter
from hashlib import sha256
from pathlib import Path
import json, sys

out = Path(sys.argv[1])
mode = sys.argv[2]
case = "desktop-bbc-news"
report = {}

def records(log):
    for line in log.read_text().splitlines():
        if line.startswith('{"'):
            try:
                yield json.loads(line)
            except ValueError:
                continue

for arm in ("a1","b1","b2","a2"):
    path = out / arm
    row, = json.loads((path / "summary.json").read_text())
    assert row["state"] == "presented" and row["documentColorsAtLeast"] >= 2, row
    assert row["firstFrame"]["engine"]["backend"] == "native", row
    assert row["scrollChangesPixels"], row
    first = row["firstFrame"]["t"]
    entries = [r for r in records(path / (case+".log")) if r.get("t",float("inf")) <= first]
    phase = {r["phase"]:r["t"] for r in entries if r["type"] == "startup-document-phase"}
    requests = [r for r in entries if r["type"] == "startup-sync-wire"]
    https = [r for r in requests if r["transfer"] == "pinned" and r["method"] == "GET"]
    assert https and any(r["status"] == 200 for r in https), (mode,arm,requests)
    reply_signature = [(r["host"],r["method"],r["transfer"],r["status"],r["bodyDigest"]) for r in requests]
    report[arm] = {
        "firstMs":row["presentedMs"],"windowMs":row["windowMs"],"scrollMs":row.get("scrollObservedMs"),
        "scriptStartMs":round(phase["script-ready"]-phase["script-start"],1),
        "pinnedFetchMs":round(sum(r["fetchMs"] for r in https),1),
        "pinnedRoutes":len({(entry["host"],entry["route"]) for entry in https}),
        "pinnedStatuses":dict(Counter(r["status"] for r in https)),
        "replies":len(requests),"repliesFingerprint":sha256(json.dumps(reply_signature).encode()).hexdigest(),
        "firstPng":sha256((path / (case+".png")).read_bytes()).hexdigest(),
        "spans":phase,
    }
summary = {"mode":mode,"arms":report,
           "identicalReplies":len({r["repliesFingerprint"] for r in report.values()})==1,
           "identicalPngs":len({r["firstPng"] for r in report.values()})==1}
(out / "pair.json").write_text(json.dumps(summary,indent=2)+"\n")
print("```json",json.dumps(summary,indent=2),"```",sep="\n")
if mode == "replay":
    assert summary["identicalReplies"],summary
