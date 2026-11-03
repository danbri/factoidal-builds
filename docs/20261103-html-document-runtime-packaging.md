# HTML document runtime packaging, 3 November 2026

The HTML runtime packager now accepts the reviewed `WebDocument` initializer.
Its existing recursive import walk includes `WebRenderScript`,
`WebRenderFontRequests` and their Lean dependencies. A package is refused when
any of those sources is absent from the build witness or differs from the
committed source. Unreviewed initializers remain refused.

The seven-file browser runtime inventory is unchanged. It contains the Lean
scene engine and WebGPU transport. It does not package the local browser
UI/server, QuickJS WASM, external font broker or font resources.

For a source with `WebDocument.lean`, native macOS packaging adds a checksummed
`html-document-request.json`, documents the `--document` invocation, and runs
that invocation from the relocated bundle. An error JSON result fails the
qualification check. The CLI accepts supplied resource bytes and DOM commands;
it does not fetch URLs, execute JavaScript or open the browser MVP.

This change keeps the publisher's core-main ancestry check and release
finalization unchanged. It does not publish npm. Packager unit tests use
synthetic inputs to check omissions, source changes, relocation and error
refusal; they are not browser or GPU qualification. Actual native execution
remains the macOS candidate workflow's responsibility.
