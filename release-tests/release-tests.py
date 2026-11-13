#!/usr/bin/env python3
"""release-tests.py: full test runs of Factoidal releases, with records that can be trusted.

`.github/workflows/release-tests.yml` calls it. Every step also runs on a laptop.

  resolve      choose what to test: the release (core commit and its release tags), the
               WPT commit, the platform, the shards, the suites; write plan.json
  wpt-inputs   Chrome's wpt.fyi summary at the WPT commit and the list of every name
               Chrome runs (the denominator and the work list of a full run)
  wpt-shard    run one shard of that list with the release's engine library and a WPT
               server of the shard's own; check the server for the whole run
  wpt-merge    join the shards, score with core's wpt-full.py, apply the validity rules
  suite-run    run a group of the other conformance suites from the release's binaries
  suite-score  parse the suite logs (core's generate-report.sh and l4w3c's TOTAL lines)
  rivals       other browsers' wpt.fyi results at the WPT commit, on the same scale
  record       append the rows to runs.csv / rivals.csv / differential.csv and write
               runs/<run_id>/meta.json on the results branch, and push
  seed-local   rows for a local full run (the first: core tests/browser-wpt/wpt-full-20261113.json)

Validity (wpt_validity, suite_validity) is decided here, before a row is written. A row
with valid=false is kept with its reasons and is never a score. The README of the
results branch defines every column (README-results.md in this directory).

Nothing here builds Lean or F*. Downloads (releases, WPT, wpt.fyi summaries) are data:
they go to directories of their own, and no interpreter runs from inside them; the one
program that runs from the WPT tree is WPT's own server, which core's tool starts.
"""
import argparse, csv, datetime, gzip, hashlib, io, json, os, platform, re, shutil, signal, socket
import subprocess, sys, tarfile, time, urllib.error, urllib.request

BUILDS_REPO = os.environ.get("GITHUB_REPOSITORY") or "danbri/factoidal-builds"
CORE_REPO = "danbri/factoidal-core"
RESULTS_BRANCH = os.environ.get("RESULTS_BRANCH", "wpt-scores")
RESULTS_RELEASE = "test-results"
RAW = f"https://raw.githubusercontent.com/{BUILDS_REPO}/{RESULTS_BRANCH}"
WPT_REPO = "https://github.com/web-platform-tests/wpt"
CORE_RUNTIME = "labs/demos/foafnaut/.build/native-html/runtime"
WPT_PORTS = (8000, 8001, 8002, 8003, 8443, 8444, 8445, 8446, 8888, 8889, 9000)

# A test-server failure: the page or a subtest could not reach WPT's server.
SERVER_FAILURE = re.compile(r"fetch failed|Connection refused|ECONNREFUSED")
SERVER_FAILURE_MAX = 0.005           # share of names; at or above it the run is invalid
PROBE_FAILURES_MAX = 2               # consecutive failed probes of the WPT server

# The macOS engine set and the Linux one (the Linux set is published once build.yml
# makes it; until then a Linux WPT run has no engine and resolve does not plan one).
ENGINE_SET = {"macos-arm64": "foafnaut-darwin-arm64", "linux-x86_64": "foafnaut-linux-x86_64"}
ENGINE_FILE = {"macos-arm64": "foafnaut/libweb-render.dylib", "linux-x86_64": "foafnaut/libweb-render.so"}
RUNNER_LABEL = {"macos-arm64": "macos-15", "linux-x86_64": "ubuntu-latest"}

RUNS_COLUMNS = [
    "run_id", "started_utc", "finished_utc", "trigger", "suite", "platform", "engine", "script_engine",
    "factoidal_commit", "commit_utc", "snapshot_branch", "release_tag", "wpt_commit",
    "names_total", "names_run", "passed", "denominator", "share_pct", "share_ex_encoding_pct",
    "ok", "error", "timeout", "skip", "crash", "stall", "no_result", "other",
    "failed", "server_failures", "valid", "invalid_reason", "kind", "shards", "wall_minutes",
    "repeat_of", "runner", "workflow_run_url", "result_url", "meta_url",
]
RIVALS_COLUMNS = ["recorded_utc", "wpt_commit", "browser", "version", "channel", "wptfyi_run_id", "run_time_utc",
                  "passed", "denominator", "share_pct", "share_ex_encoding_pct", "names_total", "names_reported",
                  "partial", "summary_url"]
RIVALS = [("chrome", "stable"), ("firefox", "stable"), ("safari", "stable"), ("edge", "stable"),
          ("servo", "experimental"), ("wpewebkit", "experimental"), ("ladybird", "experimental")]
PARTIAL_BELOW = 0.95                 # a rival run reporting fewer of Chrome's names is partial


def log(msg):
    print(f"release-tests: {msg}", file=sys.stderr, flush=True)


def die(msg, code=1):
    log(f"FAILED: {msg}")
    sys.exit(code)


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def http(url, dest=None, accept=None, timeout=120, tries=4, method="GET"):
    """GET with a time limit and a few tries. The token goes to api.github.com only."""
    headers = {"User-Agent": "factoidal-release-tests"}
    if accept:
        headers["Accept"] = accept
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers, method=method), timeout=timeout) as r:
                if dest is None:
                    return r.read()
                with open(dest + ".part", "wb") as f:
                    shutil.copyfileobj(r, f)
                os.replace(dest + ".part", dest)
                return None
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code in (401, 403, 404, 422):
                break
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"GET {url}: {last}")


def api(path):
    return json.loads(http("https://api.github.com/" + path.lstrip("/"), accept="application/vnd.github+json"))


def gh_output(**kv):
    out = os.environ.get("GITHUB_OUTPUT")
    lines = [f"{k}={v}" for k, v in kv.items()]
    if out:
        with open(out, "a") as f:
            f.write("\n".join(lines) + "\n")
    for l in lines:
        log("output " + l)


def summary(text):
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        with open(p, "a") as f:
            f.write(text.rstrip() + "\n\n")
    print(text)


def runner_info():
    info = {"os": platform.system(), "machine": platform.machine(), "cpus": os.cpu_count(),
            "python": platform.python_version(), "image_os": os.environ.get("ImageOS"),
            "image_version": os.environ.get("ImageVersion"), "runner_name": os.environ.get("RUNNER_NAME"),
            "runner_environment": os.environ.get("RUNNER_ENVIRONMENT")}
    try:
        if platform.system() == "Darwin":
            info["os_version"] = subprocess.run(["sw_vers", "-productVersion"], capture_output=True, text=True).stdout.strip()
            info["memory_bytes"] = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout.strip() or 0)
        else:
            info["os_version"] = platform.release()
            for l in open("/proc/meminfo"):
                if l.startswith("MemTotal:"):
                    info["memory_bytes"] = int(l.split()[1]) * 1024
    except Exception as e:  # runner facts are notes, not inputs
        info["note"] = f"runner facts incomplete: {e}"
    for tool, args in (("deno", ["--version"]), ("node", ["--version"]), ("git", ["--version"])):
        if shutil.which(tool):
            out = subprocess.run([tool] + args, capture_output=True, text=True).stdout.strip().splitlines()
            info[tool] = out[0] if out else None
    return info


# ---- releases ---------------------------------------------------------------------------

def list_releases(pages=3):
    out = []
    for page in range(1, pages + 1):
        got = api(f"repos/{BUILDS_REPO}/releases?per_page=100&page={page}")
        out += got
        if len(got) < 100:
            break
    return out


def releases_by_commit(releases):
    """{short: {"sets": {set: release}, "commit": 40-hex or None}} for build-<short>-<set> tags."""
    by = {}
    for r in releases:
        m = re.fullmatch(r"build-([0-9a-f]{12})-(.+)", r.get("tag_name") or "")
        if not m or r.get("draft"):
            continue
        e = by.setdefault(m[1], {"sets": {}, "commit": None})
        e["sets"][m[2]] = r
        c = re.search(r"/commit/([0-9a-f]{40})", r.get("body") or "")
        if c and c[1].startswith(m[1]):
            e["commit"] = c[1]
    return by


def complete(entry, sets):
    return all(s in entry["sets"] for s in sets)


def newest_complete(by, sets):
    order = sorted(((k, v) for k, v in by.items() if complete(v, sets)),
                   key=lambda kv: max(kv[1]["sets"][s].get("published_at") or "" for s in sets), reverse=True)
    return order[0] if order else (None, None)


