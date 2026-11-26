### Since the previous full run: -624 subtests (-0.0274 points)

Previous: `20261126T2004Z-wpt-linux-x86_64-gh45887197212a1`, core `25ed4f09e`, 92.6571%. This run: core `c105a71cc`, 92.6296%; 5 commits between.
Tests that lost subtests: 2 (-655); that gained: 2 (+31). Page outcomes: CRASH -1, OK +2, STALL -1.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| shadow-dom | 14,726 | 14,154 | 13,500 | -654 |
| third_party/test262 | 53,838 | 46,418 | 46,417 | -1 |

**Directories that rose** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| streams | 5,796 | 5,550 | 5,580 | +30 |
| fetch | 13,314 | 8,822 | 8,823 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| shadow-dom/declarative | 654 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /shadow-dom/declarative/declarative-shadow-dom-attachment.html | 654 | 0 | 654 |
| /third_party/test262/test/built-ins/Temporal/PlainDate/prototype/toString/prop-desc.test262.html | 1 | 0 | 1 |

**Commits between** (5)

- `d647ff096` Foafnaut: an img of an SVG file draws the view of its svgView(...) fragment (viewBox, preserveAspectRatio, transform)
- `ed987c363` WebRender: svgViewOf type fix (String.dropEnd)
- `98f8f01b9` Render scores: wpt-images-native 18 pass of 279 at 49266437b (svgView fragments)
- `653b79d94` Design record: the wpt-images-native render score row, steps and open causes
- `c105a71cc` Main gates: allow-list rows for Net/Socks5 and WebAudio recursion; dataflow inventory regenerated for WebAudio/

