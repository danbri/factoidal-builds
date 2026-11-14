### Crashes, stalls and harness timeouts

CRASH 51, STALL 9, TIMEOUT 4759; no list of the previous run to compare with.

**CRASH** (51, by top directory)

- connection-allowlist/
  - `/connection-allowlist/tentative/dedicated-worker.sub.window.html`: the page ended without the harness completion (4 subtests reported)
- content-security-policy/
  - `/content-security-policy/embedded-enforcement/required_csp-header.html`: the test process was killed (SIGKILL)
  - `/content-security-policy/frame-src/frame-src-blocked-path-matching.sub.html`: the page ended without the harness completion (1 subtests reported)
- dom/
  - `/dom/ranges/Range-compareBoundaryPoints.html`: halted: step budget exhausted
  - `/dom/ranges/Range-set.html`: halted: step budget exhausted
- editing/
  - `/editing/run/justifycenter.html?1001-2000`: the test process was killed (SIGKILL)
- fetch/
  - `/fetch/api/basic/keepalive.any.html`: the page ended without the harness completion (12 subtests reported)
  - `/fetch/metadata/generated/element-video-poster.https.sub.html`: the test process was killed (SIGKILL)
  - `/fetch/metadata/generated/element-video-poster.sub.html`: the test process was killed (SIGKILL)
  - `/fetch/metadata/generated/worker-dedicated-constructor.https.sub.html`: the page ended without the harness completion (2 subtests reported)
  - `/fetch/metadata/generated/worker-dedicated-constructor.sub.html`: the page ended without the harness completion (1 subtests reported)
  - `/fetch/security/dangling-markup/dangling-markup-mitigation-allowed-apis.https.html`: the page ended without the harness completion (8 subtests reported)
- html/
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
  - `/upgrade-insecure-requests/gen/srcdoc-inherit.meta/unset/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/srcdoc-inherit.meta/upgrade/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.http-rp/upgrade/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
  - `/upgrade-insecure-requests/gen/top.meta/unset/worker-classic.https.html`: the page ended without the harness completion (2 subtests reported)
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

**STALL** (9, by top directory)

- content-security-policy/
  - `/content-security-policy/generic/policy-inherited-correctly-by-plznavigate.html`: no result in 300s of wall time
- css/
  - `/css/css-flexbox/abspos/position-absolute-013.html`: no result in 300s of wall time
  - `/css/selectors/invalidation/has-complexity.html`: no result in 300s of wall time
- dom/
  - `/dom/events/scrolling/input-text-scroll-event-when-using-arrow-keys.html`: no result in 300s of wall time
- fetch/
  - `/fetch/metadata/unload.https.sub.html`: no result in 300s of wall time
- html/
  - `/html/browsers/browsing-the-web/history-traversal/pageswap/pageswap-iframe.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-inherited-from-required-csp.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-initial-empty-document-toward-same-origin.html`: no result in 300s of wall time
  - `/html/webappapis/dynamic-markup-insertion/opening-the-input-stream/ignore-opens-during-unload.window.html`: no result in 300s of wall time

