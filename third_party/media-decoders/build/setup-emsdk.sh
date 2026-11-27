#!/bin/bash
# Install Emscripten 6.0.8, the version build-media.sh requires (and the one factoidal-builds
# uses in build.yml), into DIR (default ./emsdk, not committed). Then: source DIR/emsdk_env.sh
#
# With git and github.com: a clone of emsdk at tag 6.0.8. Without them (a network that allows
# only raw.githubusercontent.com and storage.googleapis.com): the emsdk files of that tag,
# one by one. emsdk then downloads the toolchain from storage.googleapis.com either way.
set -euo pipefail
VER=6.0.8
DIR=${1:-$PWD/emsdk}
if [ ! -x "$DIR/emsdk" ]; then
  if git clone --depth 1 --branch "$VER" https://github.com/emscripten-core/emsdk "$DIR" 2>/dev/null; then :; else
    rm -rf "$DIR"; mkdir -p "$DIR"
    for f in emsdk emsdk.py emsdk_env.sh emsdk_manifest.json emscripten-releases-tags.json \
             legacy-binaryen-tags.txt legacy-emscripten-tags.txt llvm-tags-64bit.txt; do
      curl -sSfL -o "$DIR/$f" "https://raw.githubusercontent.com/emscripten-core/emsdk/$VER/$f"
    done
    chmod +x "$DIR/emsdk"
  fi
fi
"$DIR/emsdk" install "$VER"
"$DIR/emsdk" activate "$VER"
echo "now: source $DIR/emsdk_env.sh"
