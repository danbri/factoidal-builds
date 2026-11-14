#!/usr/bin/env python3
"""The performance gate of factoidal-core (core's skills/perf-gate/SKILL.md; workflow perf.yml).

Runs core's performance fixtures (labs/demos/foafnaut/fixtures/perf, made by its
make_fixtures.py) and the BubblePopJS page benchmarks (labs/demos/foafnaut/js_perf_bench.ts)
with one or more engine libraries, on the same machine, samples interleaved, and compares a
head engine with a base engine against the margins below. Exit 1 when the head is slower.

    perf.py run --core CORE --engine base=LIB:HOSTROOT --engine head=LIB:HOSTROOT --out DIR [--samples 3]
    perf.py compare --summary DIR/summary.json --base base --head head --out DIR   (exit 1: slower)
    perf.py rows --summary DIR/summary.json --label head --core-commit SHA --engine-tag TAG --out rows.json
    perf.py record --rows rows.json [--repo .]        (append to perf.csv on the branch wpt-scores)
    perf.py baseline --head SHA                        (newest Linux engine release of an ancestor on main)

CORE is the checkout whose fixtures, harness (tests/browser-wpt/perf-run.ts) and benchmark
pages are used for every engine. HOSTROOT is a checkout of the engine's own commit: the host
sources (labs/demos/foafnaut/*.ts, docs/web/hub/foafnaut/*.mjs) that speak to that library.
"""
import argparse
import csv
import json
import os
import re
import statistics
import subprocess
import sys
import time

BUILDS_REPO = os.environ.get("GITHUB_REPOSITORY", "danbri/factoidal-builds")
CORE_REPO = os.environ.get("CORE_REPO", "danbri/factoidal-core")
RESULTS_BRANCH = os.environ.get("RESULTS_BRANCH", "wpt-scores")
FIXTURES = "labs/demos/foafnaut/fixtures/perf"
HARNESS = "tests/browser-wpt/perf-run.ts"
JS_BENCH = "labs/demos/foafnaut/js_perf_bench.ts"
FONT = "third_party/fonts/noto-sans/NotoSans-Regular.ttf"
STUB = ("// Stand-in for the Wasm build (perf.py): the perf harness runs the native library only.\n"
        "export default async function(){const no=()=>{throw new Error(\"the Wasm build is not loaded by the perf harness\")};"
        "return {ccall:no,cwrap:no,UTF8ToString:no,HEAPU8:new Uint8Array(0),_malloc:no,_free:no};}\n")

# ---- the margins (stated in core's skills/perf-gate/SKILL.md; change both together) ---------
# Exact counters: the same on every sample of one engine, so any rise is real.
COUNTER_ZERO = {"frame_layouts", "script_layouts"}          # no rise at all
COUNTER_PCT = 2.0                                           # others: a rise of more than 2 %
COUNTERS = COUNTER_ZERO | {"script_instructions", "script_jobs", "script_tasks", "engine_calls", "js_steps"}
# Wall times: the median of the samples, head against base on the same runner, samples
# interleaved. Slower only when all three hold: the median is more than 30 % higher, more
# than 30 ms higher, and the fastest head sample is slower than the slowest base sample.
TIME_RATIO, TIME_MS = 1.30, 30.0
TIMES = {"first_layout_ms", "settled_layout_ms", "resize_layout_ms", "script_ms", "engine_ms", "js_ms"}
# Recorded, never gated: output size, not cost (a rendering fix may change them).
RECORDED = {"primitives", "settled_primitives", "dom_changes", "dom_calls", "parse_ms", "domcall_us"}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def die(msg):
    log("perf.py: " + msg)
    sys.exit(2)


# ---- run ------------------------------------------------------------------------------------

def prepare_host(root):
    """The host sources import the Wasm runtime module: a stand-in when there is none."""
    rt = os.path.join(root, "labs/demos/foafnaut/.build/native-html/runtime")
    os.makedirs(rt, exist_ok=True)
    p = os.path.join(rt, "web-render.mjs")
    if not os.path.exists(p):
        with open(p, "w") as f:
            f.write(STUB)


