from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

capture, survey, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
capture_bytes = capture.read_bytes()
assert sha256(capture_bytes).hexdigest() == "b32f0d193c4041b5703c13a2e8e5b6669223a33d9c3e216ed6d886fbfd9fe3f8"
log = "logs/desktop-bbc-news.watch.log"
if survey.is_dir():
    lines = (survey / log).read_text().splitlines()
else:
    with ZipFile(survey) as z:
        lines = z.read(log).decode().splitlines()
def bbc_photo(url):
    parsed = urlsplit(url)
    return parsed.scheme == "https" and parsed.netloc == "ichef.bbci.co.uk" and parsed.path.startswith("/ace/standard/")


wanted = set()
for line in lines:
    if not line.startswith('{"type":"realpages-replay-miss"'):
        continue
    url = json.loads(line)["url"]
    if bbc_photo(url):
        wanted.add(url)


def fetch(url):
    body, separator, metadata = subprocess.check_output(
        ["curl", "--proto", "=https", "--max-time", "20", "--max-filesize", "3000000",
         "--retry", "1", "-fsS", "-w", "\n%{http_code} %{content_type}", url]
    ).rpartition(b"\n")
    status, kind = (metadata.decode().split(" ", 1) if separator else ("", ""))
    assert status == "200" and kind.startswith("image/") and body, (url, status, kind, len(body))
    return url, kind, body


with ZipFile(BytesIO(capture_bytes)) as original:
    manifest = json.loads(original.read("manifest.json"))
    assert manifest["url"] == "https://www.bbc.co.uk/news"
    first = {}
    for item in manifest["entries"]:
        first.setdefault(item["url"], item)
    bodyless = {
        url for url, item in first.items()
        if bbc_photo(url) and item["status"] == 200 and not item.get("body")
    }
    missing = sorted((wanted - first.keys()) | bodyless)
    assert len(missing) > 10 and bodyless, (len(missing), len(bodyless))
    audit = {"requested": len(missing), "bodyless": len(bodyless), "responses": [], "misses": []}
    replacements = {}
    with ZipFile(output / "bbc-uk-with-photos.zip", "w", ZIP_DEFLATED) as bundle:
        for name in original.namelist():
            if name != "manifest.json":
                bundle.writestr(name, original.read(name))
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = [(url, pool.submit(fetch, url)) for url in missing]
            for index, (url, future) in enumerate(futures):
                try:
                    url, kind, body = future.result()
                except (subprocess.SubprocessError, AssertionError) as error:
                    audit["misses"].append({"url": url, "reason": str(error)})
                    continue
                name = f"bodies/foafnaut-photos/{index:03d}"
                bundle.writestr(name, body)
                replacements[url] = {
                    "url": url, "status": 200, "headers": [["content-type", kind]], "body": name,
                    "bytes": len(body), "source": "foafnaut-photo-recapture",
                }
                audit["responses"].append({"url": url, "type": kind, "bytes": len(body), "sha256": sha256(body).hexdigest()})
        # Replay serves the first recorded entry for a URL. Remove the bodyless placeholder.
        manifest["entries"] = [item for item in manifest["entries"] if item["url"] not in replacements]
        manifest["entries"].extend(replacements.values())
        leading = ("8e201a50", "c4219c10", "006fad50", "43f09a20")
        visible = [url for url in bodyless if any(key in url for key in leading)]
        assert set(visible).issubset(replacements), [url for url in visible if url not in replacements]
        assert len({key for key in leading if any(key in url for url in visible)}) == len(leading), visible
        bundle.writestr("manifest.json", json.dumps(manifest))
(output / "photo-coverage.json").write_text(json.dumps(audit, indent=2) + "\n")
print(f"Added {len(audit['responses'])} of {audit['requested']} recorded UK photo requests.")
assert len(audit["responses"]) >= 10
