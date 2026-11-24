import hashlib
import json
import pathlib
import sys
import zipfile

snapshot, target = map(pathlib.Path, sys.argv[1:])
target.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(snapshot) as archive:
    manifest = json.loads(archive.read("manifest.json"))
    entries = [entry for entry in manifest["entries"] if entry.get("body") and entry["status"] == 200]
    document = next(entry for entry in entries if entry["url"] == manifest["url"])
    (target / "page.html").write_bytes(archive.read(document["body"]))
    def stylesheet(entry):
        headers = {name.lower(): value for name, value in entry["headers"]}
        return headers.get("content-type", "").split(";", 1)[0].strip() == "text/css"
    css = {entry["url"]: archive.read(entry["body"]).decode("utf-8", errors="replace")
           for entry in entries if stylesheet(entry)}
    (target / "input.json").write_text(json.dumps({
        "url": manifest["url"],
        "width": int(manifest["viewport"].split("x")[0]),
        "snapshotSHA256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        "css": css
    }))
