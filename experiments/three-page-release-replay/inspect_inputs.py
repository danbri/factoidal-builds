"""Verify a fixture before replay and save its Chrome reference."""
import hashlib
import json
from pathlib import Path
import struct
import sys
from zipfile import ZipFile

fixtures, site, archive, output = sys.argv[1:]
case = json.loads(Path(fixtures).read_text())[site]
out = Path(output)
out.mkdir(parents=True, exist_ok=True)


def check(data, expected, label):
    digest = hashlib.sha256(data).hexdigest()
    assert digest == expected, (label, digest, expected)
    return digest


check(Path(archive).read_bytes(), case["archive_sha256"], "archive")
with ZipFile(archive) as capture:
    manifest = json.loads(capture.read("manifest.json"))
    assert manifest["id"] == case["id"], manifest["id"]
    entries = {e["url"]: e for e in manifest["entries"] if e.get("body")}
    document = entries[case["url"]]
    assert document["status"] == 200 and document["type"] == "Document"
    check(capture.read(document["body"]), case["html_sha256"], "HTML")
    for url, digest in case.get("assets", {}).items():
        check(capture.read(entries[url]["body"]), digest, url)
    reference = capture.read("reference.png")
    check(reference, case["reference_sha256"], "Chrome PNG")
    width, height = struct.unpack(">II", reference[16:24])
    assert (width, height) == (1280, 735), (width, height)

(out / "chrome.png").write_bytes(reference)
(out / "fixture.json").write_text(json.dumps(case, indent=2) + "\n")
job = {"url": case["url"], "width": width, "height": height, "file": "page.png"}
(out / "jobs.jsonl").write_text(json.dumps(job) + "\n")
