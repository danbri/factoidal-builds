#!/bin/bash
# ACTIONS_RUNNER_HOOK_JOB_COMPLETED of the owner's Mac runner: remove what the job left, so
# the Mac's disk is as before (checkouts, .lake, build outputs, the leanc object cache and shim
# the macOS jobs keep in $HOME). Only paths inside the runner's _work directory and the two
# CI-only directories are touched.
set -u
DIR=${FOAFNAUT_RUNNER_DIR:-$HOME/actions-runner}
WORK="$DIR/_work"
clean() {   # clean <dir>: remove its contents when it is inside $WORK
  local d=$1
  [ -n "$d" ] && [ -d "$d" ] || return 0
  case "$(cd "$d" && pwd -P)/" in "$(cd "$WORK" && pwd -P)/"?*) ;; *) echo "foafnaut-mac: not cleaning $d (outside $WORK)"; return 0 ;; esac
  find "$d" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null || true
}
clean "${GITHUB_WORKSPACE:-}"
clean "${RUNNER_TEMP:-}"
rm -rf "$HOME/leanc-cache" "$HOME/leanc-shim"
echo "foafnaut-mac: workspace cleaned; $(df -h "$HOME" | awk 'NR==2{print $4}') free"
