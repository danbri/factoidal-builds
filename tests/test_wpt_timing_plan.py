import gzip
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

RELEASE_TESTS = Path(__file__).resolve().parents[1] / "release-tests"


def load_script(name, file):
    spec = importlib.util.spec_from_file_location(name, RELEASE_TESTS / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


timing = load_script("wpt_timing_plan", "wpt_timing_plan.py")
release_tests = load_script("release_tests", "release-tests.py")


class TimingPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.names = [f"/a/test-{i:03}.html?variant=x" for i in range(95)]
        self.raw = timing.list_bytes(self.names)
        self.full_sha = timing.digest(self.raw)
        self.release = "f" * 40
        (self.directory / "full.list").write_bytes(self.raw)
        self.timing = self.directory / "historical.json.gz"
        source = {
            "format": timing.TIMING_FORMAT,
            "sources": [{"workflow_run_id": 10}],
            "platform": timing.PLATFORM,
            "script_engine": timing.ENGINE,
            "default_half_ms": 200,
            "weights_half_ms": {name: 700_000 - i * 1000 for i, name in enumerate(self.names[:4])},
        }
        self.timing.write_bytes(gzip.compress(json.dumps(source).encode(), mtime=0))
        self.timing_sha = timing.digest(self.timing.read_bytes())

    def create(self):
        plan_sha = timing.create(self.directory, self.timing, self.timing_sha, self.full_sha, self.release)
        return {"timing_plan_sha256": plan_sha, "wpt_commit": self.release, "full_list_sha256": self.full_sha}

    def test_exact_list_and_original_worker_capacity(self):
        options = self.create()
        lists, manifest = timing.load(self.directory, options, self.names, 12, 3)
        self.assertEqual(options, self.create())
        self.assertCountEqual(self.names, [name for shard in lists for name in shard])
        self.assertEqual(manifest["names_without_timing"], 91)
        self.assertEqual(manifest["timing_sha256"], self.timing_sha)
        self.assertEqual((self.directory / "wpt-timing-source.json.gz").read_bytes(), self.timing.read_bytes())
        self.assertEqual([len(shard) for shard in lists], [len(self.names[i::12]) for i in range(12)])
        buckets = [shard[i::3] for shard in lists for i in range(3)]
        self.assertTrue(all(len(set(worker) & set(self.names[:4])) <= 1 for worker in buckets))
        self.assertEqual(list(map(len, buckets)), [len(self.names[s::12][i::3])
                                                  for s in range(12) for i in range(3)])

    def test_duplicate_name_fails_even_if_every_hash_matches(self):
        options = self.create()
        lists, manifest = timing.load(self.directory, options, self.names, 12, 3)
        lists[0][0] = lists[1][0]
        tampered = timing.list_bytes(lists[0])
        (self.directory / "wpt-timing-shard-0.list").write_bytes(tampered)
        manifest["shard_sha256"][0] = timing.digest(tampered)
        manifest_bytes = json.dumps(manifest).encode()
        (self.directory / timing.PLAN).write_bytes(manifest_bytes)
        options["timing_plan_sha256"] = timing.digest(manifest_bytes)
        with self.assertRaisesRegex(ValueError, "each input name exactly once"):
            timing.load(self.directory, options, self.names, 12, 3)

    def test_rejects_wrong_pin_worker_count_and_wpt_revision(self):
        options = self.create()
        with self.assertRaisesRegex(ValueError, "timing artifact SHA-256"):
            timing.create(self.directory, self.timing, "0" * 64, self.full_sha, self.release)
        with self.assertRaisesRegex(ValueError, "requires 12 Linux"):
            timing.load(self.directory, options, self.names, 12, 2)
        with self.assertRaisesRegex(ValueError, "input revision"):
            timing.load(self.directory, dict(options, wpt_commit="0" * 40), self.names, 12, 3)

    def test_rejects_altered_shard_bytes_before_execution(self):
        options = self.create()
        (self.directory / "wpt-timing-shard-0.list").write_bytes(b"")
        with self.assertRaisesRegex(ValueError, "shard 0 SHA-256"):
            timing.load(self.directory, options, self.names, 12, 3)

    def test_default_importlib_caller_needs_no_sibling_path(self):
        script = Path(release_tests.__file__).resolve()
        command = """
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("rt", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert callable(module.fetch_set)
assert "wpt_timing_plan" not in sys.modules
"""
        subprocess.run([sys.executable, "-I", "-c", command, str(script)],
                       cwd=self.directory, check=True)

    def test_existing_shard_entrypoint_selects_opt_in_list(self):
        planned = self.create()
        for options, platform, expected in [
            (planned, timing.PLATFORM, (self.directory / "wpt-timing-shard-0.list").read_bytes()),
            (planned, "macos-arm64", timing.list_bytes(self.names[::12])),
            ({"wpt_commit": self.release}, timing.PLATFORM, timing.list_bytes(self.names[::12])),
        ]:
            (self.directory / "inputs.json").write_text(json.dumps(options))
            work = self.directory / "work"
            run = release_tests.argparse.Namespace(
                inputs=self.directory, index=0, shards=12, jobs=3, work=work, out=self.directory,
                platform=platform, script_engine=timing.ENGINE,
            )
            with (patch.dict(sys.modules, {"wpt_timing_plan": timing}),
                  patch.object(release_tests, "runner_info", side_effect=InterruptedError),
                  self.assertRaises(InterruptedError)):
                release_tests.cmd_wpt_shard(run)
            self.assertEqual((work / "shard.list").read_bytes(), expected)


if __name__ == "__main__":
    unittest.main()
