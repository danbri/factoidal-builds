"""The Mac release lane's decisions (scripts/darwin-status.py): which release counts as newest,
how long main has been ahead, when to dispatch, when to look ahead for landing PRs, and that a
capped wait is never repeated in the same lag episode."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("darwin_status", ROOT / "scripts" / "darwin-status.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

NOW = m.ts("2026-11-16T22:00:00Z")
H = "h" * 40


def commit(sha, parents, date):
    return {"sha": sha, "parents": [{"sha": p} for p in parents], "commit": {"committer": {"date": date}}}


def state(behind=True, lane=(), lag=10, since="2026-11-16T21:50:00Z", failure=None):
    return {"behind": behind, "lane_runs": list(lane), "lag_min": lag, "behind_since": since,
            "main": {"sha": H}, "last_failure": failure}


class Releases(unittest.TestCase):
    def test_newest_by_commit_not_by_publication(self):
        rels = [
            {"tag_name": "build-aaaaaaaaaaaa-foafnaut-darwin-arm64", "published_at": "2026-11-16T17:00:00Z",
             "body": "Built from https://github.com/x/y/commit/" + "a" * 40},
            {"tag_name": "build-bbbbbbbbbbbb-foafnaut-darwin-arm64", "published_at": "2026-11-16T16:00:00Z",
             "body": "Built from https://github.com/x/y/commit/" + "b" * 40},
            {"tag_name": "build-cccccccccccc-darwin-arm64", "published_at": "2026-11-16T18:00:00Z", "body": ""},
        ]
        cands = m.mac_releases(rels)
        self.assertEqual([c["sha"][0] for c in cands], ["a", "b"])
        dates = {"a" * 40: "2026-11-16T11:00:00Z", "b" * 40: "2026-11-16T12:00:00Z"}
        self.assertEqual(m.newest_mac_release(cands, dates.get)["sha"], "b" * 40)
        self.assertIsNone(m.newest_mac_release([], dates.get))


class BehindSince(unittest.TestCase):
    def test_first_parent_walk(self):
        # main: R <- M1 (merge of side S, older date) <- M2 = head
        cs = [commit(H, ["m1"], "2026-11-16T21:00:00Z"),
              commit("m1", ["r", "s"], "2026-11-16T20:00:00Z"),
              commit("s", ["r"], "2026-11-15T09:00:00Z")]
        self.assertEqual(m.behind_since(H, "r", cs), "2026-11-16T20:00:00Z")

    def test_not_behind(self):
        self.assertIsNone(m.behind_since(H, H, []))


class Decide(unittest.TestCase):
    def test_released(self):
        self.assertEqual(m.decide(state(behind=False), {}, NOW)[0], "none")

    def test_pending_lane_run_is_enough(self):
        self.assertEqual(m.decide(state(lane=[{"id": 1, "status": "pending"}]), {}, NOW)[0], "none")
        self.assertEqual(m.decide(state(lane=[{"id": 1, "status": "queued"}]), {}, NOW)[0], "none")

    def test_building_head(self):
        self.assertEqual(m.decide(state(lane=[{"id": 1, "status": "in_progress", "sha": H}]), {}, NOW)[0], "none")

    def test_building_older_queues_newest_without_wait(self):
        self.assertEqual(m.decide(state(lane=[{"id": 1, "status": "in_progress", "sha": "o" * 40}]), {}, NOW)[0],
                         "dispatch")

    def test_idle_lane_looks_ahead(self):
        self.assertEqual(m.decide(state(), {}, NOW)[0], "wait-then-dispatch")

    def test_never_wait_twice_past_the_cap(self):
        prev = {"last_decision": {"capped": True, "behind_since": "2026-11-16T21:50:00Z"}}
        self.assertEqual(m.decide(state(), prev, NOW)[0], "dispatch")
        # a new lag episode (main moved past a newer release) may wait again
        self.assertEqual(m.decide(state(since="2026-11-16T21:55:00Z"), prev, NOW)[0], "wait-then-dispatch")

    def test_no_wait_when_far_behind(self):
        self.assertEqual(m.decide(state(lag=95), {}, NOW)[0], "dispatch")

    def test_recent_failure_of_head_is_not_retried_every_poll(self):
        f = {"id": 9, "sha": H, "at": "2026-11-16T21:00:00Z"}
        self.assertEqual(m.decide(state(failure=f), {}, NOW)[0], "none")
        old = dict(f, at="2026-11-16T10:00:00Z")
        self.assertEqual(m.decide(state(failure=old), {}, NOW)[0], "wait-then-dispatch")


class Landing(unittest.TestCase):
    def pr(self, n, sha, labels=()):
        return {"number": n, "head": {"sha": sha}, "labels": [{"name": l} for l in labels]}

    def test_signals(self):
        a, b, c, d = ("a" * 40, "b" * 40, "c" * 40, "d" * 40)
        prs = [self.pr(1, a, ["landing"]), self.pr(2, b), self.pr(3, c), self.pr(4, d)]
        runs = [
            {"title": f"core {b}", "status": "in_progress", "conclusion": None, "updated_at": "2026-11-16T21:59:00Z", "lean": "success"},
            {"title": f"core {c}", "status": "in_progress", "conclusion": None, "updated_at": "2026-11-16T21:59:00Z", "lean": None},
            {"title": f"core {d} +macOS", "status": "completed", "conclusion": "success", "updated_at": "2026-11-16T21:30:00Z", "lean": None},
        ]
        got = {c["number"] for c in m.landing_candidates(prs, runs, NOW)}
        self.assertEqual(got, {1, 2, 4})
        # green long ago: not about to land
        self.assertEqual({c["number"] for c in m.landing_candidates(prs, runs, NOW, green_min=10)}, {1, 2})

    def test_failed_gate_is_not_a_candidate(self):
        a = "a" * 40
        runs = [{"title": f"core {a}", "status": "completed", "conclusion": "failure",
                 "updated_at": "2026-11-16T21:59:00Z", "lean": None}]
        self.assertEqual(m.landing_candidates([self.pr(5, a)], runs, NOW), [])


if __name__ == "__main__":
    unittest.main()
