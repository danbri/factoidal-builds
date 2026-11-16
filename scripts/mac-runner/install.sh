#!/bin/bash
# install.sh: install (or update) the overnight GitHub Actions runner for danbri/factoidal-builds
# on the owner's Mac. Run from a checkout of factoidal-builds: bash scripts/mac-runner/install.sh
#   - downloads the official actions/runner release for macOS arm64 into ~/actions-runner and
#     verifies its sha256 against the release notes;
#   - registers it (labels self-hosted, macOS, ARM64, foafnaut-mac) with a registration token
#     from the GitHub API;
#   - copies the controls (tick.sh, runner.sh, job hooks) to ~/actions-runner/ctl and sets the
#     job hooks, the Lean build lock and the 4 GiB floor in ~/actions-runner/.env;
#   - installs the launchd job org.foafnaut.mac-runner, which runs ctl/tick.sh every 5 minutes
#     (runner up 22:00-07:00 local only).
# Controls afterwards: ~/actions-runner/ctl/runner.sh status|off|on|now|logs|uninstall.
set -euo pipefail
REPO=danbri/factoidal-builds
DIR=${FOAFNAUT_RUNNER_DIR:-$HOME/actions-runner}
HERE=$(cd "$(dirname "$0")" && pwd)
LABEL=org.foafnaut.mac-runner
PLIST=$HOME/Library/LaunchAgents/$LABEL.plist
LEANLOCK=${FOAFNAUT_LEANLOCK:-$HOME/working/foafnaut-tools/leanlock.sh}
NAME=${RUNNER_NAME:-$(scutil --get LocalHostName 2>/dev/null || hostname -s)-foafnaut}
[ "$(uname -s)-$(uname -m)" = Darwin-arm64 ] || { echo "macOS arm64 only" >&2; exit 1; }
FREE=$(df -k "$HOME" | awk 'NR==2{printf "%d", $4/1048576}')
[ "$FREE" -ge 4 ] || { echo "only ${FREE} GiB free; the floor is 4 GiB" >&2; exit 1; }
[ -x "$LEANLOCK" ] || { echo "Lean build lock not found: $LEANLOCK" >&2; exit 1; }

mkdir -p "$DIR/ctl"
cd "$DIR"
if [ ! -x ./config.sh ]; then
  REL=$(gh api repos/actions/runner/releases/latest)
  VER=$(printf '%s' "$REL" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])')
  SHA=$(printf '%s' "$REL" | python3 -c 'import json,re,sys; m=re.search(r"<!-- BEGIN SHA osx-arm64 -->([0-9a-f]{64})<!-- END SHA osx-arm64 -->", json.load(sys.stdin)["body"]); print(m.group(1) if m else "")')
  [ -n "$SHA" ] || { echo "no osx-arm64 checksum in the $VER release notes" >&2; exit 1; }
  T=actions-runner-osx-arm64-${VER#v}.tar.gz
  curl -fsSL -o "$T" "https://github.com/actions/runner/releases/download/$VER/$T"
  echo "$SHA  $T" | shasum -a 256 -c -
  tar xzf "$T"
  rm -f "$T"
  echo "installed actions/runner $VER (sha256 $SHA verified)"
fi
cp "$HERE"/tick.sh "$HERE"/runner.sh "$HERE"/job-started.sh "$HERE"/job-completed.sh ctl/
chmod +x ctl/*.sh

if [ ! -f .runner ]; then
  TOKEN=$(gh api -X POST "repos/$REPO/actions/runners/registration-token" -q .token)
  ./config.sh --unattended --url "https://github.com/$REPO" --token "$TOKEN" \
    --name "$NAME" --labels foafnaut-mac --work _work --replace
fi

# Job environment: hooks, Lean lock, disk floor, marker read by builds' scripts.
touch .env
grep -vE '^(ACTIONS_RUNNER_HOOK_JOB_STARTED|ACTIONS_RUNNER_HOOK_JOB_COMPLETED|FOAFNAUT_[A-Z_]+)=' .env > .env.new || true
cat >> .env.new <<ENV
ACTIONS_RUNNER_HOOK_JOB_STARTED=$DIR/ctl/job-started.sh
ACTIONS_RUNNER_HOOK_JOB_COMPLETED=$DIR/ctl/job-completed.sh
FOAFNAUT_MAC_RUNNER=1
FOAFNAUT_RUNNER_DIR=$DIR
FOAFNAUT_LEANLOCK=$LEANLOCK
FOAFNAUT_MIN_FREE_GIB=4
ENV
mv .env.new .env
# PATH for jobs: elan and Homebrew first (config.sh wrote .path from this shell's PATH).
printf '%s\n' "$HOME/.elan/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin" > .path

mkdir -p "$(dirname "$PLIST")"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$DIR/ctl/tick.sh</string></array>
  <key>StartInterval</key><integer>300</integer>
  <key>RunAtLoad</key><true/>
  <key>AbandonProcessGroup</key><true/>
  <key>Nice</key><integer>5</integer>
  <key>StandardOutPath</key><string>$DIR/ctl/launchd.log</string>
  <key>StandardErrorPath</key><string>$DIR/ctl/launchd.log</string>
</dict>
</plist>
PL
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "launchd job $LABEL loaded; runner window 22:00-07:00 local. Status: $DIR/ctl/runner.sh status"
