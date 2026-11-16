### Since the previous full run: +2,024 subtests (+0.0891 points)

Previous: `20261116T1512Z-wpt-macos-arm64-gh43893779183a1`, core `c5121e3aa`, 91.9093%. This run: core `1ad66797e`, 91.9984%; 18 commits between.
Tests that lost subtests: 60 (-149); that gained: 65 (+2,173). Page outcomes: CRASH -1, ERROR +2, NO_RESULT +19, OK -43, STALL -2, TIMEOUT +25.

**Directories that fell** (8; the first 8)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| xhr | 2,344 | 1,816 | 1,791 | -25 |
| html/syntax | 8,984 | 8,679 | 8,656 | -23 |
| html/semantics | 22,381 | 15,193 | 15,171 | -22 |
| third_party/test262 | 53,833 | 45,710 | 45,688 | -22 |
| websockets | 2,389 | 1,260 | 1,246 | -14 |
| dom/nodes | 15,595 | 14,838 | 14,837 | -1 |
| preload | 956 | 243 | 242 | -1 |
| workers | 1,598 | 704 | 703 | -1 |

**Directories that rose** (10; the first 10)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| selection/(root) | 33,918 | 32,388 | 33,664 | +1,276 |
| url | 12,437 | 11,768 | 12,356 | +588 |
| webidl | 838 | 500 | 647 | +147 |
| html/infrastructure | 1,664 | 918 | 979 | +61 |
| referrer-policy | 8,815 | 4,911 | 4,949 | +38 |
| webcodecs | 3,922 | 2,575 | 2,584 | +9 |
| shadow-dom | 14,720 | 14,121 | 14,129 | +8 |
| content-security-policy | 4,544 | 2,499 | 2,503 | +4 |
| html/browsers | 3,309 | 766 | 767 | +1 |
| mathml | 4,321 | 1,088 | 1,089 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 13 directories, the first 13)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| third_party/test262 | 30 | 30 |
| xhr | 29 | 8 |
| html/semantics | 26 | 5 |
| html/syntax | 23 | 1 |
| referrer-policy/gen | 12 | 2 |
| referrer-policy/4K | 8 | 2 |
| websockets/interfaces | 7 | 4 |
| dom/nodes | 5 | 2 |
| websockets | 4 | 1 |
| websockets/constructor | 2 | 2 |
| preload | 1 | 1 |
| websockets/security | 1 | 1 |
| workers/interfaces | 1 | 1 |

