# The daily WPT score job

Date: 2026-11-10. Files: `.github/workflows/wpt-score.yml`,
`scripts/wpt-score-job.py`, `scripts/wpt-score-history.sh`.

## What the job does

Each day at 02:47 UTC, and on a manual start, four jobs run in parallel: two WPT
commits times two page script engines (BubblePopJS, QuickJS-NG in WasmVM).

- `pinned` is the WPT commit of factoidal-core's last record
  (`tests/browser-wpt/wpt-score-YYYYMMDD.json`, today `fea36e49dd`). A change in
  this score is a change in the engine.
- `latest` is the newest WPT commit that has a Chrome stable run on wpt.fyi. The
  difference from `pinned` is the change in WPT.

Each job takes the newest release of this repository whose core commit is in the
history of core `main` (sets `foafnaut-web` and `foafnaut-darwin-arm64` of one
commit), checks every file against `build-info.json`, fetches WPT at the commit
(`git fetch --depth 1`, 1.2 GB on disk), gets Chrome's `summary_v2` file from
wpt.fyi (the denominator), and runs core's `wpt-score.py` (`sample`, `run`,
`score`). No Lean build runs.

Sample: seed 20261108 (the seed of the 2026-11-09 record), 10 names a stratum, the
3 largest always, variants `all`: 4,004 names at `fea36e49dd`. The record of
2026-11-09 used 25 and 5 (5,898 window names). The same seed and numbers each day
give the same names, so two days can be compared. The 95% range is about 1.6
times as wide as with 25 names a stratum.

Limits: the test run stops at 240 minutes (`max_minutes`), the step at 300, the
job at 320. A run that stops at the limit is recorded as `INCOMPLETE` with the
count of names that ran.

Results: an artifact for each job (score JSON with one line a test, the record,
raw result lines, logs; kept 90 days), the job summary (score, 95% range, WPT
commit, engine commit, date), and one line a score in `history.jsonl` on the
branch `wpt-scores` (the workflow token with `contents: write`; no other secret).

## What a run needs (measured on Linux x86_64, 2026-11-10)

- Python 3 (3.13.18 used), Deno 2.9.4, git. No GPU, no window library
  (`libnative-window.dylib` is not loaded), no Lean toolchain for the released
  macOS library.
- Network: github.com (WPT, the releases), wpt.fyi and storage.googleapis.com
  (Chrome's run and summary). The tests themselves use no network: WPT's server
  runs on 127.0.0.1 (ports 8000-8003, 8443-8446, 8888, 8889, 9000) and WPT's host
  names resolve only inside the runner. Nothing is written to `/etc/hosts`.
- An engine. The runner (`testharness-run.ts`) always imports the engine's Wasm
  module from `labs/demos/foafnaut/.build/native-html/runtime/` of the core
  checkout, also when the engine is the native library. Set `foafnaut-web` holds
  it, and the QuickJS-NG guest `qjs-wasmvm.wasm`.
- The native engine library. `wpt-score.py run` starts the runner with
  `--engine native --native-engine FILE` and has no other choice.

## Which engine a release gives

| Engine | In a release | Usable by core's tool today |
| --- | --- | --- |
| `libweb-render.dylib` (macOS arm64) | set `foafnaut-darwin-arm64` | yes, on macOS |
| Wasm engine `web-render.wasm` | set `foafnaut-web` | no: the tool has no `--engine wasm` |
| Linux native library | none (`build-web-render.sh` makes no library on Linux) | not built |

So the scheduled job runs on `macos-15` with the released library. That is the
configuration of the 2026-11-09 record. It was not run on macOS in the session
that wrote it; the Linux runs below used a library linked by hand.

## Measurements behind the choice

One sample: 33 names of `/console`, `/dom`, `/domparsing`, `/url` at WPT
`fea36e49dd` (seed 20261108, 3 a stratum, 1 largest always, window variants),
3 processes, stall limit 120 s, a 4-CPU cloud machine that another build shared.
Passed subtests are the sum over the 33 names, capped at Chrome's count.

| Engine | Page scripts | Wall time | Passed subtests | Notes |
| --- | --- | ---: | ---: | --- |
| native (Linux library, linked by hand) | BubblePopJS | 41 s | 21,661 | |
| native (Linux library, linked by hand) | QuickJS-NG | 361 s | 15,105 | 4 names TIMEOUT |
| Wasm engine of release `386f8fb43f73` | BubblePopJS | 161 s | 14,254 | 1 name STALL, 3 TIMEOUT |
| Wasm engine of release `386f8fb43f73` | QuickJS-NG | 541 s | 446 | stopped at the 9 minute limit, 28 of 33 names, 8 STALL |

The native library was linked from the objects of a local build of
`build-web-render.sh --native` (2026-11-10 06:58 UTC), and the Wasm engine is of
core `386f8fb43f73`, so the two are not the same source. The time difference is
large all the same: the Wasm engine is 4 times slower with BubblePopJS, and with
QuickJS-NG (an interpreter in WasmVM, in Wasm) most heavy tests do not end. The
Wasm engine is therefore not a replacement for the native library in this job.

The job script on that subset, with the unchanged tool of core `518e81526`:
`run --wpt pinned --script-engine bubblepop --smoke` took 89 s (42 s of tests)
and gave estimate 57,148 of 82,429 subtests of those four directories (95% range
50,311 to 63,985), measured 21,661 in 33 tests. This is a subset number with 3
names a stratum, not the whole-WPT score.

## Changes proposed for factoidal-core (not applied)

1. `wpt-score.py run`: stop a part whose runner ends three times with no result.
   Today a runner that cannot start (no library, no Wasm module, no guest) is
   started again until `--max-hours`, and the tool then exits 0 (seen: 10
   minutes, 0 of 33 results). The job script has a one-test start check for this.
   The same patch adds `run --engine wasm`.
2. `build-web-render.sh --native` on Linux: make `engines/libweb-render.so`. The
   static Lean runtime can not go into a shared library on Linux (`relocation
   R_X86_64_TPOFF32 against _mi_heap_default cannot be used with -shared`, Lean
   4.33.1), so the library links Lean's shared runtime and needs the toolchain at
   run time. With that library in a release (a new job in `build.yml`, about 20
   minutes of build), this job can move to `ubuntu-latest`.
3. `wpt-score.py tree` extracts symbolic links of the tarball with
   `filter="fully_trusted"`. The job uses `git fetch` and not `tree`.

## Local run

```sh
python3 scripts/wpt-score-job.py fetch-engine --core ../factoidal-core --dest /tmp/w/engine
python3 scripts/wpt-score-job.py run --core ../factoidal-core --engine-dir /tmp/w/engine \
  --wpt pinned --script-engine bubblepop --smoke --work /tmp/w/work --out /tmp/w/out
python3 scripts/wpt-score-job.py summarize --records /tmp/w/out --markdown /tmp/w/summary.md
bash scripts/wpt-score-history.sh /tmp/w/out --no-push
```

`run` copies the engine's Wasm module into
`labs/demos/foafnaut/.build/native-html/runtime/` of the core checkout (a build
directory that git ignores). `--smoke` samples four directories and is marked
SUBSET in every output. On Linux, `fetch-engine` takes the Wasm engine; give
`run` a native library with `--native-engine`.
