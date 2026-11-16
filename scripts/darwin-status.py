#!/usr/bin/env python3
"""The Mac release of core main: status, landing look-ahead and the decision to build.

Owner rule 2026-11-16: for all tangible progress there is always a Mac build of main done or
building. A Mac release is the release build-<12 hex>-foafnaut-darwin-arm64 of this repository
(what `foafnaut --latest` installs); build.yml makes it in its main lane (concurrency group
build-factoidal-main: one running run and the newest pending one; a pending run resolves main's
head when it starts). mac-release.yml runs this every 15 minutes:

  status   prints the status JSON (written to latest/darwin-status.json): main's head, the newest
           Mac release, how long main has been ahead of it, the main lane's runs.
  poll     status, then the decision: nothing to do (released, a lane run waiting or building
           head, or head's Mac build failed within RETRY_H), or dispatch build.yml with an empty
           core_ref; before a dispatch onto an idle lane, a bounded look-ahead for core PRs that
           are about to land (wait_for_landing). Writes the status JSON with the decision.

Landing soon (a cheap signal, read from the GitHub API):
  - an open core PR with the label `landing` (a landing agent sets it when it starts waiting on
    the merge gate and removes it when it merges or gives up: skills/ci-runner in core), or
  - an open core PR whose head commit has a build.yml run (run-name "core <40 hex>") that is
    still running with its `lean` job passed, or that passed within the last LANDING_GREEN_MIN.
The wait ends when no candidate is left (merged, closed, failed, label removed) or after WAIT_CAP
minutes. It is skipped when main has already been ahead of the Mac release for NO_WAIT_LAG_MIN
minutes, or when the previous wait of the same lag episode hit the cap (never twice in a row),
so the Mac release does not fall more than about two hours behind main. The wait runs here, on a
Linux runner, before build.yml is dispatched, so no macOS runner time is spent on it.

Env: GH_TOKEN, CORE_REPO (danbri/factoidal-core), BUILDS_REPO (GITHUB_REPOSITORY), WAIT_CAP
(30 min), NO_WAIT_LAG_MIN (90), RETRY_H (6), LANDING_GREEN_MIN (60), ALERT_LAG_MIN (120).
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time

CORE = os.environ.get("CORE_REPO", "danbri/factoidal-core")
BUILDS = os.environ.get("BUILDS_REPO") or os.environ.get("GITHUB_REPOSITORY") or "danbri/factoidal-builds"
TAG_RE = re.compile(r"^build-([0-9a-f]{12})-foafnaut-darwin-arm64$")
LANE_PREFIX = "core main (Mac release lane"
WAITING = ("queued", "pending", "waiting", "requested")


def env_num(name, default):
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return float(default)


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp()


def iso(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gh(path, raw=False):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"gh api {path}: {out.stderr.strip()[:300]}")
    return out.stdout if raw else json.loads(out.stdout)


# ---------- pure parts (tested in tests/test_darwin_status.py) ----------

def mac_releases(releases, n=8):
    """The n most recently published foafnaut-darwin-arm64 releases, newest first, each
    {tag, sha (40 hex from the notes, or ''), published_at, url}."""
    out = []
    for r in releases:
        if TAG_RE.match(r.get("tag_name", "")) and r.get("published_at"):
            m = re.search(r"/commit/([0-9a-f]{40})", r.get("body") or "")
            out.append({"tag": r["tag_name"], "sha": m.group(1) if m else "", "published_at": r["published_at"],
                        "url": r.get("html_url", "")})
    out.sort(key=lambda r: r["published_at"], reverse=True)
    return out[:n]


def newest_mac_release(cands, commit_date):
    """The Mac release of the newest main commit (not the last published: a build of an older
    commit can publish after a newer one). commit_date(sha) -> ISO time."""
    best, best_t = None, ""
    for r in cands:
        if not r["sha"]:
            continue
        t = commit_date(r["sha"])
        if t > best_t:
            best, best_t = dict(r, committed_at=t), t
    return best


def behind_since(head_sha, rel_sha, compare_commits):
    """When main first moved past the released commit: the committer time of the oldest commit
    on main's first-parent line after rel_sha (a merge's time is when the PR landed). The
    commits are those of the compare rel...main (any order). None when not behind."""
    if not rel_sha or head_sha == rel_sha:
        return None
    by = {c["sha"]: c for c in compare_commits}
    cur, oldest = head_sha, None
    while cur in by:
        oldest = by[cur]
        parents = oldest.get("parents") or []
        cur = parents[0]["sha"] if parents else None
    if oldest is None:
        return None
    return oldest["commit"]["committer"]["date"]


def decide(st, prev, now, retry_h=6, no_wait_lag_min=90):
    """What poll does next: ('none'|'dispatch'|'wait-then-dispatch', reason)."""
    if not st["behind"]:
        return "none", "the newest Mac release is main's head"
    lane = st["lane_runs"]
    if any(r["status"] in WAITING for r in lane):
        return "none", "a main-lane run is waiting; it builds main's head when it starts"
    building = [r for r in lane if r["status"] == "in_progress" and r.get("sha") == st["main"]["sha"]]
    if building:
        return "none", f"run {building[0]['id']} is building main's head"
    lf = st.get("last_failure")
    if lf and lf.get("sha") == st["main"]["sha"] and now - ts(lf["at"]) < retry_h * 3600:
        return "none", (f"the Mac build of main's head failed in run {lf['id']} at {lf['at']}; "
                        f"next try with a newer main, the nightly run, or after {retry_h:g} h")
    if any(r["status"] == "in_progress" for r in lane):
        return "dispatch", "a main-lane run builds an older main; queue the newest behind it"
    pw = (prev or {}).get("last_decision") or {}
    if pw.get("capped") and pw.get("behind_since") == st.get("behind_since"):
        return "dispatch", "the previous look-ahead of this lag hit the cap: no second wait"
    if st.get("lag_min", 0) >= no_wait_lag_min:
        return "dispatch", f"main has been ahead of the Mac release for {st['lag_min']} min: no wait"
    return "wait-then-dispatch", "lane idle"


def landing_candidates(prs, runs, now, green_min=60):
    """Open core PRs about to land: label `landing`, or a build.yml run of the PR head that is
    running past its lean job or passed within green_min minutes. runs: [{title,status,
    conclusion,updated_at,lean}] with lean = the lean job's conclusion or None."""
    by_sha = {}
    for r in runs:
        m = re.fullmatch(r"core ([0-9a-f]{40})( \+macOS)?", r.get("title", ""))
        if m:
            by_sha.setdefault(m.group(1), []).append(r)
    out = []
    for p in prs:
        labels = {l["name"] for l in p.get("labels", [])}
        why = None
        if "landing" in labels:
            why = "label landing"
        else:
            for r in by_sha.get(p["head"]["sha"], []):
                if r["status"] != "completed" and r.get("lean") == "success":
                    why = "merge gate running, lean passed"
                    break
                if (r["status"] == "completed" and r.get("conclusion") == "success"
                        and now - ts(r["updated_at"]) < green_min * 60):
                    why = "merge gate green"
                    break
        if why:
            out.append({"number": p["number"], "why": why})
    return out


