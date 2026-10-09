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
if [ -z "$REF" ]; then
  if git ls-remote --exit-code --heads "$CORE_URL" main >/dev/null 2>&1; then
    REF=main
  else
    REF=claude/core-split
  fi
fi
if [[ "$REF" =~ ^[0-9a-f]{40}$ ]]; then
  SHA="$REF"
else
  SHA="$(git ls-remote "$CORE_URL" "refs/heads/$REF" "refs/tags/$REF" | awk 'NR==1{print $1}')"
fi
[ -n "$SHA" ] || { echo "::error::cannot resolve $REF in $CORE_URL"; exit 1; }
SHORT="${SHA:0:12}"

# A commit is "already built" when its linux-x86_64 release exists.
EXISTS=false
if gh release view "build-$SHORT-linux-x86_64" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
  EXISTS=true
fi
PROCEED=true
case "$EVENT" in
  schedule) [ "$EXISTS" = true ] && PROCEED=false ;;
  workflow_dispatch) [ "$EXISTS" = true ] && [ "${FORCE:-false}" != true ] && PROCEED=false ;;
  push) PROCEED=true ;;   # a change to this repository's build scripts
esac
echo "core $REF = $SHA (releases exist: $EXISTS) -> proceed=$PROCEED"
{
  echo "ref=$REF"; echo "sha=$SHA"; echo "short=$SHORT"; echo "proceed=$PROCEED"
} >> "$GITHUB_OUTPUT"
