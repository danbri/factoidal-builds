"""The merge gate and the Mac runner choice.

scripts/mac-runs-on.py sends a macOS job to the owner's Mac only for dispatch or schedule
events in this repository, with a fresh heartbeat, enough window left and enough disk.
scripts/resolve-core.sh runs the macOS jobs for core main commits, schedules and on request,
and not for a dispatch of a commit that is not on core main.
scripts/mac-runner/job-started.sh refuses jobs from other events, repositories and actors.
"""
import importlib.util
import json
import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("mac_runs_on", ROOT / "scripts" / "mac-runs-on.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

NOW = 1_800_000_000
GOOD = json.dumps({"seen": NOW - 60, "until": NOW + 8 * 3600, "free_gib": 20})
R = "danbri/factoidal-builds"


class RunsOn(unittest.TestCase):
    def pick(self, var=GOOD, event="workflow_dispatch", repo=R, need=12, lead=3, mode="auto"):
        return m.choose(var, event, repo, need, lead, mode, now=NOW)[0]

    def test_online_mac_is_preferred(self):
        self.assertEqual(self.pick(), m.SELF)
        self.assertEqual(self.pick(event="schedule"), m.SELF)

    def test_pull_request_and_forks_never_reach_the_mac(self):
        for ev in ("pull_request", "pull_request_target", "push", "workflow_run", "issue_comment"):
            self.assertEqual(self.pick(event=ev), m.HOSTED, ev)
            self.assertEqual(self.pick(event=ev, mode="self-hosted"), m.HOSTED, ev)
        self.assertEqual(self.pick(repo="someone/factoidal-builds"), m.HOSTED)
        self.assertEqual(self.pick(repo="someone/factoidal-builds", mode="self-hosted"), m.HOSTED)

    def test_fallbacks(self):
        self.assertEqual(self.pick(var=""), m.HOSTED)
        self.assertEqual(self.pick(var="not json"), m.HOSTED)
        self.assertEqual(self.pick(var="[1]"), m.HOSTED)
        self.assertEqual(self.pick(var=json.dumps({"seen": "x"})), m.HOSTED)
        stale = json.dumps({"seen": NOW - 3600, "until": NOW + 8 * 3600, "free_gib": 20})
        self.assertEqual(self.pick(var=stale), m.HOSTED)
        late = json.dumps({"seen": NOW - 60, "until": NOW + 3600, "free_gib": 20})
        self.assertEqual(self.pick(var=late), m.HOSTED)
        self.assertEqual(self.pick(var=late, lead=0.5), m.SELF)
        off = json.dumps({"seen": NOW - 60, "until": 0, "free_gib": 20})
        self.assertEqual(self.pick(var=off), m.HOSTED)
        tight = json.dumps({"seen": NOW - 60, "until": NOW + 8 * 3600, "free_gib": 5})
        self.assertEqual(self.pick(var=tight), m.HOSTED)
        self.assertEqual(self.pick(var=tight, need=4), m.SELF)

    def test_modes(self):
        self.assertEqual(self.pick(mode="github"), m.HOSTED)
        self.assertEqual(self.pick(var="", mode="self-hosted"), m.SELF)


def resolve_macos(event, sha_on_main, input_macos="", schedule=""):
    """Run the macOS decision of resolve-core.sh with gh replaced by a stub."""
    with tempfile.TemporaryDirectory() as d:
        stub = pathlib.Path(d) / "gh"
        status = "identical" if sha_on_main else "diverged"
        stub.write_text(f"#!/bin/sh\necho {status}\n")
        stub.chmod(0o755)
        env = dict(os.environ, PATH=f"{d}:{os.environ['PATH']}", EVENT=event, SHA="a" * 40,
                   INPUT_MACOS=input_macos, SCHEDULE=schedule, CORE_REPO="danbri/factoidal-core")
        out = subprocess.run(["bash", str(ROOT / "scripts" / "resolve-macos.sh")], env=env,
                             capture_output=True, text=True, check=True).stdout
        return dict(l.split("=", 1) for l in out.split() if "=" in l)


class MacosJobs(unittest.TestCase):
    def test_pr_head_dispatch_is_linux_only(self):
        self.assertEqual(resolve_macos("workflow_dispatch", False)["macos"], "false")

    def test_pr_head_dispatch_with_input_runs_macos(self):
        self.assertEqual(resolve_macos("workflow_dispatch", False, "true")["macos"], "true")

    def test_main_commit_keeps_the_release_path(self):
        self.assertEqual(resolve_macos("workflow_dispatch", True)["macos"], "true")
        self.assertEqual(resolve_macos("schedule", True)["macos"], "true")
        self.assertEqual(resolve_macos("push", True)["macos"], "true")

    def test_nightly(self):
        r = resolve_macos("schedule", True, schedule="41 2 * * *")
        self.assertEqual((r["macos"], r["nightly"]), ("true", "true"))
        self.assertEqual(resolve_macos("schedule", True, schedule="23 * * * *")["nightly"], "false")


class JobStartedHook(unittest.TestCase):
    def run_hook(self, **env):
        with tempfile.TemporaryDirectory() as d:
            e = dict(os.environ, HOME=d, GITHUB_REPOSITORY=R, GITHUB_EVENT_NAME="workflow_dispatch",
                     GITHUB_ACTOR="danbri", FOAFNAUT_MIN_FREE_GIB="0")
            e.update(env)
            return subprocess.run(["bash", str(ROOT / "scripts" / "mac-runner" / "job-started.sh")],
                                  env=e, capture_output=True, text=True).returncode

    def test_accepts_owner_dispatch_and_schedule(self):
        self.assertEqual(self.run_hook(), 0)
        self.assertEqual(self.run_hook(GITHUB_EVENT_NAME="schedule"), 0)
        self.assertEqual(self.run_hook(GITHUB_ACTOR="github-actions[bot]"), 0)

    def test_refuses_others(self):
        self.assertNotEqual(self.run_hook(GITHUB_EVENT_NAME="pull_request"), 0)
        self.assertNotEqual(self.run_hook(GITHUB_EVENT_NAME="pull_request_target"), 0)
        self.assertNotEqual(self.run_hook(GITHUB_REPOSITORY="fork/factoidal-builds"), 0)
        self.assertNotEqual(self.run_hook(GITHUB_ACTOR="someone-else"), 0)
        self.assertNotEqual(self.run_hook(GITHUB_EVENT_NAME=""), 0)

    def test_refuses_low_disk(self):
        self.assertNotEqual(self.run_hook(FOAFNAUT_MIN_FREE_GIB="1000000"), 0)


if __name__ == "__main__":
    unittest.main()
