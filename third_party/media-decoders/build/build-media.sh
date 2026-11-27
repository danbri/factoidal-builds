#!/bin/bash
# Build the audio and video decoders that the Lean WasmVM engine runs, as standalone
# WebAssembly modules (records in danbri/factoidal-core:
# docs/designissues/2026-11-08-media-wasmvm.md, docs/designissues/2026-11-26-foafnaut-audio-plan.md).
#
# Home: danbri/factoidal-builds, third_party/media-decoders/build/ (owner, 2026-11-26:
# "vendor them into factoidal-builds/ repo third_party/ with provenance version and license
# info. Include wasm and build chain."). PROVENANCE.md beside wasm/ lists what this made.
#
# Usage: build/setup-emsdk.sh; source <emsdk>/emsdk_env.sh; build/build-media.sh [WORKDIR] [OUTDIR]
#   WORKDIR (default ./work, not committed) gets the pinned release tarballs (checked by
#   SHA-256), their sources and the objects. OUTDIR (default ../wasm) gets
#   opus-wasmvm.wasm, vorbis-wasmvm.wasm, vp8-wasmvm.wasm, mp3-wasmvm.wasm and SHA256SUMS.
#
# Libraries and licences (all permissive):
#   libopus 1.5.2     https://opus-codec.org         BSD 3-clause (decoder; float build)
#   libogg 1.3.5      https://xiph.org/ogg/          BSD 3-clause (ogg_packet and the bit reader)
#   libvorbis 1.3.7   https://xiph.org/vorbis/       BSD 3-clause (decoder files only)
#   libvpx 1.15.2     https://www.webmproject.org/   BSD 3-clause and a patent grant (VP8 decoder only)
#   minimp3           https://github.com/lieff/minimp3  CC0-1.0 (MPEG-1/2 layers I to III
#                     decoder; a copy of the header is in ../src/minimp3/, checked by SHA-256)
# The containers (Ogg, WebM, MP3 frames and tags) are read in Lean (L4Factoidal/Media in
# factoidal-core), not by these libraries: the modules get one packet or frame per call.
#
# Flags, and why:
#   Emscripten 6.0.8              the version factoidal-builds uses for its other Wasm
#                                 (build.yml); setup-emsdk.sh installs it. Another version is
#                                 refused unless MEDIA_ANY_EMCC=1 (its output is then not
#                                 the vendored bytes)
#   -sSTANDALONE_WASM --no-entry  WASI imports only, no JavaScript glue
#   -mno-simd128                  the engine has no SIMD
#   no threads                    libvpx: --disable-multithread
#   libvpx: --target=generic-gnu, no assembly, no run-time CPU detection: plain C
#   -sSUPPORT_LONGJMP=wasm        libvpx's setjmp/longjmp error path as Wasm exceptions
#                                 (legacy try/catch/delegate, which WasmVM runs), not
#                                 the JavaScript invoke_* imports of the default
#   -ffile-prefix-map             the work directory does not appear in the output (assert
#                                 messages), so another machine gives the same bytes
#   -O2                           speed matters more than size for a decoder in an
#                                 interpreter (-Oz sizes are printed with MEDIA_OZ=1)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mkdir -p "${1:-$PWD/work}" && cd "${1:-$PWD/work}" && pwd)
OUT=$(mkdir -p "${2:-$HERE/../wasm}" && cd "${2:-$HERE/../wasm}" && pwd)
EMCC=${EMCC:-emcc}
EMCONFIGURE=${EMCONFIGURE:-emconfigure}
EMMAKE=${EMMAKE:-emmake}
OPT="${OPT:--O2} -ffile-prefix-map=$WORK=/work -ffile-prefix-map=$HERE=/build"
EMVER=$("$EMCC" --version | sed -n '1s/.* \([0-9][0-9.]*\) (.*/\1/p')
if [ "$EMVER" != "6.0.8" ] && [ "${MEDIA_ANY_EMCC:-0}" != 1 ]; then
  echo "emcc is $EMVER, not 6.0.8: run setup-emsdk.sh and source emsdk_env.sh (or MEDIA_ANY_EMCC=1)" >&2; exit 1
