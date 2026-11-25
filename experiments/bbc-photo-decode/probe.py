import functools
import http.server
import json
import os
from pathlib import Path
import subprocess
import threading
from zipfile import ZipFile

from PIL import Image

OUT = Path("out").resolve()
CAPTURE = Path("capture/bbc-uk-with-photos.zip").resolve()
RENDERER = Path("core/tests/browser-wpt/reftest-render.ts").resolve()
FOAFNAUT = Path("core/labs/demos/foafnaut").resolve()
ENGINE = Path("engine/libweb-render.so").resolve()
# Identifiers of the four images shown as alt text on the frozen UK first viewport.
LEADS = ("5d721e40", "0fff68f0", "7a525660", "e3f9d920")


def run(url, width, height, file, replay=None):
    args = ["deno", "run", "--no-check", "--no-config", "--no-npm", "--unstable-ffi", "-A"]
    env = os.environ.copy()
    if replay:
        args += ["--preload", str(FOAFNAUT / "realpages/replay.ts")]
        env["REALPAGES_REPLAY"] = str(replay)
    job = OUT / f"{file}.jsonl"
    job.write_text(json.dumps({"url": url, "width": width, "height": height, "file": f"{file}.png"}) + "\n")
    with (OUT / f"{file}.log").open("w") as log:
        subprocess.run(args + [str(RENDERER), "--native-engine", str(ENGINE), "--list", str(job),
                               "--out", str(OUT)], env=env, stdout=log, stderr=subprocess.STDOUT,
                       timeout=120, check=True)
    records = (OUT / f"{file}.log").read_text(errors="replace").splitlines()
    assert any(line.startswith("__done ") and json.loads(line[7:])["status"] == "ok" for line in records), file


def main():
    fixtures = OUT / "fixtures"
    fixtures.mkdir()
    with ZipFile(CAPTURE) as z:
        manifest = json.loads(z.read("manifest.json"))
        for i, needle in enumerate(LEADS):
            row, = (e for e in manifest["entries"]
                    if e.get("source") == "foafnaut-photo-recapture" and needle in e["url"])
            x = fixtures / f"lead-{i}.webp"
            x.write_bytes(z.read(row["body"]))
            with Image.open(x) as photo:
                image = photo.convert("RGB")
                image.save(fixtures / f"lead-{i}.png")
                for extension in ("webp", "png"):
                    (fixtures / f"lead-{i}-{extension}.html").write_text(
                        f'<!doctype html><style>body{{margin:0;background:white}}img{{display:block}}</style>'
                        f'<img width="{image.width}" height="{image.height}" src="lead-{i}.{extension}" alt="">'
                    )
            assert x.stat().st_size == row["bytes"]

    # Read the browser host's actual requested resource diagnostics and held image names.
    host = RENDERER.read_text()
    key = '  const {source,options}=page.request(job.width,job.height,{textScalePercent:100,zoomUnit:100});'
    assert host.count(key) == 1
    RENDERER.write_text(
        'import {consoleOf} from "../../labs/demos/foafnaut/native_console.ts";\n' +
        host.replace(key, key + '''
  console.error(JSON.stringify({type:"photo-probe",file:job.file,
    issues:consoleOf(page).filter(e=>e.source==="System"&&e.feature?.includes("image")),
    held:(options.heldImages as {key:string}[]|undefined)?.map(i=>i.key)??[],
    inline:(options.images as {key:string}[]|undefined)?.map(i=>i.key)??[]}));
''')
    )

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=fixtures)
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        origin = f"http://127.0.0.1:{server.server_port}"
        for i in range(len(LEADS)):
            for extension in ("webp", "png"):
                case = f"lead-{i}-{extension}"
                run(f"{origin}/{case}.html", 512, 300, case)
        server.shutdown()
    run(manifest["url"], 1280, 735, "bbc-uk", CAPTURE)
    stats = {}
    for path in sorted(OUT.glob("lead-*.png")):
        with Image.open(path) as result:
            crop = result.convert("RGB").crop((10, 10, 250, 150))
            stats[path.stem] = {"uniqueColors": len(set(crop.getdata()))}
    (OUT / "colors.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats))
    assert all(row["uniqueColors"] > 100 for key, row in stats.items() if key.endswith("-png")), stats


if __name__ == "__main__":
    main()
