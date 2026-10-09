#!/usr/bin/env bash
# Compile and run the KaRaMeL C delta-log demo from factoidal-core's
# committed C (formal/fstar/c-output/deltalog/). Same compile and link
# lines as core's tools/karamel-c-build.sh steps after the krml lowering;
# the krml headers and krmllib come from the toolchain-cache branch.
# Usage: build-deltalog-demo.sh CORE_DIR BUILDS_DIR
set -euo pipefail
CORE="$(cd "$1" && pwd)"; BUILDS="$(cd "$2" && pwd)"
KRML_HOME="${KRML_HOME:-$HOME/karamel}"
if [ ! -d "$KRML_HOME/include/krml" ]; then
  mkdir -p "$KRML_HOME"
  git -C "$BUILDS" fetch -q origin toolchain-cache
  T=$(git -C "$BUILDS" ls-tree --name-only origin/toolchain-cache | grep '^krml-.*-linux-x86_64\.tar\.gz$' | head -1)
  git -C "$BUILDS" show "origin/toolchain-cache:$T" | tar -xz -C "$KRML_HOME"
fi
cd "$CORE/formal/fstar"
DL_DIR=c-output/deltalog
DL_OV="$DL_DIR/compat-override"
DL_CFLAGS=(-I "$DL_OV" -I "$KRML_HOME/include" -I "$KRML_HOME/krmllib/dist/minimal" -I "$DL_DIR")
gcc -c "${DL_CFLAGS[@]}" "$DL_DIR/Factoidal_DeltaLog.c" -o "$DL_DIR/Factoidal_DeltaLog.o"
gcc -c "${DL_CFLAGS[@]}" "$DL_DIR/krmlinit.c" -o "$DL_DIR/krmlinit.o"
gcc -c "${DL_CFLAGS[@]}" "$DL_OV/prims64.c" -o "$DL_DIR/prims64.o"
for f in fstar_char fstar_string fstar_uint32; do
  gcc -c "${DL_CFLAGS[@]}" -I "$KRML_HOME/krmllib/dist/generic" \
    "$KRML_HOME/krmllib/dist/generic/$f.c" -o "$DL_DIR/$f.o"
done
gcc -c "${DL_CFLAGS[@]}" "$DL_DIR/demo/deltalog_stubs.c" -o "$DL_DIR/demo/deltalog_stubs.o"
gcc -c "${DL_CFLAGS[@]}" "$DL_DIR/demo/delta_log_demo.c" -o "$DL_DIR/demo/delta_log_demo.o"
gcc "$DL_DIR/demo/delta_log_demo.o" "$DL_DIR/Factoidal_DeltaLog.o" "$DL_DIR/krmlinit.o" \
    "$DL_DIR/prims64.o" "$DL_DIR/fstar_char.o" "$DL_DIR/fstar_string.o" "$DL_DIR/fstar_uint32.o" \
    "$DL_DIR/demo/deltalog_stubs.o" -o "$DL_DIR/demo/delta_log_demo"
OUT="$("./$DL_DIR/demo/delta_log_demo")"
echo "$OUT"
grep -q 'All checks passed' <<<"$OUT"