def fetch_set(tag, set_name, dest):
    """Download <set>.tar.gz and build-info.json of a release, check the tarball's sha256
    and every file against build-info.json, and unpack it into dest/<set>."""
    d, dl = os.path.join(dest, set_name), os.path.join(dest, "download-" + set_name)
    for p in (d, dl):
        if os.path.exists(p):
            shutil.rmtree(p)
        os.makedirs(p)
    for name in ("build-info.json", set_name + ".tar.gz"):
        target = os.path.join(dl, name)
        try:
            http(f"https://github.com/{BUILDS_REPO}/releases/download/{tag}/{name}", dest=target, timeout=900)
        except RuntimeError as e:
            rel = api(f"repos/{BUILDS_REPO}/releases/tags/{tag}")
            asset = next((x for x in rel.get("assets", []) if x.get("name") == name), None)
            if not asset:
                die(f"{tag}: no asset {name} ({e})")
            log(f"{name}: download address failed; trying the API")
            http(asset["url"], dest=target, accept="application/octet-stream", timeout=900)
    info = json.load(open(os.path.join(dl, "build-info.json")))
    art = info["artifacts"][set_name + ".tar.gz"]
    tarball = os.path.join(dl, set_name + ".tar.gz")
    if sha256(tarball) != art["sha256"]:
        die(f"{tag}: the sha256 of {set_name}.tar.gz is not the one in build-info.json; nothing unpacked")
    with tarfile.open(tarball) as tf:
        tf.extractall(d, filter="data")
    listed, seen = art["files"], set()
    for dp, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(dp, f)
            if os.path.islink(p):
                continue
            relp = os.path.relpath(p, d)
            seen.add(relp)
            if relp not in listed or sha256(p) != listed[relp]["sha256"]:
                die(f"{tag}: {relp} is not listed in build-info.json or its sha256 differs")
    if set(listed) - seen:
        die(f"{tag}: files of build-info.json are missing: {sorted(set(listed) - seen)[:5]}")
    os.remove(tarball)
    log(f"{tag}: {len(seen)} files checked against build-info.json (core {info['source_commit'][:12]})")
    return {"tag": tag, "tarball_sha256": art["sha256"], "files": len(seen),
            "build_info": {k: v for k, v in info.items() if k != "artifacts"}}


# ---- wpt.fyi ------------------------------------------------------------------------------

def wptfyi_runs(query):
    return json.loads(http("https://wpt.fyi/api/runs?" + query))


def newest_aligned():
    runs = wptfyi_runs("label=master&label=stable&aligned&product=chrome&product=firefox&product=safari&product=edge&max-count=1")
    if not runs:
        die("wpt.fyi gave no aligned stable runs")
    return runs[0]["full_revision_hash"], runs


def chrome_run(sha):
    for q in (f"product=chrome&label=master&label=stable&sha={sha}", f"product=chrome&label=master&sha={sha}"):
        runs = wptfyi_runs(q)
        if runs:
            return runs[0]
    die(f"wpt.fyi has no Chrome run at WPT {sha}: without it there is no denominator", 2)


def load_summary(url, dest):
    if not os.path.exists(dest):
        raw = http(url, timeout=600)
        if raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
        with open(dest, "wb") as f:
            f.write(raw)
    return json.load(open(dest))


def top(name):
    return name.split("?")[0].split("/")[1]


# ---- results branch -------------------------------------------------------------------------

def read_csv_url(name):
    try:
        text = http(f"{RAW}/{name}", tries=2).decode()
    except RuntimeError:
        return []
    return list(csv.DictReader(io.StringIO(text)))


# ---- snapshot branches in factoidal-core -------------------------------------------------------

SNAPSHOT_KEEP_DAYS = 14


def core_api(method, path, body=None):
    """factoidal-core's API with CORE_SNAPSHOT_TOKEN (the workflow token can not write to
    another repository)."""
    token = os.environ.get("CORE_SNAPSHOT_TOKEN")
    req = urllib.request.Request(f"https://api.github.com/repos/{CORE_REPO}/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                                          "User-Agent": "factoidal-release-tests"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        return json.loads(data) if data else None


def snapshot(commit, chosen_utc, runs):
    """Point wpt-snap/<YYYYMMDD-HHMM>-<sha12> at the tested commit, so the tool and source
    of the run stay named when main moves. Snapshots older than SNAPSHOT_KEEP_DAYS are
    deleted unless a valid run in runs.csv names them."""
    if not os.environ.get("CORE_SNAPSHOT_TOKEN"):
        return "", "no snapshot: the secret CORE_SNAPSHOT_TOKEN (contents: write on factoidal-core) is not set; the commit id pins the source"
    stamp = chosen_utc[:16].replace("-", "").replace(":", "").replace("T", "-")
    name = f"wpt-snap/{stamp}-{commit[:12]}"
    try:
        core_api("POST", "git/refs", {"ref": f"refs/heads/{name}", "sha": commit})
    except urllib.error.HTTPError as e:
        return "", f"no snapshot: creating {name} answered HTTP {e.code}"
    keep = {r["snapshot_branch"] for r in runs if r.get("valid") == "true"}
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=SNAPSHOT_KEEP_DAYS)).strftime("%Y%m%d")
    try:
        for ref in core_api("GET", "git/matching-refs/heads/wpt-snap/") or []:
            b = ref["ref"][len("refs/heads/"):]
            m = re.match(r"wpt-snap/(\d{8})-", b)
            if m and m[1] < cutoff and b not in keep:
                core_api("DELETE", f"git/refs/heads/{b}")
                log(f"deleted old snapshot {b}")
    except urllib.error.HTTPError as e:
        log(f"snapshot clean-up: HTTP {e.code}")
    return name, "made by this run"


# ---- resolve ------------------------------------------------------------------------------

