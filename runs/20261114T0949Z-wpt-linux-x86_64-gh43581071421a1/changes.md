### Since the previous full run: +11,329 subtests (+0.4992 points)

Previous: `20261114T0907Z-wpt-linux-x86_64-gh43577416594a1`, core `5cfcaf872`, 85.7741%. This run: core `2b464c0a8`, 86.2733%; 87 commits between.
Tests that lost subtests: 13 (-22); that gained: 2,361 (+11,351). Page outcomes: CRASH -3, ERROR -13, NO_RESULT -6, OK +367, STALL +6, TIMEOUT -351.

**Directories that fell** (3; the first 3)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-contain | 499 | 181 | 179 | -2 |
| html/browsers | 3,303 | 631 | 629 | -2 |
| css/css-scroll-snap | 852 | 487 | 486 | -1 |

**Directories that rose** (61; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webnn | 13,986 | 465 | 5,541 | +5,076 |
| IndexedDB | 5,853 | 32 | 1,792 | +1,760 |
| editing/run | 96,745 | 94,429 | 95,424 | +995 |
| html/canvas | 6,235 | 2,142 | 3,023 | +881 |
| html/semantics | 22,364 | 12,957 | 13,520 | +563 |
| webcodecs | 3,922 | 1,022 | 1,580 | +558 |
| third_party/test262 | 53,833 | 36,348 | 36,644 | +296 |
| web-locks | 517 | 35 | 207 | +172 |
| WebCryptoAPI/modern-algos | 14,348 | 6,340 | 6,484 | +144 |
| uievents | 491 | 229 | 353 | +124 |
| pointerevents | 2,749 | 481 | 575 | +94 |
| css/geometry | 1,575 | 443 | 517 | +74 |
| fs | 1,121 | 9 | 82 | +73 |
| css/css-sizing | 6,523 | 2,160 | 2,222 | +62 |
| WebCryptoAPI/(root) | 310 | 196 | 252 | +56 |
| html/dom | 72,323 | 68,023 | 68,076 | +53 |
| storage | 482 | 68 | 113 | +45 |
| css/selectors | 6,266 | 2,840 | 2,882 | +42 |
| editing/plaintext-only | 1,707 | 1,526 | 1,560 | +34 |
| html/editing | 868 | 456 | 484 | +28 |
| workers | 1,598 | 367 | 385 | +18 |
| dom/events | 927 | 642 | 659 | +17 |
| infrastructure | 285 | 47 | 64 | +17 |
| geolocation | 134 | 14 | 27 | +13 |
| clipboard-apis | 253 | 16 | 28 | +12 |
| css/css-overflow | 1,209 | 480 | 491 | +11 |
| editing/other | 16,742 | 12,021 | 12,030 | +9 |
| selection/contenteditable | 252 | 134 | 143 | +9 |
| selection/textcontrols | 78 | 16 | 25 | +9 |
| content-security-policy | 4,544 | 1,767 | 1,774 | +7 |
| css/css-ui | 2,416 | 1,448 | 1,455 | +7 |
| html/infrastructure | 1,664 | 598 | 604 | +6 |
| css/css-borders | 1,709 | 757 | 762 | +5 |
| fullscreen | 248 | 107 | 112 | +5 |
| webidl | 838 | 625 | 630 | +5 |
| css/cssom-view | 2,696 | 741 | 745 | +4 |
| file-system-access | 163 | 32 | 36 | +4 |
| html/interaction | 842 | 318 | 322 | +4 |
| inert | 113 | 24 | 28 | +4 |
| accelerometer | 153 | 5 | 8 | +3 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 7 directories, the first 7)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-sizing | 10 | 3 |
| third_party/test262 | 5 | 5 |
| css/css-contain | 2 | 1 |
| html/browsers | 2 | 1 |
| css/css-scroll-snap | 1 | 1 |
| fetch/metadata | 1 | 1 |
| web-locks | 1 | 1 |

**Tests that lost most** (the first 13 of 13)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /css/css-sizing/contain-intrinsic-size/contain-intrinsic-size-logical-003.html | 12 | 6 | 48 |
| /css/css-contain/contain-inline-size-replaced.html | 2 | 0 | 30 |
| /css/css-sizing/svg-intrinsic-size-009.html | 2 | 0 | 12 |
| /css/css-sizing/svg-intrinsic-size-010.html | 2 | 0 | 12 |
| /html/browsers/the-windowproxy-exotic-object/windowproxy-define-own-property-unforgeable-same-origin.html | 4 | 2 | 8 |
| /css/css-scroll-snap/snap-events/scrollsnapchanging/scrollsnapchanging-on-user-scroll.tentative.html | 1 | 0 | 7 |
| /fetch/metadata/generated/element-iframe.sub.html | 13 | 12 | 18 |
| /third_party/test262/test/built-ins/DataView/prototype/getFloat16/detached-buffer-before-outofrange-byteoffset.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/DataView/prototype/getFloat16/detached-buffer.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/DataView/prototype/setFloat16/detached-buffer-before-outofrange-byteoffset.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/built-ins/DataView/prototype/setFloat16/detached-buffer.test262.html | 1 | 0 | 1 |
| /third_party/test262/test/staging/sm/Array/redefine-length-frozen-dictionarymode-array.test262.html | 1 | 0 | 1 |
| /web-locks/non-secure-context.any.worker.html | 1 | 0 | 1 |

