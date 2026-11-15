# hub-data

Data files of the Hub pages, written by workflows of this repository. Every change is a commit, so the log of this branch is the history of the numbers.

- `conformance/`: the Conformance page (https://danbri.github.io/factoidal/web/hub/conformance/), written by `.github/workflows/conformance-data.yml` on main with factoidal-core's `tests/browser-wpt/passmap-data.py --hub`; schema `docs/web/hub/conformance/data.schema.json` in factoidal-core.
