# Checked SVG policy package gate, 2026-11-03

The [macOS packaging run](https://github.com/danbri/factoidal-builds/actions/runs/41619103206)
failed at `compiled primitive count differs from exported SVG`. The log reports
292 compiled SVG primitives and 39,452 storage floats. The policy/count gate
was stale after the SVG exporter began batching glyph cells into compound
paths and the storage ABI gained path/stroke/transform/clip payloads.

`NativeSceneSVG.shapeElements` emits one filled `<path>` per nonblank glyph.
Each path may contain many closed cell contours. Quadratic and cubic shapes
also emit one path. The gate counted rect/circle/ellipse/line/polygon but omitted
path, so it counted fewer SVG paints than the actual compiler. Adding path to
the element set preserves the exact equality check: a compound path is one
retained paint, regardless of its contour or edge count. This is an exporter
profile check, not an implementation of general SVG rendering semantics.

The next gate would also have failed: its old storage cursor handled only five
fixed vec4 rows and polygon point padding. `NativeSVG.Primitive.rows` now has
the following exact layout:

- 20 fixed floats, including geometry tag/count, fill rule, packed mode,
  paint colors, stroke width, opacity, stroke piece count and active flag.
- Polygon: two floats per point, padded to a vec4 boundary. Path tag 6:
  four floats per linear edge, including all compound contours.
- 20 floats per stroke piece: strip tag 4, disk tag 2 or triangle tag 7.
- Eight inverse affine floats when the mode's transform bit is set.
- Twelve floats per clip, whose count is the mode divided by four.

The mode is cap bit + 2*transform flag + 4*clip count. The revised validator
checks all integral fields and flags, each payload boundary, padding, stroke
piece tags, clip activation/bounds and the exact final storage cursor. It
retains the original finite Float32 range, total storage bound, primitive
count equality, shader binding, CPU probe, viewport, policy evidence and web
asset checks. It does not skip records or accept an arbitrary tail.

No renderer or exported SVG changed in this repair. Existing Lean source has
`compilePrimitives_length`/`Scene.compiled_length`: backend compilation retains
one record per retained paint. Stroke pieces and flattened path edges live
inside that record; they are not extra `primitiveCount` entries.

## Verification

An existing local Lean WASM FOAFNaut exporter and SVG compiler reproduced the
same count failure without compilation. The exported SVG has 36 rects, 105
lines, 49 circles and 79 compound paths: 269 paints. The old gate counted only
190. The artifact has exactly 269 primitives and 33,688 storage floats. Its
105 line records contain three stroke pieces each; the new cursor reaches
the exact end of the buffer. The repaired complete gate passes this evidence.
The local model differs from the CI model; this is a reproduction of the
mechanism, not a claim to have rerun the 292-paint macOS artifact.

Evidence: `/private/tmp/factoidal-policy-count-repro/reproduction-report.json`.
SVG SHA-256:
`4404b4c2392eb7c8d73cc095414c5215120035191021800f946a5214e149d4de`.
Artifact SHA-256:
`39fa9f78e1755f4b3f78975767511a1e4e4a13d6baa914e7c9a666a25a5feab4`.
Existing producer WASM SHA-256:
`cf7d6f80d02b35ef78f5783679c57ff1cb580f010aaa9965e087cd7d47bf5265`.
Existing SVG compiler WASM SHA-256:
`520224f6274333deb13a70b55ecf29db20edf1cbc3720beed5b421424171af36`.
The check used actual compiled Lean WASM, not a native macOS executable or GPU.

The repaired gate also passes the older local rectangle-glyph native package:
1,565 primitives, 31,308 floats, SVG SHA-256
`6b6c6ab57cf9c398c5f84750f938e439448d21e62496fa174a35e06771468525`.

`python3 -m unittest tests/test_foafnaut_policy.py` passes 16 tests. All original
controls remain. New controls cover compound paths as a single paint, each
stroke-piece tag, complete transform/clip tails and 18 malformed payload
variants. Wrong primitive counts still fail, as do truncated or undeclared
tails, unsupported tags, fractional flags/counts and damaged padding/bounds.
The existing build-and-relocate stub controls also remain green. Creating
these package checks makes no new GPU, pixel-equivalence or scheduling claim.
