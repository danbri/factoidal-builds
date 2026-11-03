#!/usr/bin/env bash
# Package only after portable CPU tests and checks of relocated executables.
# No GPU or WindowServer availability is inferred from these checks.
set -euo pipefail
CORE=$(cd "${1:?core checkout required}" && pwd)
OUT=${2:?output directory required}
mkdir -p "$OUT/stage" "$OUT/meta"
OUT=$(cd "$OUT" && pwd)
LAB="$CORE/labs/demos/foafnaut"
POLICY_CHECK="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/check-foafnaut-policy.py"
PACKAGE="$OUT/stage/foafnaut"
bash "$LAB/build-executables.sh" "$PACKAGE"
# A newer core packager includes a checksummed inventory with additional sources.
# Keep that inventory intact; add these files only for older core revisions.
for name in source-SHA256SUMS tool-versions.txt; do
  if [ ! -f "$PACKAGE/$name" ]; then cp "$LAB/.build/$name" "$PACKAGE/"; fi
done
# The HTML/CSS producer is a native Lean CLI, not a claim that a GPU window ran.
if [ -f "$LAB/build-web-render.sh" ]; then
  bash "$LAB/build-web-render.sh" --native
  cp "$LAB/.build/web-render/web-render-native" "$PACKAGE/lean-html-scene-darwin-arm64"
  cp "$LAB/.build/web-render/source-witness.json" "$PACKAGE/native-html-source-witness.json"
  mkdir -p "$PACKAGE/html-fixtures"
  cp "$LAB/web-render/fixtures/"*.html "$PACKAGE/html-fixtures/"
  if [ -f "$LAB/WebRenderRDF.lean" ]; then
    cp "$LAB/web-render/fixtures/graph.nt" "$PACKAGE/html-fixtures/"
  fi
  cat > "$PACKAGE/HTML_RENDERER.txt" <<'EOF'
Lean HTML/CSS scene producer for macOS ARM64

./lean-html-scene-darwin-arm64 html-fixtures/boxes.html 120 160
./lean-html-scene-darwin-arm64 html-fixtures/boxes.html 120 160 --pixels
./lean-html-scene-darwin-arm64 html-fixtures/graph.nt 380 340 --rdf

The first emits a checked scene artifact; --pixels emits CPU reference RGB JSON.
The RDF example is present when this source includes the N-Triples frontend.
This CLI needs no Lean, Node or Deno installation. It does not open a GPU window.
The separate public WebGPU viewer paints the same scene. Named CPU/relocation
checks do not establish complete HTML/CSS/SVG conformance or native GPU behavior.
EOF
  (cd "$PACKAGE" && shasum -a 256 lean-html-scene-darwin-arm64 native-html-source-witness.json HTML_RENDERER.txt html-fixtures/* >> SHA256SUMS)
fi


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
  if [ -x ./lean-html-scene-darwin-arm64 ]; then
    ./lean-html-scene-darwin-arm64 html-fixtures/boxes.html 120 160 > "$CHECK/html.json"
    if [ -f html-fixtures/graph.nt ]; then
      ./lean-html-scene-darwin-arm64 html-fixtures/graph.nt 380 340 --rdf > "$CHECK/rdf.json"
    fi
  fi
  if [ -f "$LAB/FoafNaut.lean" ]; then
    ./native-webgpu-ui-darwin-arm64 --demo foafnaut --emit-artifact "$CHECK/foaf.json"
  fi
  # Source capability detection preserves older lab packages. A capable source
  # cannot silently omit the exported report, storage artifact or web assets.
  if [ -f "$LAB/PolicyBridge.lean" ]; then
    ./native-webgpu-ui-darwin-arm64 --demo foafnaut --emit-svg "$CHECK/checked.svg"
    ./native-webgpu-svg-darwin-arm64 "$CHECK/checked.svg" --emit-artifact "$CHECK/checked-native.json"
    python3 "$POLICY_CHECK" "$CHECK"
    cp "$CHECK/checked.svg.policy.json" "$OUT/meta/foafnaut-policy.json"
  fi
  python3 - "$CHECK" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
names = ['still', 'svg'] + (['foaf'] if (root / 'foaf.json').exists() else [])
names += [name for name in ['html','rdf'] if (root / f'{name}.json').exists()]
for name in names:
    artifact = json.loads((root / f'{name}.json').read_text())
    assert artifact['width'] > 0 and artifact['height'] > 0, name
    assert artifact['wgsl'] and artifact['data'] and artifact['checks'], name
    if name == 'rdf': assert artifact['rdf'] == {'syntax':'N-Triples 1.1','triples':3}
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
