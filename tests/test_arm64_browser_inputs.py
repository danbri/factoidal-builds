import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


script = Path(__file__).resolve().parents[1] / "scripts/verify-arm64-browser-inputs.py"
spec = importlib.util.spec_from_file_location("browser_inputs", script)
inputs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inputs)


class InputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.build = Path(self.temp.name)
        self.commit = "a" * 40
        self.repository = "example/builds"
        self.run = "641"
        engines = ("engines/render-plan.mjs", "engines/render-plan.wasm",
                   "web-render/engines/web-render.mjs", "web-render/engines/web-render.wasm")
        inventory = b""
        for relative in engines:
            path = self.build / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(relative.encode())
            inventory += f"{hashlib.sha256(relative.encode()).hexdigest()}  {relative}\n".encode()
        rows = {"foafnaut-linux-x86_64/engine-SHA256SUMS": {"sha256": hashlib.sha256(inventory).hexdigest()}}
        for relative in ("tool-versions.txt", "source-SHA256SUMS"):
            (self.build / relative).write_bytes(relative.encode())
            rows["foafnaut-linux-x86_64/" + relative] = {"sha256": hashlib.sha256(relative.encode()).hexdigest()}
        release = "foafnaut-browser-linux-x86_64"
        self.receipt = {"set": release, "source_repo": "danbri/factoidal-core", "source_commit": self.commit,
                        "run_url": "https://github.com/example/builds/actions/runs/641",
                        "artifacts": {release + ".tar.gz": {"files": rows}}}

    def verify(self):
        return inputs.verify(self.build, self.receipt, self.commit, self.repository, self.run)

    def test_matches_and_rejects_changed_inputs(self):
        self.assertEqual(set(self.verify()), {"source-SHA256SUMS", "tool-versions.txt", "engine-SHA256SUMS"})
        for name in ("engines/render-plan.mjs", "web-render/engines/web-render.wasm", "tool-versions.txt",
                     "source-SHA256SUMS"):
            with self.subTest(name=name):
                path = self.build / name
                original = path.read_bytes()
                path.write_bytes(original + b"changed")
                with self.assertRaisesRegex(ValueError, "differs"):
                    self.verify()
                path.write_bytes(original)

    def test_rejects_native_worker_and_different_engine_build(self):
        native = self.build / "web-render/engines/libweb-render.so"
        native.touch()
        with self.assertRaisesRegex(ValueError, "native worker"):
            self.verify()
        native.unlink()
        self.receipt["run_url"] = "https://github.com/example/builds/actions/runs/642"
        with self.assertRaisesRegex(ValueError, "different inputs"):
            self.verify()
