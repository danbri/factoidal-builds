#!/usr/bin/env bash
# Install elan for a build job, or on the owner's Mac (self-hosted runner, FOAFNAUT_MAC_RUNNER
# set in the runner's .env) use the elan already there: the installer would rewrite the
# owner's shell profile and elan itself. Toolchains are shared with the owner's builds.
set -euo pipefail
if [ -n "${FOAFNAUT_MAC_RUNNER:-}" ] && [ -x "$HOME/.elan/bin/elan" ]; then
  echo "self-hosted Mac: using its elan ($("$HOME/.elan/bin/elan" --version))"
else
  curl -sSf https://elan.lean-lang.org/elan-init.sh | sh -s -- -y --default-toolchain none
fi
echo "$HOME/.elan/bin" >> "$GITHUB_PATH"
