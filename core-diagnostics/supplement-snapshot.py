import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import sys
from urllib import error, parse, request
from zipfile import ZIP_DEFLATED, ZipFile

source, watch_log, output, report = map(Path, sys.argv[1:])
sources = {
    "ichef.bbci.co.uk": (".webp", ".jpg", ".jpeg", ".png", ".avif"),
    "static.files.bbci.co.uk": (".js", ".css", ".png", ".woff2", ".svg"),
}
asset_limit = 2 * 1024 * 1024
total_limit = 12 * 1024 * 1024

def is_asset(url):
    parsed = parse.urlsplit(url)
    suffixes = sources.get(parsed.netloc.lower(), ())
    return parsed.scheme == "https" and not parsed.fragment and parsed.path.lower().endswith(suffixes)

class NoRedirects(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def read_asset(url):
    try:
        with request.build_opener(NoRedirects).open(url, timeout=12) as response:
            content_type = response.headers.get_content_type()
            if not (content_type.startswith(("image/", "font/")) or content_type in (
                "text/css", "text/javascript", "application/javascript", "application/font-woff2"
            )):
                return {"url": url, "failure": f"unexpected content type {content_type}"}, None
            body = response.read(asset_limit + 1)
            if not body or len(body) > asset_limit:
                return {"url": url, "failure": "body missing or above per-asset limit"}, None
            fields = [[k, v] for k, v in response.headers.items() if k.lower() not in {
                "set-cookie", "set-cookie2", "content-length", "content-encoding", "transfer-encoding"
            }]
            return {"url": url, "status": response.status, "statusText": response.reason,
                    "source": "supplement", "headers": fields, "bytes": len(body)}, body
    except (error.URLError, TimeoutError, OSError) as failure:
        return {"url": url, "failure": str(failure)}, None

with ZipFile(source) as original:
    manifest = json.loads(original.read("manifest.json"))
    captured = {entry["url"] for entry in manifest["entries"]}
    missing = set()
    for line in watch_log.read_text().splitlines():
        if not line.startswith('{"type":"realpages-replay-miss"'):
            continue
        url = json.loads(line)["url"]
        if url not in captured and is_asset(url):
            missing.add(url)

    added = 0
    evidence = []
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive, ThreadPoolExecutor(max_workers=5) as pool:
        for name in original.namelist():
            if name != "manifest.json":
                archive.writestr(name, original.read(name))
        for index, (receipt, blob) in enumerate(pool.map(read_asset, sorted(missing))):
            if blob and added + len(blob) <= total_limit:
                member = f"supplement/{index:04d}"
                archive.writestr(member, blob)
                manifest["entries"].append({**receipt, "body": member})
                evidence.append({**receipt, "sha256": hashlib.sha256(blob).hexdigest()})
                added += len(blob)
            else:
                evidence.append({"url": receipt["url"], "failure": receipt.get("failure", "total limit")})
        manifest["asset_supplement"] = {"utc": datetime.now(timezone.utc).isoformat(),
                                         "original_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
        manifest["bytes"] += added
        archive.writestr("manifest.json", json.dumps(manifest))

report.write_text(json.dumps(evidence, indent=2) + "\n")
if added == 0:
    raise SystemExit("No missing assets were available")