# ---------- GitHub reads ----------

def resolved_sha(run_id):
    """The core commit a build.yml run resolved (its resolve job's log), or ''."""
    try:
        jobs = gh(f"repos/{BUILDS}/actions/runs/{run_id}/jobs?per_page=100")["jobs"]
        j = next((j for j in jobs if j["name"] == "resolve" and j["conclusion"] == "success"), None)
        if not j:
            return ""
        log = gh(f"repos/{BUILDS}/actions/jobs/{j['id']}/logs", raw=True)
        m = re.search(r"core \S+ = ([0-9a-f]{40})", log)
        return m.group(1) if m else ""
    except RuntimeError:
        return ""


def mac_jobs(run_id):
    jobs = gh(f"repos/{BUILDS}/actions/runs/{run_id}/jobs?per_page=100")["jobs"]
    return {j["name"]: (j["status"], j["conclusion"]) for j in jobs
            if j["name"].startswith(("lean-macos", "foafnaut", "publish-macos")) and "host-tests" not in j["name"]
            and "engines" not in j["name"]}


def build_runs(n=60):
    return gh(f"repos/{BUILDS}/actions/workflows/build.yml/runs?per_page={n}")["workflow_runs"]


def collect(now=None):
    now = now or time.time()
    head = gh(f"repos/{CORE}/commits/main")
    head_sha = head["sha"]
    rel = newest_mac_release(mac_releases(gh(f"repos/{BUILDS}/releases?per_page=100")),
                             lambda sha: gh(f"repos/{CORE}/commits/{sha}")["commit"]["committer"]["date"])
    since = None
    if rel and rel["sha"] != head_sha:
        cmp = gh(f"repos/{CORE}/compare/{rel['sha']}...{head_sha}?per_page=250")
        since = behind_since(head_sha, rel["sha"], cmp.get("commits", []))
        if since is None:  # not on the first-parent line (should not happen): use the head's time
            since = head["commit"]["committer"]["date"]
        since = max(since, rel["committed_at"])   # main cannot have moved past it before it existed
    behind = bool(rel is None or rel["sha"] != head_sha)
    runs = build_runs()
    lane, last_failure = [], None
    for r in runs:
        if not (r.get("display_title") or "").startswith(LANE_PREFIX):
            continue
        if r["status"] != "completed":
            sha = resolved_sha(r["id"]) if r["status"] == "in_progress" else ""
            lane.append({"id": r["id"], "status": r["status"], "url": r["html_url"], "created_at": r["created_at"],
                         "sha": sha, "mac_jobs": {k: v[0] for k, v in mac_jobs(r["id"]).items()} if sha else {}})
        elif last_failure is None and r["conclusion"] != "success" and now - ts(r["updated_at"]) < 24 * 3600:
            sha = resolved_sha(r["id"])
            if sha == head_sha:
                mj = mac_jobs(r["id"])
                if any(c not in ("success", "skipped", None) for _, c in mj.values()):
                    last_failure = {"id": r["id"], "sha": sha, "at": r["updated_at"], "url": r["html_url"]}
    st = {
        "schema": "darwin-status/1",
        "checked_at": iso(now),
        "main": {"sha": head_sha, "committed_at": head["commit"]["committer"]["date"]},
        "mac_release": rel,
        "behind": behind,
        "behind_since": since,
        "lag_min": int((now - ts(since)) // 60) if since else 0,
        "lane_runs": lane,
        "last_failure": last_failure,
    }
    return st


def open_prs():
    return gh(f"repos/{CORE}/pulls?state=open&per_page=50")


def gate_runs():
    out = []
    for r in build_runs(80):
        if not re.fullmatch(r"core [0-9a-f]{40}( \+macOS)?", r.get("display_title") or ""):
            continue
        lean = None
        if r["status"] != "completed":
            jobs = gh(f"repos/{BUILDS}/actions/runs/{r['id']}/jobs?per_page=100")["jobs"]
            lean = next((j["conclusion"] for j in jobs if j["name"].startswith("lean (")
                         or j["name"] == "lean"), None)
        out.append({"title": r["display_title"], "status": r["status"], "conclusion": r["conclusion"],
                    "updated_at": r["updated_at"], "lean": lean})
    return out


def wait_for_landing(cap_min, step_s=120):
    """Wait while core PRs are about to land, at most cap_min minutes. Returns (minutes, [PR numbers
    seen], capped)."""
    t0, seen = time.time(), []
    while True:
        cands = landing_candidates(open_prs(), gate_runs(), time.time(),
                                   env_num("LANDING_GREEN_MIN", 60))
        for c in cands:
            if c["number"] not in seen:
                seen.append(c["number"])
                print(f"landing soon: #{c['number']} ({c['why']})")
        waited = (time.time() - t0) / 60
        if not cands:
            return round(waited), seen, False
        if waited >= cap_min:
            return round(waited), seen, True
        time.sleep(step_s)


def summary_line(st, d):
    rel = st["mac_release"] or {}
    lag = f"{st['lag_min']} min behind main" if st["behind"] else "at main's head"
    return (f"Mac release {rel.get('tag', 'none')} is {lag} ({st['main']['sha'][:12]}); "
            f"decision: {d['action']} ({d['reason']})"
            + (f"; waited {d['waited_min']} min for {', '.join('#%d' % n for n in d['waited_for'])}"
               if d.get("waited_for") else ""))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    out = sys.argv[2] if len(sys.argv) > 2 else None
    prev = {}
    if out and os.path.exists(out):
        try:
            prev = json.load(open(out))
        except ValueError:
            prev = {}
    st = collect()
    if cmd == "poll":
        action, reason = decide(st, prev, time.time(), env_num("RETRY_H", 6), env_num("NO_WAIT_LAG_MIN", 90))
        d = {"at": iso(time.time()), "action": action, "reason": reason, "head": st["main"]["sha"],
             "behind_since": st["behind_since"], "waited_min": 0, "waited_for": [], "capped": False}
        if action == "wait-then-dispatch":
            w, seen, capped = wait_for_landing(env_num("WAIT_CAP", 30))
            d.update(waited_min=w, waited_for=seen, capped=capped,
                     reason=(f"waited {w} min for " + ", ".join(f"#{n}" for n in seen)
                             + (" (cap reached)" if capped else "")) if seen else "no PR about to land: at once")
            action = "dispatch"
        if action == "dispatch":
            subprocess.run(["gh", "workflow", "run", "build.yml", "--repo", BUILDS, "-f", "core_ref="],
                           check=True)
            d["action"] = "dispatched"
            time.sleep(20)
            st = collect()
        elif prev.get("last_decision") and prev["last_decision"].get("action") == "dispatched" \
                and prev["last_decision"].get("head") == st["main"]["sha"]:
            d = prev["last_decision"]   # keep the last dispatch on record while it is built
        st["last_decision"] = d
        line = summary_line(st, d)
        print(line)
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
                f.write(line + "\n")
        if st["behind"] and st["lag_min"] > env_num("ALERT_LAG_MIN", 120):
            print(f"::warning::Mac release is {st['lag_min']} min behind core main")
    elif prev.get("last_decision"):
        st["last_decision"] = prev["last_decision"]
    text = json.dumps(st, indent=1, sort_keys=True) + "\n"
    if out:
        with open(out, "w") as f:
            f.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
