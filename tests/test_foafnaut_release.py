"""Release controls with fake GitHub/git commands; never publish or fetch."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHA = 'a' * 40
SPEC = importlib.util.spec_from_file_location('core_has_path', ROOT / 'scripts/core-has-path.py')
DETECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DETECT)


class CorePathTests(unittest.TestCase):
    def test_exact_tree_walk(self):
        calls = []
        def fetch(endpoint):
            calls.append(endpoint)
            part = ('labs', 'demos', 'foafnaut', 'build-engines.sh')[len(calls) - 1]
            return {'tree': [{'path': part, 'sha': str(len(calls)),
                              'type': 'blob' if len(calls) == 4 else 'tree', 'mode': '100755'}]}
        self.assertTrue(DETECT.has_path('o/r', SHA, 'labs/demos/foafnaut/build-engines.sh', fetch))
        self.assertEqual(calls, [f'repos/o/r/git/trees/{s}' for s in (SHA, '1', '2', '3')])

    def test_absent_file_is_optional(self):
        self.assertFalse(DETECT.has_path('o/r', SHA, 'labs/demo', lambda _: {'tree': []}))

    def test_api_error_does_not_disable_gate(self):
        def unavailable(_):
            raise subprocess.CalledProcessError(1, ['gh', 'api'])
        with self.assertRaises(subprocess.CalledProcessError):
            DETECT.has_path('o/r', SHA, 'labs/demo', unavailable)

    def test_truncation_does_not_disable_gate(self):
        with self.assertRaises(ValueError):
            DETECT.has_path('o/r', SHA, 'labs/demo', lambda _: {'tree': [], 'truncated': True})

    def test_symlink_is_not_build_script(self):
        self.assertFalse(DETECT.has_path('o/r', SHA, 'build.sh', lambda _: {
            'tree': [{'path': 'build.sh', 'type': 'blob', 'mode': '120000'}]}))


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'scripts', self.root / 'scripts')
        (self.root / 'bin').mkdir()
        self.env = dict(os.environ, PATH=f'{self.root / "bin"}:{os.environ["PATH"]}',
                        INPUT_REF=SHA, SHA=SHA, SHORT=SHA[:12], REF='main',
                        EVENT='workflow_dispatch', FORCE='false', GITHUB_REPOSITORY='test/builds',
                        GITHUB_RUN_ID='123', GITHUB_OUTPUT=str(self.root / 'outputs'),
                        TEST_LOG=str(self.root / 'gh.jsonl'), TEST_FOAF='true', TEST_STATUS='identical')
        self.command('gh', '''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
a = sys.argv[1:]
with open(os.environ['TEST_LOG'], 'a') as f: f.write(json.dumps(a)+'\\n')
if a[0] == 'api':
    if os.environ.get('TEST_API_FAIL') == '1': sys.exit(2)
    if '/compare/' in a[1]: print(os.environ['TEST_STATUS'])
    else:
        rev = a[1].split('/')[-1]
        parts = ['labs', 'demos', 'foafnaut', 'build-engines.sh']
        index = int(rev) if len(rev) == 1 else 0
        tree = [] if os.environ['TEST_FOAF'] == 'false' else [{
            'path':parts[index], 'sha':str(index+1), 'type':'blob' if index==3 else 'tree', 'mode':'100755'}]
        print(json.dumps({'tree':tree}))
elif a[:2] == ['release','view']:
    if os.environ.get('TEST_EXISTING') == 'all': print('2020-01-01T00:00:00Z')
    elif os.environ.get('TEST_EXISTING') == 'legacy' and not a[2].endswith('foafnaut-darwin-arm64'):
        print('2020-01-01T00:00:00Z')
    else: sys.exit(1)
elif a[:2] != ['release','create']: sys.exit('Unexpected gh command: '+repr(a))
''')
        self.command('git', '''#!/usr/bin/env python3
import sys
from pathlib import Path
a = sys.argv[1:]
if a[:2] == ['worktree','add']: Path(a[-2]).mkdir(parents=True)
''')

    def command(self, name, source):
        path = self.root / 'bin' / name
        path.write_text(source)
        path.chmod(0o755)

    def run_script(self, name, **environment):
        return subprocess.run(['bash', f'scripts/{name}'], cwd=self.root,
                              env=dict(self.env, **environment), text=True, capture_output=True)

    def test_resolver_old_core_keeps_three_sets(self):
        result = self.run_script('resolve-core.sh', TEST_FOAF='false', TEST_EXISTING='legacy')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('proceed=false', (self.root / 'outputs').read_text())
        self.assertIn('foafnaut=false', (self.root / 'outputs').read_text())

    def test_resolver_retries_missing_demo_set(self):
        result = self.run_script('resolve-core.sh', TEST_EXISTING='legacy')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('proceed=true', (self.root / 'outputs').read_text())
        self.assertIn('foafnaut=true', (self.root / 'outputs').read_text())

    def test_resolver_skips_complete_four_sets(self):
        result = self.run_script('resolve-core.sh', TEST_EXISTING='all')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('proceed=false', (self.root / 'outputs').read_text())

    def test_resolver_api_failure_is_error(self):
        result = self.run_script('resolve-core.sh', TEST_API_FAIL='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'outputs').exists())

    def test_pr_head_never_publishes(self):
        result = self.run_script('publish.sh', TEST_STATUS='ahead', FOAFNAUT='true')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('nothing published', result.stdout)
        self.assertFalse((self.root / 'release-out').exists())

    def test_failed_demo_job_withholds_its_release(self):
        result = self.run_script('publish.sh', FOAFNAUT='true')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('foafnaut-darwin-arm64 not published: missing artifacts', result.stdout)
        self.assertNotIn('"create"', (self.root / 'gh.jsonl').read_text())

    def test_demo_archive_provenance_and_permissions(self):
        stage = self.root / 'art/foafnaut-darwin-arm64/stage/foafnaut'
        stage.mkdir(parents=True)
        (stage / 'Native Demos.command').write_text('#!/bin/sh\necho demo\n')
        (stage / 'engine').write_bytes(b'\xcf\xfa\xed\xfe' + b'compiled fixture')
        (stage / 'gallery.svg').write_text('<svg/>')
        meta = stage.parents[1] / 'meta'
        meta.mkdir()
        (meta / 'toolchains-foafnaut.json').write_text('{"deno":"2.9.4"}')
        result = self.run_script('publish.sh', FOAFNAUT='true')
        # The demo set can publish while absent unrelated sets keep the run red.
        self.assertEqual(result.returncode, 1, result.stderr)
        out = self.root / 'release-out/foafnaut-darwin-arm64'
        info = json.loads((out / 'build-info.json').read_text())
        self.assertEqual(info['source_commit'], SHA)
        self.assertEqual(info['toolchains']['deno'], '2.9.4')
        archive = out / 'foafnaut-darwin-arm64.tar.gz'
        manifest = info['artifacts'][archive.name]
        self.assertEqual(manifest['sha256'], hashlib.sha256(archive.read_bytes()).hexdigest())
        with tarfile.open(archive) as tf:
            for member in tf:
                self.assertEqual(hashlib.sha256(tf.extractfile(member).read()).hexdigest(),
                                 manifest['files'][member.name]['sha256'])
                self.assertEqual(member.mode, 0o644 if member.name.endswith('.svg') else 0o755)
        commands = [json.loads(line) for line in (self.root / 'gh.jsonl').read_text().splitlines()]
        creates = [a for a in commands if a[:2] == ['release', 'create']]
        self.assertEqual(len(creates), 1)
        self.assertEqual(creates[0][2], f'build-{SHA[:12]}-foafnaut-darwin-arm64')
        pointer = json.loads((self.root / 'release-out/latest-foafnaut-darwin-arm64.json').read_text())
        self.assertEqual(pointer['source_commit'], SHA)


if __name__ == '__main__':
    unittest.main()