**Commits between** (87)

- `c459db37f` crypto.subtle: SubtleCrypto.supports and getPublicKey in Lean; usage, key-material and DER exactness theorems
- `efa435b6b` crypto glue: WebIDL-enumerable members, the subtle getter's brand check, getRandomValues errors, KEM operations that refuse
- `14b05c09a` WebApi: the export and usage theorems stated over crypto.subtle's own function
- `e2a1aed42` WebCryptoKeys, WebApi: each new theorem's comment says its kind, what it says and what it does not
- `b55685c59` WebCryptoKeys: the header names the 2026-11-14 record
- `610d4b48d` docs: Web Crypto record: found and left
- `a7935de50` Vendor the W3C XForms 1.1 test suite (third_party/testing/xforms11)
- `64d5f9b53` XForms: dependency graph of recalculation with its theorems
- `3088b4297` XForms: XPath 1.0 evaluation with read sets and the XForms function library
- `0dbdbea8b` XForms: the model engine as step : Model -> Event -> Model x List Output
- `0047eb9ec` XForms 1.1 suite: classification of every case and sidecar expectations
- `fff12e6d0` XForms: suite runner l4xforms (not yet compiled), label src, focus events, insert as first child
- `64b85e380` XForms: l4xforms builds and runs; repeat start index, state events when a control becomes relevant
- `731af8d66` XForms: design record with the first measured counts; engine fixes not yet compiled
- `41d33a1d3` XForms design record: counts of the second measured run
- `b5ef4d326` XForms: insert/delete event context, root replacement, NaN delete location; 214 sidecars
- `431d2c5e2` XForms: xsi:type validity, delete-location, groups in the view model; 241 sidecars
- `68e957b25` XForms: no view after a fatal error; runner checks each-value and label endings; 254 sidecars
- `f9ca68b3a` XForms sidecars: three corrections (control selection by kind, a changed value, the Result label)
- `b920a318a` XForms: alert text and in-range state of controls (xforms-in-range / xforms-out-of-range), focus given to a group goes to its first form con
- `4c41cd013` XForms engine modules in the library root, so the full Lean build checks DepGraph, Eval, Model and the recalculation theorems
- `f262d750b` WebDriver: key table, error codes and the Actions state machine (parse, ticks, input state, low-level events) with theorems
- `3bbef1a99` WebDriver.Input: hit test and capture target, boundary events, click count, event inits, trusted input state; theorems
- `6eeb6e697` Input: WebDriver actions as trusted key, pointer, mouse and wheel events through the layout's hit test; test_driver click, send_keys and act
- `9972ff708` Input: a press focuses the focusable area under it (DOM.Focus.pressTarget, proved focusable); key events go to the focused element
- `902b8aa6f` WebDriver.Gate: the endpoint is off by default, loopback only, behind a 128-bit secret, refuses Origin and foreign Host, locks after 16 refu
- `767bb3fc7` WebDriver.Protocol: the endpoint table, routing, capabilities processing, sessions and timeouts behind the gate; a refused request changes n
- `3bdfeb7e2` Input: structure instances on one line (column rule); the activation driver is built from named parts
- `75b1cb522` docs: the design record of user input, WebDriver actions and the WebDriver endpoint (threat model, proved/tested/open)
- `fbde2abf1` wdspec-run.py: run one WPT wdspec file through pytest against the WebDriver endpoint (secret from the environment, loopback host only); not 
- `79d343f48` DOM XPath projection: a node in the XML namespace is written with the prefix xml
- `77fa10472` DOM XPath adapter theorems built with the engine (build list); elemPrefix_xmlNS and attrPrefix_xmlNS
- `7e0c3e72b` Client storage core: shelves by storage key behind a backend interface, partition and quota theorems
- `27387403e` IndexedDB keys: the key type, compare two keys proved a total order with the specification's type order, key ranges, boundary tokens
- `4c04587ef` Client storage: records in key order and the cursor over them, with the cursor theorems
- `72575ec8a` IndexedDB values: the stored record of a structured serialisation, key paths evaluated on it, key injection
- `887454aa5` IndexedDB at rest: object stores, indexes, cursor step, and commits as the one way a database changes
- `c0550007b` IndexedDB in motion: transactions and their lifetime, requests, cursors, open and delete, as commands with one pump
- `a99df3b1e` IndexedDB: web_api op 200, key range checks, and the listener order of IndexedDB events from EventLoop.Dispatch.plan
- `809cc153b` IndexedDB: the page side (prelude) and tail-recursive key helpers
- `4267a4281` File System API model: the origin private file system of a storage key, swap-file writables, access handles, locks
- `ddf406793` File System API and StorageManager: web_api ops 201 and 202; estimate is the sum of the storage APIs' usage
- `26271a542` File System API and StorageManager: the page side
- `927a65625` docs: design record of client-side storage (core, IndexedDB, File System API, StorageManager)
- `352e14e59` Web Locks model: the lock manager of a storage key, with mutual exclusion proved as an invariant
- `65710e1d8` Web Locks: web_api op 203 and the page side (navigator.locks, LockManager, Lock)
- `8bdeb8696` Client storage: sizeSum as a left fold and key equality decided by the comparison, so neither recursion is input-proportional
- `4e427fbe5` docs: client storage design record covers Web Locks and its theorems
- `0080bc249` BubblePopJS: Reflect.set with a receiver; getOrInsert checks its receiver's kind; arguments in a method's parameters inside a static block
- `b1a9eb77e` BubblePopJS: a full heap stops the script (maxObjs), not the operating system the process
- `a3ca13687` BubblePopJS: ?. before a decimal digit is the conditional's ?, not optional chaining
- `8e10eea32` BubblePopJS: a regular expression literal inside a template substitution; lexer theorems
- `6f416e498` Streams Standard: the queue-with-sizes and the byte-stream fill plan as pure functions, with theorems
- `22f6787ef` BubblePopJS: ValidateAndApplyPropertyDescriptor for Object.defineProperty; the n.streams native
- `80b518bb7` Streams.lean: the test helper drain is a tail call (tail-recursion gate)
- `a8a2fb6c1` XSD Part 2 patterns: one reader with Part 1, so \d, \w, \p{..} and subtraction are enforced
- `379c42a55` XPath 4.0: simple types of the in-scope schema in cast, castable, instance of and as constructor functions
- `b3ea3222a` XPath 4.0: generalized atomic schema types against cast-only ones; decimal division rounded to nearest
- `bb6007fab` docs: the XML family measured on 2026-11-14 (XSD, QT4, XSLT, XForms, MathML and the smaller suites)
- `9db43aa4e` XSLT 4.0: the simple types of the imported schema are type names in as attributes and expressions
- `59cd28e0d` WIP (builds, not measured yet): facets tested on XSD canonical forms; XQuery cast target errors XQST0052 and XPST0080
- `6aae936ad` XPath 4.0 schema simple types: list tokens and union members walked by loops (castTokens, leavesAll), tail-recursion allow lines for the fou
- `dbdcd6a63` WebCodecs: a frame's orientation applied to its pixels in Lean (Orient: quarter turns then mirror, source_lt and byteSrc_lt bounds, half-tur
- `7abef0fe4` VideoFrame as a canvas image source: drawImage and createImageBitmap draw a frame's oriented pixels (ops 124, 126) at its display size; Vide
- `1b4101ee7` Engine integration record: components, interfaces, the path of a page in each host, where hosts differ
- `1b8883ef5` Hosts: one module for the page steps; the Hub fetches linked style sheets; script fetches carry their type
- `cd514afdf` Host parity check: expected results on the engine of main 19fb349c1, wired into test.sh
- `ff96d6a96` Engine seams: one command bound, the layout's media environment for script reads, BubblePopJS for every host name
- `b19dc9e77` matchMedia on the layout's media environment
- `cdbbbd60c` tools/foafnaut-op-audit.py: the op numbers prelude.js uses against the numbers Lean serves
- `34125158d` Integration record: script-visible state against what is drawn; fixtures and the parity check; state of the branch
- `b48f5f779` Textnaut: page requests and module scripts, as the window has
- `0a166f0c3` WebRenderScript tests: the command bound is the session's (one more than maxCommands is refused, 4097 replay)
- `1063a3684` Inline SVG reads past metadata attributes; 64 linked style sheets a page; capture size and text size flags
- `3b20c89ca` WebNN: tensor shapes: broadcasting proved commutative and associative, flat numbers and multi-indices proved one to one
- `4bedcccbd` WebNN: float16 conversion with an exhaustive round-trip theorem; tensor data types, buffers, byte encoding
- `bdeb1bf34` WebNN: the operator table and the validation and shape inference of every MLGraphBuilder method; conv output size theorem
- `c241eb37e` WebNN: data-movement operators as index maps; transpose inverse, slice bounds and index bound theorems
- `f6b16bb50` WebNN: CPU reference kernels and the checked evaluation of one operator (outputs proved to have the inferred shape)
- `5a23bab8f` WebNN: contexts, builders, graphs, tensors and dispatch as state; the bytes-in bytes-out API

