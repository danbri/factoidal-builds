import json
import re
import sys
import zipfile

with zipfile.ZipFile(sys.argv[1]) as snapshot:
    manifest = json.loads(snapshot.read("manifest.json"))
    url = manifest["reference"]["document_url"]
    document = next(entry for entry in manifest["entries"] if entry["url"] == url)
    html = snapshot.read(document["body"]).decode("utf-8")

assert url == "https://www.bbc.com/news" and document["source"] == "chrome"
nodes = []
for svg in re.findall(r"<svg\b[^>]*>[\s\S]*?</svg>", html, re.I):
    start = svg.split(">", 1)[0]
    category = re.search(r'\scategory="([^"]+)"', start)
    if category is None:
        continue
    icon = re.search(r'\sicon="([^"]+)"', start)
    assert icon is not None
    without_labels = re.sub(r'\s(?:category|icon)="[^"]+"', "", start) + svg[len(start):]
    nodes.append({"category": category.group(1), "icon": icon.group(1),
                  "original": svg, "control": without_labels})

assert len(nodes) == 31, len(nodes)
print(json.dumps({"url": url, "nodes": nodes}))
