#!/usr/bin/env python3
"""wpt-score-job.py: the Web Platform Tests score of the Foafnaut engine, with no person.

It drives factoidal-core's own tool (tests/browser-wpt/wpt-score.py: sample, run,
score) and adds what a job needs: the engine from a release, the WPT commit and
Chrome's wpt.fyi summary for it, a start check, wall-clock caps and a short record.
`.github/workflows/wpt-score.yml` calls it; the same commands run on a laptop or a
cloud machine.

  fetch-engine  find the newest factoidal-builds release of the Foafnaut engine whose
                core commit is in the history of the core checkout, check every file
                against build-info.json, and unpack it
  run           one score: one WPT commit, one page script engine
  summarize     a Markdown table and one JSON line a run, from the records of `run`

Example (a small sample of four directories, about 2 minutes):

  python3 scripts/wpt-score-job.py fetch-engine --core ../factoidal-core --dest /tmp/w/engine
  python3 scripts/wpt-score-job.py run --core ../factoidal-core --engine-dir /tmp/w/engine \\
      --wpt pinned --script-engine bubblepop --smoke --work /tmp/w/work --out /tmp/w/out
  python3 scripts/wpt-score-job.py summarize --records /tmp/w/out --markdown /tmp/w/summary.md

What a run needs (measured on Linux x86_64 and written in docs/20261110-wpt-score-job.md):
Python 3, Deno, git, the core checkout, an engine and network access to github.com
(WPT), wpt.fyi and storage.googleapis.com (Chrome's summary). No GPU, no window
library and no Lean toolchain (but a Linux engine library needs Lean's shared
runtime). The tool starts WPT's own server on 127.0.0.1 ports 8000-8003, 8443-8446,
8888, 8889 and 9000; WPT's host names resolve only inside the runner.

The WPT checkout and Chrome's summary are data from the network. They go to
directories of their own under --work. This script reads them as data, and runs no
interpreter from inside them; the one program that runs from the WPT checkout is WPT's
server, which core's tool starts.
"""
import argparse, gzip, hashlib, json, os, platform, re, shutil, signal, subprocess, sys, tarfile, time
import urllib.error, urllib.request

BUILDS_REPO = os.environ.get("FACTOIDAL_BUILDS_REPO", "danbri/factoidal-builds")
WPT_REPO = "https://github.com/web-platform-tests/wpt"
SMOKE_DIRS = "console,dom,domparsing,url"
RUNTIME = "labs/demos/foafnaut/.build/native-html/runtime"
PORTS = (8000, 8001, 8002, 8003, 8443, 8444, 8445, 8446, 8888, 8889, 9000)


def log(msg):
    print(f"wpt-score-job: {msg}", file=sys.stderr, flush=True)


def die(msg, code=1):
    log(f"FAILED: {msg}")
    sys.exit(code)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def http(url, dest=None, accept=None, token=None, timeout=120, tries=4):
    """GET with a time limit and a few tries. The token goes to api.github.com only."""
    headers = {"User-Agent": "factoidal-wpt-score-job"}
    if accept:
        headers["Accept"] = accept
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                if dest is None:
                    return r.read()
                with open(dest + ".part", "wb") as f:
                    shutil.copyfileobj(r, f)
                os.replace(dest + ".part", dest)
                return None
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code in (401, 403, 404):
                break
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"GET {url}: {last}")


def run(cmd, timeout, cwd=None, env=None, logfile=None, check=True):
    """Run a command with a wall-clock limit. With logfile, its output goes to the file
    and to this process's stderr, whole. On the limit the process group is killed."""
    log("$ " + " ".join(cmd))
    out = open(logfile, "ab") if logfile else None
    env = dict(env or os.environ, NO_COLOR="1")  # Deno's errors without colour codes in the logs
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE if out else None,
                         stderr=subprocess.STDOUT if out else None, start_new_session=True)
    deadline = time.time() + timeout
    timed_out = False
    try:
        if out:
            os.set_blocking(p.stdout.fileno(), False)
            while True:
                chunk = p.stdout.read(65536)
                if chunk:
                    out.write(chunk)
                    out.flush()
                    sys.stderr.buffer.write(chunk)
                    sys.stderr.buffer.flush()
                elif p.poll() is not None:
                    break
                else:
                    time.sleep(0.2)
                if time.time() > deadline:
                    timed_out = True
                    break
        else:
            try:
                p.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
        if timed_out:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait()
    finally:
        if out:
            out.close()
    if timed_out:
        if check:
            die(f"no end in {timeout:.0f} s: {' '.join(cmd[:4])} ...")
        return 124
    if check and p.returncode != 0:
        die(f"exit {p.returncode}: {' '.join(cmd[:4])} ...")
    return p.returncode


