### Since the previous full run: +15,008 subtests (+0.6613 points)

Previous: `20261114T0759Z-wpt-linux-x86_64-gh43573607394a1`, core `d799500c7`, 85.1045%. This run: core `6ecf053c7`, 85.7658%; 36 commits between.
Tests that lost subtests: 7 (-12); that gained: 359 (+15,020). Page outcomes: CRASH -2, ERROR -200, OK +139, STALL -1, TIMEOUT +64.

**Directories that fell** (1; the first 1)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| css/css-font-loading | 242 | 41 | 38 | -3 |

**Directories that rose** (40; the first 40)

| directory | Chrome | before | after | change |
| --- | ---: | ---: | ---: | ---: |
| webgl | 4,279 | 124 | 4,241 | +4,117 |
| trusted-types | 3,754 | 57 | 2,599 | +2,542 |
| sanitizer-api | 3,816 | 136 | 2,633 | +2,497 |
| domxpath | 1,171 | 2 | 1,164 | +1,162 |
| html/semantics | 22,364 | 11,843 | 12,956 | +1,113 |
| webcodecs | 3,922 | 10 | 1,022 | +1,012 |
| domparsing | 3,731 | 264 | 1,200 | +936 |
| html/dom | 72,323 | 67,377 | 68,019 | +642 |
| xml | 242 | 46 | 236 | +190 |
| dom/(root) | 2,759 | 1,864 | 2,017 | +153 |
| html/syntax | 8,984 | 8,512 | 8,625 | +113 |
| html/webappapis | 3,665 | 2,519 | 2,592 | +73 |
| xhr | 2,344 | 1,596 | 1,667 | +71 |
| html/browsers | 3,303 | 565 | 631 | +66 |
| content-security-policy | 4,544 | 1,710 | 1,767 | +57 |
| wai-aria | 588 | 76 | 128 | +52 |
| fetch | 13,288 | 4,445 | 4,486 | +41 |
| css/geometry | 1,575 | 404 | 443 | +39 |
| pointerevents | 2,749 | 451 | 481 | +30 |
| css/cssom | 4,463 | 2,855 | 2,876 | +21 |
| uievents | 491 | 213 | 229 | +16 |
| css/cssom-view | 2,696 | 694 | 703 | +9 |
| dom/nodes | 15,420 | 14,763 | 14,772 | +9 |
| orientation-event | 139 | 51 | 59 | +8 |
| selection/(root) | 33,918 | 33,651 | 33,659 | +8 |
| webidl | 838 | 617 | 625 | +8 |
| third_party/test262 | 53,833 | 36,341 | 36,348 | +7 |
| css/css-typed-om | 13,449 | 11,848 | 11,851 | +3 |
| custom-elements | 4,404 | 3,419 | 3,422 | +3 |
| pointerlock | 72 | 35 | 37 | +2 |
| url | 12,395 | 11,340 | 11,342 | +2 |
| css/css-anchor-position | 13,668 | 10,198 | 10,199 | +1 |
| css/css-cascade | 1,759 | 837 | 838 | +1 |
| css/css-conditional | 3,271 | 2,047 | 2,048 | +1 |
| css/css-fonts | 8,683 | 4,434 | 4,435 | +1 |
| css/css-transitions | 3,439 | 467 | 468 | +1 |
| input-events | 3,366 | 2,545 | 2,546 | +1 |
| preload | 938 | 46 | 47 | +1 |
| shadow-dom | 14,707 | 14,107 | 14,108 | +1 |
| svg/(root) | 1,754 | 1,211 | 1,212 | +1 |

**Where subtests were lost** (the losses alone, whatever the directory gained elsewhere; 3 directories, the first 3)

| directory | subtests lost | tests |
| --- | ---: | ---: |
| css/css-font-loading | 5 | 4 |
| html/webappapis | 4 | 1 |
| trusted-types | 3 | 2 |

**Tests that lost most** (the first 7 of 7)

| test | before | after | Chrome |
| --- | ---: | ---: | ---: |
| /html/webappapis/dynamic-markup-insertion/html-unsafe-methods/Document-parseHTMLUnsafe-url-moretests.html | 5 | 1 | 5 |
| /css/css-font-loading/fontface-css-connected-descriptors.html | 2 | 0 | 12 |
| /trusted-types/Element-toggleAttribute.html | 2 | 0 | 2 |
| /css/css-font-loading/fontfaceset-clear-css-connected.html | 1 | 0 | 1 |
| /css/css-font-loading/fontfaceset-delete-css-connected.html | 1 | 0 | 1 |
| /css/css-font-loading/nonexistent-file-url.html | 1 | 0 | 1 |
| /trusted-types/Document-parseHTMLUnsafe-respects-current-globals-CSP.html | 1 | 0 | 2 |

