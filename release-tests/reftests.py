#!/usr/bin/env python3
"""WPT reftests of Foafnaut releases, recorded like the other suites (the reftests.yml workflow).

WPT reftests (pages without testharness.js, compared as pictures with a reference page) carry no
weight in the headline WPT score: wpt.fyi's summaries give them no subtests, and the full run's
denominator is Chrome's subtests. This records them as suites of their own, one per WPT
directory: `wpt-reftest-svg` (svg/), `wpt-reftest-css` (css/).

Commands:
  plan    which release and WPT commit to run, which suites and shards (the job matrix);
          downloads the WPT manifest and the rival browsers' wpt.fyi summaries at that commit
  paths   the sparse checkout of WPT a suite needs (its directory, its references', support)
  score   join a suite's shard results (core's tests/browser-wpt/wpt-reftests.py run): totals,
          validity, directories, rivals at the same WPT commit, changes since the previous run
  record  append to runs.csv and reftest-rivals.csv on wpt-scores, and runs/<run_id>/ files

How a reftest is run and judged: core's tests/browser-wpt/wpt-reftests.py (WPT's own rules:
the manifest's reftest items at the WPT commit, == and != references, reference chains, fuzzy
annotations, the test's viewport size; wptrunner's comparison: per pixel the largest channel
difference, and the count of pixels that differ) and reftest-render.ts (the release's engine
library draws each page with its CPU raster, Noto Sans and the Hub's fallback fonts, page
scripts on BubblePopJS). Like wpt.fyi, a reftest is one test: PASS or not.

Score: tests passing of all reftests in the directory at the WPT commit. Rivals: the same
tests' statuses in wpt.fyi's runs at the same WPT commit (Chrome, Firefox, Safari, Edge).
Valid when every shard is present, every test has a status, and ERROR (the harness's failures)
is under 0.5% of tests. CRASH and STALL are the engine's defects: listed in meta.json
`incidents`, never ignored.
"""
import argparse, csv, datetime, gzip, importlib.util, io, json, os, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("release_tests", os.path.join(HERE, "release-tests.py"))
rt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rt)
_spec2 = importlib.util.spec_from_file_location("realpages", os.path.join(HERE, "realpages.py"))
rp = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(rp)

# suite -> (WPT directory, shards)
SUITES = {"svg": ("svg/", 1), "css": ("css/", 16)}
RIVALS_FILE = "reftest-rivals.csv"
RIVALS_COLUMNS = ["recorded_utc", "suite", "wpt_commit", "browser", "version", "wptfyi_run_id", "passed",
                  "denominator", "share_pct", "status", "reason"]
RIVAL_BROWSERS = ["chrome", "firefox", "safari", "edge"]
HARNESS_ERROR_MAX = 0.005
DROP_TESTS = 3  # more newly failing tests than this is marked DROP
SUPPORT = ["/fonts/", "/common/", "/resources/", "/images/", "/css/support/", "/css/reference/", "/css/fonts/"]


def log(m):
    print(f"reftests: {m}", file=sys.stderr, flush=True)


def suite_name(s):
    return f"wpt-reftest-{s}"


# ---- the manifest ------------------------------------------------------------------------

def manifest_reftests(path):
    m = json.load(gzip.open(path) if path.endswith(".gz") else open(path))
    out = {}

    def walk(d, p):
        for k, v in d.items():
            if isinstance(v, dict):
                walk(v, p + "/" + k)
            else:
                for item in v[1:]:
                    out[item[0] or (p + "/" + k)] = item[1]
    walk(m["items"].get("reftest", {}), "")
    return out


def cmd_paths(a):
    """The sparse-checkout lines for WPT: the suite's directory, the directories of every
    reference its tests reach (chains too), and the shared support directories."""
    from urllib.parse import urljoin
    items = manifest_reftests(a.manifest)
    prefix = "/" + SUITES[a.suite][0]
    dirs = {prefix} | set(SUPPORT)
    todo = [u for u in items if u.startswith(prefix)]
    seen = set(todo)
    while todo:
        u = todo.pop()
        for ref, _ in items.get(u, []):
            r = urljoin(u, ref)
            if r.startswith("/"):
                dirs.add(r.rsplit("/", 1)[0] + "/")
                if r in items and r not in seen:
                    seen.add(r)
                    todo.append(r)
    # a directory inside another listed one is covered by it
    keep = sorted(d for d in dirs if not any(o != d and d.startswith(o) for o in dirs))
    print("\n".join(keep))

