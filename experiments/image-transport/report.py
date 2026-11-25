"""Read the measured transfer phases and check that the paired runs agree."""
from hashlib import sha256
import json
from pathlib import Path
import sys

root, case = Path(sys.argv[1]), sys.argv[2]
arms = {}
for arm in ("a1", "b1", "b2", "a2"):
    folder = root / arm
    report, = json.loads((folder / "summary.json").read_text())
    records = []
    for line in (folder / f"{case}.log").read_text(errors="replace").splitlines():
        if line.startswith("{"):
            try:
                record = json.loads(line)
                if record.get("t", float("inf")) <= report["firstFrame"]["t"]:
                    records.append(record)
            except ValueError:
                continue
    phases = {r["phase"]: r["t"] for r in records if r.get("type") == "startup-document-phase"}
    batches = [r for r in records if r.get("type") == "startup-image-batch"]
    assert batches and max(b["loaded"] for b in batches) > 0, (case, arm, batches)
    assert report["state"] == "presented" and report["scrollChangesPixels"], report
    assert report["firstFrame"]["engine"]["backend"] == "native" and report["documentColorsAtLeast"] >= 2, report
    arms[arm] = {
        "firstMs": report["presentedMs"],
        "imageWaitMs": phases["images-bytes-ready"] - phases["images-wait-start"],
        "imageBatches": batches,
        "firstPng": sha256((folder / f"{case}.png").read_bytes()).hexdigest(),
    }

def images(arm):
    return sorted((b["wanted"], b["loaded"], b["bytes"], b["fingerprint"])
                  for b in arm["imageBatches"])

same_images = all(images(arm) == images(arms["a1"]) for arm in arms.values())
same_png = len({arm["firstPng"] for arm in arms.values()}) == 1
record = {"case": case, "sameOrderedImagesPerBatch": same_images, "sameFirstPng": same_png, "arms": arms}
(root / "comparison.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
if not (same_images and same_png):
    raise SystemExit("Live arms changed inputs or rendering. Compare the recorded receipts before drawing a timing conclusion.")
