/*
 * vp8_entry.c: the entry point of the libvpx VP8 decoder build that runs in the Lean
 * WasmVM engine (record: docs/designissues/2026-11-08-media-wasmvm.md).
 *
 * Built by tools/wasmvm/build-media.sh into a standalone Wasm module (WASI imports
 * only, no JavaScript). The host (Lean) demuxes WebM and gives one VP8 frame per
 * call. Exports:
 *
 *   mw_alloc(n) -> ptr, mw_free(ptr)
 *   mw_vp8_init() -> 0                 negative: a libvpx error code
 *   mw_vp8_decode(frame, len) -> 0     1 when the frame gave no picture; negative: error
 *   mw_vp8_width(), mw_vp8_height()    of the last picture
 *   mw_vp8_i420(out) -> bytes          the last picture as packed I420 (Y, then U, V);
 *                                      the host converts it to RGBA (Media.Yuv)
 *   mw_vp8_rgba(out) -> bytes          the last picture as RGBA (4 bytes a pixel, rows
 *                                      from the top, opacity 255), BT.601 limited
 *                                      range: a cross-check of the host's conversion
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "vpx/vpx_decoder.h"
#include "vpx/vp8dx.h"

static vpx_codec_ctx_t codec;
static int inited = 0;
static vpx_image_t *img = 0;

__attribute__((export_name("mw_alloc")))
void *mw_alloc(int32_t n) { return malloc((size_t) n); }

__attribute__((export_name("mw_free")))
void mw_free(void *p) { free(p); }

__attribute__((export_name("mw_vp8_init")))
int32_t mw_vp8_init(void) {
  if (inited) vpx_codec_destroy(&codec);
  vpx_codec_dec_cfg_t cfg = {1, 0, 0};
  int r = vpx_codec_dec_init(&codec, vpx_codec_vp8_dx(), &cfg, 0);
  inited = r == VPX_CODEC_OK;
  img = 0;
  return inited ? 0 : -r;
}

__attribute__((export_name("mw_vp8_decode")))
int32_t mw_vp8_decode(const uint8_t *frame, int32_t len) {
  if (!inited) return -100;
  int r = vpx_codec_decode(&codec, frame, (unsigned) len, 0, 0);
  if (r != VPX_CODEC_OK) return -r;
  vpx_codec_iter_t iter = 0;
  vpx_image_t *got = vpx_codec_get_frame(&codec, &iter);
  if (!got) return 1;
  img = got;
  return 0;
}

__attribute__((export_name("mw_vp8_width")))
int32_t mw_vp8_width(void) { return img ? (int32_t) img->d_w : 0; }

__attribute__((export_name("mw_vp8_height")))
int32_t mw_vp8_height(void) { return img ? (int32_t) img->d_h : 0; }

static uint8_t clamp(int v) { return (uint8_t) (v < 0 ? 0 : v > 255 ? 255 : v); }

/* BT.601, limited range, in 16.16 fixed point:
   R = 1.164(Y-16) + 1.596(V-128), G = 1.164(Y-16) - 0.392(U-128) - 0.813(V-128),
   B = 1.164(Y-16) + 2.017(U-128).
   The same arithmetic as L4Factoidal.Media.Yuv.toRgba, which the host uses; this
   export is the cross-check. */
__attribute__((export_name("mw_vp8_rgba")))
int32_t mw_vp8_rgba(uint8_t *out) {
  if (!img) return 0;
  int w = (int) img->d_w, h = (int) img->d_h;
  for (int y = 0; y < h; y++) {
    const uint8_t *yr = img->planes[0] + y * img->stride[0];
    const uint8_t *ur = img->planes[1] + (y >> 1) * img->stride[1];
    const uint8_t *vr = img->planes[2] + (y >> 1) * img->stride[2];
    uint8_t *o = out + y * w * 4;
    for (int x = 0; x < w; x++) {
      int c = 76309 * (yr[x] - 16);
      int d = ur[x >> 1] - 128, e = vr[x >> 1] - 128;
      o[0] = clamp((c + 104597 * e + 32768) >> 16);
      o[1] = clamp((c - 25674 * d - 53278 * e + 32768) >> 16);
      o[2] = clamp((c + 132201 * d + 32768) >> 16);
      o[3] = 255;
      o += 4;
    }
  }
  return w * h * 4;
}

__attribute__((export_name("mw_vp8_i420")))
int32_t mw_vp8_i420(uint8_t *out) {
  if (!img) return 0;
  int w = (int) img->d_w, h = (int) img->d_h, cw = (w + 1) / 2, ch = (h + 1) / 2;
  uint8_t *o = out;
  for (int y = 0; y < h; y++) { memcpy(o, img->planes[0] + y * img->stride[0], w); o += w; }
  for (int p = 1; p <= 2; p++)
    for (int y = 0; y < ch; y++) { memcpy(o, img->planes[p] + y * img->stride[p], cw); o += cw; }
  return (int32_t) (o - out);
}

__attribute__((export_name("mw_abi")))
int32_t mw_abi(void) { return 2; }
