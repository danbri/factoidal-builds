#!/usr/bin/env bash
# Assemble each artifact set from the downloaded job artifacts, pack it,
# publish it as a release, and update latest/<set>.json.
#
# A set is published only when EVERY artifact it needs is present: a job
# uploads its artifact as its last step, after all its gates, so a missing
# artifact means a failed gate (or a cancelled job) and the set is skipped.
#
# Env: SHA, SHORT, REF, GH_TOKEN, GITHUB_REPOSITORY, GITHUB_RUN_ID.
# Layout read: art/<artifact>/{stage,stage-native,stage-web,meta}/...
set -euo pipefail

# Only commits on factoidal-core main are published (owner, 2026-10-25:
# "only main moves factoidal-builds, releases and npm"). A build of a PR head
# runs every gate job and stops here: no release, no latest/*.json pointer.
# The GitHub compare API gives "identical" or "behind" when SHA is main's head
# or an ancestor of it.
CORE="${CORE_REPO:-danbri/factoidal-core}"
ON_MAIN=$(gh api "repos/$CORE/compare/main...$SHA" -q .status 2>/dev/null || echo unknown)
case "$ON_MAIN" in
  identical|behind) echo "core $SHA is on main ($ON_MAIN): publishing" ;;
  *) echo "core $SHA is not on core main (compare status: $ON_MAIN): gates only, nothing published"; exit 0 ;;
esac

ART=art
OUT=release-out
mkdir -p "$OUT" latest

declare -A NEEDS=(
  [linux-x86_64]="fstar-linux-x86_64/stage-native lean-linux-x86_64/stage"
  [darwin-arm64]="fstar-darwin-arm64/stage-native lean-darwin-arm64/stage"
  [web]="fstar-linux-x86_64/stage-web lean-wasm/stage"
)
# Artifacts that must exist (a gate job passed) but carry no content.
declare -A REQUIRES=(
  [linux-x86_64]=""
  [darwin-arm64]=""
  [web]="web-gates"
)
declare -A TOOLS=(
  [linux-x86_64]="fstar-linux-x86_64/meta/toolchains-fstar-linux-x86_64.json lean-linux-x86_64/meta/toolchains-lean-linux-x86_64.json"
  [darwin-arm64]="fstar-darwin-arm64/meta/toolchains-fstar-darwin-arm64.json lean-darwin-arm64/meta/toolchains-lean-darwin-arm64.json"
  [web]="fstar-linux-x86_64/meta/toolchains-fstar-linux-x86_64.json lean-linux-x86_64/meta/toolchains-lean-linux-x86_64.json lean-wasm/meta/toolchains-lean-wasm.json"
)

