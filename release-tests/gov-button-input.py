import base64
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
    css, fonts = {}, []
    for entry in entries:
        url = entry["url"]
        headers = {name.lower(): value for name, value in entry["headers"]}
        if headers.get("content-type", "").split(";", 1)[0].strip() == "text/css":
            css[url] = archive.read(entry["body"]).decode("utf-8", errors="replace")
        if url.endswith(".woff2"):
            data = archive.read(entry["body"])
            fonts.append({"url": url, "sha256": hashlib.sha256(data).hexdigest(),
                          "base64": base64.b64encode(data).decode("ascii")})
    (target / "input.json").write_text(json.dumps({
        "url": manifest["url"],
        "width": int(manifest["viewport"].split("x")[0]),
        "snapshotSHA256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        "css": css,
        "fonts": fonts
    }))
