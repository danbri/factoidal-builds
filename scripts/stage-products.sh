#!/usr/bin/env bash
# Copy the build products of a factoidal-core checkout into a staging dir,
# keeping repository-relative paths.
#
# A build product is a file that EXISTS in the checkout and is matched by
# core's .gitignore (git ls-files --others --ignored). Core's .gitignore
# lists exactly the build-product paths (tools/repo-split/core-tip-exclude.py
# is the rule), so this script needs no list of its own: whatever the build
# wrote under the given roots, and core does not track, is staged.
#
# Usage: stage-products.sh CORE_DIR OUT_DIR ROOT [ROOT...]
set -euo pipefail
CORE="$1"; OUT="$2"; shift 2
mkdir -p "$OUT"
LIST="$(mktemp)"
git -C "$CORE" ls-files --others --ignored --exclude-standard -z -- "$@" > "$LIST"
# Drop compiler intermediates even when ignored: they are not products.
python3 - "$LIST" > "$LIST.keep" <<'PY'
import re, sys
items = open(sys.argv[1], 'rb').read().split(b'\0')
skip = re.compile(rb'\.(cmi|cmx|cmo|cmt|cmti|o|a|log)$|(^|/)\.build-running$|/\.extract-state/')
for p in items:
    if p and not skip.search(p):
        sys.stdout.buffer.write(p + b'\0')
PY
N=$(tr -cd '\0' < "$LIST.keep" | wc -c)
[ "$N" -gt 0 ] || { echo "stage-products: nothing staged under $* in $CORE" >&2; exit 1; }
( cd "$CORE" && tar --null -T "$LIST.keep" -cf - ) | ( cd "$OUT" && tar -xpf - )
echo "stage-products: staged $N files under $* -> $OUT" >&2
