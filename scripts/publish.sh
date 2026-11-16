#!/usr/bin/env bash
# Assemble each artifact set from the downloaded job artifacts, pack it,
# publish it as a release, and update latest/<set>.json.
#
# A set is published only when EVERY artifact it needs is present: a job
# uploads its artifact as its last step, after all its gates, so a missing
# artifact means a failed gate (or a cancelled job) and the set is skipped.
#
# build.yml calls this twice for one run, once per publish job (2026-11-16): `publish` with
# PUBLISH_SETS="linux-x86_64 web foafnaut-web" as soon as the Linux jobs are done, and
# `publish-macos` with PUBLISH_SETS="darwin-arm64 foafnaut-darwin-arm64" when the macOS jobs
# are done. Before, one job waited for every job, so the web release (and the Hub) waited
# hours for a macOS runner while every Linux gate was green. Each set still needs only its
# own artifacts, so the split changes when a set publishes, never whether.
#
# Env: SHA, SHORT, REF, FOAFNAUT, FOAFNAUT_WEB, PUBLISH_SETS (space-separated subset of the
# sets below; empty = all), GH_TOKEN, GITHUB_REPOSITORY, GITHUB_RUN_ID.
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
  # Lean only since 2026-11-15: automatic F* builds stopped, so no set carries F* products.
  [linux-x86_64]="lean-linux-x86_64/stage"
  [darwin-arm64]="lean-darwin-arm64/stage"
  [web]="lean-wasm/stage"
  [foafnaut-darwin-arm64]="foafnaut-darwin-arm64/stage"
  [foafnaut-web]="foafnaut-web/stage"
)
# Artifacts that must exist (a gate job passed) but carry no content.
declare -A REQUIRES=(
  [linux-x86_64]=""
  [darwin-arm64]=""
  [web]="web-gates"
  [foafnaut-darwin-arm64]=""
  [foafnaut-web]=""
)
declare -A TOOLS=(
  [linux-x86_64]="lean-linux-x86_64/meta/toolchains-lean-linux-x86_64.json"
  [darwin-arm64]="lean-darwin-arm64/meta/toolchains-lean-darwin-arm64.json"
  [web]="lean-linux-x86_64/meta/toolchains-lean-linux-x86_64.json lean-wasm/meta/toolchains-lean-wasm.json"
  [foafnaut-darwin-arm64]="foafnaut-darwin-arm64/meta/toolchains-foafnaut.json"
  [foafnaut-web]="foafnaut-web/meta/toolchains-foafnaut-web.json"
)

PUBLISHED=()
SKIPPED=()
KEPT=()
SETS="linux-x86_64 darwin-arm64 web"
if [ "${FOAFNAUT:-false}" = true ]; then SETS="$SETS foafnaut-darwin-arm64"; fi
if [ "${FOAFNAUT_WEB:-false}" = true ]; then SETS="$SETS foafnaut-web"; fi
if [ -n "${PUBLISH_SETS:-}" ]; then
  for s in $PUBLISH_SETS; do
    [ -n "${NEEDS[$s]+x}" ] || { echo "::error::PUBLISH_SETS names an unknown set: $s"; exit 1; }
  done
  KEEP=""
  for SET in $SETS; do
    case " $PUBLISH_SETS " in *" $SET "*) KEEP="$KEEP $SET" ;; esac
  done
  SETS="${KEEP# }"
  echo "this job publishes: ${SETS:-none} (PUBLISH_SETS: $PUBLISH_SETS)"