# ---- plan --------------------------------------------------------------------------------

def newest_wpt_commit():
    rows = [r for r in rt.read_csv_url("runs.csv") if r["suite"] == "wpt" and r["valid"] == "true" and r["kind"] == "full"]
    return rows[-1]["wpt_commit"] if rows else ""


def cmd_plan(a):
    rel = [r for r in rp.releases() if not r.get("draft")]
    tag = ""
    if a.release:
        tag = a.release.strip()
        if rp.set_of(tag) != "foafnaut-linux-x86_64":
            rt.die(f"{tag}: give a build-<12 hex>-foafnaut-linux-x86_64 release")
    elif a.event == "workflow_run":
        mine = sorted((r for r in rel if rp.set_of(r["tag_name"]) == "foafnaut-linux-x86_64"
                       and (r["published_at"] or "") >= a.run_created), key=lambda r: r["published_at"])
        tag = mine[-1]["tag_name"] if mine else ""
    else:
        cands = sorted((r for r in rel if rp.set_of(r["tag_name"]) == "foafnaut-linux-x86_64"), key=lambda r: r["published_at"] or "")
        tag = cands[-1]["tag_name"] if cands else ""
    if not tag:
        rt.gh_output(any="false", matrix=json.dumps({"include": []}), suites_json="[]")
        rt.summary("Reftests: no Linux engine release to run")
        return
    e = rp.entry(tag, rel)
    if not e:
        rt.gh_output(any="false", matrix=json.dumps({"include": []}), suites_json="[]")
        rt.summary(f"Reftests: {tag} has no self-contained engine library")
        return
    wpt = a.wpt_commit or newest_wpt_commit()
    if not wpt:
        rt.die("no WPT commit: give --wpt-commit")
    wpt = rt.api(f"repos/web-platform-tests/wpt/commits/{wpt}")["sha"]
    c = rt.api(f"repos/{rt.CORE_REPO}/commits/{e['core_commit']}")
    runs = rt.read_csv_url("runs.csv")
    suites, why = [], []
    for s in [x.strip() for x in a.suites.split(",") if x.strip()]:
        if s not in SUITES:
            rt.die(f"unknown suite {s} (known: {', '.join(SUITES)})")
        done = [r for r in runs if r["suite"] == suite_name(s) and r["valid"] == "true" and r["factoidal_commit"] == e["core_commit"]
                and r["wpt_commit"] == wpt and r["platform"] == "linux-x86_64"]
        if done and not a.force:
            why.append(f"{suite_name(s)}: core {e['core_commit'][:12]} already has a valid run at WPT {wpt[:10]} ({done[-1]['run_id']})")
            continue
        suites.append(s)
    os.makedirs(a.out, exist_ok=True)
    # the inputs every shard shares: the manifest and the rivals' summaries at the WPT commit
    rt.http(f"https://wpt.fyi/api/manifest?sha={wpt}", dest=os.path.join(a.out, "MANIFEST.json"))
    rivals = {}
    ref_names = set(manifest_reftests(os.path.join(a.out, "MANIFEST.json")))
    for b in RIVAL_BROWSERS:
        try:
            runs_b = rt.wptfyi_runs(f"sha={wpt[:10]}&label=master&label=stable&product={b}")
        except Exception as ex:  # noqa: BLE001
            rivals[b] = {"status": "unavailable", "reason": f"wpt.fyi did not answer: {ex}"[:200]}
            continue
        if not runs_b:
            rivals[b] = {"status": "unavailable", "reason": "no stable run on wpt.fyi at this WPT commit"}
            continue
        r = runs_b[0]
        dest = os.path.join(a.out, f"{b}-summary.json")
        try:
            raw = rt.http(r["results_url"])
            try:
                raw = gzip.decompress(raw)
            except OSError:
                pass
            # only the reftests' rows: the shards do not need the rest (13 MB a browser)
            summ = json.loads(raw)
            json.dump({k: v for k, v in summ.items() if k in ref_names}, open(dest, "w"))
            rivals[b] = {"status": "ok", "version": r["browser_version"], "run_id": r["id"], "summary": os.path.basename(dest)}
        except Exception as ex:  # noqa: BLE001
            rivals[b] = {"status": "unavailable", "reason": f"summary of wpt.fyi run {r['id']} not loaded: {ex}"[:200]}
    plan = {"release_tag": tag, "core_commit": e["core_commit"], "commit_utc": c["commit"]["committer"]["date"],
            "web_tag": e["web_tag"], "wpt_commit": wpt, "suites": suites, "trigger": a.trigger, "rivals": rivals,
            "planned_utc": rt.now_utc()}
    json.dump(plan, open(os.path.join(a.out, "plan.json"), "w"), indent=1)
    matrix = [{"suite": s, "prefix": SUITES[s][0], "shard": k, "shards": SUITES[s][1]} for s in suites for k in range(SUITES[s][1])]
    rt.gh_output(any="true" if matrix else "false", matrix=json.dumps({"include": matrix}), core_commit=e["core_commit"],
                 tag=tag, web_tag=e["web_tag"], wpt_commit=wpt, suites_json=json.dumps(suites))
    rt.summary(f"Reftests plan: {tag} (core {e['core_commit'][:12]}), WPT {wpt[:10]}, suites: {', '.join(suites) or 'none'}"
               + ("".join(f"\n- skipped {w}" for w in why)))

