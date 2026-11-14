# wpt-scores: test results of Factoidal releases

Written by `.github/workflows/release-tests.yml` (code: `release-tests/release-tests.py`
on `main`). Every file here can be fetched without credentials:

- https://raw.githubusercontent.com/danbri/factoidal-builds/wpt-scores/runs.csv
- https://raw.githubusercontent.com/danbri/factoidal-builds/wpt-scores/rivals.csv
- https://raw.githubusercontent.com/danbri/factoidal-builds/wpt-scores/differential.csv (when a QuickJS run exists)
- https://raw.githubusercontent.com/danbri/factoidal-builds/wpt-scores/runs/RUN_ID/meta.json
- full WPT result of a run (factoidal-wpt-full-v1, gzip, about 1 MB):
  https://github.com/danbri/factoidal-builds/releases/download/test-results/RUN_ID.wpt-full.json.gz
  (the `result_url` column)

## Rules

- **Only rows with `valid` = `true` and `kind` = `full` are scores.** Invalid runs are kept,
  with `invalid_reason`, so that failures stay visible. They are never shown as a score.
- Rows are only appended. A row is never changed or deleted.
- **Platforms.** macOS arm64 is the shipping platform. Linux x86_64 runs the same engine
  source and gets a result first (a Linux engine is built within 20 minutes of a main
  commit that changes engine code; a full run takes 20 minutes). On the same commit the
  two agree closely (6dde36491: 71.2202% Linux, 71.2245% macOS). A valid Linux row is the
  score of a commit while that commit has no valid macOS row.
- A full WPT run is valid only if all of these are true (`wpt_validity` in
  `release-tests.py`):
  1. every name that Chrome runs at the WPT commit was run (`names_run` = `names_total`);
  2. names with a test-server failure ("fetch failed", "Connection refused") are less
     than 0.5% of the names, after one retry pass: each shard runs its server-failure
     names once more in new processes, and those results replace the first ones
     (meta.json: `server_failures_first_pass`, `shards[].retry`). A runner process can
     lose its connections to a healthy server and fail every later test;
     the retry is the same as the rerun of the 2026-11-13 local run;
  3. the engine commit, the release tag and the WPT commit are known;
  4. every shard gave results;
  5. in every shard the WPT server answered for the whole run (a probe every 10 s, no 3
     failed probes in a row, no "wptserve exited"), and no shard stopped at its time limit;
  6. the engine library that a shard ran is of the same core commit as the runner code
     (the Wasm module, which a native run loads and never calls, may be of an earlier
     release: `plan.release_sets.foafnaut-web.note` in meta.json says so);
  7. Chrome's summary gave a denominator.
- Another suite's run is valid if its runner ended (exit 0 or 1, not a time-out), its log
  has a score line, and it found at least one test (`suite_validity`).
- Sampled runs are not scores. The daily sample job of 2026-11-11 to 2026-11-12 is
  retired: its lines are in `retired/sample-history.jsonl`, marked as samples, and not in
  `runs.csv`. `wpt-score.yml` now runs only on request, as a smoke check.
- QuickJS runs are a differential check (BubblePopJS is the engine everywhere). They go
  to `differential.csv` (same columns, `kind` = `differential`), never to `runs.csv`.

## runs.csv (one row for each run of one suite on one platform)

