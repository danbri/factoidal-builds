"""Prepare ephemeral script-isolation archives from one frozen specification."""
import hashlib
import json
import pathlib
import re
import sys
import zipfile

source, out = map(pathlib.Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
url = "https://www.w3.org/TR/css-flexbox-1/"
markers = {
    "no-fixup": b"https://www.w3.org/scripts/TR/2021/fixup.js",
    "no-dfn-panel": b"/* Boilerplate: script-dfn-panel */",
    "no-ref-hints": b"/* Boilerplate: script-ref-hints */",
    "no-wpt": b"/* Boilerplate: script-wpt */",
}
pattern = re.compile(rb"<script\b([^>]*)>(.*?)</script\s*>", re.IGNORECASE | re.DOTALL)
def sha(data):
    return hashlib.sha256(data).hexdigest()

with zipfile.ZipFile(source) as original:
    manifest = json.loads(original.read("manifest.json"))
    entry = next(row for row in manifest["entries"] if row["url"] == url)
    html = original.read(entry["body"])
    receipt = {"archive": sha(source.read_bytes()), "html": sha(html), "variants": {}}
    for label, marker in markers.items():
        matches = [match for match in pattern.finditer(html) if marker in match.group(0)]
        assert len(matches) == 1, label
        script = matches[0]
        assert b"type=" not in script.group(1), label
        i = script.start() + len(b"<script")
        variant = html[:i] + b' type="application/json"' + html[i:]
        entry["bytes"] = len(variant)
        target = out / (label + ".zip")
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as derived:
            for name in original.namelist():
                body = variant if name == entry["body"] else original.read(name)
                if name == "manifest.json":
                    body = json.dumps(manifest).encode()
                derived.writestr(name, body)
        receipt["variants"][label] = {"html": sha(variant), "archive": sha(target.read_bytes())}
print(json.dumps(receipt, indent=2))