fi
sha() { if command -v sha256sum >/dev/null; then sha256sum "$1"; else shasum -a 256 "$1"; fi | cut -d' ' -f1; }

fetch() { # url file sha256
  local url=$1 file=$WORK/$2 sum=$3
  [ -f "$file" ] || curl -sSfL -o "$file" "$url"
  local got; got=$(sha "$file")
  if [ "$got" != "$sum" ]; then echo "$file: sha256 $got, expected $sum" >&2; exit 1; fi
  [ -d "$WORK/${2%.tar.gz}" ] || tar xzf "$file" -C "$WORK"
}

mkdir -p "$WORK"
fetch https://downloads.xiph.org/releases/opus/opus-1.5.2.tar.gz opus-1.5.2.tar.gz \
  65c1d2f78b9f2fb20082c38cbe47c951ad5839345876e46941612ee87f9a7ce1
fetch https://downloads.xiph.org/releases/ogg/libogg-1.3.5.tar.gz libogg-1.3.5.tar.gz \
  0eb4b4b9420a0f51db142ba3f9c64b333f826532dc0f48c6410ae51f4799b664
fetch https://downloads.xiph.org/releases/vorbis/libvorbis-1.3.7.tar.gz libvorbis-1.3.7.tar.gz \
  0e982409a9c3fc82ee06e08205b1355e5c6aa4c36bca58146ef399621b0ce5ab
# The WebM project's release tarball (the GitHub tag archive of 2026-11-08 had the
# SHA-256 26fcd3db88045dee380e581862a6ef106f49b74b6396ee95c2993a260b4636aa).
fetch https://storage.googleapis.com/downloads.webmproject.org/releases/webm/libvpx-1.15.2.tar.gz libvpx-1.15.2.tar.gz \
  79c99e7038c281e63f4540c51c264efd6ab1a8a005a9221d6e1f77109e6f57b5

LINK=(-sSTANDALONE_WASM --no-entry -sALLOW_MEMORY_GROWTH -sINITIAL_MEMORY=4MB -mno-simd128)
size() { echo "$1: $(wc -c < "$1" | tr -d ' ') bytes"; }

# --- Opus: the source lists of opus_sources.mk, celt_sources.mk, silk_sources.mk.
mklist() { # file variable
  sed -n "/^$2 = /,/^\$/p" "$1" | sed -e "s/^$2 = //" -e 's/\\$//' | tr -s ' \t' '\n' | grep '\.c$' || true
}
OPUS=$WORK/opus-1.5.2
OBJ=$WORK/obj-opus; rm -rf "$OBJ"; mkdir -p "$OBJ"
srcs=$( (mklist "$OPUS/celt_sources.mk" CELT_SOURCES; mklist "$OPUS/silk_sources.mk" SILK_SOURCES
         mklist "$OPUS/silk_sources.mk" SILK_SOURCES_FLOAT; mklist "$OPUS/opus_sources.mk" OPUS_SOURCES
         mklist "$OPUS/opus_sources.mk" OPUS_SOURCES_FLOAT) )
objs=()
for s in $srcs; do
  o=$OBJ/$(echo "$s" | tr / _).o
  "$EMCC" $OPT -mno-simd128 -DOPUS_BUILD -DUSE_ALLOCA -DHAVE_LRINTF -DHAVE_LRINT \
    -I"$OPUS/include" -I"$OPUS/celt" -I"$OPUS/silk" -I"$OPUS/silk/float" -I"$OPUS" \
    -c "$OPUS/$s" -o "$o"
  objs+=("$o")
done
"$EMCC" $OPT -mno-simd128 -I"$OPUS/include" -c "$HERE/media/opus_entry.c" -o "$OBJ/entry.o"
"$EMCC" $OPT "${objs[@]}" "$OBJ/entry.o" "${LINK[@]}" -o "$OUT/opus-wasmvm.wasm"
size "$OUT/opus-wasmvm.wasm"