def cmd_resolve(a):
    event = a.event
    plan = {"resolved_utc": now_utc(), "event": event, "workflow_run_url": a.run_url}
    releases = list_releases()
    by = releases_by_commit(releases)
    platforms = [p for p in (a.platforms or "macos-arm64").split(",") if p]
    for p in platforms:
        if p not in ENGINE_SET:
            die(f"unknown platform {p}", 2)
    suites_wanted = set(s for s in (a.suites or "wpt,w3c").split(",") if s)
    short = None
    why = None
    if event == "workflow_run":
        trigger = "factoidal-release"
        if a.build_workflow == "Foafnaut Linux engine":
            # The Linux engine is published after build.yml: run Linux WPT for it.
            platforms, suites_wanted = ["linux-x86_64"], {"wpt"}
        mark = f"/actions/runs/{a.build_run_id}"
        hits = [k for k, v in by.items() if any(mark in (r.get("body") or "") for r in v["sets"].values())]
        if not hits:
            log(f"build run {a.build_run_id} published no release: nothing to test")
            gh_output(wpt="false", suites="false", rivals="false", matrix=json.dumps({"include": []}), platforms="[]")
            json.dump({**plan, "nothing": "no release from that build run"}, open(a.out, "w"), indent=1)
            return
        short = sorted(hits, key=lambda k: max(r.get("published_at") or "" for r in by[k]["sets"].values()))[-1]
        why = f"published by build run {a.build_run_id}"
    elif event == "schedule":
        trigger = "schedule"
    else:
        trigger = "manual"
    if a.release and not short:
        m = re.fullmatch(r"(?:build-)?([0-9a-f]{12})[0-9a-f]*(?:-.+)?", a.release.strip())
        if not m or m[1] not in by:
            die(f"no release of core commit {a.release}", 2)
        short, why = m[1], f"named by the dispatch ({a.release})"
    # The candidate: the newest commit with every set that the asked runs need.
    need = sorted({ENGINE_SET[p] for p in platforms} | {"foafnaut-web"}) if "wpt" in suites_wanted else []
    if not short and "wpt" in suites_wanted and not newest_complete(by, need)[0] and "linux-x86_64" in platforms:
        platforms = [p for p in platforms if p != "linux-x86_64"] or ["macos-arm64"]
        plan["platform_note"] = "no release has a Linux engine yet: macOS only"
        need = sorted({ENGINE_SET[p] for p in platforms} | {"foafnaut-web"})
    if not short:
        waited = 0
        while True:
            short, _ = newest_complete(by, need or ["linux-x86_64"])
            why = "newest commit with complete releases"
            if event != "schedule" or a.wait_minutes <= 0:
                break
            # A build of a newer main commit that is running and should end within the
            # slack: wait for it (owner, 2026-11-13: "an hour ish wiggleroom").
            runs = api(f"repos/{BUILDS_REPO}/actions/workflows/build.yml/runs?status=in_progress&per_page=5").get("workflow_runs", [])
            started = [datetime.datetime.fromisoformat(r["run_started_at"].replace("Z", "+00:00")) for r in runs]
            if not started or waited >= a.wait_minutes:
                if started:
                    why += f"; a build was still running after {waited} min of waiting"
                break
            age = (datetime.datetime.now(datetime.timezone.utc) - min(started)).total_seconds() / 60
            if age + (a.wait_minutes - waited) < a.build_minutes:
                why += f"; a build running for {age:.0f} min would not end within the slack"
                break
            log(f"a build has run for {age:.0f} min; waiting for its releases ({waited} of {a.wait_minutes} min)")
            time.sleep(300)
            waited += 5
            by = releases_by_commit(list_releases(1) + releases)
            before = short
            short, _ = newest_complete(by, need or ["linux-x86_64"])
            if short != before:
                why = f"newest commit with complete releases, after waiting {waited} min for a running build"
                break
    if not short:
        die("no release has the sets needed: " + ", ".join(need), 2)
    entry = by[short]
    commit = entry["commit"]
    if not commit:
        info = json.loads(http(f"https://github.com/{BUILDS_REPO}/releases/download/{next(iter(entry['sets'].values()))['tag_name']}/build-info.json"))
        commit = info["source_commit"]
    c = api(f"repos/{CORE_REPO}/commits/{commit}")
    on_main = api(f"repos/{CORE_REPO}/compare/main...{commit}").get("status") in ("behind", "identical")
    sets = {s: {"tag": r["tag_name"], "published_at": r.get("published_at"), "url": r.get("html_url")}
            for s, r in sorted(entry["sets"].items())}
    plan.update({
        "trigger": trigger, "core_commit": commit, "core_short": short, "on_main": on_main,
        "commit_author_utc": c["commit"]["author"]["date"], "commit_committer_utc": c["commit"]["committer"]["date"],
        "commit_subject": c["commit"]["message"].splitlines()[0], "release_sets": sets,
        "candidate_chosen_utc": now_utc(), "candidate_why": why,
        "script_engine": a.script_engine, "kind": "differential" if a.script_engine == "quickjs" else "full",
    })
    if not on_main and trigger != "manual":
        die(f"core {commit} is not on main; branch builds run only when asked", 2)
    # The WPT commit: as asked, else the newest commit with aligned stable runs, so that
    # our result and the other browsers' share one WPT commit.
    aligned, _ = newest_aligned()
    wpt_commit = a.wpt_commit or aligned
    if not re.fullmatch(r"[0-9a-f]{40}", wpt_commit):
        die("--wpt-commit is a 40-hex WPT commit", 2)
    rivals_rows = read_csv_url("rivals.csv")
    known = {r["wpt_commit"] for r in rivals_rows}
    if trigger == "schedule" and wpt_commit not in known:
        trigger = plan["trigger"] = "browser-release"
        plan["trigger_why"] = "a WPT commit with new aligned browser runs on wpt.fyi"
    plan["wpt_commit"] = wpt_commit
    plan["wpt_aligned"] = wpt_commit == aligned
    runs = read_csv_url("runs.csv")
    # Same commit as the last valid run of this kind: still run (the repeat shows flakiness).
    prev = [r for r in runs if r["suite"] == "wpt" and r["valid"] == "true" and r["factoidal_commit"] == commit
            and r["wpt_commit"] == wpt_commit and r["platform"] in platforms]
    plan["repeat_of"] = prev[-1]["run_id"] if prev else ""
    if "wpt" in suites_wanted:
        missing_p = [p for p in platforms if ENGINE_SET[p] not in sets]
        if missing_p and len(missing_p) < len(platforms):
            plan["platform_note"] = f"{', '.join(missing_p)}: no engine release for this commit"
            platforms = [p for p in platforms if p not in missing_p]
    do_wpt = "wpt" in suites_wanted and all(ENGINE_SET[p] in sets for p in platforms) and "foafnaut-web" in sets
    if do_wpt and trigger == "factoidal-release" and prev and not a.force:
        log(f"WPT already measured validly for {short} at {wpt_commit[:10]} ({prev[-1]['run_id']}); not run again on the release trigger")
        do_wpt = False
    have_suites = [r for r in runs if r["suite"] != "wpt" and r["valid"] == "true" and r["factoidal_commit"] == commit]
    do_suites = "w3c" in suites_wanted and "linux-x86_64" in sets and not (have_suites and not a.force)
    if trigger in ("schedule", "browser-release") and have_suites:
        do_suites = False
    if do_wpt or do_suites:
        plan["snapshot_branch"], plan["snapshot_note"] = snapshot(commit, plan["candidate_chosen_utc"], runs)
    else:
        plan["snapshot_branch"], plan["snapshot_note"] = "", "nothing run"
    count = {"macos-arm64": a.shards, "linux-x86_64": a.linux_shards}
    jobs = {"macos-arm64": 3, "linux-x86_64": 4}
    include = [{"platform": p, "shard": k, "shards": count[p], "jobs": jobs[p], "runs_on": RUNNER_LABEL[p]}
               for p in platforms for k in range(count[p])] if do_wpt else []
    plan.update({"wpt": do_wpt, "suites": do_suites, "platforms": platforms if do_wpt else [],
                 "shards_by_platform": {p: count[p] for p in platforms}, "shards": a.shards})
    with open(a.out, "w") as f:
        json.dump(plan, f, indent=1)
    gh_output(wpt=str(do_wpt).lower(), suites=str(do_suites).lower(), rivals=str(do_wpt).lower(),
              matrix=json.dumps({"include": include}), platforms=json.dumps(platforms if do_wpt else []),
              core_commit=commit, core_short=short, wpt_commit=wpt_commit, trigger=trigger)
    summary(f"### Release tests plan\n\nTrigger `{trigger}`; core `{commit[:12]}` ({plan['commit_subject']}, "
            f"committed {plan['commit_committer_utc']}), {why}. WPT `{wpt_commit[:10]}`"
            f"{' (newest aligned)' if plan['wpt_aligned'] else ''}. WPT run: {do_wpt} on " + ", ".join(f"{p} ({count[p]} shards)" for p in platforms) + "; "
            f"other suites: {do_suites}." + (f" Repeat of `{plan['repeat_of']}`." if plan["repeat_of"] else ""))


# ---- WPT: inputs, shards, merge ------------------------------------------------------------

def cmd_wpt_inputs(a):
    os.makedirs(a.out, exist_ok=True)
    crun = chrome_run(a.wpt_commit)
    chrome = load_summary(crun["results_url"], os.path.join(a.out, "chrome.json"))
    names = sorted(n for n, v in chrome.items() if v["c"][1] > 0)
    with open(os.path.join(a.out, "full.list"), "w") as f:
        f.write("\n".join(names) + "\n")
    denominator = sum(v["c"][1] for v in chrome.values())
    enc = sum(v["c"][1] for n, v in chrome.items() if top(n) == "encoding")
    inputs = {"wpt_commit": a.wpt_commit, "chrome_run": {k: crun.get(k) for k in ("id", "browser_version", "os_name", "os_version", "time_start", "results_url")},
              "names": len(names), "denominator": denominator, "denominator_encoding": enc,
              "full_list_sha256": sha256(os.path.join(a.out, "full.list")), "chrome_json_sha256": sha256(os.path.join(a.out, "chrome.json"))}
    json.dump(inputs, open(os.path.join(a.out, "inputs.json"), "w"), indent=1)
    log(f"WPT {a.wpt_commit[:10]}: {len(names)} names, denominator {denominator} (Chrome {crun.get('browser_version')})")


def port_open(port):
    s = socket.socket()
    s.settimeout(1)
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def run_logged(cmd, logfile, timeout, env=None, cwd=None, monitor=None):
    """Run cmd with output to logfile (and stderr). monitor() is called every 30 s."""
    log("$ " + " ".join(cmd))
    with open(logfile, "ab") as out:
        p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, env=env, cwd=cwd, start_new_session=True)
        deadline, next_probe = time.time() + timeout, time.time() + 30
        while p.poll() is None:
            time.sleep(2)
            if monitor and time.time() >= next_probe:
                monitor()
                next_probe = time.time() + 30
            if time.time() > deadline:
                os.killpg(p.pid, signal.SIGKILL)
                p.wait()
                return 124
    return p.returncode


def read_results(d):
    out = {}
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if fn.endswith(".jsonl"):
            for line in open(os.path.join(d, fn), errors="replace"):
                if line.strip():
                    try:
                        c = json.loads(line)
                    except ValueError:
                        continue
                    out[c["file"]] = (c, line)
    return out


