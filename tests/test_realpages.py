"""release-tests/realpages.py: release sets, and record on a local results branch (no push, no network)."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('realpages', ROOT / 'release-tests/realpages.py')
RP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RP)


def git(*args, cwd):
    subprocess.run(['git', '-c', 'user.name=t', '-c', 'user.email=t@t', *args], cwd=cwd, check=True, capture_output=True)


class RealpagesTests(unittest.TestCase):
    def test_sets(self):
        self.assertEqual(RP.set_of('build-cc73af028afe-foafnaut-darwin-arm64'), 'foafnaut-darwin-arm64')
        self.assertEqual(RP.set_of('build-6efc9cffbee3-foafnaut-linux-x86_64'), 'foafnaut-linux-x86_64')
        self.assertFalse(RP.set_of('build-6efc9cffbee3-foafnaut-web'))
        self.assertFalse(RP.set_of('test-results'))

    def test_record_rotates_latest_and_appends_trend_once(self):
        with tempfile.TemporaryDirectory() as t:
            origin, repo = os.path.join(t, 'origin.git'), os.path.join(t, 'repo')
            subprocess.run(['git', 'init', '-q', '--bare', origin], check=True)
            git('clone', '-q', origin, repo, cwd=t)
            Path(repo, 'runs.csv').write_text('run_id\n')
            git('add', '-A', cwd=repo); git('commit', '-qm', 'x', cwd=repo); git('push', '-q', 'origin', 'HEAD:refs/heads/wpt-scores', cwd=repo)

            def survey(release, run):
                src = os.path.join(tempfile.mkdtemp(dir=t), 'realpages-macos-summary')
                os.makedirs(src)
                Path(src, 'summary-macos.json').write_text(json.dumps({'release': release, 'pages': []}))
                Path(src, 'trend-macos.csv').write_text(f'run_id,platform,page\n{run},macos,hn\n{run},macos,wp-stub\n')
                os.environ['GITHUB_RUN_ID'] = run
                RP.cmd_record(type('A', (), {'src': os.path.dirname(src), 'repo': repo, 'no_push': False})())

            survey('build-a-foafnaut-darwin-arm64', '1')
            survey('build-b-foafnaut-darwin-arm64', '2')
            survey('build-b-foafnaut-darwin-arm64', '2')  # the same run again adds no rows
            out = os.path.join(t, 'out')
            git('clone', '-q', '-b', 'wpt-scores', origin, out, cwd=t)
            d = Path(out, 'realpages')
            self.assertEqual(json.loads((d / 'latest-macos.json').read_text())['release'], 'build-b-foafnaut-darwin-arm64')
            self.assertEqual(json.loads((d / 'previous-macos.json').read_text())['release'], 'build-a-foafnaut-darwin-arm64')
            rows = (d / 'trend.csv').read_text().splitlines()
            self.assertEqual(rows, ['run_id,platform,page', '1,macos,hn', '1,macos,wp-stub', '2,macos,hn', '2,macos,wp-stub'])
            self.assertTrue((d / 'runs' / '2' / 'macos.json').exists())
            self.assertTrue(Path(out, 'runs.csv').exists())


if __name__ == '__main__':
    unittest.main()