def git(args, cwd, timeout=120):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=timeout)


# ---- fetch-engine ----------------------------------------------------------------------

def release_sets(native):
    """The release sets a run needs. foafnaut-web: the engine's Wasm build (the runner
    loads its module also when the engine is the native library) and the QuickJS-NG
    guest. foafnaut-darwin-arm64: libweb-render.dylib, the only native engine library
    that a release holds (2026-11-10)."""
    return ["foafnaut-web"] + (["foafnaut-darwin-arm64"] if native else [])


def cmd_fetch_engine(a):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    native = a.engine == "native"
    if native and (platform.system(), platform.machine()) != ("Darwin", "arm64"):
        die("--engine native: the only released engine library is libweb-render.dylib for macOS arm64 "
            f"(set foafnaut-darwin-arm64); this machine is {platform.system()} {platform.machine()}. "
            "Use --engine wasm, or give `run` a library with --native-engine.", 2)
    sets = release_sets(native)
    os.makedirs(a.dest, exist_ok=True)
    releases = []
    for page in (1, 2, 3):
        got = json.loads(http(f"https://api.github.com/repos/{BUILDS_REPO}/releases?per_page=100&page={page}",
                              accept="application/vnd.github+json", token=token))
        releases += got
        if len(got) < 100:
            break
    by_commit = {}
    for r in releases:
        m = re.fullmatch(r"build-([0-9a-f]{12})-(.+)", r.get("tag_name") or "")
        if m and not r.get("draft") and m[2] in sets:
            by_commit.setdefault(m[1], {})[m[2]] = r
    # Newest first, by the time of the commit's newest wanted set.
    order = sorted(by_commit.items(), key=lambda kv: max(r.get("published_at") or "" for r in kv[1].values()), reverse=True)
    chosen = None
    for short, have in order:
        if any(s not in have for s in sets):
            continue
        if a.commit:
            if not (a.commit.startswith(short) or short.startswith(a.commit)):
                continue
        else:
            full = git(["rev-parse", "-q", "--verify", short + "^{commit}"], a.core)
            if full.returncode != 0:
                continue
            if git(["merge-base", "--is-ancestor", full.stdout.strip(), "HEAD"], a.core).returncode != 0:
                continue
        chosen = (short, have)
        break
    if not chosen:
        die(f"no release of {' and '.join(sets)} from one core commit in the history of {a.core} "
            f"({len(by_commit)} commits with a wanted set in the newest {len(releases)} releases)", 2)
    short, have = chosen
    info_out = {"core_short": short, "sets": {}, "files": {}}
    for s in sets:
        rel = have[s]
        tag = rel["tag_name"]
        d = os.path.join(a.dest, s)
        dl = os.path.join(a.dest, "download-" + s)
        for p in (d, dl):
            if os.path.exists(p):
                shutil.rmtree(p)
            os.makedirs(p)
        for name in ("build-info.json", s + ".tar.gz"):
            target = os.path.join(dl, name)
            try:
                http(f"https://github.com/{BUILDS_REPO}/releases/download/{tag}/{name}", dest=target, timeout=600)
            except RuntimeError as e:
                # The download address has answered 504 for hours while the API served the
                # same asset (core tools/fetch-builds.sh, 2026-11-08).
                asset = next((x for x in rel.get("assets", []) if x.get("name") == name), None)
                if not asset:
                    die(f"{tag}: no asset {name} ({e})")
                log(f"{name}: download address failed; trying the API")
                http(asset["url"], dest=target, accept="application/octet-stream", token=token, timeout=600)
        info = json.load(open(os.path.join(dl, "build-info.json")))
        art = info["artifacts"][s + ".tar.gz"]
        tarball = os.path.join(dl, s + ".tar.gz")
        if sha256(tarball) != art["sha256"]:
            die(f"{tag}: the sha256 of {s}.tar.gz is not the one in build-info.json; nothing unpacked")
        with tarfile.open(tarball) as tf:
            tf.extractall(d, filter="data")
        listed, seen = art["files"], set()
        for dp, _, fs in os.walk(d):
            for f in fs:
                p = os.path.join(dp, f)
                relp = os.path.relpath(p, d)
                if os.path.islink(p):
                    continue
                seen.add(relp)
                if relp not in listed or sha256(p) != listed[relp]["sha256"]:
                    die(f"{tag}: {relp} is not listed in build-info.json or its sha256 differs")
        if set(listed) - seen:
            die(f"{tag}: files of build-info.json are missing: {sorted(set(listed) - seen)[:5]}")
        log(f"{tag}: {len(seen)} files checked against build-info.json (core {info['source_commit'][:12]})")
        info_out["sets"][s] = {"tag": tag, "source_commit": info["source_commit"], "published_at": rel.get("published_at"),
                               "run_url": info.get("run_url"), "tarball_sha256": art["sha256"]}
        info_out["core_commit"] = info["source_commit"]
    web = os.path.join(a.dest, "foafnaut-web", "docs/web/hub")
    files = {"wasm_runtime": os.path.join(web, "html-webgpu/runtime"),
             "quickjs_wasm": os.path.join(web, "wasm-guests/qjs-wasmvm.wasm")}
    if native:
        files["native_engine"] = os.path.join(a.dest, "foafnaut-darwin-arm64", "foafnaut/libweb-render.dylib")
    for k, p in files.items():
        if not os.path.exists(p):
            die(f"the release has no {os.path.relpath(p, a.dest)} ({k})")
    info_out["files"] = files
    info_out["engine"] = a.engine
    with open(os.path.join(a.dest, "engine.json"), "w") as f:
        json.dump(info_out, f, indent=1)
    print(json.dumps(info_out, indent=1))