# ---- score -------------------------------------------------------------------------------

def directory_of(test, depth=2):
    return "/".join(test.strip("/").split("/")[:depth]) + "/"


def previous_valid(suite, platform):
    rows = [r for r in rt.read_csv_url("runs.csv") if r["suite"] == suite and r["valid"] == "true" and r["platform"] == platform]
    return rows[-1] if rows else None


def read_results_tsv(text):
    out = {}
    rows = csv.DictReader(io.StringIO(text), delimiter="\t")
    for r in rows:
        out[r["test"]] = r["status"]
    return out


def cmd_score(a):
    plan = json.load(open(a.plan))
    suite = suite_name(a.suite)
    shards = []
    for root, _, files in os.walk(a.shards_dir):
        if "results.json" in files:
            shards.append(json.load(open(os.path.join(root, "results.json"))))
    want = SUITES[a.suite][1]
    got_idx = sorted({tuple(s["shard"]) for s in shards})
    tests = sorted((t for s in shards for t in s["tests"]), key=lambda t: t["test"])
    total = len(tests)
    st = {}
    for t in tests:
        st[t["status"]] = st.get(t["status"], 0) + 1
    passed = st.get("PASS", 0)
    # the harness's failures (ERROR); CRASH and STALL are the engine's, listed in meta.json
    harness = st.get("ERROR", 0)
    reasons = []
    # Each missing shard and why (no artifact, or an artifact without results.json): the
    # run is then partial or none, never a score; its tests are not counted as failures.
    have = {int(s["shard"][0]) for s in shards}
    missing_reasons = {}
    for k in sorted(set(range(want)) - have):
        d = os.path.join(a.shards_dir, f"reftest-shard-{a.suite}-{k}")
        missing_reasons[str(k)] = ("artifact without results.json: the shard stopped before writing them" if os.path.isdir(d)
                                   else "no artifact: the job failed, was cancelled or its runner was lost")
        print(f"::error title=Reftests {a.suite} shard {k} gave no results::{missing_reasons[str(k)]}", flush=True)
    completeness = "complete" if len(got_idx) == want else ("partial" if shards else "none")
    if len(got_idx) != want:
        reasons.append(f"{completeness} run: {len(got_idx)} of {want} shards gave results; "
                       + "; ".join(f"shard {k}: {w}" for k, w in missing_reasons.items()))
    if not total:
        reasons.append("no tests")
    if any(not t["status"] for t in tests):
        reasons.append("tests with no status")
    if total and harness >= HARNESS_ERROR_MAX * total:
        reasons.append(f"ERROR {harness} of {total} tests (limit {HARNESS_ERROR_MAX:.1%})")
    # rivals: the same tests in wpt.fyi's runs at the same WPT commit
    rivals, rival_rows = {}, []
    for b, info in plan.get("rivals", {}).items():
        if info.get("status") != "ok":
            rival_rows.append({"recorded_utc": rt.now_utc(), "suite": suite, "wpt_commit": plan["wpt_commit"], "browser": b,
                               "version": "", "wptfyi_run_id": "", "passed": "", "denominator": total, "share_pct": "",
                               "status": "unavailable", "reason": info.get("reason", "")})
            continue
        summ = json.load(open(os.path.join(os.path.dirname(a.plan), info["summary"])))
        rivals[b] = {t["test"]: (summ.get(t["test"]) or {}).get("s") for t in tests}
        n = sum(1 for v in rivals[b].values() if v == "P")
        rival_rows.append({"recorded_utc": rt.now_utc(), "suite": suite, "wpt_commit": plan["wpt_commit"], "browser": b,
                           "version": info["version"], "wptfyi_run_id": info["run_id"], "passed": n, "denominator": total,
                           "share_pct": f"{100 * n / total:.4f}" if total else "", "status": "ok", "reason": ""})
    dirs = {}
    for t in tests:
        d = dirs.setdefault(directory_of(t["test"]), {"tests": 0, "passed": 0, **{b: 0 for b in rivals}})
        d["tests"] += 1
        d["passed"] += t["status"] == "PASS"
        for b in rivals:
            d[b] += rivals[b].get(t["test"]) == "P"
    started = min(s["startedAt"] for s in shards) if shards else rt.now_utc()
    finished = max(s["finishedAt"] for s in shards) if shards else rt.now_utc()
    rid = f"{datetime.datetime.strptime(started, '%Y-%m-%dT%H:%M:%SZ'):%Y%m%dT%H%MZ}-{suite}-linux-x86_64-gh{os.environ.get('GITHUB_RUN_ID', 'local')}a{os.environ.get('GITHUB_RUN_ATTEMPT', '1')}"
    share = 100 * passed / total if total else 0.0
    wall = round((datetime.datetime.strptime(finished, "%Y-%m-%dT%H:%M:%SZ") - datetime.datetime.strptime(started, "%Y-%m-%dT%H:%M:%SZ")).total_seconds() / 60, 1)
    prev = previous_valid(suite, "linux-x86_64")
    row = {"run_id": rid, "started_utc": started, "finished_utc": finished, "trigger": plan["trigger"], "suite": suite,
           "platform": "linux-x86_64", "engine": "native-cpu-raster", "script_engine": "bubblepop",
           "factoidal_commit": plan["core_commit"], "commit_utc": plan["commit_utc"], "snapshot_branch": "",
           "release_tag": plan["release_tag"], "wpt_commit": plan["wpt_commit"], "names_total": total,
           "names_run": total - st.get("CRASH", 0) - st.get("STALL", 0), "passed": passed, "denominator": total,
           "share_pct": f"{share:.4f}", "share_ex_encoding_pct": "", "ok": passed, "error": st.get("ERROR", 0),
           "timeout": st.get("TIMEOUT", 0), "skip": 0, "crash": st.get("CRASH", 0), "stall": st.get("STALL", 0),
           "no_result": 0, "other": 0, "failed": st.get("FAIL", 0), "server_failures": harness,
           "valid": "false" if reasons else "true", "invalid_reason": "; ".join(reasons), "kind": "full",
           "shards": want, "wall_minutes": wall,
           "repeat_of": prev["run_id"] if prev and prev["factoidal_commit"] == plan["core_commit"] and prev["wpt_commit"] == plan["wpt_commit"] else "",
           "runner": f"ubuntu-latest x{want}; core tests/browser-wpt/wpt-reftests.py, CPU raster, Noto Sans",
           "workflow_run_url": a.run_url, "result_url": f"{rt.RAW}/runs/{rid}/results.tsv" + (".gz" if total > 3000 else ""),
           "meta_url": f"{rt.RAW}/runs/{rid}/meta.json"}
    since = None
    if prev and prev.get("result_url"):
        try:
            raw = rt.http(prev["result_url"], tries=2)
            if prev["result_url"].endswith(".gz"):
                raw = gzip.decompress(raw)
            ps = read_results_tsv(raw.decode())
            cur = {t["test"]: t["status"] for t in tests}
            up = sorted(k for k, v in cur.items() if v == "PASS" and ps.get(k) not in (None, "PASS"))
            down = sorted(k for k, v in cur.items() if v != "PASS" and ps.get(k) == "PASS")
            since = {"previous_run": prev["run_id"], "previous_commit": prev["factoidal_commit"], "previous_wpt_commit": prev["wpt_commit"],
                     "previous_passed": int(prev["passed"]), "passed_delta": passed - int(prev["passed"]),
                     "newly_passing": up, "newly_failing": [{"test": k, "status": cur[k]} for k in down],
                     "drop": len(down) > DROP_TESTS, "same_wpt_commit": prev["wpt_commit"] == plan["wpt_commit"]}
        except Exception as ex:  # noqa: BLE001
            since = {"previous_run": prev["run_id"], "error": f"previous results not loaded: {ex}"[:300]}
    meta = {"format": "factoidal-wpt-reftests-run-v1", "row": row,
            "rules": ("Every reftest item of the WPT manifest at wpt_commit under the suite's directory (print reftests are a "
                      "separate kind), run by core tests/browser-wpt/wpt-reftests.py by wptrunner's rules: == and != references, "
                      "reference chains, fuzzy annotations, the test's viewport size (800x600 by default); per pixel the largest "
                      "channel difference and the count of differing pixels against the fuzzy ranges. Drawn by the release's engine "
                      "library with its CPU raster (op render, cpu:true), Noto Sans and the Hub's fallback fonts "
                      "(third_party/fonts), page scripts on BubblePopJS; reftest-wait honoured for up to 6 s of page time "
                      "(TIMEOUT after). A reftest is one test, PASS or not, as on wpt.fyi."),
            "validity": {"rules": f"every shard present; every test has a status; ERROR (harness) under {HARNESS_ERROR_MAX:.1%} of tests",
                         "valid": not reasons, "reasons": reasons},
            "totals": {"tests": total, "passed": passed, "share_pct": round(share, 4), "statuses": st, "harness_errors": harness,
                       **{f"{b}_passed": sum(1 for v in rivals[b].values() if v == "P") for b in rivals},
                       **{f"{b}_share_pct": round(100 * sum(1 for v in rivals[b].values() if v == "P") / total, 4) for b in rivals if total},
                       "passed_where_chrome_passes": sum(1 for t in tests if t["status"] == "PASS" and rivals.get("chrome", {}).get(t["test"]) == "P"),
                       "chrome_passes_we_fail": sum(1 for t in tests if t["status"] != "PASS" and rivals.get("chrome", {}).get(t["test"]) == "P"),
                       # passes of pages where the engine skipped something (test or reference): both
                       # pictures may lack the same part
                       "passed_with_skips": sum(1 for t in tests if t["status"] == "PASS" and t.get("skipped"))},
            "directories": dict(sorted(dirs.items())), "rivals": rival_rows, "since_previous": since,
            "incidents": [{"test": t["test"], "status": t["status"], "message": t.get("message")} for t in tests if t["status"] in ("CRASH", "STALL")],
            "shards": [{"shard": s["shard"], "tests": len(s["tests"]), "wallSeconds": s["wallSeconds"], "pagesDrawn": s["pagesDrawn"],
                        "engineSha256": s["engine"]["sha256"]} for s in shards],
            "completeness": completeness, "shards_missing_reasons": missing_reasons,
            "plan": {k: v for k, v in plan.items() if k != "rivals"}}
    os.makedirs(a.out, exist_ok=True)
    json.dump(row, open(os.path.join(a.out, "row.json"), "w"), indent=1)
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    json.dump(rival_rows, open(os.path.join(a.out, "rivals.json"), "w"), indent=1)
    buf = io.StringIO()
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    w.writerow(["test", "status", *rivals.keys(), "max_difference", "total_pixels", "ms", "skipped", "message"])
    for t in tests:
        e = next((x for x in t["edges"] if "holds" in x and not x["holds"]), None) or (t["edges"][0] if t["edges"] else {})
        w.writerow([t["test"], t["status"], *[rivals[b].get(t["test"]) or "" for b in rivals],
                    e.get("maxDifference", ""), e.get("totalPixels", ""), t.get("ms", ""),
                    "; ".join(sorted({m for v in (t.get("skipped") or {}).values() for m in v}))[:300].replace("\t", " "),
                    (t.get("message") or "").replace("\t", " ")[:300]])
    name = "results.tsv" + (".gz" if total > 3000 else "")
    if name.endswith(".gz"):
        with gzip.open(os.path.join(a.out, name), "wt") as f:
            f.write(buf.getvalue())
    else:
        open(os.path.join(a.out, name), "w").write(buf.getvalue())
    md = summary_md(meta)
    open(os.path.join(a.out, "summary.md"), "w").write(md)
    open(os.path.join(a.out, "changes.md"), "w").write(changes_md(meta))
    rt.summary(md)
    rt.gh_output(run_id=rid, valid=row["valid"])


