### Since the previous full run: +1 subtests (+0.0000 points)

Previous: `20261125T0221Z-wpt-linux-x86_64-gh45530858958a1`, core `6fe1473fc`, 92.6338%. This run: core `1b851ac72`, 92.6338%; 7 commits between.
Tests that lost subtests: 2 (-2); that gained: 1 (+3). Page outcomes: ERROR -1, OK -2, STALL +3.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| html/semantics | 22,498 | 15,589 | 15,588 | -1 |

**Directories that rose** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 4,168 | 2,638 | 2,641 | +3 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| IndexedDB | 1 | 1 |
| html/semantics | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /html/semantics/embedded-content/the-img-element/list-of-available-images-does-not-coalesce-in-flight-requests.sub.tentative.html | 1 | 0 | 1 |

**Commits between** (7)

- `5cd7bef63` Use more of the raster budget for large SVG images
- `120c5bc89` Reuse element keys within a partial CSS restyle
- `0defebb2c` Check SVG raster sizes at fractional divisors
- `5de0dc09b` Open Foafnaut at the requested window size
- `94399281c` Merge pull request #993 from danbri/wip/foafnaut-initial-window-size
- `78276916b` Merge pull request #986 from danbri/wip/partial-restyle-element-keys
- `1b851ac72` Merge pull request #983 from danbri/wip/svg-image-budget-resolution

