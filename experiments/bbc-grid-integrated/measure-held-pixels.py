from collections import Counter
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import json

from PIL import Image

root = Path("out")
data = json.loads((root / "document-image-keys.json").read_text())
with ZipFile("capture/bbc-uk-with-photos.zip") as replay:
    entries = {entry["url"]: entry for entry in json.loads(replay.read("manifest.json"))["entries"]
               if entry.get("body")}
    rows = []
    unknown = []
    for key in dict.fromkeys(data["pictures"]):
        if key not in data["held"]:
            continue
        if key not in entries:
            unknown.append({"key": key, "reason": "held URL absent from capture manifest"})
            continue
        source = replay.read(entries[key]["body"])
        if sha256(source).hexdigest() != data["held"][key]:
            unknown.append({"key": key, "reason": "replay body has different SHA-256"})
            continue
        try:
            with Image.open(BytesIO(source)) as image:
                if image.format not in ("JPEG", "PNG", "GIF", "WEBP"):
                    unknown.append({"key": key, "format": image.format})
                    continue
                rows.append({"key": key, "pixels": image.size, "format": image.format})
        except OSError:
            unknown.append({"key": key, "reason": "file lacks known raster dimensions"})
    def cost(factor):
        return sum(w*h if w*h <= 4096 else ((w+factor-1)//factor)*((h+factor-1)//factor)
                   for w,h in (row["pixels"] for row in rows))
    result = {"counts": dict(Counter(row["format"] for row in rows)),
              "headerPixelTotals": {k: cost(k) for k in range(1,7)},
              "verifiedKnown": rows, "unclassified": unknown}
    (root / "document-image-cost.json").write_text(json.dumps(result, indent=2) + "\n")
    print(result["counts"], result["headerPixelTotals"], len(unknown))