def changes_md(meta):
    s = meta.get("since_previous")
    if not s:
        return "No previous valid run of this suite.\n"
    if s.get("error"):
        return f"Previous valid run {s['previous_run']}: {s['error']}\n"
    L = [f"### Since {s['previous_run']} (core {s['previous_commit'][:12]}"
         + ("" if s["same_wpt_commit"] else f", other WPT commit {s['previous_wpt_commit'][:10]}") + ")", "",
         f"Tests passed {s['previous_passed']:,} -> {meta['totals']['passed']:,} ({s['passed_delta']:+,})"
         + (" DROP" if s["drop"] else ""), "",
         f"Newly passing: {len(s['newly_passing']):,}. Newly not passing: {len(s['newly_failing']):,}.", ""]
    if s["newly_failing"]:
        L += ["Newly not passing:", ""] + [f"- `{x['test']}`: {x['status']}" for x in s["newly_failing"][:300]] + [""]
    if s["newly_passing"]:
        L += ["Newly passing:", ""] + [f"- `{x}`" for x in s["newly_passing"][:300]]
    return "\n".join(L) + "\n"


def summary_md(meta):
    r, t = meta["row"], meta["totals"]
    riv = [x for x in meta["rivals"] if x["status"] == "ok"]
    L = [f"### WPT reftests {r['suite']} at WPT {r['wpt_commit'][:10]}, core {r['factoidal_commit'][:12]}: "
         f"{t['passed']:,} of {t['tests']:,} = **{t['share_pct']:.2f}%**"
         + ("" if r["valid"] == "true" else f" (INVALID: {r['invalid_reason']})"), "",
         "Same tests on wpt.fyi at the same WPT commit: " + (", ".join(f"{x['browser']} {x['version']} {x['passed']:,} ({float(x['share_pct']):.2f}%)" for x in riv) or "none"),
         "", f"Statuses: {', '.join(f'{k} {v}' for k, v in sorted(t['statuses'].items()))}. Where Chrome passes and Foafnaut does not: {t['chrome_passes_we_fail']}. "
         f"Passes where the engine skipped something on the test or a reference: {t['passed_with_skips']}.",
         f"Wall {r['wall_minutes']} min on {r['shards']} shard(s).", "",
         "| directory | tests | Foafnaut | " + " | ".join(x["browser"] for x in riv) + " |", "|---|---:|---:|" + "---:|" * len(riv)]
    for d, v in meta["directories"].items():
        L.append(f"| {d} | {v['tests']} | {v['passed']} | " + " | ".join(str(v.get(x["browser"], "")) for x in riv) + " |")
    if meta.get("since_previous"):
        L += ["", changes_md(meta)]
    return "\n".join(L) + "\n"

