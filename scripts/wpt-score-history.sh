#!/usr/bin/env bash
# Append the records of one WPT score run to history.jsonl on the branch
# `wpt-scores` of this repository, and push it.
#
# Usage: scripts/wpt-score-history.sh <directory with record-*.json> [--no-push]
#   Run from a checkout of this repository. --no-push makes the commit in a
#   worktree and prints its path (for a local test).
# Env: WPT_SCORES_BRANCH (default wpt-scores), WPT_SCORES_REMOTE (default origin).
#
# The branch holds history.jsonl (one JSON line a run: date, WPT commit, page
# script engine, engine commit, estimate, 95% range, denominator, sample) and
# README.md. The whole score files stay in the workflow artifacts. Each attempt
# writes on top of the CURRENT branch in a new worktree and pushes; nothing is
# rebased (the same method as the latest/*.json pointers in publish.sh). The
# push needs `contents: write` for the workflow token and no other secret.
set -euo pipefail
RECORDS=$(cd "${1:?directory with record-*.json required}" && pwd)
PUSH=true
if [ "${2:-}" = --no-push ]; then PUSH=false; fi
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BRANCH=${WPT_SCORES_BRANCH:-wpt-scores}
REMOTE=${WPT_SCORES_REMOTE:-origin}
TMP=$(mktemp -d "${TMPDIR:-/tmp}/wpt-scores.XXXXXX")

DONE=false
for i in 1 2 3 4; do
  TREE="$TMP/tree-$i"
  FETCH_RC=0
  timeout 300 git fetch -q "$REMOTE" "+refs/heads/$BRANCH:refs/remotes/$REMOTE/$BRANCH" 2> "$TMP/fetch-$i.err" || FETCH_RC=$?
  if [ "$FETCH_RC" -eq 0 ]; then
    git worktree add -q --detach "$TREE" "refs/remotes/$REMOTE/$BRANCH"
  else
    # The fetch fails for two reasons: the branch does not exist yet, or the remote
    # did not answer. Only the first one may start a new history.
    LS_RC=0
    timeout 120 git ls-remote --exit-code --heads "$REMOTE" "$BRANCH" > /dev/null 2>&1 || LS_RC=$?
    if [ "$LS_RC" -ne 2 ]; then
      echo "wpt-score-history: cannot fetch $BRANCH (fetch exit $FETCH_RC, ls-remote exit $LS_RC):" >&2
      cat "$TMP/fetch-$i.err" >&2
      sleep $((i * 4)); continue
    fi
    echo "wpt-score-history: $REMOTE has no branch $BRANCH; starting it"
    git worktree add -q --detach "$TREE" HEAD
    git -C "$TREE" checkout -q --orphan "$BRANCH-new-$i"
    git -C "$TREE" rm -rq --cached .
    git -C "$TREE" clean -fdxq
    cat > "$TREE/README.md" <<'EOF'
# wpt-scores

`history.jsonl`: one line for each run of `.github/workflows/wpt-score.yml`
(the Web Platform Tests score of the Foafnaut engine), written by
`scripts/wpt-score-history.sh` on `main`. Fields: `measuredAt`, `wpt`
(`pinned`: the WPT commit of factoidal-core's last record; `latest`: the newest
WPT commit with a Chrome stable run on wpt.fyi), `wptCommit`, `scriptEngine`,
`engine`, `engineCoreCommit`, `estimate`, `range95`, `measured`, `denominator`
(Chrome's subtests on wpt.fyi at that WPT commit), `sample`, `runUrl`. The whole
score files are artifacts of the run at `runUrl`.
EOF
  fi
  python3 "$HERE/wpt-score-job.py" summarize --records "$RECORDS" --history "$TREE/history.jsonl"
  git -C "$TREE" add README.md history.jsonl
  if git -C "$TREE" diff --cached --quiet; then DONE=true; echo "wpt-score-history: nothing new"; break; fi
  git -C "$TREE" -c user.name="github-actions[bot]" -c user.email="41898282+github-actions[bot]@users.noreply.github.com" \
    commit -q -m "wpt-scores: $(date -u +%Y-%m-%d) $(ls "$RECORDS" | grep -c '^record-.*\.json$') records"
  if [ "$PUSH" = false ]; then
    DONE=true; echo "wpt-score-history: commit made, not pushed: $TREE"; break
  fi
  PUSH_RC=0
  timeout 300 git -C "$TREE" push -q "$REMOTE" "HEAD:refs/heads/$BRANCH" || PUSH_RC=$?
  if [ "$PUSH_RC" -eq 0 ]; then DONE=true; break; fi
  echo "wpt-score-history: push attempt $i failed with exit $PUSH_RC" >&2
  sleep $((i * 4))
done
if [ "$DONE" != true ]; then
  echo "::error::could not record the WPT scores on $BRANCH after 4 attempts"; exit 1
fi
