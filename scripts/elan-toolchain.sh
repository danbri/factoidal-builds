#!/usr/bin/env bash
# Install a Lean toolchain with elan unless it is already installed. elan 4.2.3 exits 1 with
# "'<toolchain>' is already installed" for `elan toolchain install` of an installed toolchain,
# which stopped every macOS engine build on the self-hosted Mac (2026-11-26 and 2026-11-27,
# foafnaut-macos.yml runs 268 and 269). Usage: elan-toolchain.sh TOOLCHAIN
set -euo pipefail
T=$1
ELAN="$HOME/.elan/bin/elan"
# Read the list into a variable first: a pipe into `grep -q` can end elan with SIGPIPE, which
# pipefail would report as a failure.
installed=$("$ELAN" toolchain list)
if printf '%s\n' "$installed" | awk '{print $1}' | grep -qxF "$T"; then
  echo "elan-toolchain.sh: $T is already installed"
else
  "$ELAN" toolchain install "$T"
fi
