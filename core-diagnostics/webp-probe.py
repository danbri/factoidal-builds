from pathlib import Path
import json
import sys
from zipfile import ZipFile

mode, source, dest = sys.argv[1:]
if mode == "extract":
    expected = {}
    with ZipFile(source) as z:
        for entry in json.loads(z.read("manifest.json"))["entries"]:
            if dict(entry["headers"]).get("content-type") != "image/webp":
                continue
            b = z.read(entry["body"])
            assert b[:4] == b"RIFF" and b[8:12] == b"WEBP"
            pos = 12
            alpha = False
            while pos + 8 <= len(b):
                kind = b[pos:pos+4]
                size = int.from_bytes(b[pos+4:pos+8], "little")
                if kind == b"ALPH":
                    alpha = True
                elif kind == b"VP8 ":
                    assert b[pos+11:pos+14] == b"\x9d\x01\x2a"
                    width = int.from_bytes(b[pos+14:pos+16], "little") & 0x3fff
                    height = int.from_bytes(b[pos+16:pos+18], "little") & 0x3fff
                    name = Path(entry["body"]).name + ".webp"
                    expected[name] = [width, height, alpha]
                    (Path(dest) / name).write_bytes(b)
                    break
                pos += 8 + size + size % 2
            else:
                raise AssertionError(f"no VP8 in {entry['url']}")
    assert len(expected) == 11 and sum(x[2] for x in expected.values()) == 1
    print(json.dumps(expected))
else:
    expected = json.loads(Path(source).read_text())
    actual = {}
    for line in Path(dest).read_text().splitlines():
        path, encoding, width, height, alpha = line.split("\t")
        assert encoding.endswith(".vp8") or encoding == "vp8", encoding
        actual[Path(path).name] = [int(width), int(height), alpha == "true"]
    assert actual == expected, (expected, actual)
    print(f"Matched VP8 width, height and alpha for {len(actual)} archived BBC images.")