def cmd_wpt_shard(a):
    t0 = time.time()
    started = now_utc()
    inputs = json.load(open(os.path.join(a.inputs, "inputs.json")))
    names = [l.strip() for l in open(os.path.join(a.inputs, "full.list")) if l.strip()]
    mine = names[a.index::a.shards]
    work, out = os.path.abspath(a.work), os.path.abspath(a.out)
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    shard_list = os.path.join(work, "shard.list")
    with open(shard_list, "w") as f:
        f.write("\n".join(mine) + "\n")
    meta = {"index": a.index, "shards": a.shards, "names": len(mine), "started_utc": started, "runner": runner_info(),
            "platform": a.platform, "script_engine": a.script_engine, "wpt_commit": inputs["wpt_commit"]}

    def finish(**kv):
        meta.update(kv, finished_utc=now_utc(), wall_seconds=round(time.time() - t0))
        json.dump(meta, open(os.path.join(out, "shard-meta.json"), "w"), indent=1)

    core = os.path.abspath(a.core)
    tool = os.path.join(core, "tests/browser-wpt/wpt-score.py")
    meta["tool_commit"] = subprocess.run(["git", "-C", core, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    meta["tool_sha256"] = sha256(tool)
    # The engine: the release's library and the Wasm module that the runner also loads.
    engine_dir = os.path.abspath(a.engine_dir)
    sets = {}
    sets[ENGINE_SET[a.platform]] = fetch_set(a.engine_tag, ENGINE_SET[a.platform], engine_dir)
    sets["foafnaut-web"] = fetch_set(a.web_tag, "foafnaut-web", engine_dir)
    meta["release_sets"] = sets
    lib = os.path.join(engine_dir, ENGINE_SET[a.platform], ENGINE_FILE[a.platform])
    web = os.path.join(engine_dir, "foafnaut-web", "docs/web/hub")
    if not os.path.exists(lib):
        finish(error=f"the release has no {ENGINE_FILE[a.platform]}")
        die(meta["error"])
    meta["engine_sha256"] = sha256(lib)
    runtime = os.path.join(core, CORE_RUNTIME)
    os.makedirs(runtime, exist_ok=True)
    for n in ("web-render.mjs", "web-render.wasm"):
        shutil.copyfile(os.path.join(web, "html-webgpu/runtime", n), os.path.join(runtime, n))
    for c in (sets[ENGINE_SET[a.platform]], sets["foafnaut-web"]):
        if c["build_info"]["source_commit"] != meta["tool_commit"]:
            meta.setdefault("problems", []).append(f"{c['tag']} is of core {c['build_info']['source_commit'][:12]}, the runner of {meta['tool_commit'][:12]}")
    # The WPT tree for this shard's names (core's tool, from GitHub's tarball of the commit).
    wpt_root = os.path.join(work, "wpt")
    tool_log = os.path.join(out, "tool.log")
    env = dict(os.environ, PYTHONPATH=os.path.abspath(a.pydeps) if a.pydeps else "", NO_COLOR="1")
    t_tree = time.time()
    rc = run_logged([sys.executable, tool, "tree", "--wpt-root", wpt_root, "--list", shard_list, "--commit", inputs["wpt_commit"]],
                    tool_log, 3600, env=env, cwd=work)
    meta["tree_seconds"] = round(time.time() - t_tree)
    if rc != 0:
        finish(error=f"WPT tree: exit {rc}")
        die(meta["error"])
    busy = [p for p in WPT_PORTS if port_open(p)]
    if busy:
        finish(error=f"ports {busy} in use before the run")
        die(meta["error"])
    extra = ["--", "--script-engine", a.script_engine, "--wpt-commit", inputs["wpt_commit"]]
    if a.script_engine == "quickjs":
        extra += ["--quickjs-wasm", os.path.join(web, "wasm-guests/qjs-wasmvm.wasm")]
    # The WPT server is checked every 30 s for the whole run: a server that stops makes
    # every later test "fetch failed", which a score must not count.
    probes = {"ok": 0, "failed": 0, "streak_max": 0, "streak": 0, "up_seen": False}

    def monitor():
        if port_open(8000) and port_open(8443):
            probes["ok"] += 1
            probes["up_seen"] = True
            probes["streak"] = 0
        elif probes["up_seen"]:
            probes["failed"] += 1
            probes["streak"] += 1
            probes["streak_max"] = max(probes["streak_max"], probes["streak"])

    # Start check: one test, at most 6 minutes. A runner that can not start would
    # otherwise be restarted until the time limit, with no result.
    check_dir = os.path.join(work, "start-check")
    os.makedirs(check_dir, exist_ok=True)
    first = next((n for n in mine if n.endswith(".html") and "?" not in n), mine[0]).lstrip("/")
    with open(os.path.join(check_dir, "one.list"), "w") as f:
        f.write("/" + first + "\n")
    rc = run_logged([sys.executable, tool, "run", "--list", os.path.join(check_dir, "one.list"), "--dir", check_dir,
                     "--wpt-root", wpt_root, "--native-engine", lib, "--jobs", "1", "--max-hours", "0.08"] + extra,
                    os.path.join(out, "start-check.log"), 420, env=env, cwd=work)
    for _ in range(40):
        if not any(port_open(p) for p in WPT_PORTS):
            break
        time.sleep(1)
    if not read_results(check_dir):
        for fn in ("part0.log", "wptserve.log"):
            if os.path.exists(os.path.join(check_dir, fn)):
                shutil.copyfile(os.path.join(check_dir, fn), os.path.join(out, "start-check-" + fn))
        finish(error=f"start check: no result for {first} (exit {rc})")
        die(meta["error"])
    log(f"start check passed: {first}")
    results = os.path.join(work, "results")
    os.makedirs(results, exist_ok=True)
    t_run = time.time()
    rc = run_logged([sys.executable, tool, "run", "--list", shard_list, "--dir", results, "--wpt-root", wpt_root,
                     "--native-engine", lib, "--jobs", str(a.jobs), "--max-hours", f"{a.max_minutes / 60:.3f}"] + extra,
                    tool_log, a.max_minutes * 60 + 300, env=env, cwd=work, monitor=monitor)
    run_seconds = round(time.time() - t_run)
    text = open(tool_log, errors="replace").read()
    done = read_results(results)
    want = {n.lstrip("/") for n in mine}
    ran = len(want & set(done))
    outcomes, server_failures = {}, 0
    for n, (c, line) in done.items():
        outcomes[c.get("harness", "?")] = outcomes.get(c.get("harness", "?"), 0) + 1
        if SERVER_FAILURE.search(line):
            server_failures += 1
    # Results and logs for the merge job (the runner's logs are large: gzip).
    keep = os.path.join(out, "results")
    os.makedirs(keep, exist_ok=True)
    for fn in sorted(os.listdir(results)):
        src = os.path.join(results, fn)
        if fn.endswith(".jsonl"):
            shutil.copyfile(src, os.path.join(keep, fn))
        elif fn.endswith(".log"):
            with open(src, "rb") as fi, gzip.open(os.path.join(out, fn + ".gz"), "wb") as fo:
                shutil.copyfileobj(fi, fo)
    finish(tool_exit=rc, run_seconds=run_seconds, names_run=ran, outcomes=outcomes, server_failures=server_failures,
           wptserve={"probes_ok": probes["ok"], "probes_failed": probes["failed"], "failed_streak_max": probes["streak_max"],
                     "exited_during_run": "wptserve exited" in text, "stopped_at_limit": "stopped at --max-hours" in text},
           jobs=a.jobs, max_minutes=a.max_minutes)
    log(f"shard {a.index}/{a.shards}: {ran} of {len(mine)} names in {run_seconds} s, server failures {server_failures}, "
        f"probes {probes['ok']} ok / {probes['failed']} failed, tool exit {rc}")


def wpt_validity(m):
    """The rules for a full WPT run to count as a score. Returns the reasons it does not."""
    r = []
    if m.get("kind") != "full":
        r.append(f"kind {m.get('kind')}: not a full run")
    if not re.fullmatch(r"[0-9a-f]{40}", m.get("factoidal_commit") or ""):
        r.append("engine commit unknown")
    if not m.get("release_tag"):
        r.append("release tag unknown")
    if not re.fullmatch(r"[0-9a-f]{40}", m.get("wpt_commit") or ""):
        r.append("WPT commit unknown")
    if m.get("shards_present") != m.get("shards"):
        r.append(f"shards missing: {m.get('shards_missing')}")
    if m.get("names_run") != m.get("names_total"):
        r.append(f"{(m.get('names_total') or 0) - (m.get('names_run') or 0)} of {m.get('names_total')} names not run")
    total = m.get("names_total") or 0
    if total and (m.get("server_failures") or 0) / total >= SERVER_FAILURE_MAX:
        r.append(f"test-server failures on {m['server_failures']} names ({100 * m['server_failures'] / total:.2f}%, limit {100 * SERVER_FAILURE_MAX:.1f}%)")
    for s in m.get("shard_health", []):
        if s.get("exited_during_run"):
            r.append(f"shard {s['index']}: wptserve exited during the run")
        if (s.get("failed_streak_max") or 0) >= PROBE_FAILURES_MAX:
            r.append(f"shard {s['index']}: wptserve did not answer {s['failed_streak_max']} probes in a row")
        if s.get("stopped_at_limit"):
            r.append(f"shard {s['index']}: stopped at the time limit")
        for p in s.get("problems", []):
            r.append(f"shard {s['index']}: {p}")
    if not m.get("denominator"):
        r.append("no denominator")
    return r


def outcome_columns(outcomes):
    o = {k.split(" ")[0]: 0 for k in outcomes}
    for k, v in outcomes.items():
        o[k.split(" ")[0]] = o.get(k.split(" ")[0], 0) + v
    cols = {c: o.pop(c.upper(), 0) for c in ("ok", "error", "timeout", "skip", "crash", "stall")}
    cols["no_result"] = o.pop("NO_RESULT", 0)
    cols["other"] = sum(o.values())
    return cols


def run_id_of(plan, suite, platform_):
    t = (plan.get("resolved_utc") or now_utc()).replace("-", "").replace(":", "")[:13] + "Z"
    gh = os.environ.get("GITHUB_RUN_ID")
    att = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    return f"{t}-{suite}-{platform_}" + (f"-gh{gh}a{att}" if gh else "-local")


def cmd_wpt_merge(a):
    plan = json.load(open(a.plan))
    inputs = json.load(open(os.path.join(a.inputs, "inputs.json")))
    shard_dirs, health, metas = [], [], []
    plan["shards"] = plan.get("shards_by_platform", {}).get(a.platform, plan["shards"])
    for k in range(plan["shards"]):
        d = os.path.join(a.shards_dir, f"wpt-shard-{a.platform}-{k}")
        mp = os.path.join(d, "shard-meta.json")
        if os.path.exists(mp):
            m = json.load(open(mp))
            metas.append(m)
            health.append({"index": k, **m.get("wptserve", {}), "problems": m.get("problems", []) + ([m["error"]] if m.get("error") else [])})
            if os.path.isdir(os.path.join(d, "results")):
                shard_dirs.append(os.path.join(d, "results"))
    present = sorted(m["index"] for m in metas if os.path.isdir(os.path.join(a.shards_dir, f"wpt-shard-{a.platform}-{m['index']}", "results")))
    missing = sorted(set(range(plan["shards"])) - set(present))
    os.makedirs(a.out, exist_ok=True)
    run_id = run_id_of(plan, "wpt", a.platform)
    full_json = os.path.join(a.out, "wpt-full.json")
    notes = {"run_id": run_id, "engine": f"factoidal-core {plan['core_commit'][:12]} ({plan['release_sets'][ENGINE_SET[a.platform]]['tag']}), "
             f"page scripts on {'BubblePopJS' if plan['script_engine'] == 'bubblepop' else 'QuickJS-NG in WasmVM (differential)'}",
             "run": f"{plan['shards']} shards on {a.platform}, workflow {plan.get('workflow_run_url')}"}
    json.dump(notes, open(os.path.join(a.out, "notes.json"), "w"))
    totals, dirs = {}, {}
    if shard_dirs:
        rc = subprocess.run([sys.executable, "-I", os.path.join(a.core, "tests/browser-wpt/wpt-full.py"), "--chrome", os.path.join(a.inputs, "chrome.json"),
                             "--results"] + shard_dirs + ["--denominator", str(inputs["denominator"]), "--wpt-commit", inputs["wpt_commit"],
                             "--notes", os.path.join(a.out, "notes.json"), "--out", full_json]).returncode
        if rc == 0:
            rep = json.load(open(full_json))
            totals, dirs = rep["totals"], rep["directories"]
    server_failures = 0
    for d in shard_dirs:
        for n, (c, line) in read_results(d).items():
            if SERVER_FAILURE.search(line):
                server_failures += 1
    enc = dirs.get("encoding", {"passed": 0, "chrome": 0})
    passed = totals.get("passed", 0)
    den = inputs["denominator"]
    started = min((m["started_utc"] for m in metas), default=None)
    finished = max((m.get("finished_utc") or "" for m in metas), default=None)
    wall = round(max((m.get("wall_seconds") or 0 for m in metas), default=0) / 60, 1)
    tag = plan["release_sets"].get(ENGINE_SET[a.platform], {}).get("tag")
    m = {
        "run_id": run_id, "suite": "wpt", "platform": a.platform, "engine": "bubblepopkit-native", "script_engine": plan["script_engine"],
        "kind": plan["kind"], "trigger": plan["trigger"], "factoidal_commit": plan["core_commit"], "release_tag": tag,
        "wpt_commit": inputs["wpt_commit"], "names_total": inputs["names"], "names_run": totals.get("namesRun", 0),
        "passed": passed, "denominator": den, "shards": plan["shards"], "shards_present": len(present), "shards_missing": missing,
        "server_failures": server_failures, "shard_health": health,
    }
    reasons = wpt_validity(m)
    out_cols = outcome_columns(totals.get("outcomes", {}))
    row = {
        "run_id": run_id, "started_utc": started, "finished_utc": finished, "trigger": plan["trigger"], "suite": "wpt",
        "platform": a.platform, "engine": "bubblepopkit-native", "script_engine": plan["script_engine"],
        "factoidal_commit": plan["core_commit"], "commit_utc": plan["commit_committer_utc"], "snapshot_branch": plan.get("snapshot_branch", ""),
        "release_tag": tag, "wpt_commit": inputs["wpt_commit"], "names_total": inputs["names"], "names_run": totals.get("namesRun", 0),
        "passed": passed, "denominator": den, "share_pct": f"{100 * passed / den:.4f}",
        "share_ex_encoding_pct": f"{100 * (passed - enc['passed']) / (den - enc['chrome']):.4f}" if den > enc["chrome"] else "",
        **out_cols, "failed": "", "server_failures": server_failures, "valid": "false" if reasons else "true",
        "invalid_reason": "; ".join(reasons), "kind": plan["kind"], "shards": plan["shards"], "wall_minutes": wall,
        "repeat_of": plan.get("repeat_of", ""), "runner": f"{RUNNER_LABEL[a.platform]} x{plan['shards']}",
        "workflow_run_url": plan.get("workflow_run_url", ""),
        "result_url": f"https://github.com/{BUILDS_REPO}/releases/download/{RESULTS_RELEASE}/{run_id}.wpt-full.json.gz" if totals else "",
        "meta_url": f"{RAW}/runs/{run_id}/meta.json",
    }
    meta = {"format": "factoidal-release-test-run-v1", "row": row, "plan": plan, "inputs": inputs,
            "validity": {"valid": not reasons, "reasons": reasons, "rules": wpt_validity.__doc__,
                         "server_failure_limit": SERVER_FAILURE_MAX, "probe_failure_limit": PROBE_FAILURES_MAX},
            "totals": totals, "shards": metas,
            "directories": {k: {kk: v[kk] for kk in ("names", "run", "chrome", "passed", "reported", "share", "outcomes")} for k, v in dirs.items()}}
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    json.dump(row, open(os.path.join(a.out, "row.json"), "w"), indent=1)
    if totals:
        with open(full_json, "rb") as fi, gzip.open(os.path.join(a.out, f"{run_id}.wpt-full.json.gz"), "wb") as fo:
            shutil.copyfileobj(fi, fo)
    verdict = "VALID" if not reasons else "INVALID (not a score): " + "; ".join(reasons)
    text = (f"### WPT {a.platform}: {verdict}\n\n" + (f"{passed:,} of {den:,} Chrome subtests = **{row['share_pct'][:5]}%**; "
            f"without encoding/ {row['share_ex_encoding_pct'][:5]}%. " if not reasons else
            f"Measured {passed:,} of {den:,} (not shown as a score). ") +
            f"{row['names_run']:,} of {row['names_total']:,} names; outcomes {totals.get('outcomes')}; server failures {server_failures}; "
            f"{len(present)} of {plan['shards']} shards; wall {wall} min. Run `{run_id}`.")
    summary(text)


# ---- the other suites -------------------------------------------------------------------------

# (key in generate-report.sh's latest.json totals or "l4w3c:<name>", group, log file name,
#  runner in bin/linux-x86_64, arguments, time budget in s, submodules needed).
SUITES = [
    ("sparql", "w3c", "sparql_results.log", "w3c_runner", [], 1800, ["w3c"]),
    ("rdf", "w3c", "rdf_results.log", "w3c_runner", ["--rdf"], 1800, ["w3c"]),
    ("rdf12", "w3c", "rdf12_results.log", "w3c_runner", ["--rdf12"], 900, ["w3c"]),
    ("rdf12c14n", "w3c", "rdf12c14n_results.log", "w3c_runner", ["--rdf12c14n"], 600, ["w3c"]),
    ("rdf12entail", "w3c", "rdf12entail_results.log", "w3c_runner", ["--rdf12entail"], 600, ["w3c"]),
    ("sparql12", "w3c", "sparql12_results.log", "w3c_runner", ["--sparql12"], 900, ["w3c"]),
    ("l4w3c:sparql11", "lean-w3c", "l4w3c_sparql11.log", "l4w3c", ["--quiet", "third_party/testing/w3c/sparql/sparql11/manifest-all.ttl"], 1800, ["w3c"]),
    ("l4w3c:sparql12", "lean-w3c", "l4w3c_sparql12.log", "l4w3c", ["--quiet", "third_party/testing/w3c/sparql/sparql12/manifest.ttl"], 900, ["w3c"]),
    ("l4w3c:rdf11", "lean-w3c", "l4w3c_rdf11.log", "l4w3c", ["--quiet", "third_party/testing/w3c/rdf/rdf11/manifest.ttl"], 900, ["w3c"]),
    ("l4w3c:rdf12", "lean-w3c", "l4w3c_rdf12.log", "l4w3c", ["--quiet", "third_party/testing/w3c/rdf/rdf12/manifest.ttl"], 900, ["w3c"]),
    ("l4w3c:rdfc10", "lean-w3c", "l4w3c_rdfc10.log", "l4w3c", ["--quiet", "third_party/testing/rdf-canon/tests/manifest.ttl"], 900, ["rdf-canon"]),
    ("rdfc10", "shapes", "rdfc10_results.log", "rdfc10_runner", [], 600, ["rdf-canon"]),
    ("shacl_core", "shapes", "shacl_results.log", "shacl_runner", [], 300, ["shacl"]),
    ("shacl_sparql", "shapes", "shacl_sparql_results.log", "shacl_runner", ["third_party/testing/shacl/data-shapes-test-suite/tests/sparql/manifest.ttl"], 300, ["shacl"]),
    ("shacl12_core", "shapes", "shacl12_core_results.log", "shacl_runner", ["third_party/testing/shacl/shacl12-test-suite/tests/core/manifest.ttl"], 600, ["shacl"]),
    ("shacl12_node_expr", "shapes", "shacl12_node_expr_results.log", "shacl_runner", ["third_party/testing/shacl/shacl12-test-suite/tests/node-expr/manifest.ttl"], 300, ["shacl"]),
    ("shacl12_sparql", "shapes", "shacl12_sparql_results.log", "shacl_runner", ["third_party/testing/shacl/shacl12-test-suite/tests/sparql/manifest.ttl"], 300, ["shacl"]),
    ("shacl12_rules", "shapes", "shacl12_rules_results.log", "shacl_runner", ["third_party/testing/shacl/shacl12-test-suite/tests/rules/eval/manifest.ttl"], 300, ["shacl"]),
    ("shacl12_rules_syntax", "shapes", "shacl12_rules_syntax_results.log", "shacl_runner", ["third_party/testing/shacl/shacl12-test-suite/tests/rules/syntax/manifest.ttl"], 300, ["shacl"]),
    ("shacl12_rules_wellformed", "shapes", "shacl12_rules_wellformed_results.log", "shacl_runner", ["third_party/testing/shacl/shacl12-test-suite/tests/rules/wellformed/manifest.ttl"], 300, ["shacl"]),
    ("shacl12_rules_stratification", "shapes", "shacl12_rules_stratification_results.log", "shacl_runner", ["third_party/testing/shacl/shacl12-test-suite/tests/rules/stratification/manifest.ttl"], 300, ["shacl"]),
    ("shex", "shapes", "shex_results.log", "shex_runner", [], 600, ["shex"]),
    ("jsonld_tordf", "jsonld", "jsonld_results.log", "jsonld_runner", [], 600, ["json-ld"]),
    ("jsonld_fromrdf", "jsonld", "jsonld_fromrdf_results.log", "jsonld_fromrdf_runner", [], 600, ["json-ld"]),
    ("jsonld_expand", "jsonld", "jsonld_expand_results.log", "jsonld_expand_runner", [], 600, ["json-ld"]),
    ("jsonld_compact", "jsonld", "jsonld_compact_results.log", "jsonld_compact_runner", [], 600, ["json-ld"]),
    ("jsonld_flatten", "jsonld", "jsonld_flatten_results.log", "jsonld_flatten_runner", [], 600, ["json-ld"]),
    ("owl_rl_positive_entailment", "owl", "owl_profile_rl_results.log", "owl_runner", [], 900, []),
    ("owl2_profile_el", "owl", "owl_profile_el_results.log", "owl_runner", ["third_party/testing/owl/profile-EL.rdf", "--regime", "rl"], 600, []),
    ("owl2_profile_ql", "owl", "owl_profile_ql_results.log", "owl_runner", ["third_party/testing/owl/profile-QL.rdf", "--regime", "rl"], 600, []),
    ("owl2_dl_inconsistency", "owl", "owl_type_inconsistency_results.log", "owl_runner", ["third_party/testing/owl/type-inconsistency.rdf", "--regime", "dl"], 1800, []),
    ("owl_syntax_dl_species", "owl", "owl_syntax_dl_results.log", "owl_runner", ["third_party/testing/owl/syntax-dl.rdf", "--species"], 600, []),
    ("rml_core", "misc", "rml_results.log", "rml_runner", [], 600, ["rml"]),
    ("rif_core", "misc", "rif_results.log", "rif_runner", [], 600, []),
    ("vc_stage1", "misc", "vc_results.log", "vc_runner", [], 300, ["vc"]),
    ("did_key", "misc", "did_results.log", "did_runner", [], 300, ["did"]),
    ("csvw_csv2rdf", "misc", "csvw_results.log", "csvw_runner", [], 900, ["csvw"]),
    ("csvw_csv2json", "misc", "csvw_json_results.log", "csvw_runner", ["--json"], 900, ["csvw"]),
    ("csvw_validation", "misc", "csvw_validate_results.log", "csvw_runner", ["--validate"], 900, ["csvw"]),
    ("xml_conformance", "misc", "xml_conformance_results.log", "xml_runner", ["third_party/testing/xml/xmlconf"], 900, []),
    ("xslt", "misc", "xslt_results.log", "xslt_runner", ["third_party/testing/xslt/manifest.json"], 600, []),
    ("mathml", "misc", "mathml_results.log", "mathml_runner", [], 300, []),
    ("jsonschema", "misc", "jsonschema_results.log", "jsonschema_runner", [], 300, []),
    ("schematron", "misc", "schematron_results.log", "schematron_runner", [], 300, []),
]
SUITE_GROUPS = sorted({s[1] for s in SUITES})


def cmd_suite_groups(a):
    groups = {g: sorted({sub for s in SUITES if s[1] == g for sub in s[6]}) for g in SUITE_GROUPS}
    print(json.dumps(groups) if a.json else "\n".join(f"{g}: {' '.join(v)}" for g, v in groups.items()))


def cmd_suite_run(a):
    core, out = os.path.abspath(a.core), os.path.abspath(a.out)
    os.makedirs(os.path.join(out, "logs"), exist_ok=True)
    bindir = os.path.join(os.path.abspath(a.bin), "bin", "linux-x86_64")
    status = {"group": a.group, "runner": runner_info(), "suites": {}}
    for key, group, logname, runner, args, budget, _ in SUITES:
        if group != a.group:
            continue
        exe = os.path.join(bindir, runner)
        t0 = time.time()
        st = {"runner": runner, "args": args, "budget_seconds": budget, "started_utc": now_utc()}
        if not os.access(exe, os.X_OK):
            st.update(exit=None, error=f"{runner} is not in the release")
        else:
            with open(os.path.join(out, "logs", logname), "wb") as f:
                try:
                    p = subprocess.run([exe] + args, cwd=core, stdout=f, stderr=subprocess.STDOUT, timeout=budget)
                    st["exit"] = p.returncode
                except subprocess.TimeoutExpired:
                    st["exit"] = 124
                    st["error"] = f"no end in {budget} s"
        st.update(seconds=round(time.time() - t0), finished_utc=now_utc())
        status["suites"][key] = st
        log(f"{key}: exit {st.get('exit')} in {st['seconds']} s")
    json.dump(status, open(os.path.join(out, f"status-{a.group}.json"), "w"), indent=1)


L4_TOTAL = re.compile(r"^TOTAL: (\d+) pass, (\d+) fail(.*)$", re.M)


def parse_l4w3c(text):
    m = L4_TOTAL.findall(text)
    if not m:
        return None
    p, f, rest = int(m[-1][0]), int(m[-1][1]), m[-1][2]
    nums = dict((k, int(v)) for v, k in re.findall(r"(\d+) (skip|unsupported|error)", rest))
    tot = re.search(r"out of (\d+)", rest)
    total = int(tot[1]) if tot else p + f + sum(nums.values())
    return {"pass": p, "fail": f, "total": total, **nums}


def suite_validity(st, t):
    r = []
    if st is None:
        return ["the suite did not run (group job missing)"]
    if st.get("error"):
        r.append(st["error"])
    if st.get("exit") not in (0, 1):
        r.append(f"runner exit {st.get('exit')}")
    if t is None:
        r.append("no score line in the log")
    elif not t.get("total"):
        r.append("0 tests found")
    return r


def cmd_suite_score(a):
    plan = json.load(open(a.plan))
    core = os.path.abspath(a.core)
    status = {}
    for fn in os.listdir(a.logs):
        if fn.startswith("status-"):
            status.update(json.load(open(os.path.join(a.logs, fn)))["suites"])
    od = os.path.join(core, "formal/fstar/ocaml-output")
    os.makedirs(od, exist_ok=True)
    for fn in os.listdir(os.path.join(a.logs, "logs")):
        shutil.copyfile(os.path.join(a.logs, "logs", fn), os.path.join(od, fn))
    totals = {}
    rc = subprocess.run(["bash", "formal/fstar/generate-report.sh"], cwd=core, capture_output=True, text=True)
    latest = os.path.join(core, "docs/test-results/latest.json")
    if rc.returncode == 0 and os.path.exists(latest):
        totals = json.load(open(latest)).get("totals", {})
    else:
        log("generate-report.sh failed: " + (rc.stderr or "")[-2000:])
    rows, metas = [], {}
    for key, group, logname, runner, args, budget, subs in SUITES:
        st = status.get(key)
        lp = os.path.join(od, logname)
        if key.startswith("l4w3c:"):
            t = parse_l4w3c(open(lp, errors="replace").read()) if os.path.exists(lp) else None
            engine = "lean"
        else:
            t = totals.get(key) if os.path.exists(lp) else None
            if t is not None and (t.get("present") is False or not isinstance(t, dict)):
                t = None
            engine = "fstar"
        reasons = suite_validity(st, t)
        suite = key.replace("l4w3c:", "l4w3c-")
        run_id = run_id_of(plan, suite, "linux-x86_64")
        p, tot = (t or {}).get("pass", 0), (t or {}).get("total", 0)
        row = {c: "" for c in RUNS_COLUMNS}
        row.update({
            "run_id": run_id, "started_utc": (st or {}).get("started_utc", ""), "finished_utc": (st or {}).get("finished_utc", ""),
            "trigger": plan["trigger"], "suite": suite, "platform": "linux-x86_64", "engine": engine,
            "factoidal_commit": plan["core_commit"], "commit_utc": plan["commit_committer_utc"], "snapshot_branch": plan.get("snapshot_branch", ""),
            "release_tag": plan["release_sets"].get("linux-x86_64", {}).get("tag", ""),
            "names_total": tot, "names_run": tot, "passed": p, "denominator": tot,
            "share_pct": f"{100 * p / tot:.4f}" if tot else "", "failed": (t or {}).get("fail", ""),
            "skip": (t or {}).get("skip", 0) + (t or {}).get("unsupported", 0) if t else "",
            "valid": "false" if reasons else "true", "invalid_reason": "; ".join(reasons), "kind": "full", "shards": 1,
            "wall_minutes": round(((st or {}).get("seconds") or 0) / 60, 1), "runner": "ubuntu-latest",
            "workflow_run_url": plan.get("workflow_run_url", ""), "meta_url": f"{RAW}/runs/{run_id}/meta.json",
        })
        rows.append(row)
        metas[run_id] = {"format": "factoidal-release-test-run-v1", "row": row, "plan": plan, "status": st, "totals": t,
                         "command": [f"bin/linux-x86_64/{runner}"] + args, "submodules": subs,
                         "parser": "l4w3c TOTAL line" if engine == "lean" else "formal/fstar/generate-report.sh latest.json totals." + key,
                         "validity": {"valid": not reasons, "reasons": reasons}}
    os.makedirs(a.out, exist_ok=True)
    json.dump(rows, open(os.path.join(a.out, "suite-rows.json"), "w"), indent=1)
    json.dump(metas, open(os.path.join(a.out, "suite-metas.json"), "w"), indent=1)
    md = ["### Other suites", "", "| Suite | Passed | Total | Share | Valid |", "| --- | ---: | ---: | ---: | --- |"]
    for r in rows:
        md.append(f"| {r['suite']} | {r['passed']} | {r['denominator']} | {r['share_pct'][:5] if r['valid'] == 'true' else '-'} | "
                  f"{'yes' if r['valid'] == 'true' else 'no: ' + r['invalid_reason']} |")
    summary("\n".join(md))


# ---- rivals ---------------------------------------------------------------------------------

def cmd_rivals(a):
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    chrome = json.load(open(os.path.join(a.inputs, "chrome.json")))
    want = {n: v["c"][1] for n, v in chrome.items() if v["c"][1] > 0}
    den = sum(v["c"][1] for v in chrome.values())
    enc_den = sum(c for n, c in want.items() if top(n) == "encoding")
    known = {(r["wpt_commit"], r["wptfyi_run_id"]) for r in read_csv_url("rivals.csv")}
    rows = []
    for product, channel in RIVALS:
        label = "&label=stable" if channel == "stable" else ""
        runs = wptfyi_runs(f"product={product}&label=master{label}&sha={a.wpt_commit}")
        if not runs:
            log(f"{product}: no {channel} run at {a.wpt_commit[:10]}")
            continue
        r = runs[0]
        if (a.wpt_commit, str(r["id"])) in known:
            continue
        s = load_summary(r["results_url"], os.path.join(work, f"{product}.json"))
        passed = enc = reported = 0
        for n, c in want.items():
            v = s.get(n)
            if v:
                reported += 1
                p = min(v["c"][0], c)
                passed += p
                if top(n) == "encoding":
                    enc += p
        rows.append({"recorded_utc": now_utc(), "wpt_commit": a.wpt_commit, "browser": product, "version": r.get("browser_version"),
                     "channel": channel, "wptfyi_run_id": r["id"], "run_time_utc": r.get("time_start"), "passed": passed,
                     "denominator": den, "share_pct": f"{100 * passed / den:.4f}",
                     "share_ex_encoding_pct": f"{100 * (passed - enc) / (den - enc_den):.4f}", "names_total": len(want),
                     "names_reported": reported, "partial": str(reported < PARTIAL_BELOW * len(want)).lower(),
                     "summary_url": r["results_url"]})
        os.remove(os.path.join(work, f"{product}.json"))
        log(f"{product} {r.get('browser_version')}: {passed} ({100 * passed / den:.2f}%), {reported} of {len(want)} names")
    os.makedirs(a.out, exist_ok=True)
    json.dump(rows, open(os.path.join(a.out, "rival-rows.json"), "w"), indent=1)
    if rows:
        summary("### Other browsers at WPT " + a.wpt_commit[:10] + "\n\n" + "\n".join(
            f"- {r['browser']} {r['version']}: {r['share_pct'][:5]}%{' (partial run)' if r['partial'] == 'true' else ''}" for r in rows))


# ---- record ---------------------------------------------------------------------------------

def append_csv(path, columns, rows):
    new = not os.path.exists(path)
    if not new:
        with open(path) as f:
            head = next(csv.reader(f), [])
        if head != columns:
            die(f"{path}: its columns are not {columns[:4]}...; runs.csv is never rewritten, so a column change needs a new file")
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})


