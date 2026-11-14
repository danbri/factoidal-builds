#!/usr/bin/env python3
"""The render report: a fixed list of original fixture pages drawn by the engine on each
platform, and the differences between two platforms.

  draw     run core's scene producer (labs/demos/foafnaut/.build/web-render/web-render-native,
           made by build-web-render.sh --native) on every page of the list: the checked
           scene (what the GPU would paint: sha256, and the bytes gzipped) at 800x600, and
           the CPU reference pixels as a PNG at 200x150 when they come within the time
           limit (the CPU rasteriser is slow on pages with much text). Writes manifest.json.
  compare  two draw directories of one core commit (Linux and macOS): for each page, are
           the scenes the same bytes, and how many pixels of the PNGs differ (count,
           largest channel difference). Writes report.md, report.json and a difference
           image for each page whose pixels differ.

The pages are core's own fixtures (labs/demos/foafnaut/web-render/fixtures/*.html, original
constructs); no page of a real site is drawn or stored. This is a check that the two
builds of one commit draw the same thing, not a check against another browser.
"""
import argparse, gzip, hashlib, json, os, struct, subprocess, sys, time, zlib

SCENE_SIZE = (800, 600)
PIXEL_SIZE = (200, 150)


def png_bytes(width, height, rgb):
    """An 8-bit RGB PNG from a flat list of width*height*3 values."""
    raw = bytearray()
    row = width * 3
    for y in range(height):
        raw.append(0)
        raw += bytes(rgb[y * row:(y + 1) * row])
    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def png_read(path):
    """(width, height, bytes RGB) of a PNG written by png_bytes (filter 0 rows only)."""
    data = open(path, "rb").read()
    pos, idat, width, height = 8, b"", 0, 0
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if kind == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
        elif kind == b"IDAT":
            idat += body
        pos += 12 + n
    raw = zlib.decompress(idat)
    row = width * 3
    out = bytearray()
    for y in range(height):
        line = raw[y * (row + 1):(y + 1) * (row + 1)]
        if line[0] != 0:
            raise ValueError(f"{path}: PNG filter {line[0]} (only files of this tool are read)")
        out += line[1:]
    return width, height, bytes(out)


def cmd_draw(a):
    os.makedirs(os.path.join(a.out, "scenes"), exist_ok=True)
    os.makedirs(os.path.join(a.out, "png"), exist_ok=True)
    pages = sorted(f for f in os.listdir(a.fixtures) if f.endswith(".html"))
    manifest = {"format": "factoidal-render-draw-v1", "platform": a.platform, "core_commit": a.commit, "scene_size": SCENE_SIZE,
                "pixel_size": PIXEL_SIZE, "pixel_limit_seconds": a.pixel_seconds, "pages": {}}
    for page in pages:
        src = os.path.join(a.fixtures, page)
        name = page[:-5]
        e = {"source_sha256": hashlib.sha256(open(src, "rb").read()).hexdigest()}
        t0 = time.time()
        try:
            p = subprocess.run([a.bin, src, str(SCENE_SIZE[0]), str(SCENE_SIZE[1])], capture_output=True, timeout=120)
            scene = p.stdout
            e.update(scene_exit=p.returncode, scene_bytes=len(scene), scene_sha256=hashlib.sha256(scene).hexdigest(),
                     scene_seconds=round(time.time() - t0, 2))
            if p.returncode == 0 and scene:
                with gzip.GzipFile(os.path.join(a.out, "scenes", name + ".json.gz"), "wb", mtime=0) as f:
                    f.write(scene)
            else:
                e["scene_error"] = p.stderr.decode(errors="replace")[-300:]
        except subprocess.TimeoutExpired:
            e.update(scene_exit=None, scene_error="no scene in 120 s")
        t0 = time.time()
        try:
            p = subprocess.run([a.bin, src, str(PIXEL_SIZE[0]), str(PIXEL_SIZE[1]), "--pixels"], capture_output=True, timeout=a.pixel_seconds)
            d = json.loads(p.stdout)
            w, h, px = d["width"], d["height"], d["pixels"]
            if len(px) != w * h * 3:
                raise ValueError(f"{len(px)} values for {w}x{h}")
            open(os.path.join(a.out, "png", name + ".png"), "wb").write(png_bytes(w, h, px))
            e.update(png=name + ".png", pixels_seconds=round(time.time() - t0, 2), pixels_sha256=hashlib.sha256(bytes(px)).hexdigest())
        except subprocess.TimeoutExpired:
            e.update(png=None, pixels_note=f"no pixels in {a.pixel_seconds} s (CPU rasteriser)")
        except (ValueError, KeyError) as x:
            e.update(png=None, pixels_note=f"pixels not read: {type(x).__name__}: {str(x)[:120]}")
        manifest["pages"][name] = e
        print(f"{name}: scene {e.get('scene_bytes')} bytes {str(e.get('scene_sha256'))[:12]} in {e.get('scene_seconds')} s; "
              f"pixels {e.get('png') or e.get('pixels_note')}", flush=True)
    json.dump(manifest, open(os.path.join(a.out, "manifest.json"), "w"), indent=1)


