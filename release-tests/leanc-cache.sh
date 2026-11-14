#!/usr/bin/env bash
# leanc-cache.sh: a `leanc` in front of the real one that keeps the objects of
# `leanc ... -c FILE.c -o FILE.o` by content: sha256 of the toolchain name, the flags and
# the C source. Lean's generated C for a module that did not change is the same bytes,
# so its object is copied, not compiled again (core's build-web-render.sh compiles 444
# files one at a time: 14 min on a hosted runner). Other leanc calls (link) pass through.
#
#   LEANC_REAL   the real leanc      LEANC_CACHE  the object directory
#   LEANC_ID     toolchain name (part of the key)
# Counts go to $LEANC_CACHE/.hits and .misses (one byte a call).
set -u
src=""; out=""; compile=0; prev=""
for a in "$@"; do
  [ "$prev" = "-o" ] && out=$a
  case "$a" in -c) compile=1;; *.c) src=$a;; esac
  prev=$a
done
if [ "$compile" = 1 ] && [ -n "$src" ] && [ -n "$out" ] && [ -f "$src" ] && [ -n "${LEANC_CACHE:-}" ]; then
  key=$( { printf '%s\n' "${LEANC_ID:-}"; for a in "$@"; do [ "$a" = "$src" ] || [ "$a" = "$out" ] || printf '%s\n' "$a"; done; cat "$src"; } | sha256sum | cut -d' ' -f1)
  if [ -s "$LEANC_CACHE/$key.o" ]; then
    cp "$LEANC_CACHE/$key.o" "$out" && { touch "$LEANC_CACHE/$key.o"; printf . >> "$LEANC_CACHE/.hits"; exit 0; }
  fi
  "$LEANC_REAL" "$@" || exit $?
  cp "$out" "$LEANC_CACHE/$key.o.$$" && mv "$LEANC_CACHE/$key.o.$$" "$LEANC_CACHE/$key.o"
  printf . >> "$LEANC_CACHE/.misses"
  exit 0
fi
exec "$LEANC_REAL" "$@"