def cmd_record(a):
    """Append rows found under --from (row.json + meta.json, suite-rows.json + suite-metas.json,
    rival-rows.json) to the results branch, with a new worktree each attempt, and push."""
    runs, metas, rivals, diffs = [], {}, [], []
    for dp, _, fs in os.walk(a.src):
        if "row.json" in fs and "meta.json" in fs:
            row = json.load(open(os.path.join(dp, "row.json")))
            metas[row["run_id"]] = json.load(open(os.path.join(dp, "meta.json")))
            (diffs if row["kind"] == "differential" else runs).append(row)
        if "suite-rows.json" in fs:
            runs += json.load(open(os.path.join(dp, "suite-rows.json")))
            metas.update(json.load(open(os.path.join(dp, "suite-metas.json"))))
        if "rival-rows.json" in fs:
            rivals += json.load(open(os.path.join(dp, "rival-rows.json")))
    if not (runs or rivals or diffs):
        log("nothing to record")
        return
    repo = os.path.abspath(a.repo)
    tmp = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), f"results-{os.getpid()}")
    for attempt in range(1, 6):
        tree = f"{tmp}-{attempt}"
        if subprocess.run(["git", "-C", repo, "fetch", "-q", "origin", f"+refs/heads/{RESULTS_BRANCH}:refs/remotes/origin/{RESULTS_BRANCH}"]).returncode:
            time.sleep(5 * attempt)
            continue
        subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "--detach", tree, f"refs/remotes/origin/{RESULTS_BRANCH}"], check=True)
        known = {r["run_id"] for r in (csv.DictReader(open(os.path.join(tree, "runs.csv"))) if os.path.exists(os.path.join(tree, "runs.csv")) else [])}
        new_runs = [r for r in runs if r["run_id"] not in known]
        append_csv(os.path.join(tree, "runs.csv"), RUNS_COLUMNS, new_runs)
        known_d = {r["run_id"] for r in (csv.DictReader(open(os.path.join(tree, "differential.csv"))) if os.path.exists(os.path.join(tree, "differential.csv")) else [])}
        if diffs:
            append_csv(os.path.join(tree, "differential.csv"), RUNS_COLUMNS, [r for r in diffs if r["run_id"] not in known_d])
        known_r = {(r["wpt_commit"], r["wptfyi_run_id"]) for r in (csv.DictReader(open(os.path.join(tree, "rivals.csv"))) if os.path.exists(os.path.join(tree, "rivals.csv")) else [])}
        new_rivals = [r for r in rivals if (r["wpt_commit"], str(r["wptfyi_run_id"])) not in known_r]
        if new_rivals:
            append_csv(os.path.join(tree, "rivals.csv"), RIVALS_COLUMNS, new_rivals)
        for rid, m in metas.items():
            d = os.path.join(tree, "runs", rid)
            os.makedirs(d, exist_ok=True)
            if not os.path.exists(os.path.join(d, "meta.json")):
                with open(os.path.join(d, "meta.json"), "w") as f:
                    json.dump(m, f, indent=1)
        subprocess.run(["git", "-C", tree, "add", "-A"], check=True)
        if subprocess.run(["git", "-C", tree, "diff", "--cached", "--quiet"]).returncode == 0:
            log("nothing new on the branch")
            return
        msg = f"results: {len(new_runs)} runs, {len(new_rivals)} rival rows" + (f" ({os.environ.get('GITHUB_RUN_ID')})" if os.environ.get("GITHUB_RUN_ID") else "")
        subprocess.run(["git", "-C", tree, "-c", "user.name=github-actions[bot]", "-c",
                        "user.email=41898282+github-actions[bot]@users.noreply.github.com", "commit", "-q", "-m", msg], check=True)
        if a.no_push:
            log(f"committed, not pushed: {tree}")
            return
        if subprocess.run(["git", "-C", tree, "push", "-q", "origin", f"HEAD:refs/heads/{RESULTS_BRANCH}"]).returncode == 0:
            log(f"pushed: {msg}")
            for r in new_runs + diffs:
                log(f"  {r['run_id']} {r['suite']} valid={r['valid']} {r['share_pct']}")
            return
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", tree])
        time.sleep(5 * attempt)
    die("could not push to the results branch after 5 attempts")


