#!/usr/bin/env python3
"""Full Test262 runs of Factoidal's BubblePopJS (the test262.yml workflow).

The whole tc39/test262 suite at a pinned commit: every file under test/ (FIXTURE files are
loaded by the tests that import them, not run), each in the modes Test262 runs it in
(INTERPRETING.md: sloppy and strict, onlyStrict strict, noStrict/raw sloppy, module once as a
module), with includes, negative tests by phase and type, async tests by $DONE. The runner is
core's `bubblepop-test262 test262-files` (WasmVM/Hosts/Test262Page.lean): BubblePopJS on the
page realm Foafnaut runs page scripts in (prelude.js on an empty document), built from the
release's core commit. `--realm engine` (leanjs, the interpreter alone) is a diagnostic only.

Commands:
  plan      choose the core commit (the newest main release), say whether to run
  list      the files of the checkout and their metadata (files.json)
  run       one shard: files[k::n], in --jobs processes of chunks; a process that dies or says
            nothing for --stall seconds, or grows past --rss-mb, has its current test recorded
            (CRASH or STALL) and the rest of its chunk runs in a new process
  score     join the shards: validity, headline, directories, features, changes, rivals
  record    append to runs.csv and test262-rivals.csv on wpt-scores, runs/<run_id>/ files

Headline (the number to quote): files passing in every mode they run in, of all files: the
unit test262.fyi uses, so rival engines compare on one scale. Second number: the same without
the files of the excluded features (test262-excluded-features.txt plus the stage 3 proposals
of features.txt at the pinned commit). Runs (one per file and mode) are in meta.json too.
"""
import argparse, csv, datetime, gzip, importlib.util, json, os, re, subprocess, sys, threading, time, queue, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("release_tests", os.path.join(HERE, "release-tests.py"))
rt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rt)

SUITE = "test262"
RIVALS_FILE = "test262-rivals.csv"
RIVALS_COLUMNS = ["recorded_utc", "test262_commit", "engine", "version", "passed", "denominator", "share_pct",
                  "status", "reason", "source", "generated_utc"]
# test262.fyi engine ids and the names shown for them
FYI_ENGINES = {"v8": "V8", "sm": "SpiderMonkey", "jsc": "JavaScriptCore", "qjs_ng": "QuickJS-NG", "qjs": "QuickJS",
               "xs": "XS", "libjs": "LibJS (Ladybird)", "boa": "Boa", "kiesel": "Kiesel", "nova": "Nova",
               "porffor": "Porffor", "njs": "njs", "v8_exp": "V8 (experimental flags)",
               "sm_exp": "SpiderMonkey (experimental flags)", "jsc_exp": "JavaScriptCore (experimental flags)"}
FYI = "https://data.test262.fyi"
RUNNERS = {"page": "bubblepop-test262", "engine": "leanjs"}
REALM_WHY = {
    "page": "the page realm Foafnaut runs page scripts in (core WasmVM/Hosts/Test262Page.lean: LeanJS.prepareSource, "
            "BubblePopJS with tools/wasmvm/quickjs/prelude.js on an empty document), built from the release's core commit",
    "engine": "the Lean JavaScript interpreter alone (L4Factoidal.JS, leanjs): no page objects, so no Temporal or Intl from "
              "prelude.js; a diagnostic, not the score"}
HARNESS_ERROR_MAX = 0.005      # runner-level errors (no result, a harness include missing) per run
DROP_POINTS = 0.2              # a fall of more than this many points is marked DROP


def log(m):
    print(f"test262: {m}", file=sys.stderr, flush=True)


# ---- metadata --------------------------------------------------------------------------------

def parse_meta(src):
    """flags, features, includes, negative phase/type from the /*--- ---*/ front matter."""
    m = re.search(r"/\*---(.*?)---\*/", src, re.S)
    out = {"flags": [], "features": [], "includes": [], "phase": None, "type": None}
    if not m:
        return out
    cur = None
    for line in m.group(1).split("\n"):
        t = line.strip()
        k = re.match(r"^(\w+):\s*(.*)$", line)
        if k and not line.startswith((" ", "\t")):
            key, val = k.group(1), k.group(2).strip()
            cur = key
            if key in ("flags", "features", "includes") and val.startswith("["):
                out[key] = [x.strip() for x in val.strip("[]").split(",") if x.strip()]
                cur = None
            continue
        if cur in ("features", "includes") and t.startswith("- "):
            out[cur].append(t[2:].strip())
        elif cur == "negative":
            if t.startswith("phase:"):
                out["phase"] = t[6:].strip()
            elif t.startswith("type:"):
                out["type"] = t[5:].strip()
    return out