# ---- record ------------------------------------------------------------------------------

def cmd_record(a):
    d = a.src
    row = json.load(open(os.path.join(d, "row.json")))
    meta = json.load(open(os.path.join(d, "meta.json")))
    riv = json.load(open(os.path.join(d, "rivals.json")))
    repo = os.path.abspath(a.repo)
    tmp = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), f"reftest-results-{os.getpid()}")
    for attempt in range(1, 6):
        tree = f"{tmp}-{attempt}"
        if subprocess.run(["git", "-C", repo, "fetch", "-q", "origin", f"+refs/heads/{rt.RESULTS_BRANCH}:refs/remotes/origin/{rt.RESULTS_BRANCH}"]).returncode:
            time.sleep(5 * attempt)
            continue
        subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "--detach", tree, f"refs/remotes/origin/{rt.RESULTS_BRANCH}"], check=True)
        runs_csv = os.path.join(tree, "runs.csv")
        known = {r["run_id"] for r in csv.DictReader(open(runs_csv))} if os.path.exists(runs_csv) else set()
        if row["run_id"] not in known:
            rt.append_csv(runs_csv, rt.RUNS_COLUMNS, [row])
        rpath = os.path.join(tree, RIVALS_FILE)
        old = list(csv.DictReader(open(rpath))) if os.path.exists(rpath) else []
        seen = {(r["suite"], r["wpt_commit"], r["browser"], r["version"], r["status"]) for r in old}
        new = [r for r in riv if (r["suite"], r["wpt_commit"], r["browser"], str(r["version"]), r["status"]) not in seen]
        if new:
            rt.append_csv(rpath, RIVALS_COLUMNS, new)
        rd = os.path.join(tree, "runs", row["run_id"])
        os.makedirs(rd, exist_ok=True)
        json.dump(meta, open(os.path.join(rd, "meta.json"), "w"), indent=1)
        open(os.path.join(rd, "changes.md"), "w").write(changes_md(meta))
        for name in ("results.tsv", "results.tsv.gz"):
            if os.path.exists(os.path.join(d, name)):
                with open(os.path.join(d, name), "rb") as src, open(os.path.join(rd, name), "wb") as dst:
                    dst.write(src.read())
        with open(os.path.join(rd, "directories.csv"), "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            bs = [x["browser"] for x in riv if x["status"] == "ok"]
            w.writerow(["directory", "tests", "passed", *bs])
            for k, v in meta["directories"].items():
                w.writerow([k, v["tests"], v["passed"], *[v.get(b, "") for b in bs]])
        subprocess.run(["git", "-C", tree, "add", "-A"], check=True)
        if subprocess.run(["git", "-C", tree, "diff", "--cached", "--quiet"]).returncode == 0:
            log("nothing new on the branch")
            return
        msg = f"results: {row['suite']} {row['run_id']} valid={row['valid']} {row['share_pct']}%"
        subprocess.run(["git", "-C", tree, "-c", "user.name=github-actions[bot]", "-c",
                        "user.email=41898282+github-actions[bot]@users.noreply.github.com", "commit", "-q", "-m", msg], check=True)
        if a.no_push:
            log(f"committed, not pushed: {tree}")
            return
        if subprocess.run(["git", "-C", tree, "push", "-q", "origin", f"HEAD:refs/heads/{rt.RESULTS_BRANCH}"]).returncode == 0:
            log(f"pushed: {msg}")
            return
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", tree])
        time.sleep(5 * attempt)
    rt.die("could not push to the results branch after 5 attempts")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--event", default="workflow_dispatch")
    p.add_argument("--run-created", default="")
    p.add_argument("--release", default="")
    p.add_argument("--wpt-commit", default="")
    p.add_argument("--suites", default="svg")
    p.add_argument("--trigger", default="manual")
    p.add_argument("--force", action="store_true")
    p.add_argument("--out", required=True)
    q = sub.add_parser("paths")
    q.add_argument("--manifest", required=True)
    q.add_argument("--suite", required=True)
    s = sub.add_parser("score")
    s.add_argument("--plan", required=True)
    s.add_argument("--suite", required=True)
    s.add_argument("--shards-dir", required=True)
    s.add_argument("--out", required=True)
    s.add_argument("--run-url", default="")
    r = sub.add_parser("record")
    r.add_argument("--src", required=True)
    r.add_argument("--repo", default=".")
    r.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    {"plan": cmd_plan, "paths": cmd_paths, "score": cmd_score, "record": cmd_record}[a.cmd](a)


if __name__ == "__main__":
    main()
