### Since the previous full run: +24,593 subtests (+1.0837 points)

Previous: `20261114T0516Z-wpt-linux-x86_64-gh43560691408a1`, core `eccbb6b7f`, 83.5508%. This run: core `262289028`, 84.6344%; 14 commits between.
Tests that lost subtests: 38 (-92); that gained: 785 (+24,685). Page outcomes: CRASH +1, ERROR -56, NO_RESULT +1, OK +358, STALL +2, TIMEOUT -306.

**Directories that fell** (5; the first 5)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| inert | 113 | 30 | 24 | -6 |
| upgrade-insecure-requests | 982 | 236 | 234 | -2 |
| WebCryptoAPI/(root) | 310 | 197 | 196 | -1 |
| css/css-contain | 499 | 170 | 169 | -1 |
| domparsing | 3,731 | 265 | 264 | -1 |

**Directories that rose** (46; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| editing/other | 16,742 | 2,203 | 12,020 | +9,817 |
| html/semantics | 22,364 | 7,823 | 11,840 | +4,017 |
| input-events | 3,366 | 303 | 2,545 | +2,242 |
| dom/nodes | 15,420 | 12,811 | 14,761 | +1,950 |
| html/dom | 72,323 | 65,948 | 67,368 | +1,420 |
| url | 12,395 | 10,305 | 11,340 | +1,035 |
| editing/plaintext-only | 1,707 | 593 | 1,526 | +933 |
| editing/whitespaces | 1,655 | 424 | 1,209 | +785 |
| mathml | 4,321 | 445 | 1,047 | +602 |
| html/webappapis | 3,665 | 1,893 | 2,473 | +580 |
| html/editing | 868 | 88 | 456 | +368 |
| custom-elements | 4,404 | 3,186 | 3,420 | +234 |
| html/interaction | 842 | 159 | 318 | +159 |
| selection/(root) | 33,918 | 33,556 | 33,651 | +95 |
| selection/contenteditable | 252 | 75 | 134 | +59 |
| editing/run | 96,745 | 95,374 | 95,424 | +50 |
| selection/bidi | 92 | 18 | 60 | +42 |
| shadow-dom | 14,707 | 14,070 | 14,107 | +37 |
| css/css-conditional | 3,271 | 2,015 | 2,047 | +32 |
| css/css-animations | 1,431 | 666 | 685 | +19 |
| html/infrastructure | 1,664 | 577 | 596 | +19 |
| svg/types | 1,136 | 893 | 905 | +12 |
| css/css-anchor-position | 13,668 | 10,188 | 10,198 | +10 |
| css/selectors | 6,266 | 2,830 | 2,840 | +10 |
| css/css-text | 5,863 | 3,154 | 3,162 | +8 |
| css/cssom-view | 2,696 | 682 | 690 | +8 |
| mixed-content | 2,281 | 1,112 | 1,119 | +7 |
| uievents | 491 | 206 | 213 | +7 |
| selection/caret | 27 | 3 | 9 | +6 |
| content-security-policy | 4,544 | 1,602 | 1,607 | +5 |
| css/css-display | 576 | 374 | 379 | +5 |
| css/css-ui | 2,416 | 1,445 | 1,450 | +5 |
| import-maps | 396 | 12 | 16 | +4 |
| css/css-values | 10,422 | 4,155 | 4,158 | +3 |
| focus | 55 | 1 | 4 | +3 |
| trusted-types | 3,754 | 54 | 57 | +3 |
| css/css-position | 1,553 | 574 | 576 | +2 |
| dom/events | 927 | 638 | 640 | +2 |
| svg/interact | 9,295 | 6,860 | 6,862 | +2 |
| css/css-overflow | 1,209 | 475 | 476 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 18 directories, the first 18)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-animations | 20 | 1 |
| mixed-content/gen | 20 | 11 |
| editing/run | 15 | 6 |
| inert | 8 | 3 |
| svg/interact | 8 | 1 |
| content-security-policy/gen | 3 | 3 |
| css/css-contain | 2 | 2 |
| css/selectors | 2 | 1 |
| editing/other | 2 | 1 |
| editing/plaintext-only | 2 | 1 |
| fetch/http-cache | 2 | 1 |
| upgrade-insecure-requests/gen | 2 | 1 |
| WebCryptoAPI | 1 | 1 |
| custom-elements/form-associated | 1 | 1 |
| domparsing | 1 | 1 |
| html/browsers | 1 | 1 |
| html/semantics | 1 | 1 |
| third_party/test262 | 1 | 1 |

