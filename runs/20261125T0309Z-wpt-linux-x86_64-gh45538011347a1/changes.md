### Since the previous full run: -32 subtests (-0.0014 points)

Previous: `20261125T0307Z-wpt-linux-x86_64-gh45535371955a1`, core `1b851ac72`, 92.6338%. This run: core `856332018`, 92.6324%; 4 commits between.
Tests that lost subtests: 4 (-32); that gained: 0 (+0). Page outcomes: ERROR +1, OK -2, STALL +1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| html/dom | 72,463 | 69,929 | 69,902 | -27 |
| webcodecs | 4,168 | 2,641 | 2,638 | -3 |
| fetch | 13,290 | 8,807 | 8,806 | -1 |
| html/semantics | 22,498 | 15,588 | 15,587 | -1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 4 directories, the first 4)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| html/dom | 27 | 1 |
| webcodecs | 3 | 1 |
| fetch/metadata | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 4 of 4)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/dom/aria-element-reflection.html | 27 | 0 | 27 |
| /webcodecs/image-decoder.https.any.html | 13 | 10 | 47 |
| /fetch/metadata/generated/element-img.https.sub.html | 18 | 17 | 45 |
| /html/semantics/embedded-content/the-video-element/intrinsic_sizes.htm | 3 | 2 | 5 |

**Commits between** (4)

- `84b19a75a` Position outside list markers at the float-adjusted first line
- `853a7c275` Avoid loading the Wasm document engine in native workers
- `bcbda8cce` Merge pull request #998 from danbri/wip/native-worker-without-wasm
- `856332018` Merge pull request #997 from danbri/wip/float-aware-list-marker

