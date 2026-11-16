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
                        TEST_LOG=str(self.root / 'gh.jsonl'), TEST_FOAF='true',
                        TEST_SVG_STROKE='false', TEST_SVG_PAGE='false', TEST_STATUS='identical')
        self.command('gh', '''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
a = sys.argv[1:]
with open(os.environ['TEST_LOG'], 'a') as f: f.write(json.dumps(a)+'\\n')
if a[0] == 'api':
    if os.environ.get('TEST_API_FAIL') == '1': sys.exit(2)
    if '/compare/' in a[1]:
        base = a[1].split('/compare/')[1].split('...')[0]
        if base == os.environ['SHA'] and 'TEST_POINTER_STATUS' in os.environ:
            print(os.environ['TEST_POINTER_STATUS'])
        else: print(os.environ['TEST_STATUS'])
    else:
        choices = [
            ('TEST_FOAF', 'labs/demos/foafnaut/build-engines.sh'),
            ('TEST_SVG_STROKE', 'labs/demos/foafnaut/SVGStroke.lean'),
            ('TEST_SVG_PAGE', 'docs/web/hub/svg-webgpu/index.njk'),
            ('TEST_HTML_PAGE', 'docs/web/hub/html-webgpu/index.njk'),
            ('TEST_HTML_ENGINE', 'labs/demos/foafnaut/WebRender.lean'),
            ('TEST_HTML_BUILD', 'labs/demos/foafnaut/build-web-render.sh'),
        ]
        import hashlib
        paths = [path for key,path in choices if os.environ.get(key) == 'true']
        prefixes = {''}
        for path in paths:
            parts = path.split('/')
            prefixes.update('/'.join(parts[:i]) for i in range(1,len(parts)))
        identity = lambda prefix: os.environ['SHA'] if not prefix else hashlib.sha1(prefix.encode()).hexdigest()
        prefix = next((p for p in prefixes if identity(p) == a[1].split('/')[-1]), None)
        if prefix is None: sys.exit('Unknown tree')
        children = {}
        for path in paths:
            parent = prefix+'/' if prefix else ''
            if not path.startswith(parent): continue
            tail = path[len(parent):]
            name = tail.split('/')[0]
            full = parent+name
            children[name] = {'path':name, 'sha':identity(full),
                'type':'tree' if '/' in tail else 'blob', 'mode':'040000' if '/' in tail else '100755'}
        print(json.dumps({'tree':list(children.values())}))
elif a[:2] == ['release','view']:
    if os.environ.get('TEST_EXISTING') == 'all': print('2020-01-01T00:00:00Z')
    elif os.environ.get('TEST_EXISTING') == 'legacy' and not a[2].endswith(('foafnaut-darwin-arm64','foafnaut-web')):
        print('2020-01-01T00:00:00Z')
    else: sys.exit(1)
elif a[:2] != ['release','create']: sys.exit('Unexpected gh command: '+repr(a))
''')
        self.command('git', '''#!/usr/bin/env python3
import sys
from pathlib import Path
a = sys.argv[1:]
import os, shutil
if a[:2] == ['worktree','add']:
    Path(a[-2]).mkdir(parents=True)
    seed = os.environ.get('TEST_POINTER_SEED')
    if seed: shutil.copytree(seed, Path(a[-2]) / 'latest')
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
        self.assertIn('foafnaut_web=false', (self.root / 'outputs').read_text())

    def test_resolver_retries_missing_demo_set(self):
        result = self.run_script('resolve-core.sh', TEST_EXISTING='legacy',
                                 TEST_SVG_STROKE='true', TEST_SVG_PAGE='true')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('proceed=true', (self.root / 'outputs').read_text())
        self.assertIn('foafnaut=true', (self.root / 'outputs').read_text())
        self.assertIn('foafnaut_web=true', (self.root / 'outputs').read_text())

    def test_resolver_rejects_page_without_svg_engine(self):
        result = self.run_script('resolve-core.sh', TEST_SVG_PAGE='true')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('page exists without the Lean SVGStroke', result.stdout)

    def test_html_alone_enables_browser_release(self):
        result = self.run_script('resolve-core.sh', TEST_EXISTING='legacy',
            TEST_HTML_PAGE='true', TEST_HTML_ENGINE='true', TEST_HTML_BUILD='true')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('foafnaut_web=true', (self.root / 'outputs').read_text())
        self.assertIn('proceed=true', (self.root / 'outputs').read_text())

    def test_html_page_requires_lean_engine_and_builder(self):
        for engine,builder in [('false','true'),('true','false')]:
            with self.subTest(engine=engine,builder=builder):
                result = self.run_script('resolve-core.sh', TEST_HTML_PAGE='true',
                    TEST_HTML_ENGINE=engine, TEST_HTML_BUILD=builder)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('HTML browser page exists without', result.stdout)

    def test_resolver_skips_complete_sets(self):
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

    def test_existing_release_is_never_replaced(self):
        stage = self.root / 'art/foafnaut-darwin-arm64/stage/foafnaut'
        stage.mkdir(parents=True)
        (stage / 'gallery.svg').write_text('<svg/>')
        meta = stage.parents[1] / 'meta'
        meta.mkdir()
        (meta / 'toolchains-foafnaut.json').write_text('{"deno":"2.9.4"}')
        result = self.run_script('publish.sh', FOAFNAUT='true', TEST_EXISTING='all')
        commands = [json.loads(line) for line in (self.root / 'gh.jsonl').read_text().splitlines()]
        self.assertFalse([a for a in commands if a[:2] in (['release', 'create'], ['release', 'delete'])])
        self.assertIn('foafnaut-darwin-arm64: release build-', result.stdout)
        self.assertIn('kept (already published): foafnaut-darwin-arm64', result.stdout)
        self.assertFalse((self.root / 'release-out/latest-foafnaut-darwin-arm64.json').exists())

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

    def test_svg_runtime_is_finalized_only_inside_main_release_set(self):
        from hashlib import sha256
        files = ['svg_engine.mjs', 'gpu_transport.mjs', 'render_plan.mjs', 'finite_floats.mjs',
                 'engines/svg-engine.mjs', 'engines/svg-engine.wasm',
                 'engines/render-plan.mjs', 'engines/render-plan.wasm']
        root = self.root / 'art/foafnaut-web/stage/docs/web/hub/svg-webgpu/runtime'
        rows = []
        for name in files:
            body = b'\0asm\x01\0\0\0x' if name.endswith('.wasm') else f'fixture {name}'.encode()
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            rows.append({'path':name,'bytes':len(body),'sha256':sha256(body).hexdigest()})
        (root / 'provenance.json').write_text(json.dumps({
            'format':'factoidal-svg-webgpu-runtime-v1','kind':'development','sourceCommit':SHA,
            'files':rows,'evidence':{'qualification':'development only'}}))
        html = self.root / 'art/foafnaut-web/stage/docs/web/hub/html-webgpu/runtime'
        html.mkdir(parents=True)
        html_rows = []
        for name in ['web-render.mjs','web-render.wasm','render-plan.mjs','render-plan.wasm',
                     'gpu-transport.mjs','render-plan-host.mjs','finite-floats.mjs','source-witness.json']:
            body = b'\0asm\x01\0\0\0x' if name.endswith('.wasm') else f'fixture {name}'.encode()
            (html / name).write_bytes(body)
            html_rows.append({'path':name,'bytes':len(body),'sha256':sha256(body).hexdigest()})
        (html / 'manifest.json').write_text(json.dumps({
            'format':'factoidal-html-webgpu-runtime-v1','kind':'development','sourceCommit':SHA,
            'files':html_rows,'evidence':{'qualification':'development only'}}))
        meta = self.root / 'art/foafnaut-web/meta'
        meta.mkdir(parents=True)
        (meta / 'toolchains-foafnaut-web.json').write_text('{"lean":"test","emscripten":"test"}')
        hygiene = {'counts': {'lab': {'unsafe': 29}}, 'commit': SHA, 'theorem': 'lab_ratchet'}
        (meta / 'hygiene.json').write_text(json.dumps(hygiene))
        result = self.run_script('publish.sh', FOAFNAUT='false', FOAFNAUT_WEB='true',
                                 GITHUB_REPOSITORY='danbri/factoidal-builds')
        self.assertEqual(result.returncode, 1, result.stderr)
        out = self.root / 'release-out/foafnaut-web'
        info = json.loads((out / 'build-info.json').read_text())
        self.assertEqual(info['source_commit'], SHA)
        self.assertEqual(info['hygiene'], hygiene)
        creates = [json.loads(line) for line in (self.root / 'gh.jsonl').read_text().splitlines()
                   if json.loads(line)[:2] == ['release','create']]
        self.assertEqual([cmd[2] for cmd in creates], [f'build-{SHA[:12]}-foafnaut-web'])
        archive = out / 'foafnaut-web.tar.gz'
        with tarfile.open(archive) as tf:
            manifest = json.load(tf.extractfile('docs/web/hub/svg-webgpu/runtime/provenance.json'))
            html_manifest = json.load(tf.extractfile('docs/web/hub/html-webgpu/runtime/manifest.json'))
        self.assertEqual(manifest['kind'], 'release')
        self.assertEqual(html_manifest['kind'], 'release')
        self.assertIn('/actions/runs/123', html_manifest['evidence']['releaseBuildRun'])
        self.assertIn('/actions/runs/123', manifest['evidence']['releaseBuildRun'])

    def test_foafnaut_web_without_hygiene_is_not_published(self):
        (self.root / 'art/foafnaut-web/stage').mkdir(parents=True)
        (self.root / 'art/foafnaut-web/meta').mkdir(parents=True)
        result = self.run_script('publish.sh', FOAFNAUT='false', FOAFNAUT_WEB='true',
                                 GITHUB_REPOSITORY='danbri/factoidal-builds')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('foafnaut-web not published: the engine build record has no hygiene field',
                      result.stdout + result.stderr)
        self.assertFalse((self.root / 'release-out/foafnaut-web/build-info.json').exists())

    # Split publishing (2026-11-16): build.yml's `publish` job publishes the Linux-built sets
    # without waiting for macOS runners; `publish-macos` publishes the macOS sets later.
    LINUX_SETS = 'linux-x86_64 web foafnaut-web'
    MACOS_SETS = 'darwin-arm64 foafnaut-darwin-arm64'

    def stage_set(self, artifact, toolchains):
        stage = self.root / 'art' / artifact / 'stage' / 'bin'
        stage.mkdir(parents=True)
        (stage / 'tool').write_text(f'fixture {artifact}')
        meta = self.root / 'art' / artifact / 'meta'
        meta.mkdir()
        (meta / toolchains).write_text('{"lean":"test"}')

    def stage_linux_and_web(self):
        self.stage_set('lean-linux-x86_64', 'toolchains-lean-linux-x86_64.json')
        self.stage_set('lean-wasm', 'toolchains-lean-wasm.json')
        (self.root / 'art/web-gates').mkdir(parents=True)

    def created(self):
        log = self.root / 'gh.jsonl'
        rows = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        return [a[2] for a in rows if a[:2] == ['release', 'create']]

    def test_linux_job_publishes_web_before_macos_artifacts_exist(self):
        self.stage_linux_and_web()
        result = self.run_script('publish.sh', FOAFNAUT='true', PUBLISH_SETS=self.LINUX_SETS)
        # Green: the absent macOS artifacts are not this job's sets.
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.created(), [f'build-{SHA[:12]}-linux-x86_64', f'build-{SHA[:12]}-web'])
        self.assertNotIn('darwin', result.stdout)
        self.assertTrue((self.root / 'release-out/pointer-1/latest/web.json').exists())
        self.assertFalse((self.root / 'release-out/pointer-1/latest/darwin-arm64.json').exists())

    def test_linux_job_never_publishes_macos_sets(self):
        self.stage_linux_and_web()
        self.stage_set('lean-darwin-arm64', 'toolchains-lean-darwin-arm64.json')
        self.stage_set('foafnaut-darwin-arm64', 'toolchains-foafnaut.json')
        result = self.run_script('publish.sh', FOAFNAUT='true', PUBLISH_SETS=self.LINUX_SETS)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse([t for t in self.created() if 'darwin' in t])

    def test_macos_job_publishes_only_macos_sets(self):
        self.stage_linux_and_web()
        self.stage_set('lean-darwin-arm64', 'toolchains-lean-darwin-arm64.json')
        self.stage_set('foafnaut-darwin-arm64', 'toolchains-foafnaut.json')
        result = self.run_script('publish.sh', FOAFNAUT='true', PUBLISH_SETS=self.MACOS_SETS)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.created(), [f'build-{SHA[:12]}-darwin-arm64',
                                          f'build-{SHA[:12]}-foafnaut-darwin-arm64'])

    def test_macos_job_red_when_its_gate_failed(self):
        self.stage_set('foafnaut-darwin-arm64', 'toolchains-foafnaut.json')
        result = self.run_script('publish.sh', FOAFNAUT='true', PUBLISH_SETS=self.MACOS_SETS)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('darwin-arm64 not published: missing artifacts', result.stdout)
        self.assertEqual(self.created(), [f'build-{SHA[:12]}-foafnaut-darwin-arm64'])

    def test_the_two_jobs_never_replace_a_release(self):
        self.stage_linux_and_web()
        result = self.run_script('publish.sh', FOAFNAUT='true', PUBLISH_SETS=self.LINUX_SETS,
                                 TEST_EXISTING='all')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.created(), [])
        self.assertIn('kept (already published): linux-x86_64 web', result.stdout)

    def test_unknown_publish_set_is_an_error(self):
        result = self.run_script('publish.sh', PUBLISH_SETS='web darwin')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unknown set: darwin', result.stdout)
        self.assertEqual(self.created(), [])

    def seed_pointer(self, source_commit):
        seed = self.root / 'seed'
        seed.mkdir()
        (seed / 'web.json').write_text(json.dumps({'set': 'web', 'source_commit': source_commit}))
        return str(seed)

    def test_pointer_never_moves_back_to_an_older_commit(self):
        self.stage_linux_and_web()
        newer = 'b' * 40
        result = self.run_script('publish.sh', PUBLISH_SETS='web', TEST_POINTER_SEED=self.seed_pointer(newer),
                                 TEST_POINTER_STATUS='ahead')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.created(), [f'build-{SHA[:12]}-web'])
        self.assertIn('latest/web.json kept', result.stdout)
        pointer = json.loads((self.root / 'release-out/pointer-1/latest/web.json').read_text())
        self.assertEqual(pointer['source_commit'], newer)

    def test_pointer_moves_forward(self):
        self.stage_linux_and_web()
        for status in ('behind', 'diverged'):
            with self.subTest(status=status):
                shutil.rmtree(self.root / 'release-out', ignore_errors=True)
                shutil.rmtree(self.root / 'seed', ignore_errors=True)
                result = self.run_script('publish.sh', PUBLISH_SETS='web',
                                         TEST_POINTER_SEED=self.seed_pointer('c' * 40),
                                         TEST_POINTER_STATUS=status)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                pointer = json.loads((self.root / 'release-out/pointer-1/latest/web.json').read_text())
                self.assertEqual(pointer['source_commit'], SHA)


class WorkflowSplitTests(unittest.TestCase):
    """build.yml: the web release must not wait for a macOS job (text checks; no YAML parser)."""

    def job(self, name):
        text = (ROOT / '.github/workflows/build.yml').read_text()
        start = text.index(f'\n  {name}:\n') + 1
        rest = text[start + 3:]
        import re
        m = re.search(r'\n  [a-z][a-z0-9-]*:\n', rest)
        return text[start:start + 3 + (m.start() if m else len(rest))]

    def needs(self, name):
        import re
        line = re.search(r'^    needs: \[(.*)\]$', self.job(name), re.M).group(1)
        return {n.strip() for n in line.split(',')}

    def sets(self, name):
        import re
        return set(re.search(r'PUBLISH_SETS: (.*)$', self.job(name), re.M).group(1).split())

    def test_web_publish_needs_no_macos_job(self):
        self.assertEqual(self.needs('publish'), {'resolve', 'lean', 'lean-wasm', 'web-gates',
                                                 'foafnaut-engines', 'foafnaut-host-tests'})
        self.assertNotIn('runs-on: ${{ fromJSON', self.job('publish'))

    def test_macos_publish_needs_the_macos_jobs(self):
        self.assertEqual(self.needs('publish-macos'), {'resolve', 'lean-macos', 'foafnaut'})
        self.assertIn("needs.resolve.outputs.macos == 'true'", self.job('publish-macos'))

    def test_every_set_has_exactly_one_publish_job(self):
        linux, mac = self.sets('publish'), self.sets('publish-macos')
        self.assertFalse(linux & mac)
        self.assertEqual(linux | mac, {'linux-x86_64', 'web', 'foafnaut-web',
                                       'darwin-arm64', 'foafnaut-darwin-arm64'})
        self.assertFalse([s for s in linux if 'darwin' in s])

    def test_reports_wait_for_both_publish_jobs(self):
        for job in ('metrics', 'nightly-report'):
            self.assertTrue({'publish', 'publish-macos'} <= self.needs(job), job)


if __name__ == '__main__':
    unittest.main()
