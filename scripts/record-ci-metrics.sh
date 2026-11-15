#!/usr/bin/env bash
# record-ci-metrics.sh RECORD_JSON: add one run's timing and cache record to the branch
# ci-metrics (runs.csv, runs/<run_id>.json, README.md), as release-tests records scores on
# wpt-scores. Commits with a private index (no worktree, nothing else from this checkout),
# retries on top of the current branch, and creates the branch the first time.
set -euo pipefail
REC=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
RUN=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["run_id"])' "$REC")
export GIT_AUTHOR_NAME="github-actions[bot]" GIT_AUTHOR_EMAIL="41898282+github-actions[bot]@users.noreply.github.com"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME" GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
for i in 1 2 3 4; do
  W=$(mktemp -d)
  export GIT_INDEX_FILE="$W/index"
  PARENT=()
  if git fetch -q origin ci-metrics 2>/dev/null; then
    P=$(git rev-parse FETCH_HEAD); PARENT=(-p "$P")
    git read-tree "$P"
    git show "$P:runs.csv" > "$W/runs.csv" 2>/dev/null || true
  else
    git read-tree --empty
    printf '%s\n' '# CI timing and cache records' '' \
      'One row per job of each `build.yml` run in `runs.csv`, and the full record in `runs/<run_id>.json`,' \
      'written by the `metrics` job (`scripts/ci-metrics.py` on `main`). A trend of the last runs:' \
      '`python3 scripts/ci-metrics.py trend --n 10 --records <checkout of this branch>`.' > "$W/README.md"
    git update-index --add --cacheinfo "100644,$(git hash-object -w "$W/README.md"),README.md"
  fi
  python3 "$HERE/ci-metrics.py" record --file "$REC" --dir "$W"
  git update-index --add --cacheinfo "100644,$(git hash-object -w "$W/runs.csv"),runs.csv"
  git update-index --add --cacheinfo "100644,$(git hash-object -w "$W/runs/$RUN.json"),runs/$RUN.json"
  C=$(git commit-tree "$(git write-tree)" ${PARENT[@]+"${PARENT[@]}"} -m "ci-metrics: run $RUN")
  unset GIT_INDEX_FILE
  if git push -q origin "$C:refs/heads/ci-metrics"; then echo "recorded run $RUN on ci-metrics ($C)"; exit 0; fi
  sleep $((i * 4))
done
echo "::warning::could not push the ci-metrics record after 4 attempts"