# --- Vorbis: libogg (bitwise.c, framing.c) and the libvorbis decoder files.
OGG=$WORK/libogg-1.3.5; VOR=$WORK/libvorbis-1.3.7
OBJ=$WORK/obj-vorbis; rm -rf "$OBJ"; mkdir -p "$OBJ/ogg"
cat > "$OBJ/ogg/config_types.h" <<'EOF'
#ifndef __CONFIG_TYPES_H__
#define __CONFIG_TYPES_H__
#include <stdint.h>
typedef int16_t ogg_int16_t;
typedef uint16_t ogg_uint16_t;
typedef int32_t ogg_int32_t;
typedef uint32_t ogg_uint32_t;
typedef int64_t ogg_int64_t;
typedef uint64_t ogg_uint64_t;
#endif
EOF
objs=()
for s in "$OGG/src/bitwise.c" "$OGG/src/framing.c" \
         $(for f in mdct smallft block envelope window lsp lpc analysis synthesis psy info \
                    floor1 floor0 res0 mapping0 registry codebook sharedbook lookup bitrate; do
             echo "$VOR/lib/$f.c"; done); do
  o=$OBJ/$(basename "$s" .c).o
  "$EMCC" $OPT -mno-simd128 -I"$OBJ" -I"$OGG/include" -I"$VOR/include" -I"$VOR/lib" -c "$s" -o "$o"
  objs+=("$o")
done
"$EMCC" $OPT -mno-simd128 -I"$OBJ" -I"$OGG/include" -I"$VOR/include" -c "$HERE/media/vorbis_entry.c" -o "$OBJ/entry.o"
"$EMCC" $OPT "${objs[@]}" "$OBJ/entry.o" "${LINK[@]}" -o "$OUT/vorbis-wasmvm.wasm"
size "$OUT/vorbis-wasmvm.wasm"

# --- VP8: libvpx configured for a generic target, decoder only.
VPX=$WORK/libvpx-1.15.2
B=$WORK/build-vpx
if [ ! -f "$B/libvpx.a" ]; then
  rm -rf "$B"; mkdir -p "$B"
  (cd "$B" && "$EMCONFIGURE" "$VPX/configure" --target=generic-gnu --disable-vp8-encoder \
     --disable-vp9 --enable-vp8-decoder --disable-examples --disable-tools --disable-docs \
     --disable-unit-tests --disable-multithread --disable-runtime-cpu-detect \
     --disable-webm-io --disable-libyuv --extra-cflags="$OPT -mno-simd128 -sSUPPORT_LONGJMP=wasm" >/dev/null \
   && "$EMMAKE" make -j4 >/dev/null)
fi
OBJ=$WORK/obj-vp8; rm -rf "$OBJ"; mkdir -p "$OBJ"
"$EMCC" $OPT -mno-simd128 -I"$VPX" -I"$B" -c "$HERE/media/vp8_entry.c" -o "$OBJ/entry.o"
"$EMCC" $OPT "$OBJ/entry.o" "$B/libvpx.a" "${LINK[@]}" -sSUPPORT_LONGJMP=wasm -o "$OUT/vp8-wasmvm.wasm"
size "$OUT/vp8-wasmvm.wasm"

# --- MP3: minimp3, one header file; the copy in ../src/minimp3 is checked by its SHA-256.
MP3=$HERE/../src/minimp3
[ "$(sha "$MP3/minimp3.h")" = eb4b44812cfe77a358aa1820462cc877473a8d97206009ebecd18b60a123875a ] \
  || { echo "minimp3.h: not the pinned copy" >&2; exit 1; }
OBJ=$WORK/obj-mp3; rm -rf "$OBJ"; mkdir -p "$OBJ"
"$EMCC" $OPT -mno-simd128 -I"$MP3" -c "$HERE/media/mp3_entry.c" -o "$OBJ/entry.o"
"$EMCC" $OPT "$OBJ/entry.o" "${LINK[@]}" -o "$OUT/mp3-wasmvm.wasm"
size "$OUT/mp3-wasmvm.wasm"

(cd "$OUT" && for m in opus vorbis vp8 mp3; do echo "$(sha $m-wasmvm.wasm)  $m-wasmvm.wasm"; done > SHA256SUMS)
cat "$OUT/SHA256SUMS"
if command -v wasm-tools >/dev/null; then
  for m in opus vorbis vp8 mp3; do
    echo "$m imports:"; wasm-tools print "$OUT/$m-wasmvm.wasm" | grep '(import ' | sed 's/^ */  /'
  done
fi
