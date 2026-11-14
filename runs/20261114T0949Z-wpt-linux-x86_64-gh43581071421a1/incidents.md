### Crashes, stalls and harness timeouts

CRASH 48, STALL 15, TIMEOUT 4408; against `20261114T0907Z-wpt-linux-x86_64-gh43577416594a1`: CRASH 51 -> 48 (+0 new, -3 gone), STALL 9 -> 15 (+8 new, -2 gone), TIMEOUT 4759 -> 4408 (+77 new, -428 gone).

**CRASH** (48, by top directory; NEW: not in the previous run's list)

- connection-allowlist/
  - `/connection-allowlist/tentative/dedicated-worker.sub.window.html`: the page ended without the harness completion (4 subtests reported)
- content-security-policy/
  - `/content-security-policy/embedded-enforcement/required_csp-header.html`: halted: memory limit: the script's heap is full (x5)
  - `/content-security-policy/frame-src/frame-src-blocked-path-matching.sub.html`: the page ended without the harness completion (1 subtests reported)
- dom/
  - `/dom/ranges/Range-compareBoundaryPoints.html`: halted: step budget exhausted
  - `/dom/ranges/Range-set.html`: halted: step budget exhausted
- fetch/
  - `/fetch/api/basic/keepalive.any.html`: the page ended without the harness completion (12 subtests reported)
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

**STALL** (15, by top directory; NEW: not in the previous run's list)

- IndexedDB/
  - `/IndexedDB/event-dispatch-active-flag.any.worker.html` NEW: no result in 300s of wall time
  - `/IndexedDB/idb-explicit-commit.any.worker.html` NEW: no result in 300s of wall time
  - `/IndexedDB/transaction-scheduling-across-databases.any.worker.html` NEW: no result in 300s of wall time
  - `/IndexedDB/transaction-scheduling-within-database.any.worker.html` NEW: no result in 300s of wall time
- content-security-policy/
  - `/content-security-policy/generic/policy-inherited-correctly-by-plznavigate.html`: no result in 300s of wall time
- css/
  - `/css/css-flexbox/abspos/position-absolute-013.html`: no result in 300s of wall time
- fetch/
  - `/fetch/metadata/unload.https.sub.html`: no result in 300s of wall time
- html/
  - `/html/browsers/browsing-the-web/history-traversal/pageswap/pageswap-iframe.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-inherited-from-required-csp.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-initial-empty-document-toward-same-origin.html`: no result in 300s of wall time
  - `/html/webappapis/dynamic-markup-insertion/opening-the-input-stream/ignore-opens-during-unload.window.html`: no result in 300s of wall time
- pointerevents/
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?mouse` NEW: no result in 300s of wall time
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?pen` NEW: no result in 300s of wall time
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?touch` NEW: no result in 300s of wall time
- resource-timing/
  - `/resource-timing/tentative/initiator-url/set-interval.any.worker.html` NEW: no result in 300s of wall time

**No longer CRASH** (3): `/editing/run/justifycenter.html?1001-2000`, `/fetch/metadata/generated/element-video-poster.https.sub.html`, `/fetch/metadata/generated/element-video-poster.sub.html`

**No longer STALL** (2): `/css/selectors/invalidation/has-complexity.html`, `/dom/events/scrolling/input-text-scroll-event-when-using-arrow-keys.html`

**No longer TIMEOUT** (428): `/accelerometer/Accelerometer-iframe-access.https.html`, `/accelerometer/Accelerometer.https.html`, `/accelerometer/GravitySensor.https.html`, `/accelerometer/LinearAccelerationSensor.https.html`, `/accessibility/svg-mouse-listener.html`, `/ai/decision-model/decision-model.tentative.https.window.html`, `/ai/language-model/language-model-abort.tentative.https.window.html`, `/ai/language-model/language-model-create.tentative.https.window.html`, `/ai/language-model/prompt/prompt-post-abort.tentative.https.window.html`, `/ai/language-model/prompt/streaming/prompt-streaming-post-abort.tentative.https.window.html`, `/ai/language_detection/language-detector-detect-concurrent.tentative.https.window.html`, `/ai/language_detection/language-detector-detect-post-abort.tentative.https.window.html`, `/ai/rewriter/rewriter-rewrite-concurrent.tentative.https.window.html`, `/ai/rewriter/rewriter-rewrite-post-abort.tentative.https.window.html`, `/ai/rewriter/rewriter-rewrite-streaming-concurrent.tentative.https.window.html`, `/ai/rewriter/rewriter-rewrite-streaming-post-abort.tentative.https.window.html`, `/ai/semantic_embedder/semantic-embedder-downloadprogress.tentative.https.window.html`, `/ai/summarizer/speed/summarizer-summarize-concurrent.tentative.https.window.html`, `/ai/summarizer/speed/summarizer-summarize-streaming-concurrent.tentative.https.window.html`, `/ai/summarizer/summarizer-summarize-concurrent.tentative.https.window.html`, `/ai/summarizer/summarizer-summarize-post-abort.tentative.https.window.html`, `/ai/summarizer/summarizer-summarize-streaming-concurrent.tentative.https.window.html`, `/ai/summarizer/summarizer-summarize-streaming-post-abort.tentative.https.window.html`, `/ai/translator/translator.optional.https.window.html`, `/ai/writer/writer-write-concurrent.tentative.https.window.html`, `/ai/writer/writer-write-post-abort.tentative.https.window.html`, `/ai/writer/writer-write-streaming-concurrent.tentative.https.window.html`, `/ai/writer/writer-write-streaming-post-abort.tentative.https.window.html`, `/ambient-light/AmbientLightSensor-iframe-access.https.html`, `/ambient-light/AmbientLightSensor.https.html`, `/audio-output/enumerateDevices-with-selectAudioOutput.https.html`, `/audio-output/removeTrack-after-setSinkId.https.html`, `/audio-output/setSinkId-with-selectAudioOutput.https.html`, `/clipboard-apis/async-navigator-clipboard-basics.https.html`, `/clipboard-apis/async-navigator-clipboard-change-event.tentative.https.html`, `/clipboard-apis/async-navigator-clipboard-read-sanitize.https.html`, `/clipboard-apis/async-navigator-clipboard-write-domstring.https.html`, `/clipboard-apis/async-navigator-clipboard-write-multiple.tentative.https.sub.html`, `/clipboard-apis/async-unsanitized-standard-html-read-fail.tentative.https.html`, `/clipboard-apis/permissions-policy/clipboard-read/clipboard-read-enabled-by-permissions-policy-attribute-cross-origin-tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-read/clipboard-read-enabled-by-permissions-policy-attribute-tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-read/clipboard-read-enabled-by-permissions-policy-cross-origin-tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-read/clipboard-read-enabled-by-permissions-policy.tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-read/clipboard-read-enabled-on-self-origin-by-permissions-policy.tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-write/clipboard-write-enabled-by-permissions-policy-attribute-cross-origin-tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-write/clipboard-write-enabled-by-permissions-policy-attribute-tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-write/clipboard-write-enabled-by-permissions-policy-cross-origin-tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-write/clipboard-write-enabled-by-permissions-policy.tentative.https.sub.html`, `/clipboard-apis/permissions-policy/clipboard-write/clipboard-write-enabled-on-self-origin-by-permissions-policy.tentative.https.sub.html`, `/clipboard-apis/permissions/readText-denied.https.html`, `/clipboard-apis/permissions/readText-granted.https.html`, `/clipboard-apis/permissions/writeText-denied.https.html`, `/clipboard-apis/permissions/writeText-granted.https.html`, `/clipboard-apis/text-write-read/async-writeText-read.https.html`, `/clipboard-apis/text-write-read/async-writeText-readText.https.html`, `/close-watcher/iframes/dialog-cross-origin-ynn.html`, `/close-watcher/iframes/dialog-cross-origin-ynyn.html`, `/close-watcher/user-activation/n-activate-preventDefault.html?dialog`, `/close-watcher/user-activation/n-activate.html?dialog`, `/close-watcher/user-activation/nn-activate-dialog.html`, `/close-watcher/user-activation/ny-activate-preventDefault.html?dialog`, `/close-watcher/user-activation/ny.html?dialog`, `/close-watcher/user-activation/nyn-popovers.html`, `/close-watcher/user-activation/nyyn-dialog.html`, `/close-watcher/user-activation/nyyyn-dialog.html`, `/close-watcher/user-activation/y-dialog-disconnected.html`, `/close-watcher/user-activation/y-popover-disconnected.html`, `/close-watcher/user-activation/y.html?CloseWatcher`, `/close-watcher/user-activation/y.html?dialog`, `/close-watcher/user-activation/yn-activate.html?CloseWatcher`, `/close-watcher/user-activation/yn-activate.html?dialog`, `/close-watcher/user-activation/yn.html?CloseWatcher`, `/close-watcher/user-activation/yn.html?dialog`, `/close-watcher/user-activation/ynn-CloseWatcher.html`, `/close-watcher/user-activation/ynn-dialog.html`, `/close-watcher/user-activation/yy.html?CloseWatcher`, `/close-watcher/user-activation/yy.html?dialog`, `/close-watcher/user-activation/yyn.html?CloseWatcher`, `/close-watcher/user-activation/yyn.html?dialog`, `/close-watcher/user-activation/yyy-CloseWatcher-dialog-popover.html` and 348 more

**New TIMEOUT** (77): `/IndexedDB/blob-composite-blob-reads.any.html`, `/IndexedDB/blob-composite-blob-reads.any.worker.html`, `/IndexedDB/event-dispatch-active-flag.any.html`, `/IndexedDB/get-databases.any.html`, `/IndexedDB/idb-explicit-commit.any.html`, `/IndexedDB/idb-partitioned-coverage.sub.html`, `/IndexedDB/idbindex-rename.any.html`, `/IndexedDB/idbindex-rename.any.worker.html`, `/IndexedDB/idbobjectstore-rename-store.any.html`, `/IndexedDB/idbobjectstore-rename-store.any.worker.html`, `/IndexedDB/keyorder.any.html`, `/IndexedDB/keyorder.any.worker.html`, `/IndexedDB/nested-cloning-large-multiple.any.worker.html`, `/IndexedDB/nested-cloning-large.any.worker.html`, `/IndexedDB/transaction-scheduling-across-databases.any.html`, `/IndexedDB/transaction-scheduling-within-database.any.html`, `/css/css-conditional/container-queries/scroll-state/scroll-state-scrolled-keyboard-scroll-on-body.html`, `/css/css-conditional/container-queries/scroll-state/scroll-state-scrolled-multiple-scrollers.html`, `/css/css-conditional/container-queries/scroll-state/scroll-state-scrolled-wheel-scroll.html`, `/css/css-overflow/scroll-markers/root-scroll-button-activation.html`, `/css/css-overflow/scroll-markers/root-scroll-marker-activation-in-iframe.html`, `/css/css-overflow/scroll-markers/scroll-marker-activation-scroll.html`, `/css/css-overflow/scroll-markers/scroll-marker-scroll-container.html`, `/css/css-overscroll-behavior/overscroll-behavior-single-axis-keyboard.html`, `/css/css-overscroll-behavior/overscroll-behavior-single-axis.html`, `/css/css-scroll-snap/input/snap-area-overflow-boundary-viewport-covering.html`, `/css/css-scroll-snap/overscroll-snap.html`, `/css/css-scroll-snap/snap-events/scrollsnapchanging/scrollsnapchanging-after-layout-change.tentative.html`, `/css/css-scroll-snap/snap-events/scrollsnapchanging/scrollsnapchanging-on-fast-scroll.tentative.html`, `/css/css-scroll-snap/snap-events/scrollsnapchanging/scrollsnapchanging-on-user-scroll.tentative.html`, `/css/css-scroll-snap/unrelated-gesture-scroll-during-snap.html`, `/css/css-transforms/scroll-preserve-3d.html`, `/css/css-view-transitions/navigation/pageswap-after-media-change.html?initial`, `/css/selectors/active-toplayer-001.html`, `/dom/events/scrolling/scrollend-event-fired-after-snap.html`, `/dom/events/scrolling/visibility-hidden-scrolls.html`, `/fetch/compression-dictionary/dictionary-registration.tentative.https.html`, `/html/canvas/element/manual/imagebitmap/createImageBitmap-in-worker-transfer.html`, `/html/editing/dnd/datastore/datatransferitemlist-dragstart-after-dispatch.html`, `/html/editing/dnd/events/pointer-suppression.html`, `/html/user-activation/activation-trigger-touch.tentative.html`, `/inert/inert-scrollbar-hittest.html`, `/input-events/input-events-cut-paste.html`, `/pointerevents/pointerevent-boundary-event-target-when-hover-generates-content-under-pointer.html`, `/pointerevents/pointerevent-drag-interaction.html`, `/pointerevents/pointerevent_auxclick_is_a_pointerevent.html?mouse`, `/pointerevents/pointerevent_auxclick_is_a_pointerevent.html?pen`, `/pointerevents/pointerevent_boundary_events_in_capturing.html?mouse`, `/pointerevents/pointerevent_boundary_events_in_capturing.html?pen`, `/pointerevents/pointerevent_boundary_events_in_capturing.html?touch`, `/pointerevents/pointerevent_capture_suppressing_mouse.html`, `/pointerevents/pointerevent_contextmenu_is_a_pointerevent.html?mouse`, `/pointerevents/pointerevent_contextmenu_is_a_pointerevent.html?touch`, `/pointerevents/pointerevent_pointerrawupdate_coalesced_events_attributes.https.html?mouse`, `/pointerevents/pointerevent_pointerrawupdate_coalesced_events_attributes.https.html?pen`, `/pointerevents/pointerevent_pointerrawupdate_coalesced_events_attributes.https.html?touch`, `/pointerevents/pointerevent_touch-action-inherit_parent-none_touch.html`, `/pointerevents/pointerevent_touch-action-overflow-hidden_touch.html`, `/pointerevents/pointerup_button_value_matches_corresponding_pointerdown.html`, `/storage-access-api/storage-access-beyond-cookies.getDirectory.sub.https.window.html`, `/storage-access-api/storage-access-beyond-cookies.indexedDB.sub.https.window.html`, `/storage-access-api/storage-access-beyond-cookies.locks.sub.https.window.html`, `/touch-events/single-tap-when-touchend-listener-use-sync-xhr.html`, `/uievents/mouse/attributes.html`, `/web-locks/frames.https.html`, `/web-locks/partitioned-web-locks.tentative.https.html`, `/web-locks/query-ordering.https.html`, `/web-locks/signal.https.any.html`, `/web-locks/signal.https.any.worker.html`, `/web-locks/steal.https.any.html`, `/web-locks/steal.https.any.worker.html`, `/webcodecs/video-encoder-flush.https.any.html?av1`, `/webcodecs/video-encoder-flush.https.any.html?h264_avc`, `/webcodecs/video-encoder-flush.https.any.html?vp8`, `/webcodecs/video-encoder-flush.https.any.worker.html?av1`, `/webcodecs/video-encoder-flush.https.any.worker.html?h264_avc`, `/webcodecs/video-encoder-flush.https.any.worker.html?vp8`

