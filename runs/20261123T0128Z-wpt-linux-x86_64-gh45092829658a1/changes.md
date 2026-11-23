### Since the previous full run: +41 subtests (+0.0018 points)

Previous: `20261123T0030Z-wpt-linux-x86_64-gh45088922208a1`, core `351edbb5b`, 92.6348%. This run: core `7eb6f33d5`, 92.6366%; 2 commits between.
Tests that lost subtests: 5 (-11); that gained: 5 (+52). Page outcomes: OK +1, STALL -1.

**Directories that fell** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webcodecs | 3,974 | 2,616 | 2,609 | -7 |
| IndexedDB | 5,853 | 5,504 | 5,503 | -1 |
| css/css-grid | 16,018 | 11,274 | 11,273 | -1 |
| fetch | 13,290 | 8,808 | 8,807 | -1 |

**Directories that rose** (4; the first 4)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| resource-timing | 1,220 | 68 | 115 | +47 |
| html/dom | 72,439 | 69,926 | 69,928 | +2 |
| pointerevents | 2,780 | 1,584 | 1,585 | +1 |
| preload | 956 | 242 | 243 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 5 directories, the first 5)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| webcodecs | 7 | 1 |
| IndexedDB | 1 | 1 |
| css/css-grid | 1 | 1 |
| fetch/metadata | 1 | 1 |
| pointerevents | 1 | 1 |

**Tests that lost most** (the first 5 of 5)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /webcodecs/image-decoder.https.any.html | 16 | 9 | 47 |
| /IndexedDB/interleaved-cursors-large.any.html | 1 | 0 | 1 |
| /css/css-grid/alignment/grid-content-alignment-and-self-alignment-001.html | 24 | 23 | 24 |
| /fetch/metadata/generated/element-img.https.sub.html | 19 | 18 | 45 |
| /pointerevents/pointerevent_capture_mouse.html | 1 | 0 | 8 |

**Commits between** (2)

- `4fb4c9d4d` Give HTML block elements their full user agent margins
- `7eb6f33d5` Draw static images in HTML object and embed (#789)