| Column | Meaning |
| --- | --- |
| `run_id` | `<UTC start, YYYYMMDDTHHMMZ>-<suite>-<platform>-gh<workflow run id>a<attempt>`, or `-local` for a local run. Also the directory `runs/<run_id>/` |
| `started_utc`, `finished_utc` | first shard start and last shard end (ISO 8601, UTC) |
| `trigger` | `factoidal-release` (a build.yml run published releases), `schedule` (4 times a day), `browser-release` (a scheduled run at a WPT commit with new aligned browser runs on wpt.fyi), `manual` |
| `suite` | `wpt`, or a suite key: `sparql`, `rdf`, `rdf12`, `rdf12c14n`, `rdf12entail`, `sparql12`, `rdfc10`, `shacl_*`, `shex`, `jsonld_*`, `owl*`, `rml_core`, `rif_core`, `vc_stage1`, `did_key`, `csvw_*`, `xml_conformance`, `xslt`, `mathml`, `jsonschema`, `schematron` (the F\* runners; keys of core's `formal/fstar/generate-report.sh`), `l4w3c-sparql11`, `l4w3c-sparql12`, `l4w3c-rdf11`, `l4w3c-rdf12`, `l4w3c-rdfc10` (the Lean `l4w3c`) |
| `platform` | `macos-arm64` or `linux-x86_64` |
| `engine` | `bubblepopkit-native` (the release's engine library), `fstar`, `lean` |
| `script_engine` | WPT: `bubblepop` (BubblePopJS) or `quickjs` (differential only) |
| `factoidal_commit` | the factoidal-core commit (40 hex) of the release |
| `commit_utc` | committer date of that commit |
| `snapshot_branch` | `wpt-snap/<YYYYMMDD-HHMM>-<sha12>` in factoidal-core when one was made (needs the secret `CORE_SNAPSHOT_TOKEN`), else empty; meta.json says why |
| `release_tag` | WPT: the engine release (`build-<sha12>-foafnaut-darwin-arm64`); other suites: `build-<sha12>-linux-x86_64` |
| `wpt_commit` | WPT commit of the tests and of Chrome's summary (empty for other suites) |
| `names_total` | WPT: names with at least one Chrome subtest at the WPT commit; other suites: tests found |
| `names_run` | names (tests) that have a result |
| `passed` | WPT: subtests passed, each name capped at Chrome's count for it; other suites: tests passed |
| `denominator` | WPT: Chrome's subtests on wpt.fyi at the WPT commit; other suites: tests found |
| `share_pct` | 100 × `passed` / `denominator`, 4 decimals |
| `share_ex_encoding_pct` | WPT: the same without `encoding/` (half of WPT's subtests are there) |
| `ok`, `error`, `timeout`, `skip`, `crash`, `stall`, `no_result`, `other` | WPT: page outcomes (testharness status of each name). Other suites: `skip` = skipped + unsupported |
| `failed` | other suites: tests failed |
| `server_failures` | WPT: names whose result mentions "fetch failed" or "Connection refused", after the retry pass |
| `valid` | `true` or `false` (rules above) |
| `invalid_reason` | why not valid, `; `-separated |
| `kind` | `full` (every name run, no sampling) or `differential` |
| `shards` | runners the WPT names were split over (`names[k::shards]`) |
| `wall_minutes` | WPT: the longest shard's job time; other suites: the runner's time |
| `repeat_of` | the earlier valid run of the same core commit and WPT commit, when this run repeats it (repeats show flakiness) |
| `runner` | runner label × count, or the local machine |
| `workflow_run_url` | the GitHub Actions run |
| `result_url` | full result file (WPT) |
| `meta_url` | this run's meta.json |

## rivals.csv (other browsers at a WPT commit, on the same scale)

`recorded_utc`, `wpt_commit`, `browser` (chrome, firefox, safari, edge: stable;
servo, wpewebkit, ladybird: experimental), `version`, `channel`, `wptfyi_run_id`,
`run_time_utc`, `passed` (subtests passed, each name capped at Chrome's count, only
names Chrome runs), `denominator` (Chrome's subtests), `share_pct`,
`share_ex_encoding_pct`, `names_total` (names Chrome runs), `names_reported` (of those,
names in the browser's summary), `partial` (`true` when fewer than 95% of Chrome's names
are reported: the share is then not comparable), `summary_url` (wpt.fyi summary_v2).

## runs/RUN_ID/meta.json

`row` (the CSV row), `plan` (trigger, core commit, author and committer dates, subject,
snapshot branch, release tags with publish times, the time the candidate was chosen and
why, WPT commit), `inputs` (Chrome run, list and summary sha256), `validity` (verdict,
reasons, rules), `totals`, `shards` (per shard: runner OS and image, CPU count, memory,
Python/Deno/git versions, release build-info.json contents, engine sha256, tool commit and
sha256, tree and run seconds, outcomes, server failures, WPT server probes, the retry pass,
and `memory`: the least free memory seen and each test process killed by the memory
guard; on Linux a runner that runs out of memory stops with no result, so below 1.2 GB
free the largest test process is killed and core's tool records its test as CRASH) and
`directories` (per top-level WPT directory: names, run, Chrome subtests, passed,
reported, share, outcomes). Other suites: `status` (exit, seconds), `totals`, `command`,
`parser`.

## Snapshot branches

When `CORE_SNAPSHOT_TOKEN` is set, each run that tests something makes
`wpt-snap/<YYYYMMDD-HHMM>-<sha12>` in factoidal-core at the tested commit. Snapshots older
than 14 days are deleted by the same job, except those named by a valid row of runs.csv:
the commit id already pins the source, and the branch keeps it reachable and easy to
check out; 14 days covers the time to look at a run.
