#!/usr/bin/env bash
# record-ci-metrics.sh RECORD_JSON: add one run's timing and cache record to the branch
# ci-metrics (runs.csv, runs/<run_id>.json), as release-tests records scores on wpt-scores.
# Retries on top of the current branch; creates the branch (orphan) the first time.
set -euo pipefail
REC=$1
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
for i in 1 2 3 4; do
  W=$(mktemp -d)/ci-metrics
  if git fetch -q origin ci-metrics 2>/dev/null; then
    git worktree add -q --detach "$W" FETCH_HEAD
  else
    git worktree add -q --detach "$W" HEAD
    git -C "$W" checkout -q --orphan ci-metrics-new
    git -C "$W" rm -rq . 2>/dev/null || true
    printf '%s\n' '# CI timing and cache records' '' 'One row per job of each build.yml run (runs.csv) and the full record (runs/<run_id>.json), written by the metrics job of build.yml (scripts/ci-metrics.py on main). Trend: `python3 scripts/ci-metrics.py trend --records <checkout of this branch>`.' > "$W/README.md"
  fi
  python3 scripts/ci-metrics.py record --file "$REC" --dir "$W"
  git -C "$W" add -A
  git -C "$W" commit -q -m "ci-metrics: run $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["run_id"])' "$REC")"
  if git -C "$W" push -q origin HEAD:refs/heads/ci-metrics; then exit 0; fi
  git worktree remove --force "$W"
  sleep $((i * 4))
done
echo "::warning::could not push the ci-metrics record after 4 attempts"
