### Since the previous full run: -54 subtests (-0.0024 points)

Previous: `20261117T1848Z-wpt-linux-x86_64-gh44148472362a1`, core `30355c147`, 92.6329%. This run: core `3438c02d9`, 92.6306%; 7 commits between.
Tests that lost subtests: 4 (-54); that gained: 0 (+0). Page outcomes: CRASH +1, OK -3, STALL +2.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| resource-timing | 1,207 | 115 | 68 | -47 |
| shadow-dom | 14,720 | 14,129 | 14,126 | -3 |
| webcodecs | 3,922 | 2,571 | 2,568 | -3 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| resource-timing | 47 | 1 |
| shadow-dom/declarative | 3 | 1 |
| webcodecs | 3 | 1 |
| IndexedDB | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /resource-timing/idlharness.any.worker.html | 47 | 0 | 79 |
| /shadow-dom/declarative/declarative-shadow-dom-repeats.html | 3 | 0 | 3 |
| /webcodecs/image-decoder.https.any.html | 12 | 9 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |

**Commits between** (7)

- `4c583484c` Foafnaut everyday use: checklist, host test, error pages, lazy script session, form navigation in the window
- `c9e50a42c` Forms: focus on press, Enter submits, POST plans, the page's own navigation (engine)
- `495d6d206` Downloads: the engine decides show or save, a safe name; the window saves to ~/Downloads and keeps the page
- `8b63244bc` HostContract.ops: the download decision (a query from the response's headers)
- `43a108824` HostContract: 70 operations with download (count guard; lake build HostContract.Model/Trace green)
- `06057cf26` Merge remote-tracking branch 'origin/main' into wip/daily-basics
- `3438c02d9` Merge pull request #593 from danbri/wip/daily-basics

