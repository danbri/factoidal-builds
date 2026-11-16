#!/usr/bin/env bash
# Report the nightly build.yml run (main's head, every job, macOS included).
# A failing job opens an issue labelled "nightly" in this repository, or comments on the open
# one; a green night comments and closes it. The one-line summary (also in the run summary) is
# written to be pasted into the coordination log. Owner decision 2026-11-16: macOS jobs are
# not a merge gate, and a nightly macOS failure is fixed or reverted the next morning.
# Also notes the newest scheduled foafnaut-macos.yml run on main.
# Env: GH_TOKEN, GITHUB_REPOSITORY, GITHUB_RUN_ID, GITHUB_SERVER_URL, SHORT, PROCEED.
set -euo pipefail
R=$GITHUB_REPOSITORY
URL="$GITHUB_SERVER_URL/$R/actions/runs/$GITHUB_RUN_ID"
NOW=$(date -u +%Y-%m-%dT%H:%MZ)
FAILED=$(gh api "repos/$R/actions/runs/$GITHUB_RUN_ID/jobs?per_page=100" --paginate \
  -q '.jobs[] | select(.name != "nightly-report") | select(.conclusion == "failure" or .conclusion == "cancelled" or .conclusion == "timed_out") | "\(.name) (\(.conclusion))"' \
  | paste -sd ';' - | sed 's/;/; /g')
MACOS_RUNS_ON=$(gh api "repos/$R/actions/runs/$GITHUB_RUN_ID/jobs?per_page=100" --paginate \
  -q '.jobs[] | select(.name | test("macos|foafnaut$|darwin")) | "\(.name): \((.labels // []) | join(","))"' | paste -sd ';' - | sed 's/;/; /g')
FM=$(gh api "repos/$R/actions/workflows/foafnaut-macos.yml/runs?event=schedule&per_page=1" \
  -q '.workflow_runs[0] | "\(.conclusion // .status) \(.html_url)"' 2>/dev/null || echo "unknown")
if [ "${PROCEED:-true}" != true ]; then
  FAILED="resolve did not proceed${FAILED:+; $FAILED}"
fi
if [ -n "$FAILED" ]; then STATE=FAIL; else STATE=OK; fi
LINE="$NOW nightly: core main ${SHORT:-?} build.yml $STATE${FAILED:+: $FAILED} ($URL); newest scheduled foafnaut-macos: $FM"
echo "$LINE"
{ echo "### Nightly"; echo; echo "$LINE"; echo; echo "macOS jobs ran on: ${MACOS_RUNS_ON:-none}"; } >> "${GITHUB_STEP_SUMMARY:-/dev/null}"

gh label create nightly --repo "$R" --color b60205 \
  --description "Nightly build of core main (macOS included) failed" 2>/dev/null || true
OPEN=$(gh issue list --repo "$R" --label nightly --state open --json number -q '.[0].number' 2>/dev/null || true)
if [ "$STATE" = FAIL ]; then
  BODY="$LINE

macOS jobs ran on: ${MACOS_RUNS_ON:-none}

The macOS jobs are not a merge gate. A nightly failure on main is fixed or reverted the next morning (skills/ci-runner in factoidal-core)."
  if [ -n "$OPEN" ]; then
    gh issue comment "$OPEN" --repo "$R" --body "$BODY"
  else
    gh issue create --repo "$R" --label nightly --title "Nightly build of core main failing" --body "$BODY"
  fi
elif [ -n "$OPEN" ]; then
  gh issue comment "$OPEN" --repo "$R" --body "Green again: $LINE"
  gh issue close "$OPEN" --repo "$R"
fi
