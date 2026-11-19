# Foafnaut on Linux ARM64

Extract the desktop archive and start the browser from a Linux ARM64 desktop session.

```sh
tar -xzf foafnaut-browser-linux-arm64.tar.gz
cd foafnaut-linux-arm64
sha256sum -c SHA256SUMS
./foafnaut --version
./foafnaut --url https://example.org/
```

Ubuntu 24.04 needs `libsdl2-2.0-0`, `libvulkan1` and a Vulkan driver such as
`mesa-vulkan-drivers`. The archive includes an AArch64 executable, its SDL window library,
the document worker and render-plan WebAssembly, fonts and browser pages. Control-L
focuses the address bar. Alt-Left goes back.

The release's `build-info.json` identifies the source, native tools and original engine build.
Its `window-smoke.json` records the extracted archive running under X11, Xvfb and Mesa software
Vulkan on ARM64. Mac XQuartz forwarding, physical GPUs and Wayland have separate behaviour.
