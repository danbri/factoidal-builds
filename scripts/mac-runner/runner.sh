#!/bin/bash
# runner.sh: the owner's controls for the overnight GitHub Actions runner on this Mac.
#   runner.sh status          state, window, disk, last log lines, what GitHub sees
#   runner.sh off [--now]     switch off: no new jobs; stop after the running job (--now: stop at once)
#   runner.sh on              switch back on (it starts at the next tick inside the window)
#   runner.sh now [hours]     run now for N hours (default 2), outside the window too
#   runner.sh logs            follow the runner's log
#   runner.sh uninstall       switch off, remove the launchd job, deregister from GitHub
#                             (./config.sh remove), clear MAC_RUNNER; prints how to delete the files
set -u
DIR=${FOAFNAUT_RUNNER_DIR:-$HOME/actions-runner}
CTL=$DIR/ctl
REPO=danbri/factoidal-builds
LABEL=org.foafnaut.mac-runner
PLIST=$HOME/Library/LaunchAgents/$LABEL.plist
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
listener() { pgrep -f "$DIR/bin/Runner.Listener" | head -1; }
busy() { pgrep -f "$DIR/bin/Runner.Worker" >/dev/null; }
stop_now() {
  local p; p=$(listener); [ -n "$p" ] || return 0
  kill -INT "$p"; for _ in 1 2 3 4 5 6; do sleep 5; [ -z "$(listener)" ] && return 0; done
  p=$(listener); [ -n "$p" ] && kill -TERM "$p"
}
# Run a tick now through launchd (so the runner is launchd's child, not this shell's).
kick() { launchctl kickstart "gui/$(id -u)/$LABEL" 2>/dev/null || bash "$CTL/tick.sh"; }
advertise_off() {
  gh variable set MAC_RUNNER --repo "$REPO" --body "{\"seen\": $(date +%s), \"until\": 0, \"free_gib\": 0}" >/dev/null || true
}
case "${1:-status}" in
  status)
    echo "runner dir: $DIR"
    if [ -n "$(listener)" ]; then echo "runner: running (pid $(listener))$(busy && echo ', a job is running')"; else echo "runner: not running"; fi
    [ -e "$CTL/disabled" ] && echo "switched OFF by ctl/disabled (runner.sh on to re-enable)"
    [ -f "$CTL/run-until" ] && echo "manual run until: $(date -r "$(cat "$CTL/run-until")" 2>/dev/null)"
    [ -f "$CTL/config" ] && echo "config: $(tr '\n' ' ' < "$CTL/config")"
    echo "launchd: $(launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1 && echo loaded || echo 'not loaded')"
    df -h "$HOME" | awk 'NR==2{print "disk free: " $4}'
    echo "GitHub: $(gh api "repos/$REPO/actions/runners" -q '.runners[] | "\(.name) \(.status) busy=\(.busy) [\([.labels[].name] | join(","))]"' 2>/dev/null)"
    echo "MAC_RUNNER: $(gh variable get MAC_RUNNER --repo "$REPO" 2>/dev/null)"
    echo "--- tick.log"; tail -5 "$CTL/tick.log" 2>/dev/null
    ;;
  off)
    touch "$CTL/disabled"; rm -f "$CTL/run-until"; advertise_off
    if [ "${2:-}" = --now ] || ! busy; then stop_now; echo "runner stopped and switched off"
    else echo "switched off: no new jobs; the running job finishes, then the next tick stops the runner (or: runner.sh off --now)"; fi
    ;;
  on)
    rm -f "$CTL/disabled"; echo "switched on; it runs inside the window"; kick
    ;;
  now)
    HRS=${2:-2}; rm -f "$CTL/disabled"
    echo $(( $(date +%s) + HRS * 3600 )) > "$CTL/run-until"; kick
    echo "running until $(date -r "$(cat "$CTL/run-until")")"
    ;;
  logs) tail -f "$CTL/runner.log" ;;
  uninstall)
    touch "$CTL/disabled"; launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null; rm -f "$PLIST"
    stop_now; advertise_off
    TOKEN=$(gh api -X POST "repos/$REPO/actions/runners/remove-token" -q .token)
    ( cd "$DIR" && ./config.sh remove --token "$TOKEN" )
    gh variable delete MAC_RUNNER --repo "$REPO" 2>/dev/null || true
    echo "removed from GitHub and launchd. To delete the files: rm -rf '$DIR'"
    ;;
  *) sed -n '2,10p' "$0"; exit 2 ;;
esac
