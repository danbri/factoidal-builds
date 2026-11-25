#!/usr/bin/env bash
set -euo pipefail
: "${SITE:?}" "${CAPTURE:?}" "${BASELINE:?}" "${HARNESS_CORE:?}"
unset LD_LIBRARY_PATH REFTEST_TIME REFTEST_DUMP_DIR REALPAGES_RECORD
harness=$PWD/harness
out=$PWD/out
host=$PWD/host
runtime=$PWD/runtime
mkdir -p "$out" "$runtime"
python3 "$harness/inspect_inputs.py" "$harness/fixtures.json" "$SITE" "$CAPTURE" "$out"
python3 "$harness/materialize.py" "$HARNESS_CORE" "$harness/host.sha256" "$host"
cp "$harness/host.sha256" "$out/host-files.sha256"
lscpu > "$out/runner.txt"
deno --version > "$out/deno.txt"
lab="$host/labs/demos/foafnaut"
renderer="$host/tests/browser-wpt/reftest-render.ts"
geometry_pin=3a11210be57cce4452c9d67ef199ab08ff89458e8d267272b539fc589e370786
python3 "$harness/capture_geometry.py" "$renderer" "$geometry_pin"
sha256sum "$renderer" > "$out/instrumented-renderer.sha256"

tag="build-${HARNESS_CORE:0:12}-foafnaut-web"
web=foafnaut-web.tar.gz
gh release download "$tag" -R danbri/factoidal-builds -D "$runtime" -p build-info.json -p "$web"
expected=$(jq -er --arg sha "$HARNESS_CORE" --arg asset "$web" \
  'select(.source_commit == $sha) | .artifacts[$asset].sha256' "$runtime/build-info.json")
echo "$expected  $runtime/$web" | sha256sum -c -
cp "$runtime/build-info.json" "$out/web-build-info.json"
tar -xzf "$runtime/$web" -C "$runtime" docs/web/hub/html-webgpu/runtime
bash "$lab/realpages/setup-host.sh" "$lab" "$runtime"
deno check --no-config --no-npm "$renderer" "$lab/realpages/replay.ts"

roles=(baseline)
if [[ -n ${SUCCESSOR:-} ]]; then
  [[ $SUCCESSOR =~ ^[0-9a-f]{40}$ && $SUCCESSOR != "$BASELINE" ]]
  roles+=(successor)
fi
for role in "${roles[@]}"; do
  sha="$BASELINE"
  if [[ $role == successor ]]; then sha="$SUCCESSOR"; fi
  dir="$out/$role"
  pkg=foafnaut-browser-linux-x86_64
  lib=foafnaut-linux-x86_64/libweb-render.so
  if [[ $role == successor ]]; then
    pkg=foafnaut-linux-x86_64
    lib=foafnaut/libweb-render.so
  fi
  member="$lib"
  if [[ $role == successor ]]; then member="./$lib"; fi
  asset="$pkg.tar.gz"
  tag="build-${sha:0:12}-$pkg"
  mkdir -p "$dir"
  patterns=(-p build-info.json -p "$asset")
  if [[ $role == baseline ]]; then patterns+=(-p window-smoke.json); fi
  gh release download "$tag" -R danbri/factoidal-builds -D "$dir" "${patterns[@]}"
  expected=$(jq -er --arg sha "$sha" --arg asset "$asset" \
    'select(.source_commit == $sha) | .artifacts[$asset].sha256' "$dir/build-info.json")
  engine_sha=$(jq -er --arg asset "$asset" --arg lib "$lib" \
    '.artifacts[$asset].files[$lib].sha256' "$dir/build-info.json")
  if [[ $role == baseline ]]; then
    test "$expected" = 6a92d3bb9c6808e698b8cba0f66bf71b1a42e0c82fe9672ba0fbf291210b6db7
    jq -e --arg sha "$sha" --arg archive "$expected" --arg engine "$engine_sha" \
      '.sourceCommit == $sha and .archive_sha256 == $archive and .status == "pass" and
       .sdlDriver == "x11" and .firstFrame.engine.backend == "native" and
       .firstFrame.engine.sha256 == $engine' "$dir/window-smoke.json" >/dev/null
  else
    test "$expected" = cc4865ae7b661f0bd8df6690ed00cc2e745a015c9c85586d4c5c489c53d619c0
    jq -e --arg run "$EXPECTED_ENGINE_RUN" \
      '.run_url == $run and .library.self_contained == true' "$dir/build-info.json" >/dev/null
  fi
  echo "$expected  $dir/$asset" | sha256sum -c -
  jq -n --arg s "$sha" --arg a "$expected" --arg l "$engine_sha" --arg t "$tag" \
    '{source:$s, tar_sha256:$a, library_sha256:$l, tag:$t}' > "$dir/pin.json"
  tar -xOzf "$dir/$asset" "$member" > "$PWD/libweb-render.so"
  rm "$dir/$asset"
  echo "$engine_sha  $PWD/libweb-render.so" | sha256sum -c -
  REALPAGES_REPLAY="$CAPTURE" deno run --no-config --no-npm --unstable-ffi -A \
    --preload "$lab/realpages/replay.ts" "$renderer" --native-engine "$PWD/libweb-render.so" \
    --list "$out/jobs.jsonl" --out "$dir" 2>&1 | tee "$dir/run.log"
  awk '/^__done / {sub(/^__done /,""); print}' "$dir/run.log" | jq -es \
    'if length == 1 and .[0].status == "ok" then .[0] else error("expected one successful frame") end' \
    > "$dir/result.json"
  rm "$PWD/libweb-render.so"
done
/usr/bin/python3 "$harness/compare.py" "$SITE" "$out" "${roles[@]}"
python3 - "$out" <<'PYTHON'
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
role_summary = {}
for role in ("baseline", "successor"):
    result = json.loads((out / role / "result.json").read_text())
    messages = result.get("scriptErrors", [])
    assert result.get("scripted") is True, result
    role_summary[role] = {
        "uncaught_messages": messages,
        "missing_normalize": sum("normalize is not a function" in line for line in messages),
    }
summary = json.dumps(role_summary, indent=2)
(out / "script-errors.json").write_text(summary + "\n")
print(summary)
assert role_summary["baseline"]["missing_normalize"] == 2, role_summary
assert role_summary["successor"]["missing_normalize"] == 0, role_summary
PYTHON
