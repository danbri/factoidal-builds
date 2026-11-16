"""release-tests/reftests.py: the sparse WPT paths of a suite, and scoring shard results (no network)."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('reftests', ROOT / 'release-tests/reftests.py')
RF = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RF)

MANIFEST = {"version": 9, "url_base": "/", "items": {"reftest": {
    "svg": {"a.svg": ["h", [None, [["/svg/a-ref.svg", "=="]], {}]],
            "painting": {"b.html": ["h", [None, [["/css/reference/green.html", "=="]], {}]]}},
    "css": {"reference": {"green.html": ["h", [None, [["/css/reference/ref2.html", "=="]], {}]]}}}}}


def shard(k, n, tests):
    return {"shard": [k, n], "startedAt": "2026-11-15T22:00:00Z", "finishedAt": "2026-11-15T22:10:00Z", "wallSeconds": 600,
            "pagesDrawn": 4, "engine": {"sha256": "x"},
            "tests": [{"test": t, "status": s, "edges": [{"to": "/r", "relation": "==", "maxDifference": 9, "totalPixels": 3, "holds": s == "PASS"}],
                       "ms": 10, "message": None} for t, s in tests]}


class ReftestsTests(unittest.TestCase):
    def test_paths_cover_the_suite_its_references_and_chains(self):
        with tempfile.TemporaryDirectory() as t:
            m = os.path.join(t, "MANIFEST.json")
            json.dump(MANIFEST, open(m, "w"))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                RF.cmd_paths(type("A", (), {"manifest": m, "suite": "svg"}))
            lines = out.getvalue().split()
            self.assertIn("/svg/", lines)
            self.assertIn("/css/reference/", lines)
            self.assertIn("/fonts/", lines)
            self.assertNotIn("/svg/painting/", lines, "inside /svg/")

    def test_score_joins_shards_rivals_and_validity(self):
        with tempfile.TemporaryDirectory() as t:
            json.dump({"x/a": 1}, open(os.path.join(t, "MANIFEST.json"), "w"))
            json.dump({"/svg/a.svg": {"s": "P"}, "/svg/b.html": {"s": "P"}, "/svg/c.svg": {"s": "F"}}, open(os.path.join(t, "chrome-summary.json"), "w"))
            plan = {"release_tag": "build-0123456789ab-foafnaut-linux-x86_64", "core_commit": "0123456789ab" + "0" * 28,
                    "commit_utc": "2026-11-15T21:00:00Z", "web_tag": "w", "wpt_commit": "f" * 40, "suites": ["svg"], "trigger": "manual",
                    "rivals": {"chrome": {"status": "ok", "version": "157", "run_id": 5, "summary": "chrome-summary.json"},
                               "edge": {"status": "unavailable", "reason": "no stable run"}}}
            json.dump(plan, open(os.path.join(t, "plan.json"), "w"))
            sd = os.path.join(t, "shards", "s0")
            os.makedirs(sd)
            json.dump(shard(0, 1, [("/svg/a.svg", "PASS"), ("/svg/b.html", "FAIL"), ("/svg/c.svg", "TIMEOUT")]), open(os.path.join(sd, "results.json"), "w"))
            RF.rt.read_csv_url = lambda name: []
            out = os.path.join(t, "out")
            with contextlib.redirect_stdout(io.StringIO()):
                RF.cmd_score(type("A", (), {"plan": os.path.join(t, "plan.json"), "suite": "svg", "shards_dir": os.path.join(t, "shards"),
                                            "out": out, "run_url": "u"}))
            row = json.load(open(os.path.join(out, "row.json")))
            meta = json.load(open(os.path.join(out, "meta.json")))
            self.assertEqual((row["suite"], row["passed"], row["denominator"], row["valid"]), ("wpt-reftest-svg", 1, 3, "true"))
            self.assertEqual(row["timeout"], 1)
            self.assertEqual(meta["totals"]["chrome_passed"], 2)
            self.assertEqual(meta["totals"]["chrome_passes_we_fail"], 1)
            self.assertEqual([r["status"] for r in meta["rivals"]], ["ok", "unavailable"])
            tsv = open(os.path.join(out, "results.tsv")).read().splitlines()
            self.assertEqual(tsv[0].split("\t")[:3], ["test", "status", "chrome"])
            self.assertEqual(len(tsv), 4)

    def test_a_missing_shard_or_harness_errors_make_a_run_invalid(self):
        with tempfile.TemporaryDirectory() as t:
            plan = {"release_tag": "r", "core_commit": "0" * 40, "commit_utc": "2026-11-15T21:00:00Z", "wpt_commit": "f" * 40,
                    "trigger": "manual", "rivals": {}}
            json.dump(plan, open(os.path.join(t, "plan.json"), "w"))
            sd = os.path.join(t, "shards", "s0")
            os.makedirs(sd)
            json.dump(shard(0, 16, [("/css/a.html", "PASS"), ("/css/b.html", "ERROR")]), open(os.path.join(sd, "results.json"), "w"))
            RF.rt.read_csv_url = lambda name: []
            out = os.path.join(t, "out")
            with contextlib.redirect_stdout(io.StringIO()):
                RF.cmd_score(type("A", (), {"plan": os.path.join(t, "plan.json"), "suite": "css", "shards_dir": os.path.join(t, "shards"),
                                            "out": out, "run_url": ""}))
            row = json.load(open(os.path.join(out, "row.json")))
            self.assertEqual(row["valid"], "false")
            self.assertIn("1 of 16 shards", row["invalid_reason"])
            self.assertIn("ERROR 1 of 2", row["invalid_reason"])


if __name__ == "__main__":
    unittest.main()