def flatten(o):
    """One perf-run.ts answer -> {metric: number}."""
    s = o.get("script") or {}
    fw = o.get("frame_work") or {}
    m = {"first_layout_ms": o.get("first_layout_ms"), "settled_layout_ms": o.get("settled_layout_ms"),
         "resize_layout_ms": o.get("resize_layout_ms"), "engine_ms": o.get("engine_ms"), "parse_ms": o.get("parse_ms"),
         "primitives": o.get("primitives"), "settled_primitives": o.get("settled_primitives"),
         "frame_layouts": fw.get("layouts"),
         "engine_calls": sum(c.get("n", 0) for c in (o.get("calls") or {}).values())}
    if s.get("turns"):
        m.update({"script_instructions": s.get("instructions"), "script_jobs": s.get("jobs"), "script_tasks": s.get("tasks"),
                  "script_layouts": s.get("layouts"), "dom_changes": s.get("changes"),
                  "script_ms": round((s.get("start_ms") or 0) + (s.get("settle_ms") or 0), 1)})
    rep = o.get("fixture_report") or {}
    if isinstance(rep.get("domCalls"), (int, float)):
        m["dom_calls"] = rep["domCalls"]
    return {k: v for k, v in m.items() if isinstance(v, (int, float))}


def run_one(cmd, cwd, timeout, env=None):
    t = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None, f"timed out after {timeout} s"
    line = next((x for x in reversed(p.stdout.strip().splitlines()) if x.startswith("{")), "")
    try:
        return json.loads(line), None
    except json.JSONDecodeError:
        return None, f"exit {p.returncode} after {time.time() - t:.0f} s: " + (p.stderr.strip().splitlines() or [""])[-1][:300]


