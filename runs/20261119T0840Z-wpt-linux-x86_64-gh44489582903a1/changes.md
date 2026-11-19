### Since the previous full run: -141 subtests (-0.0062 points)

Previous: `20261119T0712Z-wpt-linux-x86_64-gh44477862484a1`, core `c9b4e0735`, 92.6255%. This run: core `aae1fda3d`, 92.6193%; 13 commits between.
Tests that lost subtests: 2 (-141); that gained: 0 (+0). Page outcomes: unchanged.

**Directories that fell** (2; the first 2)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| url | 12,443 | 12,362 | 12,224 | -138 |
| webcodecs | 3,926 | 2,580 | 2,577 | -3 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 2 directories, the first 2)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| url | 138 | 1 |
| webcodecs | 3 | 1 |

**Tests that lost most** (the first 2 of 2)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /url/a-element.html?include=file | 138 | 0 | 138 |
| /webcodecs/image-decoder.https.any.html | 17 | 14 | 47 |

**Commits between** (13)

- `a792f83f8` XML Encryption 1.1: RSA-OAEP with every digest and MGF1 hash of section 5.5.2
- `e8d76eb74` Merge remote-tracking branch 'origin/main' into wip/xmlenc601-hacl-closeout
- `47c9b7d7d` Use checked HACL digest providers for XML RSA-OAEP
- `dd68adc7d` Merge remote-tracking branch 'origin/main' into wip/xmlenc601-hacl-closeout
- `ab9664bd5` Repair checked OAEP proof elaboration from compiler diagnostics
- `e4400c40f` Align checked MGF refinement with the pure flattening definition
- `cba8bc578` Correct the checked digest refusal fixture lambda layout
- `9641406dd` Reuse persistent Nat bounds in XML OAEP digest guards
- `7d4794f49` Merge remote-tracking branch 'origin/main' into wip/xmlenc601-hacl-closeout
- `978dc00fe` Set browser acceptance evidence paths in runner step scope
- `550c4f467` Publish the checked Paralliverse CPU and WebGPU Hub example
- `60e448ac8` Merge pull request #632 from danbri/wip/paralliverse-browser-acceptance
- `aae1fda3d` Merge pull request #601 from danbri/claude/spec-b-xmlenc

