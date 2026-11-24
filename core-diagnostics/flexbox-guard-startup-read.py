import hashlib
import json
import pathlib
import sys
import zipfile

source, out = map(pathlib.Path, sys.argv[1:])
url = "https://www.w3.org/scripts/TR/2021/fixup.js"
needle = b"var tocHeight = tocNav.offsetHeight;"
replacement = b"var tocHeight; if (!skipScroll) tocHeight = tocNav.offsetHeight;"
with zipfile.ZipFile(source) as original:
    manifest = json.loads(original.read("manifest.json"))
    entry = next(row for row in manifest["entries"] if row["url"] == url)
    javascript = original.read(entry["body"])
    assert javascript.count(needle) == 1
    changed = javascript.replace(needle, replacement)
    entry["bytes"] = len(changed)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as derived:
        for name in original.namelist():
            body = changed if name == entry["body"] else original.read(name)
            if name == "manifest.json":
                body = json.dumps(manifest).encode()
            derived.writestr(name, body)
print(json.dumps({"resource": url,
                  "original": hashlib.sha256(javascript).hexdigest(),
                  "guarded": hashlib.sha256(changed).hexdigest()}, indent=2))