def cmd_run(a):
    core = os.path.abspath(a.core)
    fx_dir = os.path.join(core, FIXTURES)
    gen = os.path.join(fx_dir, "make_fixtures.py")
    subprocess.run([sys.executable, gen, "--png"], check=True, capture_output=True)
    chk = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True)
    if chk.returncode:
        die("the fixtures are not what make_fixtures.py writes: " + chk.stderr.strip())
    manifest = json.load(open(os.path.join(fx_dir, "manifest.json")))
    names = [n for n in (a.fixtures.split(",") if a.fixtures else sorted(manifest["fixtures"]))]
    engines = []
    # Lean's shared runtime of each engine (Linux): --ld label=DIR, put first on LD_LIBRARY_PATH.
    ld = dict(x.split("=", 1) for x in a.ld)
    env_of = {}
    for spec in a.engine:
        label, rest = spec.split("=", 1)
        lib, host = rest.rsplit(":", 1)
        prepare_host(os.path.abspath(host))
        engines.append((label, os.path.abspath(lib), os.path.abspath(host)))
        env_of[label] = dict(os.environ, **({"LD_LIBRARY_PATH": ld[label] + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")} if label in ld else {}))
    font = a.font or os.path.join(core, FONT)
    os.makedirs(a.out, exist_ok=True)
    samples = open(os.path.join(a.out, "samples.jsonl"), "w")
    data = {}          # label -> fixture -> metric -> [values]
    problems = {}      # label -> fixture -> [why]
    t0 = time.time()
    for k in range(a.samples):
        for name in names:
            for label, lib, host in (engines if k % 2 == 0 else engines[::-1]):
                cmd = ["deno", "run", "-A", "--unstable-ffi", os.path.join(core, HARNESS), "--engine", lib,
                       "--host", os.path.join(host, "labs/demos/foafnaut"), "--fixtures", fx_dir, "--fixture", name, "--font", font]
                o, err = run_one(cmd, core, a.timeout, env_of[label])
                rec = {"sample": k, "engine": label, "fixture": name, **({"result": o} if o else {"error": err})}
                samples.write(json.dumps(rec) + "\n")
                samples.flush()
                if not o or not o.get("valid"):
                    why = err or o.get("why") or "not valid"
                    problems.setdefault(label, {}).setdefault(name, []).append(why)
                    log(f"[{k}] {label:5} {name:9} INVALID {why}")
                    continue
                for m, v in flatten(o).items():
                    data.setdefault(label, {}).setdefault(name, {}).setdefault(m, []).append(v)
                log(f"[{k}] {label:5} {name:9} first {o.get('first_layout_ms')} ms engine {o.get('engine_ms')} ms")
        if a.js:
            for label, lib, host in (engines if k % 2 == 0 else engines[::-1]):
                out = os.path.join(a.out, f"js-{label}-{k}.json")
                cmd = ["deno", "run", "-A", "--unstable-ffi", os.path.join(core, JS_BENCH), "--engine", lib, "--runs", "1", "--json", out,
                       "--host", os.path.join(host, "labs/demos/foafnaut")]
                try:
                    subprocess.run(cmd, cwd=core, capture_output=True, text=True, timeout=a.timeout, env=env_of[label])
                    j = json.load(open(out))
                except (subprocess.TimeoutExpired, OSError, json.JSONDecodeError) as e:
                    problems.setdefault(label, {}).setdefault("js", []).append(str(e)[:200])
                    log(f"[{k}] {label:5} js INVALID {e}")
                    continue
                samples.write(json.dumps({"sample": k, "engine": label, "fixture": "js", "result": j}) + "\n")
                for w, r in (j.get("workloads") or {}).items():
                    if "error" in r:
                        problems.setdefault(label, {}).setdefault("js-" + w, []).append(r["error"][:200])
                        continue
                    d = data.setdefault(label, {}).setdefault("js-" + w, {})
                    d.setdefault("js_steps", []).append(r["steps"])
                    d.setdefault("js_ms", []).append(r["ms"])
                for op, r in (j.get("domcall") or {}).items():
                    if "usPerCall" in r:
                        data.setdefault(label, {}).setdefault("domcall-" + op, {}).setdefault("domcall_us", []).append(r["usPerCall"])
                log(f"[{k}] {label:5} js {len(j.get('workloads') or {})} workloads")
    samples.close()
    summary = {"format": "factoidal-perf-v1", "set_sha256": manifest["set_sha256"], "fixtures_version": manifest["version"],
               "samples": a.samples, "seconds": round(time.time() - t0), "engines": {l: {"lib": lib} for l, lib, _ in engines},
               "medians": {}, "values": data, "problems": problems}
    for label, fxs in data.items():
        summary["medians"][label] = {f: {m: statistics.median(v) for m, v in ms.items()} for f, ms in fxs.items()}
    with open(os.path.join(a.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1, sort_keys=True)
    log(f"perf.py run: {len(names)} fixtures x {len(engines)} engines x {a.samples} samples in {summary['seconds']} s")


# ---- compare --------------------------------------------------------------------------------

def judge(metric, base, head):
    """'slower', 'faster', 'same', or 'recorded' for one metric of one fixture."""
    bm, hm = statistics.median(base), statistics.median(head)
    if metric in COUNTERS:
        if hm > bm and (metric in COUNTER_ZERO or hm > bm * (1 + COUNTER_PCT / 100)):
            return "slower"
        return "faster" if hm < bm else "same"
    if metric in TIMES:
        if hm > bm * TIME_RATIO and hm - bm > TIME_MS and min(head) > max(base):
            return "slower"
        if bm > hm * TIME_RATIO and bm - hm > TIME_MS and min(base) > max(head):
            return "faster"
        return "same"
    return "recorded"


def fmt(v):
    return f"{v:,.1f}" if isinstance(v, float) and not v.is_integer() else f"{int(v):,}"


def cmd_compare(a):
    s = json.load(open(a.summary))
    vals, probs = s["values"], s.get("problems", {})
    base, head = vals.get(a.base, {}), vals.get(a.head, {})
    allow = {x.strip() for x in (a.allow or "").split(",") if x.strip()}
    rows, slower, accepted, notes = [], [], [], []
    fixtures = sorted(set(base) | set(head) | set(probs.get(a.head, {})) | set(probs.get(a.base, {})))
    for f in fixtures:
        hp, bp = probs.get(a.head, {}).get(f), probs.get(a.base, {}).get(f)
        if hp and not bp and f in base:
            slower.append((f, "valid", "the fixture failed on the head: " + hp[0]))
            continue
        if bp and f not in base:
            notes.append(f"`{f}`: no baseline ({bp[0][:160]}); not compared")
            continue
        if f not in head:
            continue
        for m in sorted(set(base.get(f, {})) & set(head[f])):
            b, h = base[f][m], head[f][m]
            v = judge(m, b, h)
            bm, hm = statistics.median(b), statistics.median(h)
            exact = "" if m not in COUNTERS or (len(set(b)) == 1 and len(set(h)) == 1) else " (varies)"
            rows.append((f, m, bm, hm, v, exact))
            if v == "slower":
                (accepted if f"{f}.{m}" in allow else slower).append((f, m, f"{fmt(bm)} -> {fmt(hm)}"))
    md = [f"## Performance gate: {a.head} against {a.base}", "",
          f"Fixture set {s['set_sha256'][:16]} (version {s['fixtures_version']}), {s['samples']} samples a fixture, "
          f"interleaved on one runner, medians; {s['seconds']} s.", ""]
    md.append(f"**{'SLOWER: ' + str(len(slower)) + ' over the margins' if slower else 'PASS: nothing over the margins'}**" +
              (f"; {len(accepted)} accepted by perf_allow" if accepted else ""))
    md.append("")
    for f, m, what in slower:
        md.append(f"- SLOWER `{f}` {m}: {what}")
    for f, m, what in accepted:
        md.append(f"- accepted (perf_allow) `{f}` {m}: {what}")
    md += [""] + [f"- {n}" for n in notes]
    md += ["", "Margins: layouts (frame and script) no rise; other counters (script instructions, jobs, tasks, engine "
           f"calls, BubblePopJS steps) a rise over {COUNTER_PCT:g} %; times (median of samples) more than {TIME_RATIO:.2f}x "
           f"and {TIME_MS:g} ms slower with every head sample slower than every base sample. Primitives, DOM changes and "
           "per-call DOM times are recorded only.", "",
           f"| fixture | metric | {a.base} | {a.head} | |", "|---|---|--:|--:|---|"]
    for f, m, bm, hm, v, exact in rows:
        if v == "recorded" and not a.all_rows:
            continue
        md.append(f"| {f} | {m}{exact} | {fmt(bm)} | {fmt(hm)} | {'' if v in ('same', 'recorded') else v} |")
    os.makedirs(a.out, exist_ok=True)
    text = "\n".join(md) + "\n"
    open(os.path.join(a.out, "report.md"), "w").write(text)
    json.dump({"base": a.base, "head": a.head, "slower": slower, "accepted": accepted, "notes": notes,
               "rows": [dict(zip(("fixture", "metric", "base", "head", "verdict"), r[:5])) for r in rows]},
              open(os.path.join(a.out, "compare.json"), "w"), indent=1)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(text)
    print(text)
    for f, m, what in slower:
        print(f"::error::perf gate: {f} {m} {what}")
    sys.exit(1 if slower else 0)


# ---- perf.csv -------------------------------------------------------------------------------

PERF_COLUMNS = ["run_id", "recorded_utc", "core_commit", "engine_tag", "platform", "set_sha256", "fixtures_version",
                "fixture", "metric", "median", "min", "max", "samples", "kind"]


def cmd_rows(a):
    s = json.load(open(a.summary))
    rows = []
    for f, ms in sorted(s["values"].get(a.label, {}).items()):
        for m, v in sorted(ms.items()):
            kind = "counter" if m in COUNTERS else "time" if m in TIMES else "recorded"
            rows.append({"run_id": a.run_id or os.environ.get("GITHUB_RUN_ID", ""), "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                         "core_commit": a.core_commit, "engine_tag": a.engine_tag, "platform": a.platform,
                         "set_sha256": s["set_sha256"], "fixtures_version": s["fixtures_version"], "fixture": f, "metric": m,
                         "median": statistics.median(v), "min": min(v), "max": max(v), "samples": len(v), "kind": kind})
    for f, why in sorted(s.get("problems", {}).get(a.label, {}).items()):
        rows.append({"run_id": a.run_id or os.environ.get("GITHUB_RUN_ID", ""), "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                     "core_commit": a.core_commit, "engine_tag": a.engine_tag, "platform": a.platform, "set_sha256": s["set_sha256"],
                     "fixtures_version": s["fixtures_version"], "fixture": f, "metric": "invalid", "median": "", "min": "", "max": "",
                     "samples": len(why), "kind": "invalid: " + why[0][:120].replace("\n", " ")})
    old = json.load(open(a.out)) if a.append and os.path.exists(a.out) else []
    json.dump(old + rows, open(a.out, "w"), indent=0)
    log(f"perf.py rows: {len(rows)} rows for {a.core_commit[:12]}")


def cmd_record(a):
    rows = json.load(open(a.rows))
    if not rows:
        log("nothing to record")
        return
    repo = os.path.abspath(a.repo)
    tmp = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), f"perf-results-{os.getpid()}")
    for attempt in range(1, 6):
        tree = f"{tmp}-{attempt}"
        if subprocess.run(["git", "-C", repo, "fetch", "-q", "origin", f"+refs/heads/{RESULTS_BRANCH}:refs/remotes/origin/{RESULTS_BRANCH}"]).returncode:
            time.sleep(5 * attempt)
            continue
        subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "--detach", tree, f"refs/remotes/origin/{RESULTS_BRANCH}"], check=True)
        path = os.path.join(tree, "perf.csv")
        have = set()
        if os.path.exists(path):
            have = {(r["run_id"], r["core_commit"], r["fixture"], r["metric"]) for r in csv.DictReader(open(path))}
        new = [r for r in rows if (str(r["run_id"]), r["core_commit"], r["fixture"], r["metric"]) not in have]
        if not new:
            log("nothing new for perf.csv")
            return
        write_header = not os.path.exists(path)
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=PERF_COLUMNS, extrasaction="ignore")
            if write_header:
                w.writeheader()
            w.writerows(new)
        commits = sorted({r["core_commit"][:12] for r in new})
        msg = f"perf: {len(new)} rows for {', '.join(commits[:6])}{' ...' if len(commits) > 6 else ''}" + \
              (f" ({os.environ['GITHUB_RUN_ID']})" if os.environ.get("GITHUB_RUN_ID") else "")
        subprocess.run(["git", "-C", tree, "add", "perf.csv"], check=True)
        subprocess.run(["git", "-C", tree, "-c", "user.name=github-actions[bot]", "-c",
                        "user.email=41898282+github-actions[bot]@users.noreply.github.com", "commit", "-q", "-m", msg], check=True)
        if a.no_push:
            log(f"committed, not pushed: {tree}")
            return
        if subprocess.run(["git", "-C", tree, "push", "-q", "origin", f"HEAD:refs/heads/{RESULTS_BRANCH}"]).returncode == 0:
            log("pushed: " + msg)
            return
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", tree])
        time.sleep(5 * attempt)
    die("could not push perf.csv after 5 attempts")