# ---- run -------------------------------------------------------------------------------

def last_record(core):
    """The newest whole-WPT score record of core (tests/browser-wpt/wpt-score-YYYYMMDD.json)."""
    d = os.path.join(core, "tests/browser-wpt")
    names = sorted(n for n in os.listdir(d) if re.fullmatch(r"wpt-score-\d{8}\.json", n))
    if not names:
        die(f"no wpt-score-YYYYMMDD.json in {d}")
    rec = json.load(open(os.path.join(d, names[-1])))
    return names[-1], rec


def chrome_run(sha):
    """wpt.fyi's Chrome run (stable, master) for a WPT commit, or the newest one."""
    base = "https://wpt.fyi/api/runs?product=chrome&label=master"
    urls = [f"{base}&label=stable&sha={sha}", f"{base}&sha={sha}"] if sha else [f"{base}&label=stable&max-count=1"]
    for u in urls:
        runs = json.loads(http(u))
        if runs:
            return runs[0]
    die(f"wpt.fyi has no Chrome run for WPT {sha or '(newest)'}; without its summary there is no denominator", 2)


def ports_in_use():
    import socket
    busy = []
    for port in PORTS:
        s = socket.socket()
        s.settimeout(0.5)
        if s.connect_ex(("127.0.0.1", port)) == 0:
            busy.append(port)
        s.close()
    return busy


def wait_ports_free(seconds=40):
    end = time.time() + seconds
    while time.time() < end:
        if not ports_in_use():
            return True
        time.sleep(1)
    return False


def kill_leftovers(run_dir):
    """Stop what a killed tool run leaves: runner processes and WPT's server. Each has the
    run directory in its command line."""
    rc = subprocess.run(["pkill", "-KILL", "-f", run_dir], capture_output=True).returncode
    if rc not in (0, 1):
        log(f"pkill exit {rc} (leftover processes not checked)")


def results_in(run_dir):
    out = {}
    for fn in sorted(os.listdir(run_dir)) if os.path.isdir(run_dir) else []:
        if fn.endswith(".jsonl"):
            for line in open(os.path.join(run_dir, fn)):
                if line.strip():
                    c = json.loads(line)
                    out[c["file"]] = c
    return out


