"""release-tests.py wpt-merge: a WPT shard with no results is reported with its reason, and the
WPT jobs check out the Hub modules the engine host imports (2026-11-16: two runs had every shard
"missing" because docs/web/hub/foafnaut/host-trace.mjs was not in the sparse checkout)."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('release_tests', ROOT / 'release-tests/release-tests.py')
RT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RT)

PLATFORM = 'linux-x86_64'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(text)


class ShardReasonTests(unittest.TestCase):
    def test_log_cause_finds_the_module_error(self):
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, 'part0.log')
            write(p, 'START /a.html\nerror: Uncaught (in promise) TypeError: Module not found "file:///x/host-trace.mjs".\n'
                     '    at file:///x/native_html_engine.ts:7:29\n')
            self.assertIn('Module not found', RT.log_cause(p))
            self.assertEqual(RT.log_cause(os.path.join(t, 'none.log')), '')

    def test_merge_names_each_missing_shard_and_why(self):
        with tempfile.TemporaryDirectory() as t:
            plan = {'core_commit': 'a' * 40, 'commit_committer_utc': '2026-11-16T00:00:00Z', 'shards': 3, 'kind': 'full',
                    'trigger': 'manual', 'script_engine': 'bubblepop', 'workflow_run_url': 'u',
                    'release_sets': {RT.ENGINE_SET[PLATFORM]: {'tag': 'build-aaaaaaaaaaaa-foafnaut-linux-x86_64'}}}
            write(os.path.join(t, 'plan.json'), json.dumps(plan))
            write(os.path.join(t, 'inputs', 'inputs.json'), json.dumps({'wpt_commit': 'b' * 40, 'denominator': 100, 'names': 30}))
            shards = os.path.join(t, 'shards')
            # Shard 0: the start check failed, with the cause. Shard 1: no artifact at all.
            # Shard 2: an artifact with results is not needed here (no core to score it).
            write(os.path.join(shards, f'wpt-shard-{PLATFORM}-0', 'shard-meta.json'), json.dumps(
                {'index': 0, 'started_utc': '2026-11-16T00:00:00Z',
                 'error': 'start check: no result for /a.html (exit 0): error: Module not found "host-trace.mjs"'}))
            write(os.path.join(shards, f'wpt-shard-{PLATFORM}-2', 'tool.log'), 'Traceback (most recent call last):\n')
            a = argparse.Namespace(plan=os.path.join(t, 'plan.json'), inputs=os.path.join(t, 'inputs'), shards_dir=shards,
                                   core=t, platform=PLATFORM, out=os.path.join(t, 'out'))
            out = io.StringIO()
            env = {k: os.environ.pop(k) for k in ('GITHUB_STEP_SUMMARY', 'GITHUB_RUN_ID') if k in os.environ}
            try:
                with contextlib.redirect_stdout(out):
                    RT.cmd_wpt_merge(a)
            finally:
                os.environ.update(env)
            meta = json.load(open(os.path.join(t, 'out', 'meta.json')))
            why = meta['shards_missing_reasons']
            self.assertIn('Module not found', why['0'])
            self.assertIn('no artifact', why['1'])
            self.assertIn('did not start', why['2'])
            reasons = meta['validity']['reasons']
            self.assertFalse(meta['validity']['valid'])
            self.assertTrue(any(r.startswith('shard 0 missing:') and 'Module not found' in r for r in reasons), reasons)
            self.assertTrue(any(r.startswith('shard 1 missing: no artifact') for r in reasons), reasons)
            # Every planned shard is a row, with what was planned and why it has no results.
            table = meta['shard_table']
            self.assertEqual([x['index'] for x in table], [0, 1, 2])
            self.assertEqual([x['names_planned'] for x in table], [10, 10, 10])
            self.assertEqual(table[1]['status'], 'missing')
            self.assertIn('Module not found', table[0]['cause'])
            self.assertEqual(meta['completeness'], 'none')
            self.assertTrue(reasons[0].startswith('none run: 0 of 3 shards'), reasons)
            # Loud: one GitHub error annotation per missing shard, with the reason.
            notes = [l for l in out.getvalue().splitlines() if l.startswith('::error title=WPT')]
            self.assertEqual(len(notes), 3, out.getvalue())
            self.assertIn('Module not found', notes[0])


class CompletenessTests(unittest.TestCase):
    def test_partial_is_never_valid(self):
        m = {'kind': 'full', 'factoidal_commit': 'a' * 40, 'release_tag': 't', 'wpt_commit': 'b' * 40, 'denominator': 9,
             'shards': 2, 'shards_present': 1, 'shards_missing': [1], 'shards_missing_reasons': {'1': 'no artifact: lost'},
             'names_total': 20, 'names_run': 10}
        self.assertEqual(RT.completeness(m), 'partial')
        r = RT.wpt_validity(m)
        self.assertTrue(r and r[0].startswith('partial run: 1 of 2 shards'), r)
        m.update(shards_present=2, shards_missing=[], names_run=20)
        self.assertEqual(RT.completeness(m), 'complete')
        self.assertEqual(RT.wpt_validity(m), [])

    def test_log_excerpt_is_bounded(self):
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, 'x.log')
            write(p, ''.join(f'line {i}\n' for i in range(1000)))
            e = RT.log_excerpt(p, lines=5)
            self.assertEqual(e.splitlines(), [f'line {i}' for i in range(995, 1000)])
            self.assertLessEqual(len(RT.log_excerpt(p, lines=1000, limit=100)), 100)


class SparseCheckoutTests(unittest.TestCase):
    def test_wpt_jobs_check_out_the_hub_modules(self):
        for wf in ('release-tests.yml', 'branch-wpt.yml'):
            text = (ROOT / '.github/workflows' / wf).read_text()
            blocks = re.findall(r'sparse-checkout: \|\n((?:\s+[^\s:]+\n)+)', text)
            wpt = [b.split() for b in blocks if 'labs/demos/foafnaut' in b.split()]
            self.assertTrue(wpt, wf)
            for b in wpt:
                self.assertIn('docs/web/hub/foafnaut', b, wf)


class RetryWorkflowTests(unittest.TestCase):
    def test_retry_is_bounded_and_skips_all_failed(self):
        text = (ROOT / '.github/workflows/release-tests-retry.yml').read_text()
        self.assertIn("run_attempt == 1", text)          # one retry, never a third attempt
        self.assertIn('"$failed" -eq "$total"', text)     # every shard failed: not retried
        self.assertIn('"Release tests", "Test262", "WPT reftests"', text)
        for wf in ('release-tests.yml', 'test262.yml', 'reftests.yml'):   # a re-run uploads its artifacts again
            t = (ROOT / '.github/workflows' / wf).read_text()
            self.assertGreaterEqual(t.count('overwrite: true'), 2, wf)


if __name__ == '__main__':
    unittest.main()
