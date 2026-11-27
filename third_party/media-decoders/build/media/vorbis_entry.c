/*
 * vorbis_entry.c: the entry point of the libvorbis decoder build that runs in the
 * Lean WasmVM engine (record: docs/designissues/2026-11-08-media-wasmvm.md).
 *
 * Built by tools/wasmvm/build-media.sh into a standalone Wasm module (WASI imports
 * only, no JavaScript). The host (Lean) demuxes Ogg or WebM and gives one Vorbis
 * packet per call: first the three header packets, then audio packets. Exports:
 *
 *   mw_alloc(n) -> ptr, mw_free(ptr)
 *   mw_vorbis_header(pkt, len, index) -> 0   index 0, 1, 2; negative: a libvorbis error
 *   mw_vorbis_rate() -> Hz, mw_vorbis_channels() -> count   after the three headers
 *   mw_vorbis_decode(pkt, len) -> n   samples per channel written to mw_pcm(), as
 *                                     interleaved little-endian int16 (2 channels at
 *                                     most are kept); negative: an error
 *   mw_pcm() -> ptr
 *   mw_abi() -> 2                     version of this interface (1: the exports above)
 *   mw_vorbis_decode_f32(pkt, len) -> n   as mw_vorbis_decode, with every channel (8 at
 *                                     most; more is the error -102) as interleaved
 *                                     32-bit floats in mw_pcm_f32(), in Vorbis channel
 *                                     order (Vorbis I specification section 4.3.9)
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "vorbis/codec.h"

#define MAX_OUT 8192

static vorbis_info vi;
static vorbis_comment vc;
static vorbis_dsp_state vd;
static vorbis_block vb;
static int ready = 0;
static int64_t packetno = 0;
static int16_t pcm[MAX_OUT * 2];
#define MAX_CH 8
static float pcmf[MAX_OUT * MAX_CH];

__attribute__((export_name("mw_alloc")))
void *mw_alloc(int32_t n) { return malloc((size_t) n); }

__attribute__((export_name("mw_free")))
void mw_free(void *p) { free(p); }

__attribute__((export_name("mw_pcm")))
int16_t *mw_pcm(void) { return pcm; }

static ogg_packet packet(unsigned char *p, int32_t len, int bos) {
  ogg_packet op;
  op.packet = p;
  op.bytes = len;
  op.b_o_s = bos;
  op.e_o_s = 0;
  op.granulepos = -1;
  op.packetno = packetno++;
  return op;
}

__attribute__((export_name("mw_vorbis_header")))
int32_t mw_vorbis_header(unsigned char *p, int32_t len, int32_t index) {
  if (index == 0) {
    if (ready) { vorbis_block_clear(&vb); vorbis_dsp_clear(&vd); ready = 0; }
    vorbis_info_init(&vi);
    vorbis_comment_init(&vc);
    packetno = 0;
  }
  ogg_packet op = packet(p, len, index == 0);
  int r = vorbis_synthesis_headerin(&vi, &vc, &op);
  if (r != 0) return r;
  if (index == 2) {
    if (vorbis_synthesis_init(&vd, &vi) != 0) return -200;
    vorbis_block_init(&vd, &vb);
    ready = 1;
  }
  return 0;
}

__attribute__((export_name("mw_vorbis_rate")))
int32_t mw_vorbis_rate(void) { return (int32_t) vi.rate; }

__attribute__((export_name("mw_vorbis_channels")))
int32_t mw_vorbis_channels(void) { return vi.channels; }

static int16_t clip(float f) {
  int v = (int) (f * 32767.f + (f < 0 ? -0.5f : 0.5f));
  if (v > 32767) v = 32767;
  if (v < -32768) v = -32768;
  return (int16_t) v;
}

__attribute__((export_name("mw_vorbis_decode")))
int32_t mw_vorbis_decode(unsigned char *p, int32_t len) {
  if (!ready) return -100;
  ogg_packet op = packet(p, len, 0);
  if (vorbis_synthesis(&vb, &op) != 0) return -101;
  vorbis_synthesis_blockin(&vd, &vb);
  int total = 0;
  int ch = vi.channels > 2 ? 2 : vi.channels;
  float **out;
  int n;
  while ((n = vorbis_synthesis_pcmout(&vd, &out)) > 0) {
    if (total + n > MAX_OUT) n = MAX_OUT - total;
    for (int i = 0; i < n; i++)
      for (int c = 0; c < ch; c++) pcm[(total + i) * ch + c] = clip(out[c][i]);
    vorbis_synthesis_read(&vd, n);
    total += n;
    if (total >= MAX_OUT) break;
  }
  return total;
}

__attribute__((export_name("mw_abi")))
int32_t mw_abi(void) { return 2; }

__attribute__((export_name("mw_pcm_f32")))
float *mw_pcm_f32(void) { return pcmf; }

__attribute__((export_name("mw_vorbis_decode_f32")))
int32_t mw_vorbis_decode_f32(unsigned char *p, int32_t len) {
  if (!ready) return -100;
  if (vi.channels < 1 || vi.channels > MAX_CH) return -102;
  ogg_packet op = packet(p, len, 0);
  if (vorbis_synthesis(&vb, &op) != 0) return -101;
  vorbis_synthesis_blockin(&vd, &vb);
  int total = 0;
  int ch = vi.channels;
  float **out;
  int n;
  while ((n = vorbis_synthesis_pcmout(&vd, &out)) > 0) {
    if (total + n > MAX_OUT) n = MAX_OUT - total;
    for (int i = 0; i < n; i++)
      for (int c = 0; c < ch; c++) pcmf[(total + i) * ch + c] = out[c][i];
    vorbis_synthesis_read(&vd, n);
    total += n;
    if (total >= MAX_OUT) break;
  }
  return total;
}
