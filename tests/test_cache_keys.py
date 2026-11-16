"""Cache keys cover their inputs: a change to any input is a miss, the same inputs a hit.

release-tests/leanc-cache.sh (the leanc object cache of build.yml's macOS bundle job and of
foafnaut-macos.yml) keys an object on the toolchain name, the flags and the C source. ccache
(the Emscripten cache of foafnaut-engines) also covers headers; that is checked when ccache
is installed. scripts/cache-audit.sh must report a cached object that differs from a fresh
compile.
"""
import os
import pathlib
import shlex
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CC = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")


@unittest.skipUnless(CC, "no C compiler")
class LeancCacheKey(unittest.TestCase):
    def setUp(self):
        self.d = pathlib.Path(tempfile.mkdtemp())
        (self.d / "shim").mkdir()
        (self.d / "cache").mkdir()
        shutil.copy(ROOT / "release-tests/leanc-cache.sh", self.d / "shim/leanc")
        os.chmod(self.d / "shim/leanc", 0o755)
        (self.d / "a.c").write_text("int f(int x){return x+1;}\n")

    def tearDown(self):
        shutil.rmtree(self.d)

    def compile(self, ident="lean-4.33.1", flags=("-O2",)):
        env = dict(os.environ, LEANC_REAL=CC, LEANC_CACHE=str(self.d / "cache"), LEANC_ID=ident,
                   PATH=f"{self.d / 'shim'}:{os.environ['PATH']}")
        for f in (".hits", ".misses"):
            (self.d / "cache" / f).unlink(missing_ok=True)
        subprocess.run(["leanc", *flags, "-c", str(self.d / "a.c"), "-o", str(self.d / "a.o")],
                       env=env, check=True)
        hit = (self.d / "cache/.hits").exists()
        return "hit" if hit else "miss"

    def test_same_inputs_hit(self):
        self.assertEqual(self.compile(), "miss")
        self.assertEqual(self.compile(), "hit")

    def test_toolchain_flags_and_source_each_invalidate(self):
        self.compile()
        self.assertEqual(self.compile(ident="lean-4.34.0"), "miss")
        self.assertEqual(self.compile(flags=("-O3",)), "miss")
        (self.d / "a.c").write_text("int f(int x){return x+2;}\n")
        self.assertEqual(self.compile(), "miss")
        self.assertEqual(self.compile(), "hit")

    def test_audit_finds_a_wrong_cached_object(self):
        self.compile()
        cmds = self.d / "cmds.txt"
        cmds.write_text(shlex.join(["leanc", "-O2", "-c", str(self.d / "a.c"), "-o", str(self.d / "a.o")]) + "\n")
        env = dict(os.environ, LEANC_REAL=CC)
        audit = ["bash", str(ROOT / "scripts/cache-audit.sh"), str(cmds), "1", str(self.d / "audit.json")]
        self.assertEqual(subprocess.run(audit, env=env, capture_output=True).returncode, 0)
        (self.d / "b.c").write_text("int g(void){return 7;}\n")
        subprocess.run([CC, "-c", str(self.d / "b.c"), "-o", str(self.d / "a.o")], check=True)
        r = subprocess.run(audit, env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("CACHE_AUDIT DIFFERENT", r.stdout)


@unittest.skipUnless(CC and shutil.which("ccache"), "no ccache")
class CcacheKey(unittest.TestCase):
    def test_header_change_is_a_miss(self):
        d = pathlib.Path(tempfile.mkdtemp())
        try:
            (d / "h.h").write_text("#define K 1\n")
            (d / "a.c").write_text('#include "h.h"\nint f(void){return K;}\n')
            env = dict(os.environ, CCACHE_DIR=str(d / "cc"), CCACHE_COMPILERCHECK="content")
            run = lambda: subprocess.run(["ccache", CC, "-c", str(d / "a.c"), "-o", str(d / "a.o")], cwd=d, env=env, check=True)
            stats = lambda: subprocess.run(["ccache", "--print-stats"], env=env, capture_output=True, text=True).stdout
            hits = lambda: sum(int(l.split("\t")[1]) for l in stats().splitlines() if l.startswith(("direct_cache_hit", "preprocessed_cache_hit")))
            run(); run()
            self.assertEqual(hits(), 1)
            (d / "h.h").write_text("#define K 2\n")
            run()
            self.assertEqual(hits(), 1)
        finally:
            shutil.rmtree(d)


if __name__ == "__main__":
    unittest.main()