def cmd_compare(a):
    A, B = (json.load(open(os.path.join(d, "manifest.json"))) for d in (a.a, a.b))
    os.makedirs(a.out, exist_ok=True)
    rows, bad = [], 0
    for name in sorted(set(A["pages"]) | set(B["pages"])):
        x, y = A["pages"].get(name), B["pages"].get(name)
        r = {"page": name}
        if not x or not y:
            r["note"] = f"only on {(A if x else B)['platform']}"
            bad += 1
            rows.append(r)
            continue
        r["scene_same"] = bool(x.get("scene_sha256")) and x.get("scene_sha256") == y.get("scene_sha256")
        r["scene_bytes"] = [x.get("scene_bytes"), y.get("scene_bytes")]
        if x.get("png") and y.get("png"):
            wa, ha, pa = png_read(os.path.join(a.a, "png", x["png"]))
            wb, hb, pb = png_read(os.path.join(a.b, "png", y["png"]))
            if (wa, ha) != (wb, hb):
                r.update(pixels_differ=None, note=f"sizes {wa}x{ha} and {wb}x{hb}")
            else:
                differ, largest, diff = 0, 0, bytearray()
                for i in range(0, len(pa), 3):
                    d = max(abs(pa[i] - pb[i]), abs(pa[i + 1] - pb[i + 1]), abs(pa[i + 2] - pb[i + 2]))
                    if d:
                        differ += 1
                        largest = max(largest, d)
                        diff += bytes((255, 0, 0))
                    else:
                        g = 255 - (255 - (pa[i] * 3 + pa[i + 1] * 6 + pa[i + 2]) // 10) // 4   # the page, faint
                        diff += bytes((g, g, g))
                r.update(pixels=wa * ha, pixels_differ=differ, largest_difference=largest)
                if differ:
                    open(os.path.join(a.out, name + ".diff.png"), "wb").write(png_bytes(wa, ha, diff))
        else:
            r["pixels_note"] = "; ".join(f"{m['platform']}: {e.get('pixels_note')}" for m, e in ((A, x), (B, y)) if not e.get("png"))
        if not r["scene_same"] or r.get("pixels_differ"):
            bad += 1
        rows.append(r)
    rep = {"format": "factoidal-render-report-v1", "core_commit": A.get("core_commit"), "platforms": [A["platform"], B["platform"]],
           "pages": len(rows), "pages_that_differ": bad, "rows": rows}
    json.dump(rep, open(os.path.join(a.out, "report.json"), "w"), indent=1)
    L = [f"### Render report: {A['platform']} against {B['platform']}, core `{str(A.get('core_commit'))[:12]}`", "",
         f"{len(rows)} fixture pages (core's labs/demos/foafnaut/web-render/fixtures); {bad} differ. Scene: the checked scene at "
         f"{SCENE_SIZE[0]}x{SCENE_SIZE[1]}, compared as bytes. Pixels: the CPU reference pixels at {PIXEL_SIZE[0]}x{PIXEL_SIZE[1]}.", "",
         "| page | scene | scene bytes | pixels that differ | largest channel difference | note |", "| --- | --- | ---: | ---: | ---: | --- |"]
    for r in rows:
        sb = r.get("scene_bytes") or ["", ""]
        px = "" if r.get("pixels_differ") is None else f"{r['pixels_differ']:,} of {r['pixels']:,}"
        L.append(f"| {r['page']} | {'same' if r.get('scene_same') else 'DIFFERENT'} | {sb[0] if sb[0] == sb[1] else f'{sb[0]} / {sb[1]}'} | {px} | "
                 f"{r.get('largest_difference', '')} | {r.get('note') or r.get('pixels_note') or ''} |")
    md = "\n".join(L) + "\n"
    open(os.path.join(a.out, "report.md"), "w").write(md)
    print(md)
    s = os.environ.get("GITHUB_STEP_SUMMARY")
    if s:
        open(s, "a").write(md + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw")
    for k in ("--bin", "--fixtures", "--out", "--platform"):
        d.add_argument(k, required=True)
    d.add_argument("--commit", default="")
    d.add_argument("--pixel-seconds", type=int, default=60)
    c = sub.add_parser("compare")
    for k in ("--a", "--b", "--out"):
        c.add_argument(k, required=True)
    a = ap.parse_args()
    {"draw": cmd_draw, "compare": cmd_compare}[a.cmd](a)


if __name__ == "__main__":
    main()
