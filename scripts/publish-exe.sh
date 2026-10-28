#!/usr/bin/env bash
# Publish the `exe` set (single-file executables, .github/workflows/exe.yml)
# of one core commit as release build-<SHORT>-exe, and update latest/exe.json.
#
# Env: SHA, SHORT, GH_TOKEN, GITHUB_REPOSITORY, GITHUB_RUN_ID.
# Layout read: art/stage/exe/{factoidal-*,SHA256SUMS}, art/meta/toolchains-exe.json.
set -euo pipefail

# Only commits on factoidal-core main are published, as in scripts/publish.sh.
CORE="${CORE_REPO:-danbri/factoidal-core}"
ON_MAIN=$(gh api "repos/$CORE/compare/main...$SHA" -q .status 2>/dev/null || echo unknown)
case "$ON_MAIN" in
  identical|behind) echo "core $SHA is on main ($ON_MAIN): publishing" ;;
  *) echo "core $SHA is not on core main (compare status: $ON_MAIN): checks only, nothing published"; exit 0 ;;
esac

OUT=release-out
mkdir -p "$OUT"
[ -f art/stage/exe/SHA256SUMS ] || { echo "::error::art/stage/exe/SHA256SUMS missing"; exit 1; }
( cd art/stage/exe && sha256sum -c SHA256SUMS )
python3 scripts/make-release.py art/stage exe "$SHA" main "$OUT/exe" art/meta/toolchains-exe.json

TAG="build-$SHORT-exe"
RUN_URL="${GITHUB_SERVER_URL:-https://github.com}/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
if gh release view "$TAG" --repo "$GITHUB_REPOSITORY" >/dev/null 2>&1; then
  echo "replacing existing release $TAG (forced rebuild)"
  gh release delete "$TAG" --repo "$GITHUB_REPOSITORY" --yes --cleanup-tag
fi
gh release create "$TAG" --repo "$GITHUB_REPOSITORY" \
  --title "Single-file executables of factoidal-core ${SHORT}" \
  --notes "The factoidal CLI as one file per platform (deno compile, the engine wasm included), built from https://github.com/$CORE/commit/$SHA by $RUN_URL. Download the file for your platform, check it against SHA256SUMS, make it executable (chmod +x on Linux and macOS) and run it: ./factoidal-<platform> --help. The files are not signed: macOS and Windows warn before the first run. EXPERIMENTAL UNREVIEWED CODE - USE WITH CARE - DO NOT CREATE PUBLIC SERVICES USING THIS WITHOUT CAREFUL INDEPENDENT EXPERT REVIEW." \
  "$OUT/exe/exe.tar.gz" "$OUT/exe/build-info.json" art/stage/exe/SHA256SUMS art/stage/exe/factoidal-*

python3 - "$TAG" "$SHA" "$RUN_URL" > "$OUT/latest-exe.json" <<'PY'
import datetime, json, sys
tag, sha, run = sys.argv[1:4]
print(json.dumps({'set': 'exe', 'tag': tag, 'source_commit': sha, 'source_ref': 'main',
                  'run_url': run,
                  'published_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
                 indent=1, sort_keys=True))
PY

# The pointer is derived data: write it on top of the current main in a
# separate worktree and push, as scripts/publish.sh does.
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
for i in 1 2 3 4; do
  PTR="$OUT/pointer-$i"
  git fetch -q origin main
  git worktree add -q --detach "$PTR" origin/main
  mkdir -p "$PTR/latest"
  cp "$OUT/latest-exe.json" "$PTR/latest/exe.json"
  git -C "$PTR" add latest/exe.json
  if git -C "$PTR" diff --cached --quiet; then exit 0; fi
  git -C "$PTR" commit -q -m "latest: exe -> factoidal-core $SHORT"
  if git -C "$PTR" push -q origin HEAD:main; then exit 0; fi
  sleep $((i * 4))
done
echo "::error::could not push latest/exe.json after 4 attempts"
exit 1
