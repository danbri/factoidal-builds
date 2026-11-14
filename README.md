# Branch WPT check results

Written by `branch-wpt.yml` (release-tests.py `branch-record`) at the end of each check, so that a
result can be read without the GitHub API (whose hourly limit the account shares):

- `checks.csv`: one row per check (run id, core ref and commit, names, passed, baseline, difference,
  tests worse and better, CRASH/STALL/TIMEOUT counts, new crashes against the baseline, links).
- `checks/<run id>/report.md` and `report.json`: the check's report, as in the run's job summary and
  its artifact `branch-wpt-results`.

Read with `git fetch origin branch-checks` or
`curl -s https://raw.githubusercontent.com/danbri/factoidal-builds/branch-checks/checks.csv`
(raw.githubusercontent.com may serve a copy up to about 5 minutes old).
A development check of selected names, not a score: scores are on the branch `wpt-scores`.
