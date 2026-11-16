#!/usr/bin/env bash
# cache-audit.sh: check that compiler caches gave the objects a compile gives.
#
#   cache-audit.sh COMMANDS SAMPLE OUT_JSON
#
# COMMANDS is core's .build/web-render/compile-commands.txt (build-web-render.sh writes one
# shell-quoted compile command per line). SAMPLE commands are chosen at random; each is run
# again with every cache bypassed (CCACHE_DISABLE=1, no EM_COMPILER_WRAPPER, the real leanc
# instead of release-tests/leanc-cache.sh) into a temporary object, which must be byte-equal
# to the object the build used. Prints CACHE_AUDIT lines, writes OUT_JSON, exits 1 on any
# difference. It also writes the sha256 of every object named in COMMANDS to OUT_JSON, so
# a cold run and a warm run of one commit can be compared object by object.
#
# Env: LEANC_REAL (the real leanc, when the build used the leanc cache), EM_CACHE (as the build).
set -euo pipefail
COMMANDS=$1; SAMPLE=$2; OUT=$3
[ -s "$COMMANDS" ] || { echo "CACHE_AUDIT no compile commands in $COMMANDS"; exit 1; }
if command -v sha256sum >/dev/null 2>&1; then H=(sha256sum); else H=(shasum -a 256); fi
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
TOTAL=$(wc -l < "$COMMANDS" | tr -d ' ')
# A fixed sample size; the choice is random each run (python: no shuf on macOS).
python3 -c 'import random,sys; n=int(sys.argv[1]); k=min(int(sys.argv[2]),n); print("\n".join(str(i) for i in sorted(random.sample(range(1,n+1),k))))' "$TOTAL" "$SAMPLE" > "$TMP/picks"
CHECKED=0; DIFFER=0; ROWS=()
while read -r n; do
  line=$(sed -n "${n}p" "$COMMANDS")
  eval "set -- $line"
  args=(); obj=""; prev=""
  for a in "$@"; do
    if [ "$prev" = -o ]; then obj=$a; a="$TMP/audit.o"; fi
    args+=("$a"); prev=$a
  done
  [ -n "$obj" ] && [ -f "$obj" ] || { echo "CACHE_AUDIT line $n names no built object: $line"; DIFFER=$((DIFFER+1)); continue; }
  # No launcher in front, and the real compiler behind any wrapper.
  [ "${args[0]}" = ccache ] && args=("${args[@]:1}")
  [ "${args[0]}" = leanc ] && [ -n "${LEANC_REAL:-}" ] && args[0]=$LEANC_REAL
  rm -f "$TMP/audit.o"
  CCACHE_DISABLE=1 EM_COMPILER_WRAPPER= "${args[@]}" > "$TMP/log" 2>&1 || { cat "$TMP/log"; echo "CACHE_AUDIT uncached compile failed: $line"; DIFFER=$((DIFFER+1)); continue; }
  a=$("${H[@]}" "$obj" | cut -d' ' -f1); b=$("${H[@]}" "$TMP/audit.o" | cut -d' ' -f1)
  CHECKED=$((CHECKED+1))
  if [ "$a" = "$b" ]; then echo "CACHE_AUDIT same $(basename "$obj") $a"
  else echo "CACHE_AUDIT DIFFERENT $(basename "$obj") build $a uncached $b"; DIFFER=$((DIFFER+1)); fi
  ROWS+=("$(basename "$obj") $a $b")
done < "$TMP/picks"
# sha256 of every object the build made, by object name.
awk '{for(i=1;i<NF;i++) if($i=="-o") print $(i+1)}' "$COMMANDS" | while read -r q; do
  eval "o=$q"; [ -f "$o" ] && printf '%s %s\n' "$(basename "$o")" "$("${H[@]}" "$o" | cut -d' ' -f1)"
done | sort > "$TMP/objects"
python3 - "$OUT" "$TOTAL" "$CHECKED" "$DIFFER" "$TMP/objects" ${ROWS[@]+"${ROWS[@]}"} <<'PY'
import json, sys
out, total, checked, differ, objs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
rows = [r.split() for r in sys.argv[6:]]
json.dump({"format": "factoidal-cache-audit-v1", "compiles": total, "checked": checked, "different": differ,
           "sample": [{"object": o, "build": a, "uncached": b} for o, a, b in rows],
           "objects": dict(l.split() for l in open(objs) if l.strip())}, open(out, "w"), indent=1, sort_keys=True)
PY
echo "CACHE_AUDIT summary: $CHECKED of $TOTAL compiles recompiled without caches, $DIFFER different"
[ "$DIFFER" -eq 0 ]