fi
for SET in $SETS; do
  MISSING=""
  for d in ${NEEDS[$SET]} ${REQUIRES[$SET]}; do
    [ -d "$ART/$d" ] || MISSING="$MISSING $d"
  done
  if [ -n "$MISSING" ]; then
    echo "::warning::$SET not published: missing artifacts:$MISSING (a gate failed or a job did not run)"
    SKIPPED+=("$SET")
    continue
  fi
  # The engine build's Lean hygiene ratchet (core labs/demos/foafnaut/LabHygiene.lean,
  # theorem lab_ratchet): no counts in the record, no foafnaut-web release.
  if [ "$SET" = foafnaut-web ] && ! python3 -c 'import json,sys; h=json.load(open(sys.argv[1])); assert h["theorem"] and h["counts"]["lab"]' "$ART/foafnaut-web/meta/hygiene.json" 2>/dev/null; then
    echo "::warning::foafnaut-web not published: the engine build record has no hygiene field (LabHygiene.lean did not run)"
    SKIPPED+=("$SET")
    continue
  fi
  # A published release is immutable: a later run of the same commit never deletes it or
  # replaces its assets. Consumers pin a release by tag and by the sha256 of its tarball
  # (@factoidal/core's version.json, Textnaut's foafnaut-web pin, fetch-builds.sh), and a
  # rebuild never has the same bytes: build-info.json carries the build time and run, and
  # the foafnaut-web runtime manifests name the run. 2026-11-15: a run that rebuilt
  # ff075ad5a for its missing macOS bundle replaced build-ff075ad5af99-foafnaut-web, and
  # Textnaut's pin no longer matched. Such a retry now publishes only the missing sets.
  # To replace a bad release, delete it by hand first (gh release delete TAG --cleanup-tag).
  if gh release view "build-$SHORT-$SET" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
    echo "::notice::$SET: release build-$SHORT-$SET exists and is kept as published (releases are never replaced)"
    KEPT+=("$SET")
    continue
  fi
  STAGE="$OUT/stage-$SET"
  mkdir -p "$STAGE"
  for d in ${NEEDS[$SET]}; do
    ( cd "$ART/$d" && tar -cf - . ) | ( cd "$STAGE" && tar -xpf - )
  done
  if [ "$SET" = foafnaut-web ]; then
    node scripts/finalize-svg-runtime.mjs \
      --runtime "$STAGE/docs/web/hub/svg-webgpu/runtime" \
      --source-commit "$SHA" \
      --build-run "${GITHUB_SERVER_URL:-https://github.com}/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
    if [ -d "$STAGE/docs/web/hub/html-webgpu/runtime" ]; then
      node scripts/finalize-html-runtime.mjs \
        --runtime "$STAGE/docs/web/hub/html-webgpu/runtime" \
        --source-commit "$SHA" \
        --build-run "${GITHUB_SERVER_URL:-https://github.com}/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
    fi
  fi
  TOOLARGS=()
  for t in ${TOOLS[$SET]}; do TOOLARGS+=("$ART/$t"); done
  HYGIENE_JSON=$([ "$SET" = foafnaut-web ] && echo "$ART/foafnaut-web/meta/hygiene.json" || true) \
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
  RUN_URL="${GITHUB_SERVER_URL:-https://github.com}/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
  INSTALL="Install with tools/fetch-builds.sh in a factoidal-core checkout."
  if [ "$SET" = foafnaut-darwin-arm64 ]; then
    INSTALL="Experimental macOS ARM64 demos: extract the archive and open 'foafnaut/Native Demos.command' or 'foafnaut/SVG Demo.command'. No Node, Deno or Lean installation required. Unsigned; GPU/window behavior needs a desktop session. CI checks CPU engines, packaging and native loading, not visual conformance."
  fi
  if [ "$SET" = foafnaut-web ]; then
    INSTALL="Experimental SVG and Lean HTML/CSS WebGPU browser runtimes. Install with tools/fetch-builds.sh --set foafnaut-web in factoidal-core. The page and fixtures are core source; this set carries only the same-run Lean/WASM runtime. Its evidence records source/build identity and tests, not SVG conformance or GPU correctness."
  fi
  # Native sets link GNU MP statically: its licence and source pointer go with them.
  case "$SET" in linux-x86_64|darwin-arm64|foafnaut-darwin-arm64) EXTRA+=("notices/GMP-NOTICE.txt");; esac
  gh release create "$TAG" --repo "$GITHUB_REPOSITORY" \
    --title "$SET build of factoidal-core ${SHORT}" \
    --notes "Built from https://github.com/${CORE_REPO:-danbri/factoidal-core}/commit/$SHA ($REF) by $RUN_URL. $INSTALL build-info.json lists the sha256 of every file." \
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

echo "published: ${PUBLISHED[*]:-none}; kept (already published): ${KEPT[*]:-none}; skipped: ${SKIPPED[*]:-none}"
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
    # The two publish jobs of a run, and runs of different commits, finish in any order, so a
    # pointer moves only forward: it is not written when it already names a newer main commit
    # (one that has this commit as an ancestor). Any other answer (older, diverged, unknown)
    # writes it, as before.
    WROTE=()
    for s in "${PUBLISHED[@]}"; do
      CUR=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("source_commit",""))' "$PTR/latest/$s.json" 2>/dev/null || true)
      if [[ "$CUR" =~ ^[0-9a-f]{40}$ ]] && [ "$CUR" != "$SHA" ] \
         && [ "$(gh api "repos/$CORE/compare/$SHA...$CUR" -q .status 2>/dev/null || echo unknown)" = ahead ]; then
        echo "::notice::latest/$s.json kept: it names ${CUR:0:12}, newer than $SHORT"
        continue
      fi
      cp "$OUT/latest-$s.json" "$PTR/latest/$s.json"
      WROTE+=("$s")
    done
    git -C "$PTR" add latest/
    if git -C "$PTR" diff --cached --quiet; then PUSHED=true; break; fi
    git -C "$PTR" commit -q -m "latest: ${WROTE[*]} -> factoidal-core $SHORT"
    if git -C "$PTR" push -q origin HEAD:main; then PUSHED=true; break; fi
    sleep $((i * 4))
  done
  $PUSHED || { echo "::error::could not push the latest/*.json pointers after 4 attempts"; exit 1; }
fi
# The run is red when any set was skipped, so a failed gate is visible.
[ ${#SKIPPED[@]} -eq 0 ]
