#!/usr/bin/env bash
set -euo pipefail
: "${SITE:?}" "${CAPTURE:?}" "${BASELINE:?}"
unset LD_LIBRARY_PATH REFTEST_TIME REFTEST_DUMP_DIR REALPAGES_RECORD
harness=$PWD/harness
out=$PWD/out
host=$PWD/host
runtime=$PWD/runtime
mkdir -p "$out" "$runtime"
python3 "$harness/inspect_inputs.py" "$harness/fixtures.json" "$SITE" "$CAPTURE" "$out"
python3 "$harness/materialize.py" "$BASELINE" "$harness/host.sha256" "$host"
cp "$harness/host.sha256" "$out/host-files.sha256"
lscpu > "$out/runner.txt"
deno --version > "$out/deno.txt"
lab="$host/labs/demos/foafnaut"
renderer="$host/tests/browser-wpt/reftest-render.ts"
geometry_pin=3a11210be57cce4452c9d67ef199ab08ff89458e8d267272b539fc589e370786
python3 "$harness/capture_geometry.py" "$renderer" "$geometry_pin"
sha256sum "$renderer" > "$out/instrumented-renderer.sha256"

tag="build-${BASELINE:0:12}-foafnaut-web"
web=foafnaut-web.tar.gz
gh release download "$tag" -R danbri/factoidal-builds -D "$runtime" -p build-info.json -p "$web"
expected=$(jq -er --arg sha "$BASELINE" --arg asset "$web" \
  'select(.source_commit == $sha) | .artifacts[$asset].sha256' "$runtime/build-info.json")
echo "$expected  $runtime/$web" | sha256sum -c -
cp "$runtime/build-info.json" "$out/web-build-info.json"
tar -xzf "$runtime/$web" -C "$runtime" docs/web/hub/html-webgpu/runtime
bash "$lab/realpages/setup-host.sh" "$lab" "$runtime"
deno check --no-config --no-npm "$renderer" "$lab/realpages/replay.ts"

[[ $CANDIDATE =~ ^[0-9a-f]{40}$ && $CANDIDATE != "$BASELINE" ]]
roles=(baseline candidate)
for role in "${roles[@]}"; do
  sha="$BASELINE"
  dir="$out/$role"
  mkdir -p "$dir"
  if [[ $role == candidate ]]; then
    worker="$PWD/candidate-worker"
    test "$(cat "$worker/source-commit.txt")" = "$CANDIDATE"
    ( cd "$worker" && sha256sum -c SHA256SUMS )
    cp "$worker/source-commit.txt" "$worker/SHA256SUMS" candidate-artifact.json "$dir/"
    cp "$worker/libweb-render.so" "$PWD/libweb-render.so"
    engine_sha=$(sha256sum "$PWD/libweb-render.so" | cut -d ' ' -f1)
    jq -n --arg s "$CANDIDATE" --arg l "$engine_sha" --arg id "$WORKER_ARTIFACT" \
      '{source:$s, library_sha256:$l, actions_artifact_id:$id, kind:"build-worker"}' > "$dir/pin.json"
  else
    pkg=foafnaut-browser-linux-x86_64
    asset="$pkg.tar.gz"
    lib=foafnaut-linux-x86_64/libweb-render.so
    gh release download "build-${sha:0:12}-$pkg" -R danbri/factoidal-builds -D "$dir" \
      -p build-info.json -p window-smoke.json -p "$asset"
    expected=$(jq -er --arg sha "$sha" --arg asset "$asset" \
      'select(.source_commit == $sha) | .artifacts[$asset].sha256' "$dir/build-info.json")
    echo "$expected  $dir/$asset" | sha256sum -c -
    engine_sha=$(jq -er --arg asset "$asset" --arg lib "$lib" \
      '.artifacts[$asset].files[$lib].sha256' "$dir/build-info.json")
    jq -e --arg sha "$sha" --arg archive "$expected" --arg engine "$engine_sha" \
      '.sourceCommit == $sha and .archive_sha256 == $archive and .status == "pass" and
       .sdlDriver == "x11" and .presentedFrames > 0 and
       .firstFrame.engine.backend == "native" and .firstFrame.engine.sha256 == $engine' \
      "$dir/window-smoke.json" >/dev/null
    jq -n --arg s "$sha" --arg a "$expected" --arg l "$engine_sha" \
      '{source:$s, browser_tar_sha256:$a, library_sha256:$l}' > "$dir/pin.json"
    tar -xOzf "$dir/$asset" "$lib" > "$PWD/libweb-render.so"
    rm "$dir/$asset"
    echo "$engine_sha  $PWD/libweb-render.so" | sha256sum -c -
  fi
  REALPAGES_REPLAY="$CAPTURE" deno run --no-config --no-npm --unstable-ffi -A \
    --preload "$lab/realpages/replay.ts" "$renderer" --native-engine "$PWD/libweb-render.so" \
    --list "$out/jobs.jsonl" --out "$dir" 2>&1 | tee "$dir/run.log"
  awk '/^__done / {sub(/^__done /,""); print}' "$dir/run.log" | jq -es \
    'if length == 1 and .[0].status == "ok" then .[0] else error("expected one successful frame") end' \
    > "$dir/result.json"
  rm "$PWD/libweb-render.so"
done
/usr/bin/python3 "$harness/compare.py" "$SITE" "$out" "${roles[@]}"
