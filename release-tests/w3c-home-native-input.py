import json
import os
from pathlib import Path
import subprocess
import sys

lab, engine, snapshot, out = map(Path, sys.argv[1:])
out.mkdir(exist_ok=True)
host = lab / "run_html.ts"
source = host.read_text()
anchor = '        else if(typeof step==="string"&&step.startsWith("tap:")){'
assert source.count(anchor) == 1
checkpoint = '''        else if(typeof step==="string"&&step.startsWith("capture:")){
          const name=step.slice(8);
          if(!/^[a-z-]+$/.test(name))throw Error("Invalid capture name");
          const saved=shotFile;
          shotFile=Deno.env.get("W3C_PROBE_DIR")+"/"+name+".png";
          try{await takeShot();}finally{shotFile=saved;}
          const standards="https://www.w3.org/standards/about/";
          const top=current?.layers.layers.top??0;
          const regions=(frame.webRender.links as unknown[][]).filter(r=>r[1]===standards);
          const visible=regions.some(r=>{const y=windowRow(Number(r[3])+Number(r[5])/2);return y>=top&&y<height;});
          trace("native-html-w3c-checkpoint",{name,url:document.url,standardsVisible:visible,width,height});
        }
'''
host.write_text(source.replace(anchor,checkpoint+anchor))
# The desktop point comes from the prior 1280px native screenshot. The host's tap accepts
# document coordinates, so y=128 excludes the 65px browser chrome in that capture.
home = ["url:www.w3.org/", "title=W3C", "hold", "hold"]
menu = ["tap:330,128", "hold", "hold", "hold"]
about = "https://www.w3.org/standards/about/"
search = "https://www.w3.org/help/search/"
cases = [
    ("archived-desktop", "https://www.w3.org/", "1280x800", True,
     home+["capture:home"]+menu+["capture:menu",f"over:{about}","pointer:hand"]),
    ("archived-narrow", "https://www.w3.org/", "480x800", True,
     home+["capture:home"]),
    ("live-standards", "https://w3.org/", "1280x800", False,
     home+["capture:home"]+menu+["capture:menu", f"click:{about}", "hold", "hold",
       "title=About W3C web standards | Web Standards | W3C", "url:/standards/about/"]),
    ("live-search", "https://w3.org/", "1280x800", False,
     home+["capture:home", f"click:{search}", "hold", "hold",
       "title=Search | Help | W3C", "url:/help/search/"]),
]
summary = {}
try:
    for name, url, size, offline, steps in cases:
        case = out / name
        case.mkdir()
        sequence = case / "steps.json"
        sequence.write_text(json.dumps(steps))
        options = ["--preload", str(lab/"realpages/replay.ts")] if offline else []
        argv = [
            "deno","run","--no-check","--no-config","--no-npm","--node-modules-dir=none",
            "--unstable-webgpu","--unstable-ffi","-A",*options,str(host),
            "--native-engine",str(engine),"--offscreen","--offscreen-size",size+"@1",
            "--no-state","--trace-input","--follow-links","--be-liberal-in-what-we-accept",
            "--perf-summary","--steps",str(sequence),"--shot",str(case/"final.png"),
            "--shot-at-end","--url",url,
        ]
        env = {**os.environ,"W3C_PROBE_DIR":str(case)}
        if offline:
            env["REALPAGES_REPLAY"] = str(snapshot)
        log = case / "native.log"
        with log.open("w") as stream:
            try:
                result = subprocess.run(argv,cwd=lab,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=110)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
        records = []
        for line in log.read_text(errors="replace").splitlines():
            if not line.startswith("{"):
                continue
            try:
                records.append(json.loads(line))
            except ValueError:
                continue
        checks = [r for r in records if r.get("type","").startswith("native-html-test-")]
        checkpoints = {r["name"]:r for r in records if r.get("type")=="native-html-w3c-checkpoint"}
        channel = [r for r in records if r.get("type")=="native-html-engine"]
        end = next((r for r in reversed(records) if r.get("type")=="native-html-presented"),{})
        row = {"case":name,"exit":code,"checks":checks,"checkpoints":checkpoints,
               "end":end,"screenshots":sorted(p.name for p in case.glob("*.png"))}
        passed = code == 0 and all(r.get("ok",True) for r in checks)
        passed = passed and any(r.get("engine")==f"native {engine}" for r in channel)
        passed = passed and "home.png" in row["screenshots"] and "final.png" in row["screenshots"]
        if "capture:menu" in steps:
            passed = (passed and "menu.png" in row["screenshots"]
                      and not checkpoints["home"]["standardsVisible"]
                      and checkpoints.get("menu",{}).get("standardsVisible"))
        if name.startswith("live-"):
            called = about if name=="live-standards" else search
            passed = passed and end.get("url")==called
        row["passed"] = bool(passed)
        summary[name] = row
        print(json.dumps(row),flush=True)
        (out/"report.json").write_text(json.dumps(summary,indent=2)+"\n")
finally:
    host.write_text(source)
assert all(row["passed"] for row in summary.values()), "See per-case screenshots and native trace"
