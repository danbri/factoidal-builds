# wpt-scores

`history.jsonl`: one line for each run of `.github/workflows/wpt-score.yml`
(the Web Platform Tests score of the Foafnaut engine), written by
`scripts/wpt-score-history.sh` on `main`. Fields: `measuredAt`, `wpt`
(`pinned`: the WPT commit of factoidal-core's last record; `latest`: the newest
WPT commit with a Chrome stable run on wpt.fyi), `wptCommit`, `scriptEngine`,
`engine`, `engineCoreCommit`, `estimate`, `range95`, `measured`, `denominator`
(Chrome's subtests on wpt.fyi at that WPT commit), `sample`, `runUrl`. The whole
score files are artifacts of the run at `runUrl`.
