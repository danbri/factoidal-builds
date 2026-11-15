# CI timing and cache records

One row per job of each `build.yml` run in `runs.csv`, and the full record in `runs/<run_id>.json`,
written by the `metrics` job (`scripts/ci-metrics.py` on `main`). A trend of the last runs:
`python3 scripts/ci-metrics.py trend --n 10 --records <checkout of this branch>`.