**Tests that lost most** (the first 40 of 60)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/syntax/parsing/html5lib_url.html?file=tests21 | 23 | 0 | 23 |
| /html/semantics/embedded-content/the-img-element/relevant-mutations.html | 94 | 72 | 113 |
| /xhr/status-async.htm | 24 | 8 | 27 |
| /referrer-policy/gen/iframe.meta/default/xhr.http.html | 10 | 0 | 12 |
| /referrer-policy/4K/gen/top.http-rp/unsafe-url/script-tag.http.html | 6 | 0 | 12 |
| /websockets/eventhandlers.any.worker.html?wpt_flags=h2 | 4 | 0 | 4 |
| /websockets/interfaces/WebSocket/events/002.html?wss | 4 | 0 | 4 |
| /dom/nodes/Document-cloneNode-about-base-url.window.html | 4 | 1 | 5 |
| /xhr/cors-expose-star.sub.any.worker.html | 3 | 0 | 3 |
| /xhr/responseurl-after-abort.any.worker.html | 5 | 2 | 5 |
| /dom/nodes/Document-cloneNode-base-url-xml.window.html | 2 | 0 | 3 |
| /referrer-policy/4K/gen/top.meta/strict-origin-when-cross-origin/worker-module.http.html | 2 | 0 | 2 |
| /referrer-policy/gen/iframe.http-rp/origin-when-cross-origin/a-tag.http.html | 3 | 1 | 4 |
| /xhr/access-control-and-redirects-async.any.html | 7 | 5 | 7 |
| /xhr/send-conditional-cors.htm | 2 | 0 | 2 |
| /html/semantics/popovers/popovertarget-disabled-fieldset.html | 1 | 0 | 1 |
| /html/semantics/scripting-1/the-script-element/microtasks/checkpoint-after-window-onerror-module.html | 1 | 0 | 2 |
| /html/semantics/scripting-1/the-script-element/moving-between-documents/before-prepare-createHTMLDocument-success-empty-src-classic.html | 1 | 0 | 5 |
| /html/semantics/tabular-data/the-table-element/tFoot.html | 1 | 0 | 2 |
| /preload/link-header-preload-nonce.html | 1 | 0 | 2 |
| /third_party/test262/test/language/expressions/class/elements/escaped-get-field-asi-before-field.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/elements/nested-arrow-fnc-init-err-contains-super.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/elements/static-private-setter-access-on-inner-function.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/elements/syntax/early-errors/delete/field-delete-covered-err-delete-member-expression-privatename.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/elements/syntax/early-errors/grammar-special-meth-ctor-async-meth.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/gen-method/yield-identifier-spread-strict.test262.strict.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/ident-name-method-def-new-escaped.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/class/scope-gen-meth-paramsbody-var-close.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/compound-assignment/S11.13.2_A3.2_T6.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/compound-assignment/S11.13.2_A4.3_T2.1.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/compound-assignment/and-arguments-strict.test262.strict.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/compound-assignment/mod-arguments-strict.test262.strict.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/delete/11.4.1-5-3.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/dynamic-import/catch/nested-else-import-catch-file-does-not-exist.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/dynamic-import/import-attributes/2nd-param-with-non-object.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/dynamic-import/syntax/invalid/nested-async-function-await-typeof-import.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/dynamic-import/syntax/invalid/nested-else-braceless-import-defer-no-rest-param.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/dynamic-import/syntax/invalid/nested-with-expression-import-source-assignment-expr-not-optional.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/dynamic-import/syntax/valid/nested-async-function-await-import-attributes-trailing-comma-second.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/language/expressions/dynamic-import/syntax/valid/nested-function-script-code-valid.test262.html | 1 | 0 | 1 |

**Commits between** (18)

- `08bb40f3e` BubblePopJS script clock at its own rate (500 steps a ms, LeanJS.stepsPerMs), not QuickJS's 100000 instructions a ms
- `8376beed3` Real pages: sliced timer turns, input and scroll first, resumable start, JPEG fast Float.ofNat, cascade skips the table for properties apply
- `1a4323ac0` Proof fixes (setter lemmas, advanceUntil_never), scroll first holds a change made while the first frame is made, frame trace says why
- `13901383d` Start: the parse of a page that waits for module answers is kept for the next attempt (startParsed)
- `3475667a3` WebScripts: doc comment order, no keyword as a name
- `9bbe06dcd` run_html: timers held while a scroll holds a page change; --no-scroll-first and --no-input-first for comparison
- `5efbc58c2` Timeline moves at frames while an animation runs (Host.tickTask, tickTask_running): with the script clock at its own rate a long start no lo
- `657f81d25` Start: the prelude's scan for event handler content attributes reads only the elements that have an on... attribute (node_query 168, eventHa
- `d6d463db2` page-load: optional fields of inputFirst and scrollFirst (deno check)
- `724b00981` Scripts: the undo of a sync request is bounded by the heap (keepsUndo, undoHeapLimit)
- `fd53dac77` Native engine: compiled Lean code counts no heartbeat at each allocation (lean_no_heartbeat.h)
- `adb9da315` Window loop: wait for a page's next timer instead of pumping between its turns
- `0b1e2a908` Merge PRs #501, #510, #515: real pages fast and calm (sliced timer turns, input and scroll first, resumable start; bounded undo of sync requ
- `43a97d928` Frozen base URL: <base href> set or changed by script resolves reflected URLs (url/ a-element*); BaseURL theorems, 46 guards
- `fe719a70a` Base URLs at zero cost on pages without a base: inlined idle checks, slow paths out of line, base fields in BaseURL.State; encoding prescan 
- `893901e4e` Base URLs: select again only when a change can alter the selected base (no tree walk per append on a page with a base); removals name the re
- `fa038a174` Base URLs tracked from the first use only: no base work at mutations of a page that reads no URL; changedBases out of the records so command
- `1ad66797e` Frozen base URL record: lazy tracking, gated selection, timings against main, checks

