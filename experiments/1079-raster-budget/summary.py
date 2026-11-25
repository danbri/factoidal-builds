from collections import defaultdict
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageChops

out = Path("out")
roles = ("baseline","candidate")
cap = 1048576
summary = {"bbc":{}, "controls":{}}


def record(group, role, case, part):
    return json.loads((out/group/role/f"{case}.png-{part}.json").read_text())


def check_inputs(group, case):
    a,b = (record(group, role, case, "image-keys") for role in roles)
    assert a == b, (group,case,a,b)
    return a


def compare_markers(group, case, expected):
    check_inputs(group,case)
    found = {}
    for role in roles:
        bitmaps = record(group,role,case,"paint-bitmap")
        by_id = defaultdict(list)
        for bitmap in bitmaps:
            r,g,b,a = bitmap["firstPixel"]
            if g == 70 and b == 170 and a == 255 and (r-40)%3 == 0:
                by_id[(r-40)//3].append((bitmap["width"],bitmap["height"],bitmap["sha256"]))
        found[role] = {i: sorted(set((w,h) for w,h,_ in entries)) for i,entries in by_id.items()}
        if case == "duplicate":
            assert len(by_id[0]) >= 2 and len(set(by_id[0])) == 1, by_id[0]
        for source_ids,dims in expected[role]:
            for i in source_ids:
                assert found[role].get(i)==[dims], (group,case,role,i,found)
    summary["controls"][group+"/"+case] = found


before = (153,90)
after = (305,180)
natural = (610,360)
for case, keys, dims in (
    ("under", [0,1], natural),
    ("fair", range(4), after),
    ("offscreen", range(4,8), before),
    ("duplicate", range(4), after),
    ("vector", range(4), before),
):
    compare_markers("synthetic",case,{"baseline":[(keys,natural if case=="under" else before)],
                                       "candidate":[(keys,dims)]})
    if case in ("under","offscreen","vector"):
        a,b = (out/"synthetic"/role/f"{case}.png" for role in roles)
        assert a.read_bytes()==b.read_bytes(), case
compare_markers("early","late",{role:[([0,1],natural)] for role in roles})
compare_markers("late","late",{"baseline":[(range(4),before)], "candidate":[(range(4),after)]})
for role in roles:
    early = record("early",role,"late","image-keys")
    late = record("late",role,"late","image-keys")
    assert early["htmlSha256"]==late["htmlSha256"]
    assert len(early["held"])==2 and len(late["held"])==48

def pixels(w,h,k):
    return w*h if w*h <= 4096 else ((w+k-1)//k)*((h+k-1)//k)


def planned(sizes, k):
    return sum(pixels(w,h,k) for w,h in sizes)


def candidate_cost(sizes, factor):
    cost = planned(sizes,factor)
    preferred = max(1,factor//2)
    bumps = []
    eligible = 0
    for key,(w,h) in enumerate(sizes):
        if w*h <= 4096: continue
        eligible += 1
        price = pixels(w,h,preferred)-pixels(w,h,factor)
        if cost+price <= cap:
            cost += price
            bumps.append((key,price))
        if eligible==4:
            break
    return cost, bumps


with ZipFile("capture/bbc-uk-with-photos.zip") as replay:
    manifest = json.loads(replay.read("manifest.json"))
    entries = {entry["url"]:entry for entry in manifest["entries"] if entry.get("body")}
    inputs = check_inputs("bbc-1","bbc")
    assert inputs == check_inputs("bbc-2","bbc")
    sizes = []
    for key in inputs["pictures"]:
        if key not in inputs["held"]: continue
        raw = replay.read(entries[key]["body"])
        assert sha256(raw).hexdigest()==inputs["held"][key], key
        with Image.open(BytesIO(raw)) as image:
            assert image.format == "WEBP", (key,image.format)
            sizes.append(image.size)
    assert len(sizes)==62 and sizes[:4]==[(800,450)]+[(480,270)]*3
    old = planned(sizes,4)
    new,bumps = candidate_cost(sizes,4)
    assert old==744374 and new==884494 and [k for k,_ in bumps]==[0,1,2,3]
    summary["bbc"]["allocation"] = dict(baseline=old,candidate=new,limit=cap,sourceCount=len(sizes))
    summary["bbc"]["pictureKeys"] = inputs["pictures"][:4]

def timed(log):
    lines = log.read_text().splitlines()
    gpu = [json.loads(line) for line in lines if line.startswith('{"type":"reftest-time"')]
    cpu = [json.loads(line.removeprefix("__done ")) for line in lines if line.startswith("__done ")]
    packet = [json.loads(line) for line in lines if line.startswith('{"type":"raster-probe-cpu"')]
    assert len(cpu)==len(gpu)==len(packet)==1, log
    return {"instrumentedWallMs":cpu[0]["ms"],"gpuPacketMs":gpu[0]["ms"],
            "cpuPacketMs":round(packet[0]["ms"],1),"engineBreakdown":gpu[0]["timing"]}

summary["bbc"]["timings"] = {}
for role in roles:
    a,b = (out/f"bbc-{repeat}"/role for repeat in (1,2))
    a_bytes,b_bytes = (x.joinpath("bbc.png").read_bytes() for x in (a,b))
    assert a_bytes==b_bytes, role
    bitmaps = record("bbc-1",role,"bbc","paint-bitmap")
    summary["bbc"][role] = [(x["width"],x["height"],x["bounds"]) for x in bitmaps[:4]]
    assert [x[:2] for x in summary["bbc"][role]] == (
        [(200,113)]+[(120,68)]*3 if role=="baseline" else [(400,225)]+[(240,135)]*3
    )
    summary["bbc"]["timings"][role] = [timed(run/"renderer.log") for run in (a,b)]
    with Image.open(a/"bbc.png") as image:
        image.crop((16,185,505,460)).save(out/f"bbc-lead-{role}.png")
        image.crop((16,185,1264,461)).save(out/f"bbc-band-{role}.png")
assert [x[2] for x in summary["bbc"]["baseline"]]==[x[2] for x in summary["bbc"]["candidate"]]
with Image.open(out/"bbc-lead-baseline.png") as a, Image.open(out/"bbc-lead-candidate.png") as b:
    assert ImageChops.difference(a.convert("RGB"), b.convert("RGB")).getbbox()
(out/"comparison.json").write_text(json.dumps(summary,indent=2)+"\n")
print("BBC document raster cost:", summary["bbc"]["allocation"])
for role in roles:
    print(role, (summary["bbc"][role])[0], summary["bbc"]["timings"][role])
print("All six synthetic scenarios passed, including two late payload stages.")
