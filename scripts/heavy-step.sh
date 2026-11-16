#!/usr/bin/env bash
# heavy-step.sh <command...>: run a heavy build step (a Lean build) with the owner's Mac's
# rules when the job runs there (FOAFNAUT_MAC_RUNNER set in the self-hosted runner's .env):
#   - fail fast when less than FOAFNAUT_MIN_FREE_GIB (default 4) GiB are free;
#   - take the Mac's one-Lean-build-at-a-time lock (FOAFNAUT_LEANLOCK, leanlock.sh <dir> <cmd...>).
# On GitHub's runners it runs the command unchanged.
set -euo pipefail
if [ -z "${FOAFNAUT_MAC_RUNNER:-}" ]; then exec "$@"; fi
MIN=${FOAFNAUT_MIN_FREE_GIB:-4}
FREE=$(df -k "$PWD" | awk 'NR==2{printf "%d", $4/1048576}')
if [ "$FREE" -lt "$MIN" ]; then
  echo "::error::self-hosted Mac: ${FREE} GiB free, below the ${MIN} GiB floor; refusing this heavy step"
  exit 1
fi
echo "self-hosted Mac: ${FREE} GiB free; waiting for the Lean build lock" >&2
if [ -n "${FOAFNAUT_LEANLOCK:-}" ] && [ -x "$FOAFNAUT_LEANLOCK" ]; then
  exec "$FOAFNAUT_LEANLOCK" "$PWD" "$@"
fi
echo "::error::self-hosted Mac: FOAFNAUT_LEANLOCK is not set or not executable; refusing an unlocked Lean build"
exit 1
