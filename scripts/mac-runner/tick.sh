#!/bin/bash
# tick.sh: launchd runs this every 5 minutes (org.foafnaut.mac-runner, installed by install.sh).
# It keeps the owner's Mac runner up only overnight and tells build.yml whether to use it:
#   - inside the window (START_H to STOP_H local time, default 22:00-07:00), with the runner
#     not switched off (ctl/disabled) and at least MIN_FREE_GIB free: start the runner if it
#     is not running (under caffeinate -i, so the Mac does not idle-sleep mid-job);
#   - outside the window: stop it; a job still running may finish until GRACE_MIN (60) minutes
#     after STOP_H, then the runner is stopped anyway (that job fails);
#   - every tick: set the repository variable MAC_RUNNER to {"seen","until","free_gib"}
#     (until = 0 when the runner should not get new jobs). scripts/mac-runs-on.py in the
#     builds repository reads it; a heartbeat older than 20 minutes counts as offline.
# ctl/run-until (epoch seconds, written by `runner.sh now`) opens the window until then.
# Settings: ctl/config (shell assignments) may set START_H, STOP_H, GRACE_MIN, MIN_FREE_GIB.
set -u
DIR=${FOAFNAUT_RUNNER_DIR:-$HOME/actions-runner}
CTL=$DIR/ctl
REPO=danbri/factoidal-builds
START_H=22; STOP_H=7; GRACE_MIN=60; MIN_FREE_GIB=4
[ -f "$CTL/config" ] && . "$CTL/config"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
LOG=$CTL/tick.log
log() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
for f in "$LOG" "$CTL/runner.log"; do
  [ "$(stat -f %z "$f" 2>/dev/null || echo 0)" -gt 2000000 ] && mv -f "$f" "$f.1"
done
mkdir "$CTL/tick.lck" 2>/dev/null || { [ -n "$(find "$CTL/tick.lck" -mmin +15 2>/dev/null)" ] && rmdir "$CTL/tick.lck"; exit 0; }
trap 'rmdir "$CTL/tick.lck" 2>/dev/null' EXIT