def cmd_run(a):
    t_start = time.time()
    core = os.path.abspath(a.core)
    tool = os.path.join(core, "tests/browser-wpt/wpt-score.py")
    if not os.path.exists(tool):
        die(f"{tool}: not a factoidal-core checkout with the WPT score tool", 2)
    if not shutil.which("deno"):
        die("deno is not on PATH (core's tool starts `deno run`)", 2)
    if a.smoke:
        a.dirs = a.dirs or SMOKE_DIRS
        a.n, a.keep, a.variants = 3, 1, "window"
        a.max_minutes = min(a.max_minutes, 15)
        a.stall = min(a.stall, 120)
    if a.keep > a.n:
        die("--keep is more than --n", 2)
    work, out = os.path.abspath(a.work), os.path.abspath(a.out)
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)

    # The engine: from fetch-engine's directory, or named file by file.
    engine_info = {}
    if a.engine_dir:
        engine_info = json.load(open(os.path.join(a.engine_dir, "engine.json")))
        files = engine_info["files"]
        a.wasm_runtime = a.wasm_runtime or files["wasm_runtime"]
        a.quickjs_wasm = a.quickjs_wasm or files["quickjs_wasm"]
        a.native_engine = a.native_engine or files.get("native_engine")
        a.engine = a.engine or engine_info.get("engine")
    a.engine = a.engine or ("native" if a.native_engine else "wasm")
    help_text = subprocess.run([sys.executable, "-I", tool, "run", "--help"], capture_output=True, text=True, timeout=60).stdout
    tool_has_engine_option = "--engine" in help_text
    if a.engine == "wasm" and not tool_has_engine_option:
        die("--engine wasm: this core's wpt-score.py always starts the runner with `--engine native --native-engine FILE` "
            "and has no option for the Wasm engine. It needs the change of docs/20261110-wpt-score-job.md (`run --engine wasm`).", 2)
    if a.engine == "native" and not (a.native_engine and os.path.exists(a.native_engine)):
        die(f"--engine native needs the engine library (--native-engine or fetch-engine); got {a.native_engine}", 2)
    if a.script_engine == "quickjs" and not (a.quickjs_wasm and os.path.exists(a.quickjs_wasm)):
        die(f"--script-engine quickjs needs the QuickJS-NG guest (--quickjs-wasm or fetch-engine); got {a.quickjs_wasm}", 2)
    # The runner imports the engine's Wasm module from the core checkout, also when the
    # engine is the native library (labs/demos/foafnaut/native_html_engine.ts, line 4).
    runtime = os.path.join(core, RUNTIME)
    if a.wasm_runtime:
        os.makedirs(runtime, exist_ok=True)
        for name in ("web-render.mjs", "web-render.wasm"):
            shutil.copyfile(os.path.join(a.wasm_runtime, name), os.path.join(runtime, name))
    for name in ("web-render.mjs", "web-render.wasm"):
        if not os.path.exists(os.path.join(runtime, name)):
            die(f"{os.path.join(runtime, name)} is missing: give --wasm-runtime DIR (set foafnaut-web of a release) or --engine-dir", 2)

    # The WPT commit and Chrome's summary for it.
    record_name, record = last_record(core)
    if a.wpt == "pinned":
        wpt_commit, wpt_label = record["wptCommit"], "pinned"
        crun = chrome_run(wpt_commit)
    elif a.wpt == "latest":
        crun = chrome_run(None)
        wpt_commit, wpt_label = crun["full_revision_hash"], "latest"
    elif re.fullmatch(r"[0-9a-f]{40}", a.wpt):
        wpt_commit, wpt_label = a.wpt, a.wpt[:10]
        crun = chrome_run(wpt_commit)
    else:
        die("--wpt is pinned, latest or a 40-hex WPT commit", 2)
    if crun["full_revision_hash"] != wpt_commit:
        die(f"wpt.fyi answered a run of {crun['full_revision_hash']} for {wpt_commit}")
    log(f"WPT {wpt_label} = {wpt_commit}; Chrome {crun.get('browser_version')} run {crun.get('id')} of {crun.get('time_start')}")
    data = os.path.join(work, "chrome-" + wpt_commit[:12])
    os.makedirs(data, exist_ok=True)
    chrome_path = os.path.join(data, "chrome.json")
    if not os.path.exists(chrome_path):
        raw = http(crun["results_url"], timeout=300)
        if raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
        with open(chrome_path, "wb") as f:
            f.write(raw)
    chrome = json.load(open(chrome_path))
    whole_denominator = sum(v["c"][1] for v in chrome.values())
    subset = None
    if a.dirs:
        tops = tuple("/" + d.strip("/") + "/" for d in a.dirs.split(",") if d.strip())
        chrome = {n: v for n, v in chrome.items() if n.startswith(tops)}
        subset = sorted(t.strip("/") for t in tops)
        chrome_path = os.path.join(data, "chrome-subset.json")
        with open(chrome_path, "w") as f:
            json.dump(chrome, f)
    denominator = sum(v["c"][1] for v in chrome.values())
    if not denominator:
        die("Chrome's summary has no subtests for this selection", 2)
    if wpt_label == "pinned" and not subset and denominator != record["denominator"]["subtests"]:
        log(f"WARNING: Chrome's summary gives {denominator} subtests; {record_name} has {record['denominator']['subtests']}")

    tag = f"{wpt_label}-{a.script_engine}"
    run_dir = os.path.join(work, "run-" + tag)
    if os.path.exists(run_dir) and not a.resume:
        shutil.rmtree(run_dir)
    os.makedirs(run_dir, exist_ok=True)
    tool_log = os.path.join(out, f"tool-{tag}.log")
    sample_json, sample_list = os.path.join(run_dir, "sample.json"), os.path.join(run_dir, "sample.list")
    run([sys.executable, "-I", tool, "sample", "--chrome", chrome_path, "--seed", str(a.seed), "--n", str(a.n), "--keep", str(a.keep),
         "--variants", a.variants, "--out", sample_json, "--list", sample_list], timeout=300, logfile=tool_log)
    names = [l.strip() for l in open(sample_list) if l.strip()]

    # WPT at the commit, in a directory of its own.
    wpt_root = os.path.join(work, "wpt-" + wpt_commit[:12])
    marker = os.path.join(wpt_root, ".factoidal-wpt-commit")
    if not (os.path.exists(marker) and open(marker).read().strip() == wpt_commit):
        if os.path.exists(wpt_root):
            shutil.rmtree(wpt_root)
        os.makedirs(wpt_root)
        if a.wpt_source == "git":
            env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1", GIT_TERMINAL_PROMPT="0")
            run(["git", "init", "-q", wpt_root], timeout=60)
            run(["git", "-C", wpt_root, "remote", "add", "origin", WPT_REPO], timeout=60)
            run(["git", "-C", wpt_root, "fetch", "-q", "--depth", "1", "origin", wpt_commit], timeout=1800, env=env, logfile=tool_log)
            run(["git", "-C", wpt_root, "-c", "advice.detachedHead=false", "checkout", "-q", "FETCH_HEAD"], timeout=900, env=env, logfile=tool_log)
        else:
            run([sys.executable, "-I", tool, "tree", "--wpt-root", wpt_root, "--list", sample_list, "--commit", wpt_commit],
                timeout=3600, logfile=tool_log)
        with open(marker, "w") as f:
            f.write(wpt_commit + "\n")

    extra = ["--script-engine", a.script_engine, "--wpt-commit", wpt_commit]
    if a.script_engine == "quickjs":
        extra += ["--quickjs-wasm", os.path.abspath(a.quickjs_wasm)]
    engine_args = (["--engine", a.engine] if tool_has_engine_option else []) + \
                  (["--native-engine", os.path.abspath(a.native_engine)] if a.engine == "native" else [])

    def tool_run(list_file, directory, jobs, minutes):
        # The tool's own limit is --max-hours; the limit here is the backstop for a tool
        # that does not come back (its start of WPT's server alone may take 60 s).
        rc = run([sys.executable, "-I", tool, "run", "--list", list_file, "--dir", directory, "--wpt-root", wpt_root] + engine_args +
                 ["--jobs", str(jobs), "--stall", str(a.stall), "--max-hours", f"{minutes / 60:.4f}", "--"] + extra,
                 timeout=minutes * 60 + 180, logfile=tool_log, check=False)
        if rc == 124:
            kill_leftovers(directory)
        if not wait_ports_free():
            kill_leftovers(directory)
            if not wait_ports_free(10):
                log(f"WARNING: ports still in use after the run: {ports_in_use()}")
        return rc

    busy = ports_in_use()
    if busy:
        die(f"ports {busy} on 127.0.0.1 are in use; WPT's server needs {PORTS}", 2)
    # Start check: one test. A runner that cannot start (no library, no Wasm module, no
    # guest) ends before its first test, and the tool starts it again until --max-hours
    # (seen on 2026-11-10: 10 minutes, 0 of 33 results, exit 0).
    check_dir = os.path.join(run_dir, "start-check")
    if os.path.exists(check_dir):
        shutil.rmtree(check_dir)
    os.makedirs(check_dir)
    first = next((n for n in names if n.endswith(".html") and "?" not in n), names[0])
    with open(os.path.join(check_dir, "one.list"), "w") as f:
        f.write(first + "\n")
    rc = tool_run(os.path.join(check_dir, "one.list"), check_dir, 1, 4)
    if not results_in(check_dir):
        part_log = os.path.join(check_dir, "part0.log")
        tail = open(part_log, errors="replace").read()[:3000] if os.path.exists(part_log) else "(no runner log)"
        if os.path.exists(part_log):
            shutil.copyfile(part_log, os.path.join(out, f"start-check-{tag}.log"))
        die(f"start check: the runner gave no result for {first} (tool exit {rc}). Runner log, first 3000 characters:\n{tail}")
    log(f"start check passed: {first} -> {next(iter(results_in(check_dir).values()))['harness']}")

    t_run = time.time()
    results_dir = os.path.join(run_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    rc = tool_run(sample_list, results_dir, a.jobs, a.max_minutes)
    run_seconds = round(time.time() - t_run)
    done = results_in(results_dir)
    ran = sum(1 for n in names if n.lstrip("/") in done)
    complete = ran == len(names)
    if rc not in (0,) and not done:
        die(f"the tool's run ended with exit {rc} and no result")
    harness = {}
    for c in done.values():
        harness[c["harness"]] = harness.get(c["harness"], 0) + 1

    lib = a.native_engine if a.engine == "native" else os.path.join(runtime, "web-render.wasm")
    core_head = git(["rev-parse", "HEAD"], core).stdout.strip() or None
    engine_commit = a.engine_commit or engine_info.get("core_commit")
    script_name = "BubblePopJS" if a.script_engine == "bubblepop" else "QuickJS-NG in WasmVM"
    engine_note = (f"Foafnaut {a.engine} engine" + (f" from factoidal-core {engine_commit[:12]}" if engine_commit else "") +
                   f", page scripts in {script_name}")
    notes = {
        "job": "factoidal-builds scripts/wpt-score-job.py",
        "wpt": {"label": wpt_label, "commit": wpt_commit, "source": a.wpt_source,
                "chromeRun": {k: crun.get(k) for k in ("id", "browser_version", "os_name", "os_version", "time_start", "results_url")}},
        "engine": {"kind": a.engine, "coreCommit": engine_commit, "release": engine_info.get("sets"),
                   "file": os.path.basename(lib), "sha256": sha256(lib), "scriptEngine": a.script_engine,
                   **({"quickjsWasmSha256": sha256(a.quickjs_wasm)} if a.script_engine == "quickjs" else {})},
        "tool": {"coreCommit": core_head, "wptScoreSha256": sha256(tool), "lastRecord": record_name},
        "sample": {"seed": a.seed, "n": a.n, "keep": a.keep, "variants": a.variants, "names": len(names), "namesRun": ran,
                   "complete": complete, **({"subsetOfDirectories": subset, "wholeDenominator": whole_denominator} if subset else {})},
        "run": {"wallSeconds": run_seconds, "processes": a.jobs, "stallSeconds": a.stall, "maxMinutes": a.max_minutes,
                "toolExit": rc, "harness": harness, "machine": f"{platform.system()} {platform.machine()}",
                "cpus": os.cpu_count(), "url": os.environ.get("WPT_SCORE_RUN_URL")},
    }
    notes_path = os.path.join(run_dir, "notes.json")
    with open(notes_path, "w") as f:
        json.dump(notes, f, indent=1)
    score_path = os.path.join(out, f"wpt-score-{tag}.json")
    run([sys.executable, "-I", tool, "score", "--chrome", chrome_path, "--sample", sample_json, "--results", results_dir,
         "--denominator", str(denominator), "--wpt-commit", wpt_commit, "--engine-note", engine_note, "--notes", notes_path,
         "--out", score_path], timeout=600, logfile=tool_log)
    score = json.load(open(score_path))
    t = score["totals"]
    record_line = {
        "format": "factoidal-wpt-score-job-v1", "measuredAt": score["measuredAt"], "wpt": wpt_label, "wptCommit": wpt_commit,
        "scriptEngine": a.script_engine, "engine": a.engine, "engineCoreCommit": engine_commit, "toolCoreCommit": core_head,
        "suite": "WPT testharness subtests, counted as wpt.fyi counts them" + (f"; only the directories {', '.join(subset)}" if subset else ""),
        "denominator": denominator, "denominatorSource": f"Chrome {crun.get('browser_version')} on wpt.fyi at the WPT commit",
        "subset": subset, "measured": t["measuredLowerBound"], "estimate": t["extrapolated"], "range95": t["range95"],
        "estimateShare": t["extrapolatedShare"], "range95Share": t["range95Share"], "testsRun": t["testsRun"],
        "sample": notes["sample"], "wallSeconds": run_seconds, "totalSeconds": round(time.time() - t_start),
        "machine": notes["run"]["machine"], "harness": harness, "runUrl": notes["run"]["url"], "scoreFile": os.path.basename(score_path),
    }
    with open(os.path.join(out, f"record-{tag}.json"), "w") as f:
        json.dump(record_line, f, indent=1)
    # The raw results (one line a test) and the runner's logs, for the artifact.
    raw = os.path.join(out, f"raw-{tag}")
    os.makedirs(raw, exist_ok=True)
    for fn in sorted(os.listdir(results_dir)):
        if fn.endswith((".jsonl", ".log", ".list")):
            shutil.copyfile(os.path.join(results_dir, fn), os.path.join(raw, fn))
    shutil.copyfile(sample_json, os.path.join(raw, "sample.json"))
    print(line_of(record_line))
    if not complete:
        log(f"WARNING: {ran} of {len(names)} names ran before the limit of {a.max_minutes} minutes; the score is of those")
        sys.exit(3 if a.fail_incomplete else 0)


# ---- summarize -------------------------------------------------------------------------

def line_of(r):
    pct = lambda x: f"{100 * x:.2f}%"
    part = "" if r["sample"]["complete"] else f" INCOMPLETE ({r['sample']['namesRun']} of {r['sample']['names']} names)"
    return (f"{r['measuredAt'][:10]} WPT {r['wpt']} {r['wptCommit'][:10]}, {r['scriptEngine']}, {r['engine']} engine "
            f"{(r['engineCoreCommit'] or 'unknown')[:12]}: estimate {r['estimate']} of {r['denominator']} subtests ({pct(r['estimateShare'])}), "
            f"95% range {r['range95'][0]} to {r['range95'][1]} ({pct(r['range95Share'][0])} to {pct(r['range95Share'][1])}), "
            f"measured {r['measured']} in {r['testsRun']} tests{part}"
            + (f"; SUBSET {', '.join(r['subset'])} only" if r.get("subset") else ""))


def cmd_summarize(a):
    records = []
    for d in a.records:
        for dp, _, fs in os.walk(d):
            for fn in sorted(fs):
                if re.fullmatch(r"record-.*\.json", fn):
                    records.append(json.load(open(os.path.join(dp, fn))))
    records.sort(key=lambda r: (r["wpt"] != "pinned", r["scriptEngine"]))
    if not records:
        die("no record-*.json under " + ", ".join(a.records), 2)
    pct = lambda x: f"{100 * x:.2f}%"
    md = ["## Foafnaut WPT score", ""]
    if any(r.get("subset") for r in records):
        md += ["**Subset run.** Rows marked SUBSET count only the named WPT directories; they are not the whole-WPT score.", ""]
    md += ["| Date | WPT commit | Page scripts | Engine (core commit) | Estimate | 95% range | Measured | Denominator | Names run | Wall time |",
           "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in records:
        s = r["sample"]
        names = f"{s['namesRun']} of {s['names']}" + ("" if s["complete"] else " INCOMPLETE")
        md.append(f"| {r['measuredAt'][:10]} | {r['wpt']} `{r['wptCommit'][:10]}`" + (f" SUBSET {', '.join(r['subset'])}" if r.get("subset") else "") +
                  f" | {r['scriptEngine']} | {r['engine']} `{(r['engineCoreCommit'] or 'unknown')[:12]}` | {r['estimate']} ({pct(r['estimateShare'])}) | "
                  f"{r['range95'][0]} to {r['range95'][1]} ({pct(r['range95Share'][0])} to {pct(r['range95Share'][1])}) | {r['measured']} | "
                  f"{r['denominator']} | {names} | {r['wallSeconds'] // 60} min {r['wallSeconds'] % 60} s |")
    s0 = records[0]["sample"]
    md += ["", f"Suite: {records[0]['suite']}. Denominator: {records[0]['denominatorSource']}. "
               f"Sample: seed {s0['seed']}, {s0['n']} names a stratum ({s0['keep']} largest always), variants {s0['variants']}. "
               "`pinned` is the WPT commit of core's last record (a change shows our change); `latest` is the newest WPT commit "
               "with a Chrome stable run on wpt.fyi (the difference from `pinned` shows WPT's change).", ""]
    text = "\n".join(md) + "\n"
    if a.markdown:
        with open(a.markdown, "a") as f:
            f.write(text)
    if a.history:
        with open(a.history, "a") as f:
            for r in records:
                f.write(json.dumps({k: v for k, v in r.items() if k != "harness"}, separators=(",", ":"), sort_keys=True) + "\n")
    for r in records:
        print(line_of(r))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch-engine", help="download and check the newest released engine for a core checkout")
    f.add_argument("--core", required=True, help="factoidal-core checkout with history (the release must be of HEAD or an ancestor)")
    f.add_argument("--dest", required=True)
    f.add_argument("--engine", choices=["native", "wasm"], default="native" if platform.system() == "Darwin" else "wasm")
    f.add_argument("--commit", help="take the release of exactly this core commit")
    r = sub.add_parser("run", help="one score: one WPT commit, one page script engine")
    r.add_argument("--core", required=True, help="factoidal-core checkout (the tool, the runner, the last record)")
    r.add_argument("--engine-dir", help="the directory that fetch-engine wrote")
    r.add_argument("--engine", choices=["native", "wasm"])
    r.add_argument("--native-engine", help="engine library (libweb-render.dylib; on Linux a libweb-render.so)")
    r.add_argument("--wasm-runtime", help="directory with web-render.mjs and web-render.wasm (set foafnaut-web: docs/web/hub/html-webgpu/runtime)")
    r.add_argument("--quickjs-wasm", help="the QuickJS-NG guest, qjs-wasmvm.wasm")
    r.add_argument("--engine-commit", help="core commit of the engine, when not from fetch-engine")
    r.add_argument("--script-engine", choices=["quickjs", "bubblepop"], required=True)
    r.add_argument("--wpt", default="pinned", help="pinned (the WPT commit of core's last record), latest (the newest with a Chrome stable run on wpt.fyi) or a 40-hex commit")
    r.add_argument("--wpt-source", choices=["git", "tree"], default="git",
                   help="git (default): a depth-1 fetch of the whole WPT commit; tree: the tool's subset from GitHub's tarball")
    r.add_argument("--work", required=True, help="scratch directory (WPT checkout, Chrome's summary, raw results)")
    r.add_argument("--out", required=True, help="directory for the score, the record and the logs")
    r.add_argument("--seed", type=int, default=20261108)
    r.add_argument("--n", type=int, default=10, help="names drawn a stratum (the 2026-11-09 record used 25)")
    r.add_argument("--keep", type=int, default=3, help="largest names of a stratum that always run (the record used 5)")
    r.add_argument("--variants", choices=["window", "all"], default="all")
    r.add_argument("--dirs", help="comma list of top WPT directories: sample and count only these (a subset score, marked as one)")
    r.add_argument("--smoke", action="store_true", help=f"a small subset run: --dirs {SMOKE_DIRS} --n 3 --keep 1 --variants window, at most 15 minutes")
    r.add_argument("--jobs", type=int, default=3)
    r.add_argument("--stall", type=int, default=300)
    r.add_argument("--max-minutes", type=float, default=240, help="wall-clock limit of the test run")
    r.add_argument("--resume", action="store_true", help="keep the results of an earlier run in --work")
    r.add_argument("--fail-incomplete", action="store_true", help="exit 3 when the limit stopped the run")
    s = sub.add_parser("summarize", help="Markdown table and history lines from record-*.json files")
    s.add_argument("--records", nargs="+", required=True, help="directories with record-*.json")
    s.add_argument("--markdown", help="append the table to this file (the job summary)")
    s.add_argument("--history", help="append one JSON line a record to this file")
    a = ap.parse_args()
    {"fetch-engine": cmd_fetch_engine, "run": cmd_run, "summarize": cmd_summarize}[a.cmd](a)


if __name__ == "__main__":
    main()