# ---- baseline -------------------------------------------------------------------------------

def gh_json(*args):
    p = subprocess.run(["gh", "api", *args], capture_output=True, text=True)
    if p.returncode:
        return None
    return json.loads(p.stdout)


def cmd_baseline(a):  # noqa: C901
    """The newest foafnaut-linux-x86_64 release whose commit is the head or an ancestor of it
    on main: the head then has every change that engine has. Prints tag and commit."""
    tags = []
    for page in range(1, 4):
        rel = gh_json(f"repos/{BUILDS_REPO}/releases?per_page=100&page={page}") or []
        tags += [(r.get("published_at") or "", r["tag_name"]) for r in rel
                 if re.fullmatch(r"build-[0-9a-f]{12}-foafnaut-linux-x86_64", r["tag_name"]) and not r.get("draft")]
        if len(rel) < 100:
            break
    tags.sort(reverse=True)
    for _, tag in tags[: a.max_tries]:
        short = tag.split("-")[1]
        c = gh_json(f"repos/{CORE_REPO}/commits/{short}")
        if not c:
            continue
        sha = c["sha"]
        if sha == a.head and a.exclude_self:
            continue
        if sha == a.head:
            status = "identical"
        else:
            cmp = gh_json(f"repos/{CORE_REPO}/compare/{sha}...{a.head}")
            status = (cmp or {}).get("status")
        if status in ("ahead", "identical"):
            on_main = gh_json(f"repos/{CORE_REPO}/compare/{sha}...main")
            if (on_main or {}).get("status") in ("ahead", "identical"):
                print(f"tag={tag}")
                print(f"commit={sha}")
                log(f"baseline {tag} ({status} of the head)")
                return
    die("no Linux engine release of main is an ancestor of the head")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("run")
    s.add_argument("--core", required=True)
    s.add_argument("--engine", action="append", required=True, help="label=LIB:HOSTROOT")
    s.add_argument("--out", required=True)
    s.add_argument("--samples", type=int, default=3)
    s.add_argument("--fixtures", default="")
    s.add_argument("--font", default="")
    s.add_argument("--ld", action="append", default=[], help="label=DIR of that engine's libleanshared")
    s.add_argument("--timeout", type=int, default=300)
    s.add_argument("--js", action=argparse.BooleanOptionalAction, default=True)
    s.set_defaults(f=cmd_run)
    s = sub.add_parser("compare")
    s.add_argument("--summary", required=True)
    s.add_argument("--base", default="base")
    s.add_argument("--head", default="head")
    s.add_argument("--allow", default="", help="fixture.metric list of accepted rises")
    s.add_argument("--out", required=True)
    s.add_argument("--all-rows", action="store_true")
    s.set_defaults(f=cmd_compare)
    s = sub.add_parser("rows")
    s.add_argument("--summary", required=True)
    s.add_argument("--label", default="head")
    s.add_argument("--core-commit", required=True)
    s.add_argument("--engine-tag", default="")
    s.add_argument("--platform", default="linux-x86_64")
    s.add_argument("--run-id", default="")
    s.add_argument("--out", required=True)
    s.add_argument("--append", action="store_true")
    s.set_defaults(f=cmd_rows)
    s = sub.add_parser("record")
    s.add_argument("--rows", required=True)
    s.add_argument("--repo", default=".")
    s.add_argument("--no-push", action="store_true")
    s.set_defaults(f=cmd_record)
    s = sub.add_parser("baseline")
    s.add_argument("--head", required=True)
    s.add_argument("--max-tries", type=int, default=25)
    s.add_argument("--exclude-self", action="store_true", help="an older engine than the head's own (main's record)")
    s.set_defaults(f=cmd_baseline)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
