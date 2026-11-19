#!/usr/bin/env bash
# Assemble each artifact set from the downloaded job artifacts, pack it,
# publish it as a release, and update latest/<set>.json.
#
# A set is published only when EVERY artifact it needs is present: a job
# uploads its artifact as its last step, after all its gates, so a missing
# artifact means a failed gate (or a cancelled job) and the set is skipped.
#
# build.yml calls this from separate jobs for the Linux CLI and web sets, the
# Linux browser, and the macOS sets. The Linux browser arrives already packed
# so the release uses the exact archive that passed the relocated window check.
#
# Env: SHA, SHORT, REF, FOAFNAUT, FOAFNAUT_WEB, FOAFNAUT_LINUX_BROWSER,
# PUBLISH_SETS (space-separated subset; empty = all), GH_TOKEN, GITHUB_REPOSITORY, GITHUB_RUN_ID.
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
  [foafnaut-browser-linux-x86_64]="foafnaut-browser-linux-x86_64-candidate"
  [foafnaut-browser-linux-arm64]="foafnaut-browser-linux-arm64-candidate"
)
# Artifacts that must exist (a gate job passed) but carry no content.
declare -A REQUIRES=(
  [linux-x86_64]=""
  [darwin-arm64]=""
  [web]="web-gates"
  [foafnaut-darwin-arm64]=""
  [foafnaut-web]=""
  [foafnaut-browser-linux-x86_64]="foafnaut-browser-linux-x86_64-checked"
  [foafnaut-browser-linux-arm64]="foafnaut-browser-linux-arm64-checked"
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
if [ "${FOAFNAUT_LINUX_BROWSER:-false}" = true ]; then SETS="$SETS foafnaut-browser-linux-x86_64"; fi
if [ "${FOAFNAUT_LINUX_BROWSER_ARM64:-false}" = true ]; then SETS="$SETS foafnaut-browser-linux-arm64"; fi
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
  RUN_URL="${GITHUB_SERVER_URL:-https://github.com}/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
  if [[ "$SET" = foafnaut-browser-linux-* ]]; then
    CANDIDATE="$ART/${NEEDS[$SET]}"
    CHECKED="$ART/${REQUIRES[$SET]}/window-smoke.json"
    if ! python3 - "$CANDIDATE" "$CHECKED" "$SET" "$SHA" "$RUN_URL" <<'PY'
import hashlib, json, pathlib, sys

candidate, checked = map(pathlib.Path, sys.argv[1:3])
release_set, commit, run_url = sys.argv[3:]
archive = f'{release_set}.tar.gz'
build = json.loads((candidate / 'build-info.json').read_text())
smoke = json.loads(checked.read_text())
with (candidate / archive).open('rb') as stream:
    sha256 = hashlib.file_digest(stream, 'sha256').hexdigest()
files = build['artifacts'][archive]
arch = release_set.removeprefix('foafnaut-browser-linux-')
if (build['source_commit'] != commit or build['set'] != release_set or build['run_url'] != run_url
        or smoke['format'] != 'foafnaut-linux-window-smoke-v1' or smoke['status'] != 'pass'
        or smoke['sourceCommit'] != commit or smoke['archive_sha256'] != sha256
        or files['sha256'] != sha256
        or smoke['executableSha256'] != files['files'][f'foafnaut-linux-{arch}/foafnaut']['sha256']
        or (arch == 'arm64' and (smoke.get('runnerMachine') != 'aarch64' or smoke.get('worker') != 'wasm'))):
    sys.exit('Window smoke evidence does not match the browser archive and source commit')
PY
    then
      echo "::warning::$SET not published: missing or invalid window smoke evidence"
      SKIPPED+=("$SET")
      continue
    fi
    mkdir -p "$OUT/$SET"
    cp "$CANDIDATE/$SET.tar.gz" "$CANDIDATE/build-info.json" "$CHECKED" "$OUT/$SET/"
  else
    STAGE="$OUT/stage-$SET"
    mkdir -p "$STAGE"
    for d in ${NEEDS[$SET]}; do
      ( cd "$ART/$d" && tar -cf - . ) | ( cd "$STAGE" && tar -xpf - )
    done
    if [ "$SET" = foafnaut-web ]; then
      node scripts/finalize-svg-runtime.mjs \
        --runtime "$STAGE/docs/web/hub/svg-webgpu/runtime" \
        --source-commit "$SHA" --build-run "$RUN_URL"
      if [ -d "$STAGE/docs/web/hub/html-webgpu/runtime" ]; then
        node scripts/finalize-html-runtime.mjs \
          --runtime "$STAGE/docs/web/hub/html-webgpu/runtime" \
          --source-commit "$SHA" --build-run "$RUN_URL"
      fi
    fi
    TOOLARGS=()
    for t in ${TOOLS[$SET]}; do TOOLARGS+=("$ART/$t"); done
    HYGIENE_JSON=$([ "$SET" = foafnaut-web ] && echo "$ART/foafnaut-web/meta/hygiene.json" || true) \
      python3 scripts/make-release.py "$STAGE" "$SET" "$SHA" "$REF" "$OUT/$SET" "${TOOLARGS[@]}"
  fi

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
  INSTALL="Install with tools/fetch-builds.sh in a factoidal-core checkout."
  if [ "$SET" = foafnaut-darwin-arm64 ]; then
    INSTALL="Experimental macOS ARM64 demos: extract the archive and open 'foafnaut/Native Demos.command' or 'foafnaut/SVG Demo.command'. No Node, Deno or Lean installation required. Unsigned; GPU/window behavior needs a desktop session. CI checks CPU engines, packaging and native loading, not visual conformance."
  fi
  if [ "$SET" = foafnaut-web ]; then
    INSTALL="Experimental SVG and Lean HTML/CSS WebGPU browser runtimes. Install with tools/fetch-builds.sh --set foafnaut-web in factoidal-core. The page and fixtures are core source; this set carries only the same-run Lean/WASM runtime. Its evidence records source/build identity and tests, not SVG conformance or GPU correctness."
  fi
  if [[ "$SET" = foafnaut-browser-linux-* ]]; then
    ARCH=${SET#foafnaut-browser-linux-}
    INSTALL="Linux $ARCH browser built and tested on Ubuntu 24.04. Extract the archive and run foafnaut-linux-$ARCH/foafnaut. The executable includes Deno and Lean WASM. See the bundled README for desktop dependencies. The extracted archive passed the native X11 window smoke on Xvfb using Mesa software Vulkan."
    EXTRA+=("$OUT/$SET/window-smoke.json")
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
    # The publish jobs of a run, and runs of different commits, finish in any order, so a
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