**Commits between** (36)

- `47630f756` WPT plan: progress table rows for the full runs of 6b442d48e to d799500c7 (78.5% to 85.1%)
- `096af0a4f` HTML sanitization decisions (HTML 8.6): configurations, the modifier methods, the walk; node_query 192 and 193
- `1963ecfb7` Sanitizer: the tree is checked against the configuration after the walk and the root emptied when it does not conform; safe_output proved fo
- `e7c2a500b` Sanitizer API: the Sanitizer interface, setHTML, appendHTML, prependHTML, beforeHTML, afterHTML, replaceWithHTML and their Unsafe forms, Doc
- `ba7e64b0e` Trusted Types decisions: the two CSP directives, sinks that require trusted values, the compliant-string outcome, policy creation, the attri
- `fe3908168` Trusted Types: trustedTypes, policies, TrustedHTML, TrustedScript, TrustedScriptURL; the attribute, markup and script-text sinks ask HTML.Tr
- `acf4d2f8c` Interface objects: accessor functions are named get x and set x; a getter that answered for a plain object checks its interface (Web IDL 3.7
- `2c224cc5e` docs: DOM and HTML record, steps 5 to 8 (Sanitizer API, Trusted Types, interface objects)
- `95ad10ff2` Range.createContextualFragment: the command records the fragment's own node number; its scripts run when inserted
- `d17d31197` img.currentSrc: parse a srcset attribute, parse a sizes attribute, the source set of a picture, select an image source (HTML 4.8.4.3) in Lea
- `fa41e65f5` The window's event handler attributes are own properties of the global object (Web IDL 3.7.6)
- `2db04faba` new FormData(form, submitter): the entry list of a form in Lean (HTML 4.10.21.4), the formdata event; node_query 196
- `5b70624fe` DOM XPath: document.evaluate over the XPath 1.0 evaluator
- `229bc0e03` XSLTProcessor over the XSLT 1.0 processor; DOMParser documents keep prefixes, namespace declarations and CDATA sections
- `671fc6dbf` XMLSerializer: the XML serialization of DOM Parsing in the engine
- `de2a7dcda` DOMParser: the document has the URL of the page's document
- `85ea6fa0a` DOM XPath adapter: theorems and tests; design record
- `2fb86e4a4` innerHTML and outerHTML getters in XML documents: the XML serialization
- `19f02ea96` tail-recursion allow list: DOM.XmlSerialize.serializeNode (depth of the DOM tree)
- `d67491b8e` design record: proved, tested only and open for the browser's XML APIs
- `784c80080` DOMParser XML documents keep the document type; readiness of script-made documents
- `eb5bfd4f6` Document.rootElement: the document element when it is an svg element
- `ea4f5fb37` XSLTProcessor.transformToFragment: parse an html result as createContextualFragment does
- `0193239ed` XSLTProcessor: an html result is written for the HTML parser
- `2a56c60be` DOM XPath adapter: more theorems (the HTML name test changes QName tests only; result conversions; Text serialization); axioms printed
- `66bf5b9b5` design record: proof status
- `2bcbf55de` WebGL: the rendering context interfaces from one table of the IDL in Lean (PageGl.Table, PageGl.Idl, web_api op 100); the object interfaces;
- `ccab9b0e1` WebCodecs: pixel formats and the frame layout in Lean, with the bounds theorem of copyTo and the buffer constructor (copyPlan_inBounds)
- `0e0306a01` WebCodecs: VideoFrame rotation (exact on doubles), visible rectangle and display size in Lean; ofBuffer_inBounds
- `be43de7bd` WebCodecs: configuration validity and the web_api ops 120 to 125 (frame from a buffer, frame from a frame, copy plan, configuration check)
- `e37ae3e34` WebCodecs page objects: VideoFrame (from bytes and from a frame), VideoColorSpace, encoded chunks and the four codecs over Lean's ops; inter
- `1cd3a0d45` WebGL: the state machine and GL error model in Lean (PageGl.State: first error wins for every command, image byte bounds), overload signatur
- `ce2421d1b` WebGL page glue: arguments converted by the IDL's overload signatures, modelled commands through Lean's state machine (op 102), the drawing 
- `2a145e10e` WebCodecs: pixel conversions in Lean (RGB re-orderings, I420 and NV12 round trips proved, Y'CbCr to R'G'B' by exact integer arithmetic), cop
- `8a99922cc` WebCodecs: codec strings in Lean (fixed names accepted exactly, VP9 profile constraints, avc1/avc3), read by the configuration check
- `6ecf053c7` docs: WebGL and WebCodecs record (assessment, design, GLSL translator subset, codec options, proved/tested/open)