def modes_of(flags):
    if "module" in flags:
        return ["module"]
    if "onlyStrict" in flags:
        return ["strict"]
    if "noStrict" in flags or "raw" in flags:
        return ["sloppy"]
    return ["sloppy", "strict"]


def cmd_list(a):
    root = os.path.abspath(a.root)
    files = {}
    for dp, dns, fns in os.walk(os.path.join(root, "test")):
        dns.sort()
        for fn in sorted(fns):
            if fn.endswith(".js") and not fn.endswith("_FIXTURE.js"):
                p = os.path.join(dp, fn)
                rel = os.path.relpath(p, root)
                m = parse_meta(open(p, encoding="utf-8", errors="replace").read())
                files[rel] = {"modes": modes_of(m["flags"]), "features": m["features"], "flags": m["flags"]}
    proposals = []
    ft = os.path.join(root, "features.txt")
    if os.path.exists(ft):
        sec = None
        for line in open(ft):
            if line.startswith("## ") and line[3:].strip() in ("Proposed language features", "Standard language features", "Test-Harness Features"):
                sec = line[3:].strip()
            elif sec == "Proposed language features" and line.strip() and not line.startswith("#"):
                proposals.append(line.strip())
    json.dump({"files": files, "proposals": proposals}, open(a.out, "w"))
    log(f"{len(files)} files, {sum(len(v['modes']) for v in files.values())} runs, {len(proposals)} stage 3 features")


# ---- running ---------------------------------------------------------------------------------

def rss_mb(pid):
    try:
        for line in open(f"/proc/{pid}/status"):
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) // 1024
    except OSError:
        pass
    return 0