# ---- seed: a local full run --------------------------------------------------------------------

def cmd_seed_local(a):
    rep = json.load(open(a.report))
    t = rep["totals"]
    den = rep["denominator"]["subtests"]
    enc = rep["directories"]["encoding"]
    run_id = a.run_id
    row = {c: "" for c in RUNS_COLUMNS}
    row.update({
        "run_id": run_id, "started_utc": a.started, "finished_utc": a.finished, "trigger": "manual", "suite": "wpt",
        "platform": "macos-arm64", "engine": "bubblepopkit-native", "script_engine": "bubblepop",
        "factoidal_commit": a.commit, "commit_utc": a.commit_utc, "release_tag": a.release_tag, "wpt_commit": rep["wptCommit"],
        "names_total": t["namesInChrome"], "names_run": t["namesRun"], "passed": t["passed"], "denominator": den,
        "share_pct": f"{100 * t['passed'] / den:.4f}", "share_ex_encoding_pct": f"{100 * (t['passed'] - enc['passed']) / (den - enc['chrome']):.4f}",
        **outcome_columns(t["outcomes"]), "server_failures": a.server_failures, "kind": "full", "shards": 1,
        "wall_minutes": a.wall_minutes, "runner": "local Mac (8 CPUs, 16 GB), wpt-score.py run --jobs 3",
        "result_url": f"https://github.com/{BUILDS_REPO}/releases/download/{RESULTS_RELEASE}/{run_id}.wpt-full.json.gz",
        "meta_url": f"{RAW}/runs/{run_id}/meta.json",
    })
    m = {"run_id": run_id, "kind": "full", "factoidal_commit": a.commit, "release_tag": a.release_tag, "wpt_commit": rep["wptCommit"],
         "names_total": t["namesInChrome"], "names_run": t["namesRun"], "server_failures": int(a.server_failures),
         "shards": 1, "shards_present": 1, "shards_missing": [], "denominator": den, "shard_health": []}
    reasons = wpt_validity(m)
    row.update(valid="false" if reasons else "true", invalid_reason="; ".join(reasons))
    meta = {"format": "factoidal-release-test-run-v1", "row": row, "validity": {"valid": not reasons, "reasons": reasons},
            "notes": rep.get("notes"), "local": a.note, "totals": t,
            "directories": {k: {kk: v[kk] for kk in ("names", "run", "chrome", "passed", "reported", "share", "outcomes")} for k, v in rep["directories"].items()}}
    os.makedirs(a.out, exist_ok=True)
    json.dump(row, open(os.path.join(a.out, "row.json"), "w"), indent=1)
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    meta["source_report"] = f"https://github.com/{CORE_REPO}/blob/{a.core_commit_of_report}/tests/browser-wpt/wpt-full-20261113.json"
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    with open(a.report, "rb") as fi, gzip.open(os.path.join(a.out, f"{run_id}.wpt-full.json.gz"), "wb") as fo:
        shutil.copyfileobj(fi, fo)
    print(json.dumps(row, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("resolve")
    r.add_argument("--event", required=True)
    r.add_argument("--build-run-id", default="")
    r.add_argument("--run-url", default="")
    r.add_argument("--release", default="")
    r.add_argument("--wpt-commit", default="")
    r.add_argument("--suites", default="wpt,w3c")
    r.add_argument("--platforms", default="macos-arm64")
    r.add_argument("--script-engine", default="bubblepop", choices=["bubblepop", "quickjs"])
    r.add_argument("--shards", type=int, default=4, help="macOS shards")
    r.add_argument("--linux-shards", type=int, default=16)
    r.add_argument("--build-workflow", default="", help="workflow_run: the name of the workflow that ended")
    r.add_argument("--force", action="store_true")
    r.add_argument("--wait-minutes", type=int, default=0, help="schedule only: how long to wait for a running build")
    r.add_argument("--build-minutes", type=int, default=100, help="the usual length of a build.yml run")
    r.add_argument("--out", required=True)
    w = sub.add_parser("wpt-inputs")
    w.add_argument("--wpt-commit", required=True)
    w.add_argument("--out", required=True)
    s = sub.add_parser("wpt-shard")
    for k in ("--inputs", "--core", "--engine-dir", "--work", "--out", "--engine-tag", "--web-tag"):
        s.add_argument(k, required=True)
    s.add_argument("--index", type=int, required=True)
    s.add_argument("--shards", type=int, required=True)
    s.add_argument("--platform", default="macos-arm64", choices=sorted(ENGINE_SET))
    s.add_argument("--script-engine", default="bubblepop", choices=["bubblepop", "quickjs"])
    s.add_argument("--jobs", type=int, default=3)
    s.add_argument("--max-minutes", type=int, default=150)
    s.add_argument("--pydeps", help="directory with PyYAML for wptserve's Test262 pages")
    m = sub.add_parser("wpt-merge")
    for k in ("--plan", "--inputs", "--shards-dir", "--core", "--out"):
        m.add_argument(k, required=True)
    m.add_argument("--platform", default="macos-arm64")
    g = sub.add_parser("suite-groups")
    g.add_argument("--json", action="store_true")
    sr = sub.add_parser("suite-run")
    for k in ("--group", "--core", "--bin", "--out"):
        sr.add_argument(k, required=True)
    ss = sub.add_parser("suite-score")
    for k in ("--plan", "--core", "--logs", "--out"):
        ss.add_argument(k, required=True)
    rv = sub.add_parser("rivals")
    for k in ("--wpt-commit", "--inputs", "--work", "--out"):
        rv.add_argument(k, required=True)
    rc = sub.add_parser("record")
    rc.add_argument("--from", dest="src", required=True)
    rc.add_argument("--repo", default=".")
    rc.add_argument("--no-push", action="store_true")
    sl = sub.add_parser("seed-local")
    for k in ("--report", "--run-id", "--started", "--finished", "--commit", "--commit-utc", "--release-tag",
              "--server-failures", "--wall-minutes", "--core-commit-of-report", "--note", "--out"):
        sl.add_argument(k, required=True)
    a = ap.parse_args()
    {"resolve": cmd_resolve, "wpt-inputs": cmd_wpt_inputs, "wpt-shard": cmd_wpt_shard, "wpt-merge": cmd_wpt_merge,
     "suite-groups": cmd_suite_groups, "suite-run": cmd_suite_run, "suite-score": cmd_suite_score, "rivals": cmd_rivals,
     "record": cmd_record, "seed-local": cmd_seed_local}[a.cmd](a)


if __name__ == "__main__":
    main()
