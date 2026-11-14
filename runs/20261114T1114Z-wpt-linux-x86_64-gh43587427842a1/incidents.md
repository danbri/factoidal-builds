### Crashes, stalls and harness timeouts

CRASH 61, STALL 18, TIMEOUT 4382; against `20261114T1029Z-wpt-linux-x86_64-gh43585273487a1`: CRASH 48 -> 61 (+13 new, -0 gone), STALL 17 -> 18 (+2 new, -1 gone), TIMEOUT 4394 -> 4382 (+59 new, -71 gone).

**CRASH** (61, by top directory; NEW: not in the previous run's list)

- IndexedDB/
  - `/IndexedDB/idbindex-multientry.any.html` NEW: halted: memory limit: the script's heap is full (x5)
  - `/IndexedDB/keypath.any.html` NEW: the test process was killed (SIGABRT) [thread 'main' (2518) has overflowed its stack; fatal runtime error: stack overflow, aborting]
  - `/IndexedDB/keypath.any.sharedworker.html` NEW: the test process was killed (SIGABRT) [thread 'main' (2535) has overflowed its stack; fatal runtime error: stack overflow, aborting]
  - `/IndexedDB/keypath.any.worker.html` NEW: the test process was killed (SIGABRT) [thread 'main' (2531) has overflowed its stack; fatal runtime error: stack overflow, aborting]
- connection-allowlist/
  - `/connection-allowlist/tentative/dedicated-worker.sub.window.html`: the page ended without the harness completion (4 subtests reported)
- content-security-policy/
  - `/content-security-policy/embedded-enforcement/required_csp-header.html`: halted: memory limit: the script's heap is full (x5)
  - `/content-security-policy/frame-src/frame-src-blocked-path-matching.sub.html`: the page ended without the harness completion (1 subtests reported)
  - `/content-security-policy/inside-worker/sharedworker-connect-src.sub.html` NEW: the page ended without the harness completion (6 subtests reported)
  - `/content-security-policy/inside-worker/sharedworker-script-src.sub.html` NEW: the page ended without the harness completion (7 subtests reported)
- dom/
  - `/dom/ranges/Range-compareBoundaryPoints.html`: halted: step budget exhausted
  - `/dom/ranges/Range-set.html`: halted: step budget exhausted
- fetch/
  - `/fetch/api/basic/keepalive.any.html`: the page ended without the harness completion (12 subtests reported)
  - `/fetch/metadata/generated/worker-dedicated-constructor.https.sub.html`: the page ended without the harness completion (2 subtests reported)
  - `/fetch/metadata/generated/worker-dedicated-constructor.sub.html`: the page ended without the harness completion (1 subtests reported)
  - `/fetch/security/dangling-markup/dangling-markup-mitigation-allowed-apis.https.html`: the page ended without the harness completion (8 subtests reported)
- html/
  - `/html/cross-origin-embedder-policy/reporting-to-endpoint.https.html` NEW: the page ended without the harness completion (4 subtests reported)
  - `/html/dom/reflection-embedded.html`: halted: step budget exhausted
  - `/html/dom/reflection-forms.html`: halted: step budget exhausted
  - `/html/dom/reflection-tabular.html`: halted: step budget exhausted
  - `/html/dom/reflection-text.html`: halted: step budget exhausted
  - `/html/editing/focus/sequential-focus-navigation-and-the-tabindex-attribute/focus-tabindex-event.html`: the page ended without the harness completion (1 subtests reported)
  - `/html/semantics/forms/the-form-element/form-action-submission.html`: the page ended without the harness completion (1 subtests reported)
  - `/html/webappapis/scripting/events/compile-event-handler-settings-objects.html`: the page ended without the harness completion (1 subtests reported)
- idle-detection/
  - `/idle-detection/idle-detection-disabled-by-permissions-policy.https.sub.html`: ReferenceError: IdleDetector is not defined (then no harness completion; 2 subtests reported)
- resource-timing/
  - `/resource-timing/resource-timing-level1.sub.html`: the page ended without the harness completion (5 subtests reported)
- serial/
  - `/serial/serial-allowed-by-permissions-policy-attribute.https.sub.html`: TypeError: Cannot read properties of undefined (reading 'getPorts') (then no harness completion; 1 subtests reported)
  - `/serial/serial-allowed-by-permissions-policy.https.sub.html`: TypeError: Cannot read properties of undefined (reading 'getPorts') (then no harness completion; 2 subtests reported)
  - `/serial/serial-disabled-by-permissions-policy.https.sub.html`: TypeError: Cannot read properties of undefined (reading 'getPorts') (then no harness completion; 2 subtests reported)
- service-workers/
  - `/service-workers/service-worker/sandboxed-iframe-fetch-event.https.html`: the page ended without the harness completion (7 subtests reported)
  - `/service-workers/service-worker/worker-in-sandboxed-iframe-by-csp-fetch-event.https.html`: the page ended without the harness completion (3 subtests reported)
  - `/service-workers/service-worker/worker-interception-redirect.https.html`: the page ended without the harness completion (1 subtests reported)
  - `/service-workers/service-worker/worker-interception.https.html`: the page ended without the harness completion (13 subtests reported)
- svg/
  - `/svg/interact/scripted/pointer-events-fill-stroke-hittest.html`: halted: step budget exhausted
- upgrade-insecure-requests/
  - `/upgrade-insecure-requests/gen/srcdoc-inherit.meta/unset/sharedworker-classic.https.html` NEW: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/srcdoc-inherit.meta/unset/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/srcdoc-inherit.meta/upgrade/sharedworker-classic.https.html` NEW: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/srcdoc-inherit.meta/upgrade/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.http-rp/upgrade/sharedworker-classic.https.html` NEW: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.http-rp/upgrade/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.meta/unset/sharedworker-classic.https.html` NEW: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.meta/unset/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.meta/upgrade/sharedworker-classic.https.html` NEW: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.meta/upgrade/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
- wasm/
  - `/wasm/core/f32.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/f32_cmp.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/f64.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/f64_cmp.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/simd/simd_f32x4_arith.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/simd/simd_f32x4_cmp.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/simd/simd_f32x4_pmin_pmax.wast.js.html`: halted: step budget exhausted (x2)
  - `/wasm/core/simd/simd_f64x2_arith.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/simd/simd_f64x2_cmp.wast.js.html`: halted: step budget exhausted
  - `/wasm/core/simd/simd_f64x2_pmin_pmax.wast.js.html`: halted: step budget exhausted (x2)
  - `/wasm/serialization/module/identity-not-preserved.html`: the page ended without the harness completion (1 subtests reported)
- webhid/
  - `/webhid/hid-allowed-by-permissions-policy-attribute.https.sub.html`: the page ended without the harness completion (2 subtests reported)
  - `/webhid/hid-allowed-by-permissions-policy.https.sub.html`: the page ended without the harness completion (3 subtests reported)
- webusb/
  - `/webusb/usb-allowed-by-permissions-policy-attribute.https.sub.html`: the page ended without the harness completion (2 subtests reported)
  - `/webusb/usb-allowed-by-permissions-policy.https.sub.html`: the page ended without the harness completion (3 subtests reported)
  - `/webusb/usb-disabled-by-permissions-policy.https.sub.html`: the page ended without the harness completion (4 subtests reported)
- workers/
  - `/workers/modules/dedicated-worker-options-credentials.html`: the page ended without the harness completion (21 subtests reported)
  - `/workers/modules/shared-worker-options-credentials.html` NEW: the page ended without the harness completion (21 subtests reported)

**STALL** (18, by top directory; NEW: not in the previous run's list)

- IndexedDB/
  - `/IndexedDB/idb-explicit-commit.any.worker.html`: no result in 300s of wall time
  - `/IndexedDB/transaction-scheduling-across-databases.any.worker.html`: no result in 300s of wall time
  - `/IndexedDB/transaction-scheduling-within-database.any.worker.html`: no result in 300s of wall time
- compression/
  - `/compression/compression-large-flush-output.any.html`: no result in 300s of wall time
  - `/compression/compression-large-flush-output.any.sharedworker.html` NEW: no result in 300s of wall time
  - `/compression/compression-large-flush-output.any.worker.html`: no result in 300s of wall time
- content-security-policy/
  - `/content-security-policy/generic/policy-inherited-correctly-by-plznavigate.html`: no result in 300s of wall time
- css/
  - `/css/css-flexbox/abspos/position-absolute-013.html`: no result in 300s of wall time
  - `/css/css-variables/variable-cycles.html`: no result in 300s of wall time
  - `/css/selectors/invalidation/has-complexity.html`: no result in 300s of wall time
- fetch/
  - `/fetch/metadata/unload.https.sub.html` NEW: no result in 300s of wall time
- html/
  - `/html/browsers/browsing-the-web/history-traversal/pageswap/pageswap-iframe.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-inherited-from-required-csp.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-initial-empty-document-toward-same-origin.html`: no result in 300s of wall time
  - `/html/webappapis/dynamic-markup-insertion/opening-the-input-stream/ignore-opens-during-unload.window.html`: no result in 300s of wall time
- pointerevents/
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?mouse`: no result in 300s of wall time
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?pen`: no result in 300s of wall time
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?touch`: no result in 300s of wall time

**No longer STALL** (1): `/IndexedDB/event-dispatch-active-flag.any.worker.html`

**No longer TIMEOUT** (71): `/IndexedDB/event-dispatch-active-flag.any.html`, `/content-security-policy/generic/generic-0_10_1.sub.html`, `/content-security-policy/generic/generic-0_2_2.sub.html`, `/content-security-policy/script-src-attr-elem/script-src-attr-blocked-src-allowed.html`, `/content-security-policy/script-src-attr-elem/script-src-elem-allowed-attr-blocked.html`, `/content-security-policy/script-src-attr-elem/script-src-elem-blocked-src-allowed.html`, `/content-security-policy/script-src/script-src-1_1.html`, `/content-security-policy/script-src/script-src-1_2.html`, `/content-security-policy/script-src/script-src-report-only-policy-works-with-external-hash-policy.html`, `/content-security-policy/script-src/script-src-report-only-policy-works-with-hash-policy.html`, `/content-security-policy/script-src/script-src-strict_dynamic_double_policy_honor_source_expressions.sub.html`, `/content-security-policy/script-src/scripthash-unicode-normalization.sub.html`, `/content-security-policy/securitypolicyviolation/blockeduri-inline.html`, `/content-security-policy/securitypolicyviolation/targeting-for-inline-handler-in-markup-then-disconnected.html`, `/content-security-policy/securitypolicyviolation/targeting-for-inline-handler-in-markup.html`, `/content-security-policy/unsafe-hashes/script_event_handlers_denied_missing_unsafe_hashes.html`, `/content-security-policy/unsafe-hashes/script_event_handlers_denied_wrong_hash.html`, `/content-security-policy/worker-src/dedicated-none.sub.html`, `/cookiestore/change_eventhandler_for_already_expired.https.window.html`, `/cookiestore/change_eventhandler_for_attribute_change.https.window.html`, `/cookiestore/change_eventhandler_for_document_cookie.https.window.html`, `/cookiestore/change_eventhandler_for_no_change.https.window.html`, `/cookiestore/change_eventhandler_for_no_name_and_no_value.https.window.html`, `/cookiestore/change_eventhandler_for_no_name_equals_in_value.https.window.html`, `/cookiestore/change_eventhandler_for_no_name_multiple_values.https.window.html`, `/cookiestore/cookieStore_event_basic.https.window.html`, `/cookiestore/cookieStore_event_delete.https.window.html`, `/cookiestore/cookieStore_event_overwrite.https.window.html`, `/fetch/metadata/unload.https.sub.html`, `/html/cross-origin-embedder-policy/reporting-report-to-must-be-string.https.window.html`, `/html/cross-origin-embedder-policy/shared-workers.https.html`, `/idle-detection/idlharness.https.window.html`, `/mixed-content/gen/iframe-inherit.http-rp/opt-in/sharedworker-classic.https.html`, `/mixed-content/gen/iframe-inherit.meta/opt-in/sharedworker-classic.https.html`, `/mixed-content/gen/iframe-inherit.meta/unset/sharedworker-classic.https.html`, `/referrer-policy/gen/iframe.http-rp/no-referrer-when-downgrade/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/no-referrer/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/origin-when-cross-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/same-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/strict-origin-when-cross-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/strict-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/unsafe-url/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.http-rp/unset/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/always/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/default/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/never/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/no-referrer-when-downgrade/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/no-referrer/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/origin-when-cross-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/origin-when-crossorigin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/same-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/strict-origin-when-cross-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/strict-origin/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/unsafe-url/sharedworker-classic.http.html`, `/referrer-policy/gen/iframe.meta/unset/sharedworker-classic.http.html`, `/service-workers/cache-storage/sandboxed-iframes.https.html`, `/trusted-types/Document-parseHTMLUnsafe-respects-current-globals-CSP.html`, `/trusted-types/TrustedTypePolicyFactory-createPolicy-cspTests-none.html`, `/trusted-types/TrustedTypePolicyFactory-createPolicy-cspTests.html`, `/trusted-types/require-trusted-types-for.html`, `/trusted-types/trusted-types-reporting-clipping-of-sample.html`, `/trusted-types/trusted-types-reporting-clipping-of-sample.tentative.html`, `/trusted-types/trusted-types-reporting-for-HTMLScriptElement.html`, `/trusted-types/trusted-types-source-file-path.html`, `/trusted-types/trusted-types-svg-script-set-href.html`, `/uievents/textInput/basic.html`, `/uievents/textInput/enter-textarea-contenteditable.html`, `/workers/SharedWorker-detach-frame-in-error-event.html`, `/workers/name-property.html`

**New TIMEOUT** (59): `/IndexedDB/idbindex-multientry.any.sharedworker.html`, `/IndexedDB/idbindex-rename.any.sharedworker.html`, `/IndexedDB/idbobjectstore-rename-store.any.sharedworker.html`, `/IndexedDB/interleaved-cursors-large.any.sharedworker.html`, `/IndexedDB/interleaved-cursors-small.any.sharedworker.html`, `/IndexedDB/keyorder.any.sharedworker.html`, `/IndexedDB/nested-cloning-large-multiple.any.sharedworker.html`, `/IndexedDB/nested-cloning-large.any.sharedworker.html`, `/clipboard-apis/async-navigator-clipboard-basics.https.html`, `/connection-allowlist/tentative/shared-worker.sub.window.html`, `/content-security-policy/inside-worker/sharedworker-report-only.sub.html`, `/content-security-policy/securitypolicyviolation/inside-shared-worker.html`, `/content-security-policy/wasm-unsafe-eval/script-src-spv-asynch.any.sharedworker.html`, `/encoding/encodeInto-tail-unmodified.any.sharedworker.html`, `/fetch/api/abort/general.any.sharedworker.html`, `/fetch/api/cors/data-url-shared-worker.html`, `/fetch/range/general.any.sharedworker.html`, `/html/canvas/offscreen/wide-gamut-canvas/2d.color.space.toBlob.toDataURL.jpeg.linear.float.html`, `/html/canvas/offscreen/wide-gamut-canvas/2d.color.space.toBlob.toDataURL.png.linear.float.html`, `/html/cross-origin-embedder-policy/credentialless/cache-storage.https.window.html?shared_worker`, `/html/semantics/embedded-content/the-canvas-element/toBlob.jpeg.html`, `/html/semantics/embedded-content/the-canvas-element/toBlob.png.html`, `/html/semantics/embedded-content/the-img-element/currentSrc-blob-cache.html`, `/html/webappapis/scripting/processing-model-2/unhandled-promise-rejections/promise-rejection-events.sharedworker.html`, `/permissions-policy/shared-worker-permissions-policy-allow-option.https.tentative.html`, `/permissions-policy/shared-worker-permissions-policy-connect.https.tentative.html`, `/quirks/percentage-height-calculation.html`, `/secure-contexts/basic-shared-worker.html`, `/secure-contexts/basic-shared-worker.https.html`, `/service-workers/cache-storage/cache-abort.https.any.html`, `/service-workers/cache-storage/cache-abort.https.any.sharedworker.html`, `/service-workers/cache-storage/cache-abort.https.any.worker.html`, `/storage-access-api/storage-access-beyond-cookies.caches.sub.https.window.html`, `/storage-access-api/storage-access-beyond-cookies.estimate.sub.https.window.html`, `/trusted-types/DedicatedWorker-constructor-from-SharedWorker.html`, `/trusted-types/ServiceWorkerContainer-register-from-SharedWorker.https.html`, `/trusted-types/SharedWorker-block-eval-function-constructor.html`, `/trusted-types/SharedWorker-eval.html`, `/trusted-types/SharedWorker-importScripts.html`, `/trusted-types/SharedWorker-setTimeout-setInterval.html`, `/trusted-types/block-string-assignment-to-SharedWorker-setTimeout-setInterval.html`, `/trusted-types/trusted-types-reporting-for-SharedWorker-DedicatedWorker-constructor.html`, `/trusted-types/trusted-types-reporting-for-SharedWorker-ServiceWorkerContainer-register.https.html`, `/trusted-types/trusted-types-reporting-for-SharedWorker-eval.html`, `/trusted-types/trusted-types-reporting-for-SharedWorker-function-constructor.html`, `/trusted-types/trusted-types-reporting-for-SharedWorker-importScripts.html`, `/trusted-types/trusted-types-reporting-for-SharedWorker-setTimeout-setInterval.html`, `/web-locks/signal.https.any.sharedworker.html`, `/web-locks/steal.https.any.sharedworker.html`, `/webcodecs/image-decoder.https.any.html`, `/webcodecs/image-decoder.https.any.worker.html`, `/workers/baseurl/alpha/importScripts-in-sharedworker.html`, `/workers/baseurl/alpha/xhr-in-sharedworker.html`, `/workers/constructors/SharedWorker/same-origin.html`, `/workers/semantics/structured-clone/shared.html`, `/workers/shared-worker-from-blob-url.window.html`, `/workers/shared-worker-parse-error-failure.html`, `/workers/shared-worker-partitioned.tentative.html`, `/workers/shared-worker-runtime-error-is-not-parse-error.html`

