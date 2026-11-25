#!/usr/bin/env bash
# Install elan for a build job, or on the owner's Mac (self-hosted runner, FOAFNAUT_MAC_RUNNER
# set in the runner's .env) use the elan already there: the installer would rewrite the
# owner's shell profile and elan itself. Toolchains are shared with the owner's builds.
set -euo pipefail
if [ -n "${FOAFNAUT_MAC_RUNNER:-}" ] && [ -x "$HOME/.elan/bin/elan" ]; then
  echo "self-hosted Mac: using its elan ($("$HOME/.elan/bin/elan" --version))"
else
  # elan-init downloads a second asset from GitHub. Retry the whole install,
  # since retrying only the bootstrap download would miss errors from that asset.
  for attempt in 1 2 3; do
    if curl -sSf https://elan.lean-lang.org/elan-init.sh | sh -s -- -y --default-toolchain none; then
      break
    fi
    if [ "$attempt" -eq 3 ]; then
      exit 1
    fi
    echo "elan installation attempt $attempt failed. Retrying." >&2
    sleep "$((attempt * 5))"
  done
fi
echo "$HOME/.elan/bin" >> "$GITHUB_PATH"
