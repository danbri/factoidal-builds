"""release-tests.py: the lean-xml group's rows (xml_score) from the lanes' scoreboard JSON: the
QT4 totals (empty label), one row per qt4tests family and the XSLT 4.0 streaming directory
(label "family F"), and nothing at all when the group did not run."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('release_tests', ROOT / 'release-tests/release-tests.py')
RT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RT)

PLAN = {"trigger": "manual", "core_commit": "c" * 40, "commit_committer_utc": "2026-11-17T00:00:00Z",
        "release_sets": {"linux-x86_64": {"tag": "build-cccccccccccc-x"}}, "workflow_run_url": "u"}


def row(job, label, p, f, o):
    return {"job": job, "label": label, "status": "ok", "pass": p, "fail": f, "other": o, "total": p + f + o}


class XmlRows(unittest.TestCase):
    def score(self, rows, lanes=True):
        with tempfile.TemporaryDirectory() as d:
            if lanes is not None:
                os.makedirs(os.path.join(d, "xml"))
                st = {f"lane-{i}": {"started_utc": "a", "finished_utc": "b", "exit": 0} for i in range(len(RT.XML_LANES))}
                json.dump(st, open(os.path.join(d, "xml", "status.json"), "w"))
                if rows is not None:
                    json.dump({"rows": rows}, open(os.path.join(d, "xml", "scoreboard.json"), "w"))
            out, _ = RT.xml_score(PLAN, d)
        return {r["suite"]: r for r in out}

    def test_no_rows_when_the_group_did_not_run(self):
        self.assertEqual(self.score(None, lanes=None), {})

    def test_totals_and_families(self):
        sb = [row("l4qt4-xquery", "", 90, 5, 5), row("l4qt4-xquery", "family fn", 40, 2, 3),
              row("l4qt4-xquery", "family xs", 10, 0, 1), row("l4xslt4", "", 50, 4, 6), row("l4xslt4", "family strm", 7, 1, 2)]
        got = self.score(sb)
        self.assertEqual(len(got), len(RT.XML_ROWS))
        self.assertEqual((got["l4-qt4-xquery"]["passed"], got["l4-qt4-xquery"]["denominator"], got["l4-qt4-xquery"]["valid"]), (90, 100, "true"))
        self.assertEqual((got["l4-qt4-xquery-fn"]["passed"], got["l4-qt4-xquery-fn"]["denominator"]), (40, 45))
        self.assertEqual((got["l4-xslt4"]["passed"], got["l4-xslt4-strm"]["passed"]), (50, 7))
        # A family the run did not report is an invalid row with its reason, never a score.
        self.assertEqual(got["l4-qt4-xquery-upd"]["valid"], "false")
        self.assertIn("0 rows match", got["l4-qt4-xquery-upd"]["invalid_reason"])

    def test_no_scoreboard_json(self):
        got = self.score(None)
        self.assertTrue(all(r["valid"] == "false" for r in got.values()))
        self.assertIn("no scoreboard JSON", got["l4-c14n"]["invalid_reason"])


if __name__ == '__main__':
    unittest.main()
