import json
from pathlib import Path


def frames(path):
    records = [json.loads(line.removeprefix("__done ")) for line in path.read_text().splitlines()
               if line.startswith("__done ")]
    assert len(records) == 10
    assert all(r["status"] == "ok" for r in records)
    return {r["file"]: r["sha"] for r in records}


out = Path("out")
roles = ("baseline", "candidate")
data = {role: frames(out / (role + ".log")) for role in roles}
checks = {role: {} for role in roles}
for role, f in data.items():
    for case, ref in [("pair", "pair-ref"), ("positive", "pair-ref"), ("spaced", "pair-ref"),
                      ("wpt-1", "wpt-1-ref"), ("wpt-2", "wpt-2-ref"), ("wpt-3", "wpt-3-ref")]:
        checks[role][case] = f[case + ".png"] == f[ref + ".png"]
print(json.dumps(checks, indent=2))
(out / "summary.json").write_text(json.dumps({"checks": checks, "hashes": data}, indent=2) + "\n")
assert not checks["baseline"]["pair"], checks
assert checks["candidate"]["pair"], checks
assert not checks["candidate"]["positive"] and not checks["candidate"]["spaced"], checks
assert all(checks["candidate"][abbr] or not checks["baseline"][abbr] for abbr in ("wpt-1", "wpt-2", "wpt-3")), checks
