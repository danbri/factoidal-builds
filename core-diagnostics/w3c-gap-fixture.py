import base64
import json
import sys
from zipfile import ZipFile

with ZipFile(sys.argv[1]) as archive:
    entries = json.loads(archive.read("manifest.json"))["entries"]
    fixture = {"css": {}, "images": {}}
    for entry in entries:
        if entry["status"] != 200 or not entry.get("body"):
            continue
        url = entry["url"]
        mime = dict(entry["headers"]).get("content-type", "").split(";")[0]
        if url == "https://www.w3.org/" and mime == "text/html":
            fixture["html"] = archive.read(entry["body"]).decode()
        elif mime == "text/css":
            fixture["css"][url] = archive.read(entry["body"]).decode()
        elif url.endswith(("/svg/w3c.svg", "/groups-2025.svg")):
            fixture["images"][url] = base64.b64encode(archive.read(entry["body"])).decode()
assert "html" in fixture and len(fixture["css"]) >= 2 and len(fixture["images"]) == 2
print(json.dumps(fixture))
