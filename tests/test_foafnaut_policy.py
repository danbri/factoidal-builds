"""Packaging controls use synthetic evidence/stub binaries, never build or render."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('policy_package', ROOT / 'scripts/check-foafnaut-policy.py')
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def fixture(root):
    root.mkdir(parents=True, exist_ok=True)
    for name in CHECK.WEB_FILES:
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b'\0asm\x01\0\0\0' if name.endswith('.wasm') else b'fixture')
    (root / 'checked.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100"/><circle cx="5" cy="5" r="5"/></svg>')
    report = {'profile': 'experimental-graph-browser-v1',
              'metric': 'viewport-clipped node bounding boxes; sum of pairwise intersections',
              'timing': 'checked at export; no scheduling claim', 'enforced': True, 'withinBudget': True,
              'policy': {'application': {'minOverlapBps': 300, 'maxOverlapBps': 500, 'minCheckHz': 12, 'maxCheckHz': 16},
                         'configuration': {'overlapBps': 500, 'checkHz': 12}},
              'thresholdBasisPoints': 500, 'targetCheckHz': 12,
              'nodes': [{'person': 0, 'area': 100, 'overlapUpperBound': 0, 'withinBudget': True, 'bounds': [0, 0, 10, 10]}]}
    # Tagged storage header plus a rectangle and circle, with float-valued tags.
    artifact = {'abi': 'lean-svg-v1', 'profile': 'painted-primitives-experiment', 'binding': 'read-only-storage',
                'width': 100, 'height': 100, 'primitiveCount': 2,
                'data': [1, 1, 0, 0, 0, 0, 100, 100] +
                        [0, 0, 100, 100, 1.0, 0.0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0] +
                        [5, 5, 5, 0, 2.0, 0.0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                'wgsl': '@group(0) @binding(0) var<storage,read> params: Params;',
                'checks': [{'x': 5, 'y': 5, 'rgb': [255, 0, 0]}]}
    (root / 'checked.svg.policy.json').write_text(json.dumps(report))
    (root / 'checked-native.json').write_text(json.dumps(artifact))
    return report, artifact


class PolicyEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.report, self.artifact = fixture(self.root)

    def test_complete_export_and_storage_evidence(self):
        result = CHECK.validate(self.root)
        self.assertEqual((result['nodes'], result['primitives'], result['storage_floats']), (1, 2, 48))
        self.assertEqual(result['application']['maxOverlapBps'], 500)
        self.assertEqual(len(result['svg_sha256']), 64)

    def test_policy_mutations_fail_closed(self):
        mutations = [
            lambda r: r.update(enforced=False), lambda r: r.update(withinBudget=False),
            lambda r: r.update(profile='unknown'), lambda r: r.update(timing='guaranteed 12Hz'),
            lambda r: r['policy']['application'].update(minOverlapBps=299),
            lambda r: r['policy']['application'].update(maxOverlapBps=701),
            lambda r: r['policy']['application'].update(minOverlapBps=600),
            lambda r: r['policy']['configuration'].update(overlapBps=700),
            lambda r: r['policy']['configuration'].update(checkHz=24),
            lambda r: r['policy']['configuration'].update(checkHz=True),
            lambda r: r.update(thresholdBasisPoints=700), lambda r: r.update(nodes=[]),
            lambda r: r['nodes'][0].update(area=99), lambda r: r['nodes'][0].update(bounds=[-1, 0, 10, 10]),
            lambda r: r['nodes'][0].update(overlapUpperBound=1),
            lambda r: r['nodes'].append(copy.deepcopy(r['nodes'][0])),
            lambda r: r['nodes'].append(dict(r['nodes'][0], person=1)),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutations.index(mutate)):
                report = copy.deepcopy(self.report)
                mutate(report)
                (self.root / 'checked.svg.policy.json').write_text(json.dumps(report))
                with self.assertRaises(ValueError): CHECK.validate(self.root)

    def test_each_web_asset_is_required(self):
        for name in CHECK.WEB_FILES:
            with self.subTest(asset=name):
                path = self.root / name
                data = path.read_bytes()
                path.unlink()
                with self.assertRaises(ValueError): CHECK.validate(self.root)
                path.write_bytes(data)
        (self.root / 'web/.build/engines/layout-policy-engine.wasm').write_bytes(b'placeholder')
        with self.assertRaises(ValueError): CHECK.validate(self.root)

    def test_storage_and_probe_mutations_rejected(self):
        mutations = [lambda a: a.update(binding='uniform'), lambda a: a.update(abi='wrong'),
                     lambda a: a.update(width=101), lambda a: a.update(primitiveCount=1),
                     lambda a: a.update(data=a['data'][:-4]), lambda a: a['data'].__setitem__(8, float('nan')),
                     lambda a: a['data'].__setitem__(12, 9), lambda a: a['data'].__setitem__(13, 3),
                     lambda a: a.update(wgsl='uniform shader'), lambda a: a.update(checks=[]),
                     lambda a: a['checks'][0].update(x=100), lambda a: a['checks'][0].update(rgb=[256, 0, 0])]
        for mutate in mutations:
            with self.subTest(mutation=mutations.index(mutate)):
                artifact = copy.deepcopy(self.artifact)
                mutate(artifact)
                (self.root / 'checked-native.json').write_text(json.dumps(artifact))
                with self.assertRaises(ValueError): CHECK.validate(self.root)

    def test_duplicate_json_keys_rejected(self):
        path = self.root / 'checked.svg.policy.json'
        path.write_text(path.read_text().replace('"enforced": true', '"enforced": false, "enforced": true'))
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key'): CHECK.validate(self.root)


class PackagingPathTests(unittest.TestCase):
    def exercise(self, capable, missing_web=False):
        with tempfile.TemporaryDirectory(prefix='foaf release control ') as temp:
            root = Path(temp)
            core, output, golden, payload, commands = [root / n for n in ('core', 'output', 'golden', 'payload', 'bin')]
            fixture(golden)
            payload.mkdir(); commands.mkdir()
            if capable:
                shutil.copytree(golden / 'web', payload / 'web')
            if missing_web:
                (payload / 'web/policy_engine.mjs').unlink()
            lab = core / 'labs/demos/foafnaut'
            (lab / '.build').mkdir(parents=True)
            (lab / 'FoafNaut.lean').touch()
            if capable: (lab / 'PolicyBridge.lean').touch()
            (lab / '.build/source-SHA256SUMS').write_text('source fixture\n')
            (lab / '.build/tool-versions.txt').write_text('Lean fixture\n')
            (lab / 'toolchain-versions.env').write_text('EMSCRIPTEN_VERSION=6.0.8\n')
            (lab / 'build-executables.sh').write_text('#!/bin/sh\nmkdir -p "$1"\ncp -R "$TEST_PAYLOAD/." "$1/"\n')
            binary = '''#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
a=sys.argv[1:]; golden=Path(os.environ['TEST_GOLDEN'])
with open(os.environ['TEST_CALLS'],'a') as f:f.write(json.dumps([Path(sys.argv[0]).name]+a)+'\\n')
if '--emit-svg' in a:
 p=Path(a[a.index('--emit-svg')+1]);p.write_bytes((golden/'checked.svg').read_bytes())
 Path(str(p)+'.policy.json').write_bytes((golden/'checked.svg.policy.json').read_bytes())
elif '--emit-artifact' in a:
 p=Path(a[a.index('--emit-artifact')+1])
 if Path(sys.argv[0]).name=='native-webgpu-svg-darwin-arm64' and Path(a[0]).name=='checked.svg':
  assert Path(a[0]).read_bytes()==(golden/'checked.svg').read_bytes()
  p.write_bytes((golden/'checked-native.json').read_bytes())
 else:p.write_text(json.dumps({'width':100,'height':100,'wgsl':'shader','data':[1],'checks':[1]}))
'''
            names = ['native-webgpu-ui-darwin-arm64', 'native-webgpu-lean-darwin-arm64', 'native-webgpu-svg-darwin-arm64']
            for name in names:
                p=payload/name;p.write_text(binary);p.chmod(0o755)
            (payload/'libnative-window.dylib').write_text('fake sidecar')
            (payload/'svg-fixtures').mkdir();(payload/'svg-fixtures/gallery.svg').write_text('<svg/>')
            sums=subprocess.check_output(['shasum','-a','256',*names,'libnative-window.dylib'],cwd=payload)
            (payload/'SHA256SUMS').write_bytes(sums)
            for name in ('deno','xcrun'):
                p=commands/name;p.write_text('#!/bin/sh\necho "tool fixture"\n');p.chmod(0o755)
            env=dict(os.environ,PATH=f'{commands}:{os.environ["PATH"]}',TEST_PAYLOAD=str(payload),
                     TEST_GOLDEN=str(golden),TEST_CALLS=str(root/'calls'))
            result=subprocess.run(['bash',str(ROOT/'scripts/build-foafnaut.sh'),str(core),str(output)],env=env,text=True,capture_output=True)
            calls=[json.loads(line) for line in (root/'calls').read_text().splitlines()]
            saved=(output/'meta/foafnaut-policy.json').exists()
            return result,calls,saved

    def test_older_core_keeps_legacy_packaging_path(self):
        result,calls,saved=self.exercise(False)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertFalse(saved)
        self.assertFalse(any('--emit-svg' in a for a in calls))

    def test_capable_core_exports_and_compiles_same_relocated_svg(self):
        result,calls,saved=self.exercise(True)
        self.assertEqual(result.returncode,0,result.stderr)
        export=next(a for a in calls if '--emit-svg' in a)
        compile_=next(a for a in calls if a[0]=='native-webgpu-svg-darwin-arm64' and Path(a[1]).name=='checked.svg')
        self.assertEqual(export[-1],compile_[1])
        self.assertIn('foafnaut relocation.',export[-1])
        self.assertTrue(saved)

    def test_capable_core_cannot_silently_omit_web_demo(self):
        result,_,saved=self.exercise(True,missing_web=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('missing web asset',result.stdout+result.stderr)
        self.assertFalse(saved)


if __name__ == '__main__':
    unittest.main()
