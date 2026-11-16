#!/usr/bin/env bash
# Decide whether build.yml runs its macOS jobs (lean-macos and the foafnaut bundle) for one
# core commit. Owner decision 2026-11-16: merges are gated on the Linux jobs; the macOS jobs
# run for every core main commit (they feed the darwin releases, which publish.sh makes only
# for main), on the nightly schedule, and on request (dispatch input macos=true). A dispatch
# of a commit that is not on core main (a PR head) is Linux only by default.
#
# Inputs (env): EVENT, SHA, INPUT_MACOS (true|false|empty), SCHEDULE (github.event.schedule),
#   CORE_REPO, GH_TOKEN. Prints macos=<true|false>, nightly=<true|false> and on_main=<status>.
set -euo pipefail
NIGHTLY_CRON='41 2 * * *'
NIGHTLY=false
[ "${EVENT:-}" = schedule ] && [ "${SCHEDULE:-}" = "$NIGHTLY_CRON" ] && NIGHTLY=true
# "identical" or "behind": SHA is main's head or an ancestor of it (as in publish.sh).
ON_MAIN=$(gh api "repos/${CORE_REPO:-danbri/factoidal-core}/compare/main...$SHA" -q .status 2>/dev/null || echo unknown)
MACOS=false
case "$ON_MAIN" in identical|behind) MACOS=true ;; esac
case "${EVENT:-}" in schedule|push) MACOS=true ;; esac
[ "${INPUT_MACOS:-false}" = true ] && MACOS=true
echo "macos=$MACOS"
echo "nightly=$NIGHTLY"
printf "on_main=%q\n" "$ON_MAIN"