PUBLISHED=()
SKIPPED=()
for SET in linux-x86_64 darwin-arm64 web; do
  MISSING=""
  for d in ${NEEDS[$SET]} ${REQUIRES[$SET]}; do
    [ -d "$ART/$d" ] || MISSING="$MISSING $d"
  done
  if [ -n "$MISSING" ]; then
    echo "::warning::$SET not published: missing artifacts:$MISSING (a gate failed or a job did not run)"
    SKIPPED+=("$SET")
    continue
  fi
  # A web release that a published npm version names is never replaced
  # (danbri/factoidal issue 1038, P7): its version.json names this tag and
  # its run, and a consumer checks the wasm against them. A forced rebuild
  # of such a commit keeps the old web release; the run is red so the
  # refusal is seen. Exit 2 of the check (registry not readable) refuses too.
  if [ "$SET" = web ] && gh release view "build-$SHORT-web" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
    NAMED_RC=0
    python3 scripts/npm-names-release.py "build-$SHORT-web" "$SHA" || NAMED_RC=$?
    if [ "$NAMED_RC" -ne 1 ]; then
      echo "::error::web not replaced: build-$SHORT-web exists and an npm version names it (or the registry could not be read; check exit $NAMED_RC). The existing release is kept."
      SKIPPED+=("$SET")
      continue
    fi
  fi
  STAGE="$OUT/stage-$SET"
  mkdir -p "$STAGE"
  for d in ${NEEDS[$SET]}; do
    ( cd "$ART/$d" && tar -cf - . ) | ( cd "$STAGE" && tar -xpf - )
  done
  TOOLARGS=()
  for t in ${TOOLS[$SET]}; do TOOLARGS+=("$ART/$t"); done
  python3 scripts/make-release.py "$STAGE" "$SET" "$SHA" "$REF" "$OUT/$SET" "${TOOLARGS[@]}"

  TAG="build-$SHORT-$SET"
  EXTRA=()
  if [ "$SET" = web ] && [ -f "$ART/lean-linux-x86_64/meta/lean-scoreboard.json" ]; then
    cp "$ART/lean-linux-x86_64/meta/lean-scoreboard.json" "$OUT/$SET/"
    EXTRA+=("$OUT/$SET/lean-scoreboard.json")
  fi
  if [ "$SET" = web ] && [ -f "$ART/lean-linux-x86_64/meta/lean-scoreboard.txt" ]; then
    cp "$ART/lean-linux-x86_64/meta/lean-scoreboard.txt" "$OUT/$SET/"
    EXTRA+=("$OUT/$SET/lean-scoreboard.txt")
  fi
  if [ "$SET" = web ] && [ -f "$ART/web-gates/engine-compare.txt" ]; then
    cp "$ART/web-gates/engine-compare.txt" "$OUT/$SET/"
    EXTRA+=("$OUT/$SET/engine-compare.txt")
  fi
  if [ "$SET" = web ] && [ -f "$ART/web-gates/known-defects.txt" ]; then
    cp "$ART/web-gates/known-defects.txt" "$OUT/$SET/"
    EXTRA+=("$OUT/$SET/known-defects.txt")
  fi
  if [ "$SET" = web ] && [ -f "$ART/web-gates/l4diff.txt" ]; then
    cp "$ART/web-gates/l4diff.txt" "$OUT/$SET/"
    EXTRA+=("$OUT/$SET/l4diff.txt")
  fi
  if gh release view "$TAG" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
    echo "replacing existing release $TAG (forced rebuild)"
    gh release delete "$TAG" --repo "$GITHUB_REPOSITORY" --yes --cleanup-tag
  fi
  RUN_URL="${GITHUB_SERVER_URL:-https://github.com}/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
  gh release create "$TAG" --repo "$GITHUB_REPOSITORY" \
    --title "$SET build of factoidal-core ${SHORT}" \
    --notes "Built from https://github.com/${CORE_REPO:-danbri/factoidal-core}/commit/$SHA ($REF) by $RUN_URL. Install with tools/fetch-builds.sh in a factoidal-core checkout; build-info.json lists the sha256 of every file." \
    "$OUT/$SET/$SET.tar.gz" "$OUT/$SET/build-info.json" "${EXTRA[@]}"
  python3 - "$SET" "$TAG" "$SHA" "$REF" "$RUN_URL" > "$OUT/latest-$SET.json" <<'PY'
import datetime, json, sys
s, tag, sha, ref, run = sys.argv[1:6]
print(json.dumps({'set': s, 'tag': tag, 'source_commit': sha, 'source_ref': ref,
                  'run_url': run,
                  'published_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
                 indent=1, sort_keys=True))
PY
  PUBLISHED+=("$SET")
done

echo "published: ${PUBLISHED[*]:-none}; skipped: ${SKIPPED[*]:-none}"
if [ ${#PUBLISHED[@]} -gt 0 ]; then
  # The pointers are derived data, so each attempt writes them on top of the
  # CURRENT main in a separate worktree and pushes; nothing is rebased. (Run
  # 25 failed here: its checkout predated another run's pointer commit and
  # the rebase conflicted on latest/*.json, although every release was
  # published.) The job's own checkout is not reset: bash is still reading
  # this script from it.
  git config user.name "github-actions[bot]"
  git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
  PUSHED=false
  for i in 1 2 3 4; do
    PTR="$OUT/pointer-$i"
    git fetch -q origin main
    git worktree add -q --detach "$PTR" origin/main
    mkdir -p "$PTR/latest"
    for s in "${PUBLISHED[@]}"; do cp "$OUT/latest-$s.json" "$PTR/latest/$s.json"; done
    git -C "$PTR" add latest/*.json
    if git -C "$PTR" diff --cached --quiet; then PUSHED=true; break; fi
    git -C "$PTR" commit -q -m "latest: ${PUBLISHED[*]} -> factoidal-core $SHORT"
    if git -C "$PTR" push -q origin HEAD:main; then PUSHED=true; break; fi
    sleep $((i * 4))
  done
  $PUSHED || { echo "::error::could not push the latest/*.json pointers after 4 attempts"; exit 1; }
fi
# The run is red when any set was skipped, so a failed gate is visible.
[ ${#SKIPPED[@]} -eq 0 ]
