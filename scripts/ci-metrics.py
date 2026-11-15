#!/usr/bin/env python3
"""Timing and cache records of build.yml runs.

  ci-metrics.py run   --run-id ID [--out DIR] [--skip-job NAME]
      One run: per job queue wait, duration, the longest steps, and every cache it used
      (actions/cache hit, partial hit or miss, bytes restored; ccache and leanc object hits;
      the cache audit). Writes DIR/ci-metrics-<ID>.json and DIR/summary.md.
  ci-metrics.py record --file JSON --dir DIR
      Adds a run record to DIR/runs/<ID>.json and its job rows to DIR/runs.csv (the branch
      ci-metrics of this repository; scripts/record-ci-metrics.sh pushes it).
  ci-metrics.py trend [--n 10] [--records DIR]
      The last N completed build.yml runs that built something: per job median and last
      duration and queue wait, read from the API (and cache hit counts from DIR/runs/*.json
      when given). Prints a markdown table, so a slowdown shows.

Needs `gh` (authenticated) or GH_TOKEN. Repository: $GITHUB_REPOSITORY or danbri/factoidal-builds.
"""
import argparse, datetime as dt, json, os, re, statistics, subprocess, sys

REPO = os.environ.get("GITHUB_REPOSITORY", "danbri/factoidal-builds")


def api(path, raw=False):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gh api {path}: {r.stderr.strip()}")
    return r.stdout if raw else json.loads(r.stdout)


