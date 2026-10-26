# factoidal-builds

Builds and compiled artifacts for Factoidal. The source is
[danbri/factoidal-core](https://github.com/danbri/factoidal-core): the F\*
tree (`formal/fstar`) and the Lean 4 tree (`formal/lean4`). Nothing here is
source, and nothing here is edited by hand.

## What runs

`.github/workflows/build.yml` builds one factoidal-core commit (default
branch `main`, else `claude/core-split`) on manual dispatch, on a push here
that changes `requests/build.txt` (that commit; see `requests/README.md`) or
the build scripts, and on an hourly schedule. Scheduled runs have not
started in this repository so far (`requests/README.md`). A commit counts as
built only when all three sets have a release; a scheduled run retries a
partly built commit at most once in 24 hours (`scripts/resolve-core.sh`).
Releases are published only for commits on core `main`; a build of any
other commit runs the gates and publishes nothing. Jobs and their gates:

| Job | Builds | Gates (a failure means no artifact, so no release) |
|---|---|---|
| `lean` (Linux, macOS arm64) | full `lake build`; `l4factoidal`, `l4w3c`, `l4wasm-cli` | every theorem and `#guard`, the HACL\* extern probe, the dispatch and CLI smoke scripts; Linux also the tail-recursion audit and `tests/dataflow/run.sh`. The Lean conformance scoreboard (Linux) is a measurement, not a gate |
| `lean-wasm` (Linux) | `Wasm/build-wasm.sh` with Emscripten 6.0.8 | the build itself and its check that the wasm copies agree. It runs no tests: the npm tests run in `web-gates` |
| `fstar` (Linux), `fstar-macos` | `build-ocaml.sh extract`, `compile`; Linux also `js`, `wasm`, `npm` | the re-extracted `.ml` equal core's committed `.ml`; Linux runs `build-ocaml.sh test` (W3C suites, dashboard) |
| `web-gates` (Linux) | nothing; installs the `fstar` web products and the `lean-wasm` module into one checkout | `npm test` in `npm/factoidal` (Node 22), with no skipped test; `tests/engine-compare/run.sh`; `tests/known-defects/run.sh`. The `l4diff` differential is a measurement, not a gate |
| `publish` | packs each complete set | a set whose jobs did not all pass is not published, and the run is red; the `web` set also needs `web-gates` |

## Releases

One release per (core commit, set), tagged `build-<12 hex core commit>-<set>`:

| Set | Content (paths relative to a core checkout) |
|---|---|
| `linux-x86_64`, `darwin-arm64` | `bin/<platform>/`: the F\* CLI, HTTP server and suite runners, and the Lean CLI `l4factoidal`, `l4w3c`, `l4wasm-cli` |
| `web` | F\* JS and wasm bundles (`docs/fstar-extracted/`, `npm/factoidal/`), the Lean wasm module (`docs/web/hub/assets/l4/`, `npm/factoidal/l4-assets/`, `npm/factoidal-lean/`), the generated F\* dashboard (`docs/test-results/`), and the Lean scoreboard (`lean-scoreboard.json`, `.txt`) |

Each release carries `<set>.tar.gz` (deterministic: sorted, mtime 0) and
`build-info.json` (source commit, toolchain versions, run URL, sha256 and
size of every file). In a factoidal-core checkout, `tools/fetch-builds.sh`
picks the newest release whose commit is in your history, checks the
tarball digest and every file, and installs it; `tools/ensure-test-env.sh`
calls it.

## Publishing to npm

`.github/workflows/npm-publish.yml` publishes `@factoidal/core` from a `web`
release, by trusted publishing (OIDC, no token). Manual dispatch only:

```bash
gh workflow run npm-publish.yml --repo danbri/factoidal-builds \
  -f core_ref=<40-hex core commit; required> \
  -f dist_tag=next -f confirm=<version in npm/factoidal/package.json>
```

It refuses a release whose build run's `web-gates` job did not succeed,
installs the release into a core checkout with `tools/fetch-builds.sh`
(sha256 of every file checked), requires `confirm` to equal the package
version and the version to be new on npmjs.com, runs core's
`tools/npm-release-check.mjs` (the version agrees in `package.json`,
`package-lock.json` and `lib/version.mjs`, and `CHANGELOG.md` has a dated
heading for it), sets `repository.url` to
this repository in the packed copy (npm provenance requires it), packs with
`--ignore-scripts`, and refuses a tarball that holds an F\* bundle (`jsoo`,
`ocaml`, `npm-entry`, `hacl-wasm`), lacks `l4-assets/l4factoidal.wasm`, or
whose `l4-assets/version.json` is not stamped with that wasm's sha256 and
the release commit. Since 0.10.0 the package ships no
`l4factoidal-core.wasm`. The package's `prepublishOnly` (`npm test`) does
not run: the pack step skips scripts, and `npm publish` of a tarball runs
none. The suite gate is the `web-gates` job of the build run. The tarball
is a workflow artifact. Use `dist_tag=latest` only to make the version the
default install.

A forced rebuild never replaces a `web` release that a published
`@factoidal/core` version names (`scripts/npm-names-release.py` reads each
version's `l4-assets/version.json`); the run keeps the old release and is
red.

One-time owner step on npmjs.com before the first run: package
`@factoidal/core` → Settings → Trusted Publisher → GitHub Actions, with
organization `danbri`, repository `factoidal-builds`, workflow filename
`npm-publish.yml`, environment blank, allowed action `npm publish`. After
this change, the old workflow in `danbri/factoidal` can no longer publish.

## Git history here

`main` holds only the workflow, `scripts/`, `legacy-workflows/` (the eleven
workflows moved from `danbri/factoidal`, inactive, with what each needs to be
ported), and `latest/<set>.json` pointers written by the `publish` job.
`toolchain-cache` (F\* binary chunks, KaRaMeL, the Lean wasm work dir) and
`checked-cache` (F\* `.checked` files) are orphan branches read by core's
`tools/install-toolchain-cache.sh` and by `build.yml`.

Old releases may be deleted at any time; they are reproducible from the
source commit named in `build-info.json`.
