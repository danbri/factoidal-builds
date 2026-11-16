#!/bin/bash
# ACTIONS_RUNNER_HOOK_JOB_STARTED of the owner's Mac runner (set in ~/actions-runner/.env by
# install.sh). It runs before every job's steps; a non-zero exit fails the job before any of
# its code runs. The workflow files cannot change it: it lives on the Mac.
# Accepts only: repository danbri/factoidal-builds; events workflow_dispatch and schedule (a
# pull_request from a fork, or any other event, never runs here); actors danbri and
# github-actions[bot] (a dispatch from another workflow); at least FOAFNAUT_MIN_FREE_GIB
# (default 4) GiB free; the runner not switched off (ctl/disabled).
set -u
DIR=${FOAFNAUT_RUNNER_DIR:-$HOME/actions-runner}
refuse() { echo "::error::foafnaut-mac runner refused this job: $*"; exit 1; }
[ "${GITHUB_REPOSITORY:-}" = danbri/factoidal-builds ] || refuse "repository '${GITHUB_REPOSITORY:-}' is not danbri/factoidal-builds"
case "${GITHUB_EVENT_NAME:-}" in
  workflow_dispatch|schedule) ;;
  *) refuse "event '${GITHUB_EVENT_NAME:-}': only workflow_dispatch and schedule run on this Mac" ;;
esac
case "${GITHUB_ACTOR:-}" in
  danbri|'github-actions[bot]') ;;
  *) refuse "actor '${GITHUB_ACTOR:-}'" ;;
esac
[ -e "$DIR/ctl/disabled" ] && refuse "the owner switched the runner off ($DIR/ctl/disabled)"
MIN=${FOAFNAUT_MIN_FREE_GIB:-4}
FREE=$(df -k "$HOME" | awk 'NR==2{printf "%d", $4/1048576}')
[ "$FREE" -ge "$MIN" ] || refuse "${FREE} GiB free, below the ${MIN} GiB floor"
echo "foafnaut-mac: accepted ${GITHUB_WORKFLOW:-?} / ${GITHUB_JOB:-?} (run ${GITHUB_RUN_ID:-?}, ${GITHUB_EVENT_NAME}, ${GITHUB_ACTOR}); ${FREE} GiB free"
