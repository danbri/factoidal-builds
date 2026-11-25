from collections import Counter
from hashlib import sha256
from pathlib import Path
import json, sys

out = Path(sys.argv[1])
case = sys.argv[2]
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
    font = [r for r in entries if r["type"] == "startup-web-font"]
    assert font and font[0]["phase"]=="discover",font
    transfers = [r for r in font if r["phase"] in {"loaded","refused"}]
    report[arm] = {
        "firstMs":row["presentedMs"],"windowMs":row["windowMs"],"scrollMs":row.get("scrollObservedMs"),
        "documentMs":round(phase["script-resources-ready"]-phase["prepare-enter"],1),
        "fontReadyMs":round(phase["web-fonts-ready"]-phase["prepare-enter"],1),
        "fontDiscoveryMs":round(font[0]["ms"],1),
        "fontTransferMs":round(sum((r.get("readMs") or r["ms"]) for r in transfers),1),
        "fontRegistrationMs":round(sum(r["ms"]-r["readMs"] for r in transfers if r.get("readMs") is not None),1),
        "fontCount":dict(Counter(r["phase"] for r in transfers)),
        "fonts":[r["sha256"] for r in transfers if r["phase"]=="loaded"],
        "phase":phase,
        "firstPng":sha256((path / (case+".png")).read_bytes()).hexdigest(),
    }
summary = {"case":case,"arms":report,
           "identicalFonts":len({tuple(r["fonts"]) for r in report.values()})==1,
           "identicalPngs":len({r["firstPng"] for r in report.values()})==1}
(out / "pair.json").write_text(json.dumps(summary,indent=2)+"\n")
print("```json",json.dumps(summary,indent=2),"```",sep="\n")
