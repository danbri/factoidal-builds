#!/usr/bin/env python3
"""Choose where a macOS job runs: the owner's Mac (self-hosted, overnight) or GitHub's macos-15.

GitHub cannot fall back from one runner label to another once a job is queued, so the
choice is made before the job starts, in a resolve job, from the repository variable
MAC_RUNNER. The Mac publishes that variable every few minutes while its runner is up
(scripts/mac-runner/tick.sh):

    {"seen": <epoch s>, "until": <epoch s the overnight window ends, 0 when off>, "free_gib": <n>}

The Mac's runner is chosen only when all of these hold, else macos-15:
  - the repository is danbri/factoidal-builds and the event is workflow_dispatch or schedule
    (never pull_request: a fork's code must not reach the Mac; the runner's job-started
    hook refuses such jobs as well);
  - the heartbeat is fresh (seen within STALE_S, default 20 min);
  - the window has at least LEAD_H hours left (a heavy job must finish before 07:00);
  - the Mac reported at least NEED_GIB free (the job's own need plus the 4 GiB floor).
MODE (a dispatch input): auto (default), github (always macos-15) or self-hosted (always
the Mac, still only for dispatch/schedule in this repository; the job waits for the Mac).

Writes runs_on=<JSON for runs-on> and reason=<text> to $GITHUB_OUTPUT when set, and
prints both.
"""
import json
import os
import sys
import time

HOSTED = "macos-15"
SELF = ["self-hosted", "macOS", "ARM64", "foafnaut-mac"]
REPO = "danbri/factoidal-builds"


def choose(var, event, repo, need_gib, lead_h, mode="auto", now=None, stale_s=1200):
    now = int(time.time()) if now is None else now
    mode = (mode or "auto").strip()
    if mode == "github":
        return HOSTED, "input mac_runner=github"
    if repo != REPO:
        return HOSTED, f"repository {repo} is not {REPO}"
    if event not in ("workflow_dispatch", "schedule"):
        return HOSTED, f"event {event}: the Mac takes only workflow_dispatch and schedule"
    if mode == "self-hosted":
        return SELF, "input mac_runner=self-hosted (waits for the Mac's runner)"
    try:
        st = json.loads(var) if var else {}
        if not isinstance(st, dict):
            st = {}
    except ValueError:
        st = {}
    try:
        seen = int(st.get("seen", 0))
        until = int(st.get("until", 0))
        free = float(st.get("free_gib", 0))
    except (TypeError, ValueError):
        return HOSTED, "MAC_RUNNER is malformed"
    if seen <= 0 or now - seen > stale_s:
        return HOSTED, f"Mac runner heartbeat stale or absent (seen {seen}, now {now})"
    if until - now < lead_h * 3600:
        return HOSTED, f"Mac runner off or its window ends within {lead_h} h"
    if free < need_gib:
        return HOSTED, f"Mac has {free:g} GiB free, this job needs {need_gib:g}"
    return SELF, f"Mac runner online until {until}, {free:g} GiB free"


def main():
    runs_on, reason = choose(
        os.environ.get("MAC_RUNNER", ""),
        os.environ.get("EVENT", ""),
        os.environ.get("REPO", ""),
        float(os.environ.get("NEED_GIB", "12")),
        float(os.environ.get("LEAD_H", "3")),
        os.environ.get("MODE", "auto"),
    )
    js = json.dumps(runs_on)
    print(f"macOS jobs run on {js}: {reason}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"runs_on={js}\nreason={reason}\n")


if __name__ == "__main__":
    sys.exit(main())
