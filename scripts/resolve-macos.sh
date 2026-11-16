#!/usr/bin/env bash
# Decide whether build.yml runs its macOS jobs (lean-macos and the foafnaut bundle) for one
# core commit. Owner decision 2026-11-16: merges are gated on the Linux jobs; the macOS jobs
# run for main's head in the main lane (they feed the darwin releases, which publish.sh makes
# only for main), on the nightly schedule, and on request (dispatch input macos=true). A dispatch
# that names a commit (a PR head, or a main commit) is Linux only by default.
#
# Inputs (env): EVENT, SHA, INPUT_REF (the dispatch's core_ref), INPUT_MACOS (true|false|empty), SCHEDULE (github.event.schedule),
#   CORE_REPO, GH_TOKEN. Prints macos=<true|false>, nightly=<true|false> and on_main=<status>.
set -euo pipefail
NIGHTLY_CRON='41 2 * * *'
NIGHTLY=false
[ "${EVENT:-}" = schedule ] && [ "${SCHEDULE:-}" = "$NIGHTLY_CRON" ] && NIGHTLY=true
# "identical" or "behind": SHA is main's head or an ancestor of it (as in publish.sh).
ON_MAIN=$(gh api "repos/${CORE_REPO:-danbri/factoidal-core}/compare/main...$SHA" -q .status 2>/dev/null || echo unknown)
# Owner rule 2026-11-16 ("always a Mac build of main done or building"): the macOS jobs of main
# run in the main lane only, the runs of the concurrency group build-factoidal-main (the hourly
# poll, a push here, and a dispatch with an empty core_ref, which mac-release.yml sends). That
# group keeps one running run and the newest pending one, and a pending run resolves main's head
# when it starts, so the Mac release always moves to the newest main. A dispatch that names a
# commit (a merge check of a main commit, say) runs the Linux jobs only: before, each such
# dispatch also queued two macOS jobs of an older main commit in front of the release.
MACOS=false
case "${EVENT:-}" in
  schedule|push) MACOS=true ;;
  workflow_dispatch)
    if [ -z "${INPUT_REF:-}" ] || [ "${INPUT_REF:-}" = main ]; then
      case "$ON_MAIN" in identical|behind) MACOS=true ;; esac
    fi ;;
esac
[ "${INPUT_MACOS:-false}" = true ] && MACOS=true
echo "macos=$MACOS"
echo "nightly=$NIGHTLY"
printf "on_main=%q\n" "$ON_MAIN"