def cmd_run(a):
    root, out = os.path.abspath(a.root), os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    allf = sorted(json.load(open(a.files))["files"])
    mine = allf[a.shard::a.shards]
    chunks = [mine[i:i + a.chunk] for i in range(0, len(mine), a.chunk)]
    q = queue.Queue()
    for c in chunks:
        q.put(c)
    lines, lock, t0 = [], threading.Lock(), time.time()
    procs = {"started": 0, "crashes": 0}

    def run_chunk(names, k):
        while names:
            lst = os.path.join(out, f"chunk-{k}.list")
            with open(lst, "w") as f:
                f.write("\n".join(names) + "\n")
            p = subprocess.Popen([a.leanjs, "test262-files", root, lst], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, errors="replace", bufsize=1)
            with lock:
                procs["started"] += 1
            st = {"last": time.time(), "why": None}

            def watchdog():
                while p.poll() is None:
                    if time.time() - st["last"] > a.stall:
                        st["why"] = ("STALL", f"no result in {a.stall} s")
                        p.kill()
                        return
                    r = rss_mb(p.pid)
                    if r > a.rss_mb:
                        st["why"] = ("CRASH", f"killed by the runner: {r} MB resident, over {a.rss_mb} MB")
                        p.kill()
                        return
                    time.sleep(1)
            threading.Thread(target=watchdog, daemon=True).start()
            err = []
            threading.Thread(target=lambda: err.append(p.stderr.read()), daemon=True).start()
            got, cur = [], None
            for l in p.stdout:
                st["last"] = time.time()
                l = l.rstrip("\n")
                if l.startswith("START "):
                    cur = l[6:]
                elif l[:5] in ("PASS ", "FAIL ", "SKIP "):
                    got.append(l)
                    cur = None
            p.wait()
            time.sleep(0.2)
            with lock:
                lines.extend(got)
            done = {g.split(" ")[1] for g in got}
            if cur is None:
                rest = [n for n in names if n not in done]
                if rest and p.returncode != 0:
                    # died between tests (or before the first): every test left has no result
                    with lock:
                        for n in rest:
                            lines.append(f"CRASH {n} - the runner process ended ({p.returncode}) before this test")
                return
            rel, mode = cur.rsplit(" ", 1)
            kind, why = st["why"] or ("CRASH", f"exit {p.returncode}: " + " ".join(("".join(err))[-300:].split())[:200])
            with lock:
                procs["crashes"] += 1
                lines.append(f"{kind} {rel} {mode} {why}")
            i = names.index(rel)
            # the modes of `rel` not yet run go to a new process with the rest of the chunk
            names = names[i + 1:]
            later = [m for m in json_modes.get(rel, []) if m != mode and f"{rel} {m}" not in {" ".join(g.split(" ")[1:3]) for g in got}]
            with lock:
                for m in later:
                    if json_modes[rel].index(m) > json_modes[rel].index(mode):
                        lines.append(f"{kind} {rel} {m} not run: the process ended in its {mode} run")

    json_modes = {k: v["modes"] for k, v in json.load(open(a.files))["files"].items()}

    def worker(k):
        while True:
            try:
                c = q.get_nowait()
            except queue.Empty:
                return
            run_chunk(c, k)
    ts = [threading.Thread(target=worker, args=(k,)) for k in range(a.jobs)]
    for th in ts:
        th.start()
    for th in ts:
        th.join()
    lines.sort()
    with open(os.path.join(out, "results.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    info = {"shard": a.shard, "shards": a.shards, "files": len(mine), "lines": len(lines), "seconds": round(time.time() - t0),
            "jobs": a.jobs, "processes": procs["started"], "process_ends": procs["crashes"]}
    json.dump(info, open(os.path.join(out, "shard.json"), "w"))
    log(f"shard {a.shard}/{a.shards}: {len(mine)} files, {len(lines)} runs, {info['seconds']} s")


# ---- scoring ---------------------------------------------------------------------------------

def directory_of(rel):
    parts = rel.split("/")          # test/<section>/<X>/...
    if len(parts) <= 3:
        return parts[1]
    return f"{parts[1]}/{parts[2]}"


def read_excluded(path, proposals):
    ex = {}
    for line in open(path):
        line = line.split("#", 1)
        name = line[0].strip()
        if name:
            ex[name] = (line[1].strip() if len(line) > 1 else "")
    for p in proposals:
        ex.setdefault(p, "stage 3 proposal (features.txt, Proposed language features)")
    return ex


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "factoidal-release-tests"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    return gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw


def fetch_retry(url, tries=3):
    last = None
    for i in range(tries):
        try:
            return fetch(url)
        except Exception as e:  # noqa: BLE001
            last = e
            if "404" in str(e):
                break
            time.sleep(4 * (i + 1))
    raise RuntimeError(f"{url}: {last}")


def rivals(test262_commit, sections):
    """Rows for test262-rivals.csv from test262.fyi, and the rivals' per-directory passes. A rival
    whose numbers cannot be had, or that test262.fyi ran at another Test262 commit, is a row with
    status unavailable / other_commit, and never stops the run."""
    rows, dirs, now = [], {}, rt.now_utc()
    try:
        meta = json.loads(fetch_retry(f"{FYI}/meta.json"))
        index = json.loads(fetch_retry(f"{FYI}/index.json"))
    except Exception as e:  # noqa: BLE001
        log(f"test262.fyi unavailable: {e}")
        return [{"recorded_utc": now, "test262_commit": test262_commit, "engine": "*", "status": "unavailable",
                 "reason": f"test262.fyi did not answer: {e}"[:200], "source": FYI}], {}, None
    rev = (meta.get("test262") or {}).get("revision", "")
    gen = meta.get("times", {}).get("generatedAt")
    gen_utc = datetime.datetime.fromtimestamp(gen / 1000, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if gen else ""
    same = bool(rev) and test262_commit.startswith(rev)
    for eng, label in FYI_ENGINES.items():
        if eng not in index.get("engines", {}):
            rows.append({"recorded_utc": now, "test262_commit": test262_commit, "engine": label, "status": "unavailable",
                         "reason": "not on test262.fyi", "source": FYI, "generated_utc": gen_utc})
            continue
        p, t = index["engines"][eng], index["total"]
        rows.append({"recorded_utc": now, "test262_commit": test262_commit if same else rev, "engine": label,
                     "version": meta.get("engines", {}).get(eng, ""), "passed": p, "denominator": t,
                     "share_pct": f"{100 * p / t:.4f}" if t else "", "status": "ok" if same else "other_commit",
                     "reason": "" if same else f"test262.fyi ran Test262 {rev}, not {test262_commit[:10]}",
                     "source": f"{FYI}/index.json", "generated_utc": gen_utc})
    if same:
        for sec in sections:
            try:
                d = json.loads(fetch_retry(f"{FYI}/{sec}.json"))
            except Exception as e:  # noqa: BLE001
                log(f"test262.fyi {sec}: {e}")
                continue
            dirs[sec] = {"total": d["total"], "engines": d["engines"]}
            for k, v in d.get("files", {}).items():
                dirs[k] = {"total": v["total"], "engines": v["engines"]}
    return rows, dirs, {"revision": rev, "generated_utc": gen_utc, "same_commit": same}


def prev_valid(test262_commit, platform):
    rows = [r for r in rt.read_csv_url("runs.csv") if r["suite"] == SUITE and r["valid"] == "true"
            and r["wpt_commit"] == test262_commit and r["platform"] == platform]
    return rows[-1] if rows else None


def per_file_from_results(text):
    st = {}
    for l in text.splitlines():
        p = l.split(" ", 3)
        if len(p) < 3:
            continue
        st.setdefault(p[1], True)
        st[p[1]] = st[p[1]] and p[0] == "PASS"
    return st


def cmd_score(a):
    info = json.load(open(a.files))
    files, proposals = info["files"], info["proposals"]
    excluded = read_excluded(a.excluded, proposals)
    shard_infos, lines, missing_reasons = [], [], {}
    for k in range(a.shards):
        d = os.path.join(a.shards_dir, f"test262-shard-{k}")
        if not os.path.exists(os.path.join(d, "results.txt")):
            # Why: no artifact (the job failed or its runner was lost before the upload), or
            # an artifact without results. Its files count as no result: the run is not valid.
            missing_reasons[str(k)] = ("artifact without results.txt: the shard's runner stopped before writing them"
                                       if os.path.isdir(d) else "no artifact: the job failed, was cancelled or its runner was lost")
            print(f"::error title=Test262 shard {k} gave no results::{missing_reasons[str(k)]}", flush=True)
            continue
        shard_infos.append(json.load(open(os.path.join(d, "shard.json"))))
        lines += [l for l in open(os.path.join(d, "results.txt")).read().splitlines() if l.strip()]
    got = {}
    for l in lines:
        p = l.split(" ", 3)
        if len(p) >= 3:
            got[(p[1], p[2])] = (p[0], p[3] if len(p) > 3 else "")
    runs_total = sum(len(v["modes"]) for v in files.values())
    no_result = [(f, m) for f, v in files.items() for m in v["modes"] if (f, m) not in got]
    harness_err = [k for k, v in got.items() if v[0] == "SKIP" and "not in the harness" in v[1]]
    outcomes = {}
    for v in got.values():
        outcomes[v[0]] = outcomes.get(v[0], 0) + 1
    fpass, fwhy = {}, {}
    for f, v in files.items():
        res = [got.get((f, m), ("NORESULT", "")) for m in v["modes"]]
        fpass[f] = all(r[0] == "PASS" for r in res)
        if not fpass[f]:
            bad = next((m, r) for m, r in zip(v["modes"], res) if r[0] != "PASS")
            fwhy[f] = f"{bad[1][0]} {bad[0]} {bad[1][1]}"[:200]
    ex_files = {f for f, v in files.items() if any(x in excluded for x in v["features"])}
    passed = sum(fpass.values())
    total = len(files)
    passed_ex = sum(1 for f in files if fpass[f] and f not in ex_files)
    total_ex = total - len(ex_files)
    runs_passed = sum(1 for v in got.values() if v[0] == "PASS")
    reasons = []
    missing_shards = a.shards - len(shard_infos)
    if missing_shards:
        reasons.append(f"{'partial' if shard_infos else 'none'} run: {len(shard_infos)} of {a.shards} shards gave results; "
                       + "; ".join(f"shard {k}: {w}" for k, w in missing_reasons.items()))
    if len(no_result) + len(harness_err) > HARNESS_ERROR_MAX * runs_total:
        reasons.append(f"{len(no_result)} runs with no result and {len(harness_err)} harness errors, over {HARNESS_ERROR_MAX:.1%} of {runs_total:,} runs")
    if total < a.min_files:
        reasons.append(f"only {total} files listed (fewer than {a.min_files}: not the whole suite)")
    dirs, secs, feats = {}, {}, {}
    for f, v in files.items():
        for key, tab in ((directory_of(f), dirs), (f.split("/")[1], secs)):
            d = tab.setdefault(key, {"total": 0, "passed": 0, "runs": 0, "runs_passed": 0})
            d["total"] += 1
            d["passed"] += fpass[f]
            d["runs"] += len(v["modes"])
            d["runs_passed"] += sum(1 for m in v["modes"] if got.get((f, m), ("",))[0] == "PASS")
        for x in v["features"] or ["(none)"]:
            t = feats.setdefault(x, {"total": 0, "passed": 0, "excluded": x in excluded})
            t["total"] += 1
            t["passed"] += fpass[f]
    for tab in (dirs, secs, feats):
        for d in tab.values():
            d["share_pct"] = round(100 * d["passed"] / d["total"], 4) if d["total"] else 0.0
    fails = {}
    for (f, m), (s, why) in got.items():
        if s != "PASS":
            key = (s, re.sub(r"\d+", "N", why)[:70])
            fails[key] = fails.get(key, 0) + 1
    started = a.started or rt.now_utc()
    rid = (f"{started.replace('-', '').replace(':', '')[:13]}Z-test262-{a.platform}"
           + (f"-gh{os.environ['GITHUB_RUN_ID']}a{os.environ.get('GITHUB_RUN_ATTEMPT', '1')}" if os.environ.get("GITHUB_RUN_ID") else "-local"))
    wall = round((time.time() - datetime.datetime.strptime(started, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()) / 60, 1) if a.started else ""
    share = 100 * passed / total if total else 0.0
    share_ex = 100 * passed_ex / total_ex if total_ex else 0.0
    prev = prev_valid(a.test262_commit, a.platform) if not a.no_prev else None
    row = {"run_id": rid, "started_utc": started, "finished_utc": rt.now_utc(), "trigger": a.trigger, "suite": SUITE,
           "platform": a.platform, "engine": "bubblepopjs-page" if a.realm == "page" else "bubblepopjs-engine", "script_engine": "bubblepop",
           "factoidal_commit": a.core_commit, "commit_utc": a.commit_utc, "snapshot_branch": "", "release_tag": a.release_tag,
           "wpt_commit": a.test262_commit, "names_total": total, "names_run": total - len({f for f, _ in no_result}),
           "passed": passed, "denominator": total, "share_pct": f"{share:.4f}", "share_ex_encoding_pct": f"{share_ex:.4f}",
           "ok": outcomes.get("PASS", 0), "error": outcomes.get("FAIL", 0), "timeout": 0, "skip": outcomes.get("SKIP", 0),
           "crash": outcomes.get("CRASH", 0), "stall": outcomes.get("STALL", 0), "no_result": len(no_result), "other": 0,
           "failed": total - passed, "server_failures": len(harness_err), "valid": "false" if reasons else "true",
           "invalid_reason": "; ".join(reasons), "kind": "full", "shards": a.shards, "wall_minutes": wall,
           "repeat_of": prev["run_id"] if prev and prev["factoidal_commit"] == a.core_commit else "",
           "runner": f"ubuntu-latest x{a.shards} ({shard_infos[0]['jobs'] if shard_infos else '?'} processes each); "
                     f"{RUNNERS[a.realm]} built from core {a.core_commit[:12]}",
           "workflow_run_url": a.run_url, "result_url": a.result_url.replace("RUN_ID", rid) if a.result_url else "",
           "meta_url": f"{rt.RAW}/runs/{rid}/meta.json"}
    # changes against the previous valid run at the same Test262 commit
    since = None
    if prev and prev.get("result_url"):
        try:
            pf = per_file_from_results(fetch_retry(prev["result_url"]).decode())
            newly_pass = sorted(f for f in files if fpass[f] and pf.get(f) is False)
            newly_fail = sorted(f for f in files if not fpass[f] and pf.get(f) is True)
            pts = share - float(prev["share_pct"])
            since = {"previous_run": prev["run_id"], "previous_commit": prev["factoidal_commit"], "previous_passed": int(prev["passed"]),
                     "passed_delta": passed - int(prev["passed"]), "points": round(pts, 4), "drop": pts < -DROP_POINTS,
                     "newly_passing": newly_pass, "newly_failing": [{"file": f, "why": fwhy.get(f, "")} for f in newly_fail]}
        except Exception as e:  # noqa: BLE001
            since = {"previous_run": prev["run_id"], "error": f"previous results not loaded: {e}"[:300]}
    riv_rows, riv_dirs, riv_info = ([], {}, None) if a.no_rivals else rivals(a.test262_commit, sorted(secs))
    rival_dirs = {}
    for k, v in riv_dirs.items():
        rival_dirs[k] = {"total": v["total"], **{FYI_ENGINES.get(e, e): n for e, n in v["engines"].items() if e in ("v8", "sm", "jsc", "qjs_ng")}}
    meta = {"format": "factoidal-test262-run-v1", "row": row,
            "rules": ("tc39/test262 at wpt_commit (for suite test262 that column holds the Test262 commit); every file under test/ "
                      "except _FIXTURE files, each in the modes Test262 runs it in (sloppy and strict; onlyStrict strict; noStrict and "
                      "raw sloppy; module once, as a module); includes from harness/; negative tests pass on the named error type in "
                      "the named phase; async tests pass on Test262:AsyncTestComplete. A file passes when every mode passes "
                      "(the unit of test262.fyi). passed/denominator: files. share_ex_encoding_pct holds, for this suite, the share "
                      "without the files of the excluded features (totals.share_ex_features_pct). $262: global and "
                      "detachArrayBuffer only (createRealm, evalScript, gc, agent, IsHTMLDDA absent: those tests fail)."),
            "engine": {"script_engine": "bubblepop", "realm": a.realm, "runner": RUNNERS[a.realm] + " test262-files",
                       "why": REALM_WHY[a.realm],
                       "core_commit": a.core_commit, "release_tag": a.release_tag},
            "validity": {"rules": f"every file listed and every shard present; runs with no result plus harness errors under "
                                  f"{HARNESS_ERROR_MAX:.1%} of runs; at least {a.min_files} files",
                         "valid": not reasons, "reasons": reasons, "no_result": len(no_result), "harness_errors": len(harness_err),
                         "no_result_sample": [f"{f} {m}" for f, m in no_result[:50]]},
            "totals": {"files": total, "passed": passed, "share_pct": round(share, 4), "files_ex_features": total_ex,
                       "passed_ex_features": passed_ex, "share_ex_features_pct": round(share_ex, 4), "runs": runs_total,
                       "runs_passed": runs_passed, "runs_share_pct": round(100 * runs_passed / runs_total, 4) if runs_total else 0.0,
                       "outcomes": outcomes},
            "excluded_features": sorted(excluded), "excluded_features_why": excluded,
            "sections": dict(sorted(secs.items())), "directories": dict(sorted(dirs.items())), "features": dict(sorted(feats.items())),
            "top_failures": [{"status": k[0], "why": k[1], "runs": v} for k, v in sorted(fails.items(), key=lambda kv: -kv[1])[:80]],
            "incidents": {"crash_or_stall": [f"{v[0]} {f} {m} {v[1]}" for (f, m), v in sorted(got.items()) if v[0] in ("CRASH", "STALL")][:1000]},
            "since_previous": since, "rivals": {"source": riv_info, "rows": riv_rows, "directories": rival_dirs},
            "completeness": "complete" if not missing_shards and not no_result else ("partial" if shard_infos else "none"),
            "shards_missing_reasons": missing_reasons, "shards": shard_infos}
    os.makedirs(a.out, exist_ok=True)
    json.dump(row, open(os.path.join(a.out, "row.json"), "w"), indent=1)
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    with gzip.open(os.path.join(a.out, f"{rid}.test262.txt.gz"), "wt") as f:
        f.write("\n".join(sorted(lines)) + "\n")
    md = summary_md(meta)
    open(os.path.join(a.out, "summary.md"), "w").write(md)
    open(os.path.join(a.out, "changes.md"), "w").write(changes_md(meta))
    rt.summary(md)
    rt.gh_output(run_id=rid, valid=row["valid"])


def changes_md(meta):
    s = meta.get("since_previous")
    if not s:
        return "No previous valid run at this Test262 commit.\n"
    if s.get("error"):
        return f"Previous valid run {s['previous_run']}: {s['error']}\n"
    L = [f"### Since {s['previous_run']} (core {s['previous_commit'][:12]})", "",
         f"Files passed {s['previous_passed']:,} -> {meta['totals']['passed']:,} ({s['passed_delta']:+,}; "
         f"{s['points']:+.4f} points){' DROP' if s['drop'] else ''}", "",
         f"Newly passing: {len(s['newly_passing']):,}. Newly failing: {len(s['newly_failing']):,}.", ""]
    if s["newly_failing"]:
        L += ["Newly failing:", ""] + [f"- `{x['file']}`: {x['why']}" for x in s["newly_failing"][:300]] + [""]
    if s["newly_passing"]:
        L += ["Newly passing:", ""] + [f"- `{x}`" for x in s["newly_passing"][:300]]
    return "\n".join(L) + "\n"


def summary_md(meta):
    r, t = meta["row"], meta["totals"]
    L = [f"### Test262 {r['wpt_commit'][:10]} on BubblePopJS, core {r['factoidal_commit'][:12]}: "
         f"{t['passed']:,} of {t['files']:,} files = **{t['share_pct']:.2f}%**; without the excluded features "
         f"{t['passed_ex_features']:,} of {t['files_ex_features']:,} = **{t['share_ex_features_pct']:.2f}%**"
         + ("" if r["valid"] == "true" else f" (INVALID: {r['invalid_reason']})"), "",
         f"Runs (file x mode): {t['runs_passed']:,} of {t['runs']:,} = {t['runs_share_pct']:.2f}%. Outcomes: {t['outcomes']}. "
         f"Wall {r['wall_minutes']} min on {r['shards']} shards.", ""]
    rv = [x for x in meta["rivals"]["rows"] if x.get("status") in ("ok", "other_commit")]
    if rv:
        L += ["Other engines (test262.fyi" + ("" if meta["rivals"]["source"]["same_commit"] else ", OTHER Test262 commit") + "): "
              + ", ".join(f"{x['engine']} {float(x['share_pct']):.2f}%" for x in rv if x["engine"] in ("V8", "SpiderMonkey", "JavaScriptCore", "QuickJS-NG")), ""]
    miss = [x for x in meta["rivals"]["rows"] if x.get("status") == "unavailable"]
    if miss:
        L += ["Unavailable rivals: " + "; ".join(f"{x['engine']}: {x['reason']}" for x in miss), ""]
    L += ["| section | files | passed | share |", "| --- | ---: | ---: | ---: |"]
    L += [f"| {k} | {v['total']:,} | {v['passed']:,} | {v['share_pct']:.2f}% |" for k, v in meta["sections"].items()]
    worst = sorted(meta["directories"].items(), key=lambda kv: -(kv[1]["total"] - kv[1]["passed"]))[:25]
    L += ["", "Directories with the most failing files:", "", "| directory | files | failing | share |", "| --- | ---: | ---: | ---: |"]
    L += [f"| {k} | {v['total']:,} | {v['total'] - v['passed']:,} | {v['share_pct']:.2f}% |" for k, v in worst]
    L += ["", "Commonest failure reasons (runs):", ""] + [f"- {f['runs']:,} {f['status']} {f['why']}" for f in meta["top_failures"][:20]]
    if meta.get("since_previous"):
        L += ["", changes_md(meta)]
    return "\n".join(L) + "\n"


# ---- record ----------------------------------------------------------------------------------

def cmd_record(a):
    d = a.src
    row = json.load(open(os.path.join(d, "row.json")))
    meta = json.load(open(os.path.join(d, "meta.json")))
    riv = meta.get("rivals", {}).get("rows", [])
    repo = os.path.abspath(a.repo)
    tmp = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), f"t262-results-{os.getpid()}")
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
        rp = os.path.join(tree, RIVALS_FILE)
        old = list(csv.DictReader(open(rp))) if os.path.exists(rp) else []
        seen = {(r["test262_commit"], r["engine"], r["version"], r["status"]) for r in old}
        new = [r for r in riv if (r.get("test262_commit", ""), r.get("engine", ""), r.get("version", "") or "", r.get("status", "")) not in seen]
        if new:
            rt.append_csv(rp, RIVALS_COLUMNS, new)
        rd = os.path.join(tree, "runs", row["run_id"])
        os.makedirs(rd, exist_ok=True)
        json.dump(meta, open(os.path.join(rd, "meta.json"), "w"), indent=1)
        open(os.path.join(rd, "changes.md"), "w").write(changes_md(meta))
        with open(os.path.join(rd, "directories.csv"), "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["directory", "files", "passed", "share_pct", "runs", "runs_passed"])
            for k, v in meta["directories"].items():
                w.writerow([k, v["total"], v["passed"], v["share_pct"], v["runs"], v["runs_passed"]])
        with open(os.path.join(rd, "features.csv"), "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["feature", "files", "passed", "share_pct", "excluded"])
            for k, v in meta["features"].items():
                w.writerow([k, v["total"], v["passed"], v["share_pct"], str(v["excluded"]).lower()])
        subprocess.run(["git", "-C", tree, "add", "-A"], check=True)
        if subprocess.run(["git", "-C", tree, "diff", "--cached", "--quiet"]).returncode == 0:
            log("nothing new on the branch")
            return
        msg = f"results: test262 {row['run_id']} valid={row['valid']} {row['share_pct']}%"
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


# ---- plan ------------------------------------------------------------------------------------

def cmd_plan(a):
    """The core commit to test: --ref when given, else the newest release of core main on Linux
    (build-<sha12>-linux-x86_64 or build-<sha12>-foafnaut-linux-x86_64)."""
    tag = ""
    if a.ref:
        sha = rt.api(f"repos/{rt.CORE_REPO}/commits/{a.ref}")["sha"]
    else:
        rels = rt.api(f"repos/{rt.BUILDS_REPO}/releases?per_page=60")
        cand = [r for r in rels if re.fullmatch(r"build-[0-9a-f]{12}-(foafnaut-)?linux-x86_64", r["tag_name"]) and not r.get("draft")]
        if not cand:
            rt.die("no Linux release of core main found")
        cand.sort(key=lambda r: r["published_at"] or r["created_at"], reverse=True)
        tag = cand[0]["tag_name"]
        sha = rt.api(f"repos/{rt.CORE_REPO}/commits/{tag.split('-')[1]}")["sha"]
    c = rt.api(f"repos/{rt.CORE_REPO}/commits/{sha}")
    st = rt.api(f"repos/{rt.CORE_REPO}/compare/main...{sha}").get("status")
    on_main = st in ("behind", "identical")
    run = True
    why = "run"
    prev = prev_valid(a.test262_commit, "linux-x86_64")
    if a.trigger == "factoidal-release" and prev and prev["factoidal_commit"] == sha:
        run, why = False, f"{sha[:12]} already has a valid Test262 run at this commit ({prev['run_id']})"
    rt.gh_output(sha=sha, utc=c["commit"]["committer"]["date"], on_main=str(on_main).lower(), release_tag=tag,
                 run=str(run).lower())
    rt.summary(f"Test262 plan: core {sha[:12]} ({tag or 'given ref'}), on main: {on_main}, Test262 {a.test262_commit[:10]}: {why}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--ref", default="")
    p.add_argument("--trigger", default="manual")
    p.add_argument("--test262-commit", required=True)
    p = sub.add_parser("list")
    p.add_argument("--root", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("run")
    for k in ("--leanjs", "--root", "--files", "--out"):
        p.add_argument(k, required=True)
    p.add_argument("--shard", type=int, default=0)
    p.add_argument("--shards", type=int, default=1)
    p.add_argument("--jobs", type=int, default=4)
    p.add_argument("--chunk", type=int, default=200)
    p.add_argument("--stall", type=int, default=120)
    p.add_argument("--rss-mb", type=int, default=3000)
    p = sub.add_parser("score")
    for k in ("--files", "--shards-dir", "--out", "--core-commit", "--test262-commit"):
        p.add_argument(k, required=True)
    p.add_argument("--shards", type=int, required=True)
    p.add_argument("--excluded", default=os.path.join(HERE, "test262-excluded-features.txt"))
    for k in ("--commit-utc", "--started", "--run-url", "--release-tag", "--result-url"):
        p.add_argument(k, default="")
    p.add_argument("--trigger", default="manual")
    p.add_argument("--platform", default="linux-x86_64")
    p.add_argument("--realm", choices=["page", "engine"], default="page")
    p.add_argument("--min-files", type=int, default=50000)
    p.add_argument("--no-prev", action="store_true")
    p.add_argument("--no-rivals", action="store_true")
    p = sub.add_parser("record")
    p.add_argument("--from", dest="src", required=True)
    p.add_argument("--repo", default=".")
    p.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    {"plan": cmd_plan, "list": cmd_list, "run": cmd_run, "score": cmd_score, "record": cmd_record}[a.cmd](a)


if __name__ == "__main__":
    main()
