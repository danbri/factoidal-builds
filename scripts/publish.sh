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
  python3 - "$SET" "$TAG" "$SHA" "$REF" "$RUN_URL" > "latest/$SET.json" <<'PY'
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
  git config user.name "github-actions[bot]"
  git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git add latest/*.json
  if ! git diff --cached --quiet; then
    git commit -q -m "latest: ${PUBLISHED[*]} -> factoidal-core $SHORT"
    for i in 1 2 3 4; do
      git push -q origin HEAD:main && break
      sleep $((i * 4)); git pull -q --rebase origin main
    done
  fi
fi
# The run is red when any set was skipped, so a failed gate is visible.
[ ${#SKIPPED[@]} -eq 0 ]
