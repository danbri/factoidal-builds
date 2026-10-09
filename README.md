# factoidal-builds

Builds and compiled artifacts for Factoidal. The source is
[danbri/factoidal-core](https://github.com/danbri/factoidal-core): the F\*
tree (`formal/fstar`) and the Lean 4 tree (`formal/lean4`). Nothing here is
source, and nothing here is edited by hand.

## What runs

`.github/workflows/build.yml` builds one factoidal-core commit (default
branch `main`, else `claude/core-split`), on a schedule four times a day
(skipped when that commit already has releases), on manual dispatch, and on
changes to the build scripts here. Jobs and their gates:

| Job | Builds | Gates (a failure means no artifact, so no release) |
|---|---|---|
| `lean` (Linux, macOS arm64) | full `lake build`; `l4factoidal`, `l4w3c`, `l4wasm-cli` | every theorem and `#guard`, the HACL\* extern probe, the dispatch and CLI smoke scripts, the Lean conformance scoreboard (Linux) |
| `lean-wasm` (Linux) | `Wasm/build-wasm.sh` with Emscripten 6.0.8 | the npm Lean-engine tests against the new module |
| `fstar` (Linux, macOS arm64) | `build-ocaml.sh extract`, `compile`; Linux also `js`, `wasm`, `npm` | the re-extracted `.ml` equal core's committed `.ml`; Linux runs `build-ocaml.sh test` (W3C suites, dashboard) |
| `publish` | packs each complete set | a set whose jobs did not all pass is not published, and the run is red |

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

## Git history here

`main` holds only the workflow, `scripts/`, `legacy-workflows/` (the eleven
workflows moved from `danbri/factoidal`, inactive, with what each needs to be
ported), and `latest/<set>.json` pointers written by the `publish` job.
`toolchain-cache` (F\* binary chunks, KaRaMeL, the Lean wasm work dir) and
`checked-cache` (F\* `.checked` files) are orphan branches read by core's
`tools/install-toolchain-cache.sh` and by `build.yml`.

Old releases may be deleted at any time; they are reproducible from the
source commit named in `build-info.json`.