def t(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def minutes(a, b):
    return round((b - a).total_seconds() / 60, 2) if a and b else None


TS = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+Z ")


def parse_log(text):
    """Cache facts from one job log."""
    caches, cur = [], None
    out = {"caches": caches}
    for raw in text.splitlines():
        line = TS.sub("", raw)
        m = re.match(r"##\[group\]Run actions/cache(/restore|/save)?@", line)
        if m:
            cur = {"action": "cache" + (m.group(1) or ""), "key": None, "result": None, "bytes": None}
            caches.append(cur)
            continue
        if cur is not None:
            if line.startswith("  key: ") and cur["key"] is None:
                cur["key"] = line[7:].strip()
            elif line.startswith("Cache restored from key: "):
                k = line.split(": ", 1)[1].strip()
                cur["result"] = "hit" if k == cur["key"] else "partial"
                cur["restored_key"] = k
            elif line.startswith("Cache not found for input keys"):
                cur["result"] = "miss"
            elif line.startswith("Cache saved with key") or line.startswith("Cache saved successfully"):
                cur["result"] = cur["result"] or "saved"
            m2 = re.match(r"Cache Size: ~\d+ MB \((\d+) B\)", line)
            if m2:
                cur["bytes"] = int(m2.group(1))
        m = re.match(r"\s*Hits:\s+(\d+)\s*/\s*(\d+)", line)
        if m:
            out["ccache"] = {"hits": int(m.group(1)), "lookups": int(m.group(2))}
        m = re.match(r"C objects: (\d+) from the cache, (\d+) compiled", line)
        if m:
            out["leanc_objects"] = {"hits": int(m.group(1)), "compiled": int(m.group(2))}
        m = re.match(r"CACHE_AUDIT summary: (\d+) of (\d+) compiles recompiled without caches, (\d+) different", line)
        if m:
            out["cache_audit"] = {"checked": int(m.group(1)), "compiles": int(m.group(2)), "different": int(m.group(3))}
    return out


def cmd_run(a):
    run = api(f"repos/{REPO}/actions/runs/{a.run_id}")
    created = t(run["created_at"])
    jobs = api(f"repos/{REPO}/actions/runs/{a.run_id}/jobs?per_page=100")["jobs"]
    rec = {"format": "factoidal-ci-metrics-v1", "run_id": run["id"], "run_url": run["html_url"],
           "event": run["event"], "builds_branch": run["head_branch"], "builds_sha": run["head_sha"],
           "title": run.get("display_title"), "created_at": run["created_at"], "jobs": []}
    for j in jobs:
        if j["name"] in a.skip_job or j["status"] != "completed":
            continue
        c, s, e = t(j["created_at"]), t(j["started_at"]), t(j["completed_at"])
        steps = sorted(({"name": x["name"], "minutes": minutes(t(x["started_at"]), t(x["completed_at"]))}
                        for x in j.get("steps", []) if x.get("started_at") and x.get("completed_at")),
                       key=lambda x: -(x["minutes"] or 0))
        job = {"name": j["name"], "conclusion": j["conclusion"], "runner": (j.get("labels") or [""])[0],
               "queue_minutes": minutes(c, s), "minutes": minutes(s, e),
               "start_after_dispatch_minutes": minutes(created, s), "end_after_dispatch_minutes": minutes(created, e),
               "longest_steps": steps[:4]}
        try:
            job.update(parse_log(api(f"repos/{REPO}/actions/jobs/{j['id']}/logs", raw=True)))
        except RuntimeError as err:
            job["log_error"] = str(err)[:200]
        rec["jobs"].append(job)
    ends = [x["end_after_dispatch_minutes"] for x in rec["jobs"] if x["end_after_dispatch_minutes"] is not None]
    rec["wall_minutes"] = max(ends) if ends else None
    os.makedirs(a.out, exist_ok=True)
    json.dump(rec, open(os.path.join(a.out, f"ci-metrics-{a.run_id}.json"), "w"), indent=1)
    md = [f"### Timing and caches, run {a.run_id}", "",
          f"Wall clock to the last finished job: {rec['wall_minutes']} min.", "",
          "| Job | Result | Queue (min) | Run (min) | Ends at (min) | Caches | Compiler caches |",
          "| --- | --- | ---: | ---: | ---: | --- | --- |"]
    for x in sorted(rec["jobs"], key=lambda x: x["end_after_dispatch_minutes"] or 0):
        cs = ", ".join(f"{(c['key'] or '?').split('-')[0]} {c['result'] or '?'}"
                       + (f" {c['bytes'] // 1048576} MB" if c.get("bytes") else "") for c in x.get("caches", []))
        cc = []
        if "ccache" in x:
            cc.append(f"ccache {x['ccache']['hits']}/{x['ccache']['lookups']}")
        if "leanc_objects" in x:
            lo = x["leanc_objects"]
            cc.append(f"leanc {lo['hits']}/{lo['hits'] + lo['compiled']}")
        if "cache_audit" in x:
            au = x["cache_audit"]
            cc.append(f"audit {au['checked']} checked, {au['different']} different")
        md.append(f"| {x['name']} | {x['conclusion']} | {x['queue_minutes']} | {x['minutes']} | "
                  f"{x['end_after_dispatch_minutes']} | {cs or '-'} | {'; '.join(cc) or '-'} |")
    open(os.path.join(a.out, "summary.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


CSV_COLUMNS = ["run_id", "created_at", "event", "builds_branch", "wall_minutes", "job", "conclusion", "runner",
               "queue_minutes", "minutes", "end_after_dispatch_minutes", "cache_restores", "cache_hits",
               "cache_bytes_restored", "ccache_hits", "ccache_lookups", "leanc_hits", "leanc_compiled",
               "audit_checked", "audit_different"]


def cmd_record(a):
    import csv
    rec = json.load(open(a.file))
    os.makedirs(os.path.join(a.dir, "runs"), exist_ok=True)
    json.dump(rec, open(os.path.join(a.dir, "runs", f"{rec['run_id']}.json"), "w"), indent=1)
    path = os.path.join(a.dir, "runs.csv")
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, CSV_COLUMNS)
        if new:
            w.writeheader()
        for x in rec["jobs"]:
            restores = [c for c in x.get("caches", []) if c["action"] != "cache/save"]
            w.writerow({"run_id": rec["run_id"], "created_at": rec["created_at"], "event": rec["event"],
                        "builds_branch": rec["builds_branch"], "wall_minutes": rec["wall_minutes"], "job": x["name"],
                        "conclusion": x["conclusion"], "runner": x["runner"], "queue_minutes": x["queue_minutes"],
                        "minutes": x["minutes"], "end_after_dispatch_minutes": x["end_after_dispatch_minutes"],
                        "cache_restores": len(restores), "cache_hits": sum(c["result"] in ("hit", "partial") for c in restores),
                        "cache_bytes_restored": sum(c.get("bytes") or 0 for c in restores),
                        "ccache_hits": x.get("ccache", {}).get("hits", ""), "ccache_lookups": x.get("ccache", {}).get("lookups", ""),
                        "leanc_hits": x.get("leanc_objects", {}).get("hits", ""),
                        "leanc_compiled": x.get("leanc_objects", {}).get("compiled", ""),
                        "audit_checked": x.get("cache_audit", {}).get("checked", ""),
                        "audit_different": x.get("cache_audit", {}).get("different", "")})


def cmd_trend(a):
    runs = api(f"repos/{REPO}/actions/workflows/build.yml/runs?status=completed&per_page=50")["workflow_runs"]
    rows, seen = {}, 0
    order = []
    for r in runs:
        jobs = api(f"repos/{REPO}/actions/runs/{r['id']}/jobs?per_page=100")["jobs"]
        if len(jobs) <= 1:  # the resolve job alone: nothing to build
            continue
        seen += 1
        order.append(r["id"])
        for j in jobs:
            if not j["started_at"] or not j["completed_at"]:
                continue
            name = re.sub(r" \(.*\)$", "", j["name"]) + (" (macOS)" if "macos" in " ".join(j.get("labels") or []) else "")
            d = rows.setdefault(name, {"minutes": [], "queue": [], "last": None})
            d["minutes"].append(minutes(t(j["started_at"]), t(j["completed_at"])))
            d["queue"].append(minutes(t(j["created_at"]), t(j["started_at"])))
            if d["last"] is None:
                d["last"] = (r["id"], d["minutes"][-1])
        if seen >= a.n:
            break
    hits = {}
    if a.records and os.path.isdir(os.path.join(a.records, "runs")):
        for rid in order:
            p = os.path.join(a.records, "runs", f"{rid}.json")
            if os.path.exists(p):
                for x in json.load(open(p))["jobs"]:
                    h = hits.setdefault(re.sub(r" \(.*\)$", "", x["name"]), [0, 0])
                    for c in x.get("caches", []):
                        if c["action"] != "cache/save":
                            h[1] += 1
                            h[0] += c["result"] in ("hit", "partial")
    print(f"Last {seen} build.yml runs that built something (newest {order[0] if order else '-'})\n")
    print("| Job | Runs | Median (min) | Last (min, run) | Max (min) | Median queue | Max queue | Cache restores hit |")
    print("| --- | ---: | ---: | --- | ---: | ---: | ---: | --- |")
    for n, d in sorted(rows.items(), key=lambda kv: -statistics.median(kv[1]["minutes"])):
        h = hits.get(n.replace(" (macOS)", ""))
        print(f"| {n} | {len(d['minutes'])} | {statistics.median(d['minutes']):.1f} | {d['last'][1]:.1f} ({d['last'][0]}) | "
              f"{max(d['minutes']):.1f} | {statistics.median(d['queue']):.1f} | {max(d['queue']):.1f} | "
              f"{f'{h[0]}/{h[1]}' if h else '-'} |")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--run-id", required=True)
    r.add_argument("--out", default=".")
    r.add_argument("--skip-job", action="append", default=[])
    rc = sub.add_parser("record")
    rc.add_argument("--file", required=True)
    rc.add_argument("--dir", required=True)
    tr = sub.add_parser("trend")
    tr.add_argument("--n", type=int, default=10)
    tr.add_argument("--records")
    a = p.parse_args()
    {"run": cmd_run, "record": cmd_record, "trend": cmd_trend}[a.cmd](a)


if __name__ == "__main__":
    main()