NOW=$(date +%s)
H=$((10#$(date +%H))); M=$((10#$(date +%M)))
listener() { pgrep -f "$DIR/bin/Runner.Listener" | head -1; }
busy() { pgrep -f "$DIR/bin/Runner.Worker" >/dev/null; }
FREE=$(df -k "$HOME" | awk 'NR==2{printf "%d", $4/1048576}')

if [ "$START_H" -gt "$STOP_H" ]; then
  { [ "$H" -ge "$START_H" ] || [ "$H" -lt "$STOP_H" ]; } && INWIN=true || INWIN=false
else
  { [ "$H" -ge "$START_H" ] && [ "$H" -lt "$STOP_H" ]; } && INWIN=true || INWIN=false
fi
END=0
if [ "$INWIN" = true ]; then
  # The next STOP_H:00 local time.
  END=$(python3 -c 'import sys,datetime as d; n=d.datetime.now(); t=n.replace(hour=int(sys.argv[1]),minute=0,second=0,microsecond=0); t = t if t>n else t+d.timedelta(days=1); print(int(t.timestamp()))' "$STOP_H")
fi
MANUAL=$(cat "$CTL/run-until" 2>/dev/null || echo 0)
case "$MANUAL" in ''|*[!0-9]*) MANUAL=0 ;; esac
[ "$MANUAL" -gt "$NOW" ] && [ "$MANUAL" -gt "$END" ] && END=$MANUAL
WANT=false
[ "$END" -gt "$NOW" ] && WANT=true
[ -e "$CTL/disabled" ] && WANT=false

PID=$(listener)
if [ "$WANT" = true ] && [ "$FREE" -ge "$MIN_FREE_GIB" ]; then
  if [ -z "$PID" ]; then
    log "start runner (window until $(date -r "$END" +%H:%M), ${FREE} GiB free)"
    ( cd "$DIR" && nohup caffeinate -i ./run.sh >> "$CTL/runner.log" 2>&1 & )
    sleep 5; PID=$(listener)
  fi
elif [ -n "$PID" ]; then
  SINCE=$(( (H * 60 + M - STOP_H * 60 + 1440) % 1440 ))   # minutes since STOP_H:00
  if busy && [ ! -e "$CTL/disabled" ] && [ "$SINCE" -lt "$GRACE_MIN" ]; then
    log "outside the window; a job is running, waiting (${SINCE} of ${GRACE_MIN} min grace)"
  else
    log "stop runner (want=$WANT, ${FREE} GiB free, busy=$(busy && echo yes || echo no))"
    kill -INT "$PID" 2>/dev/null
    for _ in 1 2 3 4 5 6; do sleep 5; [ -z "$(listener)" ] && break; done
    P2=$(listener); [ -n "$P2" ] && kill -TERM "$P2" 2>/dev/null
    PID=""
  fi
fi

ADV_UNTIL=0
[ -n "$PID" ] && [ "$WANT" = true ] && ADV_UNTIL=$END
gh variable set MAC_RUNNER --repo "$REPO" --body "{\"seen\": $NOW, \"until\": $ADV_UNTIL, \"free_gib\": $FREE}" >/dev/null 2>>"$LOG" \
  || log "could not set MAC_RUNNER"

# The Mac release lane (mac-release.yml writes latest/darwin-status.json).
# 1. Fallback trigger: GitHub drops most scheduled events in danbri/factoidal-builds, so when no
#    poll of mac-release.yml has been made for POLL_LATE_MIN (20) minutes and none is waiting or
#    running, dispatch one (a Linux job of about a minute; no Mac time). All day, not only in the
#    runner's window.
# 2. Into the coordination log: each dispatch decision of the lane (with any look-ahead wait)
#    and, at most hourly, an alert when the Mac release has fallen more than ALERT_LAG_MIN (120)
#    minutes behind core main. The lag is computed fresh from the GitHub API
#    (ctl/darwin-status.py status, at most every FRESH_MIN (10) minutes), not read from the
#    committed JSON, which is only as new as the last poll that ran.
LAST_POLL=$(gh api "repos/$REPO/actions/workflows/mac-release.yml/runs?per_page=10" \
  --jq '[.workflow_runs[] | select(.conclusion != "cancelled")] | (map(select(.status != "completed")) | length | tostring) + " " + (.[0].created_at // "")' 2>>"$LOG")
if [ -n "$LAST_POLL" ]; then
  ACTIVE=${LAST_POLL%% *}; LAST_AT=${LAST_POLL#* }
  AGE=$(python3 -c 'import sys,datetime as d; t=sys.argv[1]; print(int((d.datetime.now(d.timezone.utc)-d.datetime.strptime(t,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=d.timezone.utc)).total_seconds()//60) if t else 9999)' "$LAST_AT")
  if [ "$ACTIVE" = 0 ] && [ "$AGE" -ge "${POLL_LATE_MIN:-20}" ]; then
    if gh workflow run mac-release.yml --repo "$REPO" >/dev/null 2>>"$LOG"; then
      log "dispatched mac-release.yml (last poll ${AGE} min ago)"
    else
      log "could not dispatch mac-release.yml"
    fi
  fi
fi
COORD_LOG=${COORD_LOG:-$HOME/working/foafnaut/fncg/coordination.log}
if [ -f "$COORD_LOG" ]; then
  gh api "repos/$REPO/contents/latest/darwin-status.json" -H 'Accept: application/vnd.github.raw' \
    > "$CTL/darwin-status.json.new" 2>/dev/null && mv -f "$CTL/darwin-status.json.new" "$CTL/darwin-status.json"
  if [ -f "$CTL/darwin-status.py" ] && { [ ! -f "$CTL/darwin-status.fresh.json" ] \
       || [ -n "$(find "$CTL/darwin-status.fresh.json" -mmin +"${FRESH_MIN:-10}" 2>/dev/null)" ]; }; then
    BUILDS_REPO=$REPO python3 "$CTL/darwin-status.py" status > "$CTL/darwin-status.fresh.json.new" 2>>"$LOG" \
      && mv -f "$CTL/darwin-status.fresh.json.new" "$CTL/darwin-status.fresh.json" \
      || { rm -f "$CTL/darwin-status.fresh.json.new"; log "fresh darwin status failed"; }
  fi
  python3 - "$CTL" "$COORD_LOG" "${ALERT_LAG_MIN:-120}" <<'PY' 2>>"$LOG" || log "darwin-status check failed"
import datetime as dt, json, os, sys, time
ctl, coord, alert = sys.argv[1], sys.argv[2], int(sys.argv[3])
def load(name):
    try:
        return json.load(open(os.path.join(ctl, name)))
    except (OSError, ValueError):
        return None
def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp()
def seen(name, value):
    p = os.path.join(ctl, name)
    old = open(p).read() if os.path.exists(p) else ""
    if old == value:
        return True
    open(p, "w").write(value)
    return False
committed = load("darwin-status.json") or {}
fresh = load("darwin-status.fresh.json")
now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
lines = []
dec = committed.get("last_decision") or {}
if dec.get("action") == "dispatched" and not seen("darwin-decision", dec.get("at", "")):
    lines.append(f"macalways-ci: Mac release lane: dispatched build.yml for core main {dec.get('head','')[:12]} ({dec.get('reason','')})")
# The alert: from the fresh status when it is under 30 minutes old, else from the committed JSON
# with the lag recomputed from behind_since (and the status's age stated), never a stored lag_min.
d, src = None, ""
if fresh and fresh.get("checked_at") and time.time() - ts(fresh["checked_at"]) < 1800:
    d = fresh
elif committed.get("main"):
    d, src = committed, f"; status JSON of {committed.get('checked_at', '?')}, no fresh read"
if d and d.get("behind"):
    lag = int((time.time() - ts(d["behind_since"])) // 60) if d.get("behind_since") else d.get("lag_min", 0)
    if lag > alert:
        rel = (d.get("mac_release") or {}).get("tag", "none")
        key = f"{d['main']['sha']} {int(time.time() // 3600)}"
        if not seen("darwin-alert", key):
            runs = ", ".join(f"{r['id']} {r['status']}" for r in d.get("lane_runs", [])) or "no lane run"
            lines.append(f"macalways-ci: ALERT Mac release {rel} is {lag} min behind core main {d['main']['sha'][:12]} "
                         f"(behind since {d.get('behind_since')}; lane: {runs}{src})")
with open(coord, "a") as f:
    for l in lines:
        f.write(f"{now} {l}\n")
PY
fi