**Tests that lost most** (the first 38 of 38)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-animations/parsing/keyframes-name-invalid.html | 20 | 0 | 20 |
| /editing/run/insertlinebreak.html?1-1000 | 1,000 | 990 | 1,000 |
| /svg/interact/focus-inside-hidden-svg-containers-04.html | 8 | 0 | 8 |
| /inert/inert-canvas-fallback-content.html | 9 | 3 | 12 |
| /mixed-content/gen/top.http-rp/opt-in/worklet-layout-import-data.https.html | 6 | 2 | 8 |
| /css/selectors/focus-within-009.html | 4 | 2 | 12 |
| /editing/other/link-boundaries-insertion.html | 2 | 0 | 2 |
| /editing/plaintext-only/plaintext-only-in-designMode.html | 2 | 0 | 3 |
| /fetch/http-cache/freshness.any.html | 10 | 8 | 17 |
| /mixed-content/gen/iframe-inherit.meta/unset/sharedworker-import-data.https.html | 6 | 4 | 8 |
| /mixed-content/gen/iframe-inherit.meta/unset/worker-module.https.html | 2 | 0 | 4 |
| /mixed-content/gen/iframe-inherit.meta/unset/worklet-audio-import-data.https.html | 6 | 4 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/fetch.https.html | 8 | 6 | 8 |
| /mixed-content/gen/srcdoc-inherit.http-rp/opt-in/worker-import-data.https.html | 6 | 4 | 8 |
| /mixed-content/gen/srcdoc-inherit.meta/opt-in/worklet-layout-import-data.https.html | 4 | 2 | 5 |
| /upgrade-insecure-requests/gen/sharedworker-module-data.meta/unset/fetch.https.html | 6 | 4 | 6 |
| /WebCryptoAPI/algorithm-discards-context.https.window.html | 1 | 0 | 13 |
| /content-security-policy/gen/top.http-rp/script-src-wildcard/worklet-audio-import-data.https.html | 6 | 5 | 12 |
| /content-security-policy/gen/top.meta/script-src-wildcard/worklet-layout-import-data.https.html | 6 | 5 | 12 |
| /content-security-policy/gen/top.meta/worker-src-wildcard/script-tag.https.html | 12 | 11 | 12 |
| /css/css-contain/content-visibility/content-visibility-054.html | 1 | 0 | 1 |
| /css/css-contain/content-visibility/content-visibility-087.html | 1 | 0 | 1 |
| /custom-elements/form-associated/ElementInternals-target-element-is-held-strongly.html | 1 | 0 | 1 |
| /domparsing/innerhtml-03.xhtml | 3 | 2 | 8 |
| /editing/run/delete.html?1-1000 | 995 | 994 | 1,000 |
| /editing/run/delete.html?5001-6000 | 996 | 995 | 1,000 |
| /editing/run/forwarddelete.html?1-1000 | 999 | 998 | 1,000 |
| /editing/run/forwarddelete.html?4001-5000 | 999 | 998 | 1,000 |
| /editing/run/insertimage.html | 942 | 941 | 962 |
| /html/browsers/browsing-the-web/history-traversal/pageswap/pageswap-iframe.html | 1 | 0 | 1 |
| /html/semantics/forms/the-select-element/customizable-select-listbox/customizable-select-listbox-keyboard-behavior.optional.html | 1 | 0 | 4 |
| /inert/inert-in-shadow-dom.html | 1 | 0 | 1 |
| /inert/nested-inert-unfocusable.html | 2 | 1 | 3 |
| /mixed-content/gen/iframe-inherit.http-rp/opt-in/worklet-animation-import-data.https.html | 6 | 5 | 8 |
| /mixed-content/gen/iframe-inherit.meta/opt-in/beacon.https.html | 4 | 3 | 5 |
| /mixed-content/gen/top.http-rp/opt-in/sharedworker-import.https.html | 6 | 5 | 8 |
| /mixed-content/gen/top.meta/unset/fetch.https.html | 8 | 7 | 8 |
| /third_party/test262/test/built-ins/String/prototype/lastIndexOf/S15.5.4.8_A1_T6.test262.html | 1 | 0 | 1 |

**Commits between** (14)

- `2b65f1a6a` XHTML pages: createElement makes HTML elements; definitions and scripts only in documents with a browsing context; a clone keeps its is valu
- `bfc949f66` Popovers, dialogs and invoker buttons; element states for :popover-open, :modal and :defined
- `a87a434fb` A dialog that is not open and a popover that is not showing are not rendered
- `8f886e466` Focus: focus(), blur(), activeElement, the focus events, :focus, :focus-visible, :focus-within
- `aa954f521` docs: DOM and HTML record, steps 2 to 4
- `f6e3b5c71` innerText and outerText (HTML 3.2.7)
- `cb2d1a33d` innerText is node_query 191 (190 is the hyperlink op); an inserted script runs with its node document
- `472e451d6` The rest of the global event handlers; MathMLElement; draggable; a frame's inserted script does not run once the frame is removed
- `305596d50` wpt-runs skill: the macOS engine build, the record of changes with each full run, the branch check's baseline and gate report
- `261d925b9` Editing: keys and test_driver key actions, browser rules for line breaks, joins and typing, Selection.modify, text controls
- `7f1f29e12` Editing: plaintext-only Enter is a line break, beforeinput target range stays in the editing host, joined lines keep their white-space span,
- `78563b711` Tail-recursion gate: allow-list lines with bounds for Editing.extractRange and fixDisallowedAncestors
- `2598f05e7` Focus: an editing host that takes the focus gets the selection first (the caret of focus() in an editing host, with the focus update steps)
- `262289028` Tail-recursion allow list: the nesting recursions of CSS values, each with its bound

