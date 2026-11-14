### Crashes, stalls and harness timeouts

CRASH 48, STALL 17, TIMEOUT 4394; against `20261114T0949Z-wpt-linux-x86_64-gh43581071421a1`: CRASH 48 -> 48 (+0 new, -0 gone), STALL 15 -> 17 (+4 new, -2 gone), TIMEOUT 4408 -> 4394 (+31 new, -45 gone).

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

**STALL** (17, by top directory; NEW: not in the previous run's list)

- IndexedDB/
  - `/IndexedDB/event-dispatch-active-flag.any.worker.html`: no result in 300s of wall time
  - `/IndexedDB/idb-explicit-commit.any.worker.html`: no result in 300s of wall time
  - `/IndexedDB/transaction-scheduling-across-databases.any.worker.html`: no result in 300s of wall time
  - `/IndexedDB/transaction-scheduling-within-database.any.worker.html`: no result in 300s of wall time
- compression/
  - `/compression/compression-large-flush-output.any.html` NEW: no result in 300s of wall time
  - `/compression/compression-large-flush-output.any.worker.html` NEW: no result in 300s of wall time
- content-security-policy/
  - `/content-security-policy/generic/policy-inherited-correctly-by-plznavigate.html`: no result in 300s of wall time
- css/
  - `/css/css-flexbox/abspos/position-absolute-013.html`: no result in 300s of wall time
  - `/css/css-variables/variable-cycles.html` NEW: no result in 300s of wall time
  - `/css/selectors/invalidation/has-complexity.html` NEW: no result in 300s of wall time
- html/
  - `/html/browsers/browsing-the-web/history-traversal/pageswap/pageswap-iframe.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-inherited-from-required-csp.html`: no result in 300s of wall time
  - `/html/browsers/sandboxing/sandbox-initial-empty-document-toward-same-origin.html`: no result in 300s of wall time
  - `/html/webappapis/dynamic-markup-insertion/opening-the-input-stream/ignore-opens-during-unload.window.html`: no result in 300s of wall time
- pointerevents/
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?mouse`: no result in 300s of wall time
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?pen`: no result in 300s of wall time
  - `/pointerevents/coalesced_events_attributes_under_load.https.optional.html?touch`: no result in 300s of wall time

**No longer STALL** (2): `/fetch/metadata/unload.https.sub.html`, `/resource-timing/tentative/initiator-url/set-interval.any.worker.html`

**No longer TIMEOUT** (45): `/css/css-pseudo/marker-hit-testing.html`, `/html/editing/dnd/events/pointer-suppression.html`, `/html/user-activation/activation-trigger-touch.tentative.html`, `/pointerevents/compat/pointerevent_touch-action_two-finger_interaction.html`, `/pointerevents/pointerevent_boundary_events_in_capturing.html?mouse`, `/pointerevents/pointerevent_boundary_events_in_capturing.html?pen`, `/pointerevents/pointerevent_boundary_events_in_capturing.html?touch`, `/pointerevents/pointerevent_element_haspointercapture.html?mouse`, `/pointerevents/pointerevent_element_haspointercapture.html?pen`, `/pointerevents/pointerevent_element_haspointercapture.html?touch`, `/pointerevents/pointerevent_element_haspointercapture_release_pending_capture.html?mouse`, `/pointerevents/pointerevent_element_haspointercapture_release_pending_capture.html?pen`, `/pointerevents/pointerevent_element_haspointercapture_release_pending_capture.html?touch`, `/pointerevents/pointerevent_pointercancel_touch.html`, `/pointerevents/pointerevent_pointerleave_after_pointercancel_touch.html`, `/pointerevents/pointerevent_pointerleave_descendant_over.html`, `/pointerevents/pointerevent_pointermove.html`, `/pointerevents/pointerevent_pointermove_isprimary_same_as_pointerdown.html?mouse`, `/pointerevents/pointerevent_pointermove_isprimary_same_as_pointerdown.html?touch`, `/pointerevents/pointerevent_pointermove_on_chorded_mouse_button.html`, `/pointerevents/pointerevent_pointerout_after_pointercancel_touch.html`, `/pointerevents/pointerevent_pointerout_pen.html`, `/pointerevents/pointerevent_pointerout_received_once.html`, `/pointerevents/pointerevent_releasepointercapture_events_to_original_target.html?pen`, `/pointerevents/pointerevent_releasepointercapture_events_to_original_target.html?touch`, `/pointerevents/pointerevent_releasepointercapture_onpointercancel_touch.html`, `/pointerevents/pointerevent_releasepointercapture_pointerup_touch.html`, `/pointerevents/pointerevent_releasepointercapture_release_right_after_capture.html?mouse`, `/pointerevents/pointerevent_releasepointercapture_release_right_after_capture.html?pen`, `/pointerevents/pointerevent_releasepointercapture_release_right_after_capture.html?touch`, `/pointerevents/pointerevent_sequence_at_implicit_release_on_click.html?mouse`, `/pointerevents/pointerevent_sequence_at_implicit_release_on_click.html?pen`, `/pointerevents/pointerevent_sequence_at_implicit_release_on_click.html?touch`, `/pointerevents/pointerevent_sequence_at_implicit_release_on_drag.html`, `/pointerevents/pointerevent_setpointercapture_inactive_button_mouse.html`, `/pointerevents/pointerevent_setpointercapture_override_pending_capture_element.html?mouse`, `/pointerevents/pointerevent_setpointercapture_override_pending_capture_element.html?pen`, `/pointerevents/pointerevent_setpointercapture_override_pending_capture_element.html?touch`, `/pointerevents/pointerevent_setpointercapture_pointerup_mouse.html`, `/pointerevents/pointerevent_setpointercapture_pointerup_touch.html`, `/pointerevents/pointerlock/pointerevent_pointermove_on_chorded_mouse_button_when_locked.html`, `/pointerevents/pointerlock/pointerevent_pointerrawupdate_in_pointerlock.https.html`, `/touch-events/multi-touch-interactions.html`, `/touch-events/multi-touch-interfaces.html`, `/touch-events/single-tap-when-touchend-listener-use-sync-xhr.html`

**New TIMEOUT** (31): `/cookiestore/change_eventhandler_for_already_expired.https.window.html`, `/cookiestore/change_eventhandler_for_attribute_change.https.window.html`, `/cookiestore/change_eventhandler_for_document_cookie.https.window.html`, `/cookiestore/change_eventhandler_for_http_cookie_and_set_cookie_headers.https.window.html`, `/cookiestore/change_eventhandler_for_no_change.https.window.html`, `/cookiestore/change_eventhandler_for_no_name_and_no_value.https.window.html`, `/cookiestore/change_eventhandler_for_no_name_equals_in_value.https.window.html`, `/cookiestore/change_eventhandler_for_no_name_multiple_values.https.window.html`, `/cookiestore/cookieStore_event_basic.https.window.html`, `/cookiestore/cookieStore_event_delete.https.window.html`, `/cookiestore/cookieStore_event_overwrite.https.window.html`, `/css/css-transitions/non-rendered-element-004.tentative.html`, `/css/selectors/invalidation/media-loading-pseudo-classes-in-has.sub.html`, `/css/selectors/media/media-loading-state.sub.html`, `/css/selectors/media/media-playback-state-timing.html`, `/css/selectors/media/media-playback-state.html`, `/css/selectors/media/media-playing-paused-style-invalidation.html`, `/css/selectors/media/sound-state.html`, `/fetch/metadata/unload.https.sub.html`, `/geolocation/idlharness.https.window.html`, `/html/canvas/element/manual/wide-gamut-canvas/encode-hdr.html`, `/html/semantics/forms/the-select-element/customizable-select/select-events-2.optional.html`, `/pointerevents/coalesced_events_attributes.https.html?mouse`, `/pointerevents/pointerevent_boundary_events_cross_origin.html`, `/pointerevents/pointerevent_mouse_pointercapture_inactivate_pointer.html`, `/pointerevents/pointerevent_pointercapture-in-shadow-dom.html`, `/pointerevents/pointerevent_pointercapture-not-lost-in-chorded-buttons.html`, `/pointerevents/pointerevent_releasepointercapture_invalid_pointerid.html`, `/pointerevents/predicted_events_attributes.html?mouse`, `/shadow-dom/focus/focus-shadowhost-display-none.html`, `/streams/transferable/writable-stream.html`

