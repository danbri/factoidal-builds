#!/usr/bin/env bash
# Resolve which danbri/factoidal-core commit to build, and whether to build.
#
# Inputs (env): INPUT_REF (branch, tag or 40-hex commit; empty = default),
#   FORCE ("true" to rebuild a commit that already has releases),
#   EVENT (github.event_name), GH_TOKEN, GITHUB_OUTPUT, GITHUB_REPOSITORY.
# Default ref: `main` if core has it, else `claude/core-split` (the branch
# the 2026-10-09 split was pushed to; the owner renames it to main).
# Outputs: ref, sha, short (12 hex), proceed (true|false).
set -euo pipefail
CORE_URL="https://github.com/${CORE_REPO:-danbri/factoidal-core}"
REF="${INPUT_REF:-}"
# A push that changes requests/build.txt asks for a build of the core commit
# named on its first non-comment line (see requests/README.md). Scheduled runs
# have never started in this repository, and a push to core cannot start this
# workflow without a cross-repository token, so this file is how a core
# commit reaches a build.
REQUESTED=false
if [ -z "$REF" ] && [ "${EVENT:-}" = push ] && [ -f requests/build.txt ]; then
  CHANGED=""
  if [ -n "${PUSH_BEFORE:-}" ] && [ "${PUSH_BEFORE}" != 0000000000000000000000000000000000000000 ]; then
    CHANGED="$(gh api "repos/$GITHUB_REPOSITORY/compare/${PUSH_BEFORE}...${PUSH_AFTER}" \
               --jq '.files[].filename' 2>/dev/null || true)"
  fi
  if printf '%s\n' "$CHANGED" | grep -qx 'requests/build.txt'; then
    REQ="$(grep -vE '^[[:space:]]*(#|$)' requests/build.txt | head -n 1 | awk '{print $1}')"
    if [[ "$REQ" =~ ^[0-9a-f]{40}$ ]]; then
      REF="$REQ"; REQUESTED=true
    else
      echo "::error::requests/build.txt: first line is not a 40-hex core commit: '$REQ'"; exit 1
    fi
  fi
fi
if [ -z "$REF" ]; then
  # Exact match: `git ls-remote URL main` also matches refs/heads/claude/main.
  if git ls-remote "$CORE_URL" refs/heads/main | grep -q 'refs/heads/main$'; then
    REF=main
  else
    REF=claude/core-split
  fi
fi
if [[ "$REF" =~ ^[0-9a-f]{40}$ ]]; then
  SHA="$REF"
else
  SHA="$(git ls-remote "$CORE_URL" "refs/heads/$REF" "refs/tags/$REF" \
         | awk -v h="refs/heads/$REF" -v t="refs/tags/$REF" '$2==h||$2==t{print $1; exit}')"
fi
[ -n "$SHA" ] || { echo "::error::cannot resolve $REF in $CORE_URL"; exit 1; }
SHORT="${SHA:0:12}"

# A commit is "already built" only when EVERY set has a release
# (danbri/factoidal issue 1038, P1). Before, the linux-x86_64 release alone
# counted, so a commit whose web set failed (web-gates red) was never built
# again: 25 of 102 built core commits had no web set on 2026-10-26.
SETS="linux-x86_64 darwin-arm64 web"
HAVE=""; MISSING=""; NEWEST=""
for s in $SETS; do
  AT="$(gh release view "build-$SHORT-$s" --repo "$GITHUB_REPOSITORY" \
        --json publishedAt -q .publishedAt 2>/dev/null || true)"
  if [ -n "$AT" ]; then
    HAVE="$HAVE $s"
    [[ "$AT" > "$NEWEST" ]] && NEWEST="$AT"
  else
    MISSING="$MISSING $s"
  fi
done
EXISTS=false
[ -z "$MISSING" ] && EXISTS=true
# A scheduled run retries a partly built commit at most once per
# RETRY_HOURS (default 24), counted from its newest set release (a retry
# publishes the sets that pass again, so that time moves). A gate that
# fails every time therefore costs one build a day, not one an hour.
RETRY_DUE=true
if [ -n "$HAVE" ] && [ -n "$MISSING" ] && [ -n "$NEWEST" ]; then
  AGE_H=$(python3 -c 'import sys,datetime as d; t=d.datetime.strptime(sys.argv[1],"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=d.timezone.utc); print(int((d.datetime.now(d.timezone.utc)-t).total_seconds()//3600))' "$NEWEST")
  if [ "$AGE_H" -lt "${RETRY_HOURS:-24}" ]; then RETRY_DUE=false; fi
  echo "::warning::core $SHORT is partly built: has${HAVE}; missing${MISSING}; newest set release ${AGE_H} h old (retry after ${RETRY_HOURS:-24} h: due=$RETRY_DUE)"
fi
PROCEED=true
case "$EVENT" in
  schedule) { [ "$EXISTS" = true ] || [ "$RETRY_DUE" = false ]; } && PROCEED=false ;;
  workflow_dispatch) [ "$EXISTS" = true ] && [ "${FORCE:-false}" != true ] && PROCEED=false ;;
  push) PROCEED=true ;;   # a change to this repository's build scripts
esac
echo "core $REF = $SHA (requested by requests/build.txt: $REQUESTED; all sets released: $EXISTS; missing:${MISSING:- none}) -> proceed=$PROCEED"
{
  echo "ref=$REF"; echo "sha=$SHA"; echo "short=$SHORT"; echo "proceed=$PROCEED"
} >> "$GITHUB_OUTPUT"
