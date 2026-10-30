#!/usr/bin/env bash
# Package only after portable CPU tests and checks of relocated executables.
# No GPU or WindowServer availability is inferred from these checks.
set -euo pipefail
CORE=$(cd "${1:?core checkout required}" && pwd)
OUT=${2:?output directory required}
mkdir -p "$OUT/stage" "$OUT/meta"
OUT=$(cd "$OUT" && pwd)
LAB="$CORE/labs/demos/foafnaut"
PACKAGE="$OUT/stage/foafnaut"
bash "$LAB/build-executables.sh" "$PACKAGE"
cp "$LAB/.build/source-SHA256SUMS" "$LAB/.build/tool-versions.txt" "$PACKAGE/"

# A fresh location, with spaces, catches embedded development checkout paths.
CHECK=$(mktemp -d "${TMPDIR:-/tmp}/foafnaut relocation.XXXXXX")
trap 'rm -rf "$CHECK"' EXIT
cp -R "$PACKAGE/." "$CHECK/"
(
  cd "$CHECK"
  shasum -a 256 -c SHA256SUMS
  DEMOS=(springs layout vectors)
  if [ -f "$LAB/FoafNaut.lean" ]; then DEMOS+=(foafnaut); fi
  for demo in "${DEMOS[@]}"; do
    ./native-webgpu-ui-darwin-arm64 --demo "$demo" --check-engine
  done
  ./native-webgpu-ui-darwin-arm64 --diagnose
  ./native-webgpu-lean-darwin-arm64 --emit-artifact "$CHECK/still.json"
  ./native-webgpu-svg-darwin-arm64 svg-fixtures/gallery.svg --emit-artifact "$CHECK/svg.json"
  if [ -f "$LAB/FoafNaut.lean" ]; then
    ./native-webgpu-ui-darwin-arm64 --demo foafnaut --emit-artifact "$CHECK/foaf.json"
  fi
  python3 - "$CHECK" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
names = ['still', 'svg'] + (['foaf'] if (root / 'foaf.json').exists() else [])
for name in names:
    artifact = json.loads((root / f'{name}.json').read_text())
    assert artifact['width'] > 0 and artifact['height'] > 0, name
    assert artifact['wgsl'] and artifact['data'] and artifact['checks'], name
print('Relocated compiled engines and native library load passed; no GPU rendering claimed')
PY
) 2>&1 | tee "$OUT/meta/foafnaut-smoke.txt"
python3 - "$LAB" "$OUT/meta/toolchains-foafnaut.json" <<'PY'
import json, pathlib, subprocess, sys
lab, target = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
versions = dict(line.split('=', 1) for line in (lab / 'toolchain-versions.env').read_text().splitlines()
                if line and not line.startswith('#'))
target.write_text(json.dumps({
    'lean': (lab / '.build/tool-versions.txt').read_text().splitlines()[0],
    'deno': subprocess.check_output(['deno', '--version'], text=True).splitlines()[0],
    'emscripten': versions['EMSCRIPTEN_VERSION'],
    'clang': subprocess.check_output(['xcrun', 'clang', '--version'], text=True).splitlines()[0],
    'foafnaut_platform': 'darwin-arm64',
    'foafnaut_gpu_gate': 'not run: CPU/packaging/native-load gates only',
}, indent=2) + '\n')
PY
