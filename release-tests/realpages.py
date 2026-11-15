#!/usr/bin/env python3
"""The real-page survey of each Foafnaut release (.github/workflows/realpages.yml).

  resolve   which releases to survey: the release a finished build run published, or a
            dispatched tag, or the newest of each platform. Writes the job matrix.
  previous  the summary to compare with: the newest survey of another release of that
            platform on the results branch (realpages/latest-<p>.json, else previous-<p>.json).
  record    append the trend rows and the summaries to the results branch (wpt-scores,
            directory realpages/), with a new worktree each attempt, and push.

The survey itself is core's labs/demos/foafnaut/realpages/survey.ts; the table and the
regressions are its compare.ts. Nothing here reads or stores page content: the results are
numbers, verdicts and defect lists.
"""
import argparse, csv, glob, io, json, os, re, subprocess, sys, time, urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "danbri/factoidal-builds")
RESULTS_BRANCH = os.environ.get("RESULTS_BRANCH", "wpt-scores")
DIR = "realpages"
# Release set -> survey platform. macOS: build.yml's full set (with the window library) or
# foafnaut-macos.yml's engine-only set; Linux: foafnaut-linux.yml's x86_64 library.
SETS = {"foafnaut-darwin-arm64": "macos", "foafnaut-engine-darwin-arm64": "macos", "foafnaut-linux-x86_64": "linux"}
RUNS_ON = {"macos": "macos-15", "linux": "ubuntu-latest"}
WORKFLOW_SETS = {"Build Factoidal from factoidal-core": ["foafnaut-darwin-arm64"],
                 "Foafnaut macOS engine": ["foafnaut-engine-darwin-arm64"],
                 "Foafnaut Linux engine": ["foafnaut-linux-x86_64"]}


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def gh_json(*args):
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out) if out.strip() else None


def releases():
    rows = []
    for page in range(1, 4):
        got = gh_json("api", f"repos/{REPO}/releases?per_page=100&page={page}")
        rows += got or []
        if not got or len(got) < 100:
            break
    return rows


def build_info(tag):
    out = subprocess.run(["gh", "release", "download", tag, "-R", REPO, "-p", "build-info.json", "-O", "-"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def set_of(tag):
    m = re.fullmatch(r"build-[0-9a-f]{12}-(.+)", tag or "")
    return m and m[1] in SETS and m[1]


def entry(tag, all_releases):
    info = build_info(tag)
    s = set_of(tag)
    p = SETS[s]
    if p == "linux" and not (info.get("library") or {}).get("self_contained"):
        log(f"{tag}: not a self-contained library (it needs the Lean toolchain); not surveyed")
        return None
    sha = info["source_commit"]
    tags = {r["tag_name"] for r in all_releases}
    web = f"build-{sha[:12]}-foafnaut-web"
    if web not in tags:
        webs = sorted((r for r in all_releases if re.fullmatch(r"build-[0-9a-f]{12}-foafnaut-web", r["tag_name"])),
                      key=lambda r: r["published_at"] or "")
        web = webs[-1]["tag_name"] if webs else ""
    return {"platform": p, "runs_on": RUNS_ON[p], "tag": tag, "set": s, "core_commit": sha, "web_tag": web}


def cmd_resolve(a):
    rel = [r for r in releases() if not r.get("draft")]
    tags = []
    if a.event == "workflow_run":
        # A run may end red and still publish a set whose own jobs passed (build.yml): the
        # release of that set made after the run started is the one it published.
        for s in WORKFLOW_SETS.get(a.workflow, []):
            mine = sorted((r for r in rel if set_of(r["tag_name"]) == s and (r["published_at"] or "") >= a.run_created),
                          key=lambda r: r["published_at"])
            if mine:
                tags.append(mine[-1]["tag_name"])
            else:
                log(f"run {a.workflow} ({a.conclusion}) published no {s} release")
    elif a.release:
        for t in a.release.split(","):
            if not set_of(t.strip()):
                sys.exit(f"::error::{t}: not a release of {', '.join(SETS)}")
            tags.append(t.strip())
    else:
        for p in a.platforms.split(","):
            cands = sorted((r for r in rel if SETS.get(set_of(r["tag_name"]) or "") == p.strip()), key=lambda r: r["published_at"] or "")
            for r in reversed(cands):
                e = entry(r["tag_name"], rel)
                if e:
                    tags.append(r["tag_name"])
                    break
    matrix = [e for e in (entry(t, rel) for t in tags) if e]
    out = {"include": matrix}
    log(json.dumps(out, indent=1))
    with open(a.github_output or os.devnull, "a") as f:
        f.write(f"matrix={json.dumps(out)}\n")
        f.write(f"any={'true' if matrix else 'false'}\n")


def raw(path):
    url = f"https://raw.githubusercontent.com/{REPO}/{RESULTS_BRANCH}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        log(f"{path}: {e}")
        return None


def cmd_previous(a):
    for name in (f"latest-{a.platform}.json", f"previous-{a.platform}.json"):
        s = raw(f"{DIR}/{name}")
        if s and s.get("release") != a.release:
            with open(a.out, "w") as f:
                json.dump(s, f)
            print(f"previous survey: {s.get('release')} ({name})")
            return
    print("no previous survey of another release")


def cmd_record(a):
    found = []
    for path in sorted(glob.glob(os.path.join(a.src, "**", "summary-*.json"), recursive=True)):
        p = re.fullmatch(r"summary-(\w+)\.json", os.path.basename(path))[1]
        trend = os.path.join(os.path.dirname(path), f"trend-{p}.csv")
        found.append((p, json.load(open(path)), open(trend).read().splitlines() if os.path.exists(trend) else []))
    if not found:
        log("nothing to record")
        return
    repo = os.path.abspath(a.repo)
    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    tmp = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), f"realpages-{os.getpid()}")
    for attempt in range(1, 6):
        tree = f"{tmp}-{attempt}-{time.time_ns()}"
        if subprocess.run(["git", "-C", repo, "fetch", "-q", "origin", f"+refs/heads/{RESULTS_BRANCH}:refs/remotes/origin/{RESULTS_BRANCH}"]).returncode:
            time.sleep(5 * attempt)
            continue
        subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "--detach", tree, f"refs/remotes/origin/{RESULTS_BRANCH}"], check=True)
        try:
            if record_in(tree, found, run_id, a.no_push):
                return
        finally:
            if not a.no_push:
                subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", tree])
        time.sleep(5 * attempt)
    sys.exit("could not push to the results branch after 5 attempts")


def record_in(tree, found, run_id, no_push):
    """Write the results into a worktree of the results branch and push; False when the push
    lost a race (the caller tries again on the new branch head)."""
    d = os.path.join(tree, DIR)
    os.makedirs(os.path.join(d, "runs", run_id), exist_ok=True)
    trend_path = os.path.join(d, "trend.csv")
    known = set()
    if os.path.exists(trend_path):
        known = {(r["run_id"], r["platform"]) for r in csv.DictReader(open(trend_path))}
    for p, summary, rows in found:
        with open(os.path.join(d, "runs", run_id, f"{p}.json"), "w") as f:
            json.dump(summary, f, indent=1)
        if rows and (run_id, p) not in known:
            header, body = rows[0], rows[1:]
            new = not os.path.exists(trend_path)
            with open(trend_path, "a") as f:
                if new:
                    f.write(header + "\n")
                f.write("\n".join(body) + "\n")
        latest = os.path.join(d, f"latest-{p}.json")
        if os.path.exists(latest):
            old = json.load(open(latest))
            if old.get("release") != summary.get("release"):
                os.replace(latest, os.path.join(d, f"previous-{p}.json"))
        with open(latest, "w") as f:
            json.dump(summary, f, indent=1)
    subprocess.run(["git", "-C", tree, "add", "-A"], check=True)
    if subprocess.run(["git", "-C", tree, "diff", "--cached", "--quiet"]).returncode == 0:
        log("nothing new on the branch")
        return True
    what = ", ".join(f"{p} {s.get('release')}" for p, s, _ in found)
    msg = f"realpages: {what} ({run_id})"
    subprocess.run(["git", "-C", tree, "-c", "user.name=github-actions[bot]", "-c",
                    "user.email=41898282+github-actions[bot]@users.noreply.github.com", "commit", "-q", "-m", msg], check=True)
    if no_push:
        log(f"committed, not pushed: {tree}")
        return True
    if subprocess.run(["git", "-C", tree, "push", "-q", "origin", f"HEAD:refs/heads/{RESULTS_BRANCH}"]).returncode == 0:
        log(f"pushed: {msg}")
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("resolve")
    r.add_argument("--event", required=True)
    r.add_argument("--workflow", default="")
    r.add_argument("--conclusion", default="")
    r.add_argument("--run-created", default="")
    r.add_argument("--release", default="")
    r.add_argument("--platforms", default="macos,linux")
    r.add_argument("--github-output", default=os.environ.get("GITHUB_OUTPUT"))
    p = sub.add_parser("previous")
    p.add_argument("--platform", required=True)
    p.add_argument("--release", required=True)
    p.add_argument("--out", required=True)
    c = sub.add_parser("record")
    c.add_argument("--src", required=True)
    c.add_argument("--repo", default=".")
    c.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    {"resolve": cmd_resolve, "previous": cmd_previous, "record": cmd_record}[a.cmd](a)


if __name__ == "__main__":
    main()
