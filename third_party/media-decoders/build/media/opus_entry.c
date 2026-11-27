/*
 * opus_entry.c: the entry point of the libopus decoder build that runs in the Lean
 * WasmVM engine (record: docs/designissues/2026-11-08-media-wasmvm.md).
 *
 * Built by tools/wasmvm/build-media.sh into a standalone Wasm module (WASI imports
 * only, no JavaScript). The host (Lean) demuxes Ogg or WebM and gives one Opus packet
 * per call. Exports:
 *
 *   mw_alloc(n) -> ptr             memory for the host to write a packet into
 *   mw_free(ptr)
 *   mw_opus_init(channels) -> 0    a decoder at 48000 Hz; negative: an Opus error code
 *   mw_opus_decode(pkt, len) -> n  samples per channel written to mw_pcm(), as
 *                                  interleaved little-endian int16; negative: an error
 *   mw_pcm() -> ptr                the PCM buffer (5760 samples per channel at most)
 *   mw_abi() -> 2                  version of this interface (1: the exports above)
 *   mw_opus_decode_f32(pkt, len) -> n   as mw_opus_decode, as interleaved 32-bit
 *                                  floats in mw_pcm_f32() (libopus opus_decode_float)
 */
#include <stdint.h>
#include <stdlib.h>
#include "opus.h"

#define MAX_FRAME 5760

static OpusDecoder *dec = 0;
static int chans = 0;
static opus_int16 pcm[MAX_FRAME * 2];
static float pcmf[MAX_FRAME * 2];

__attribute__((export_name("mw_alloc")))
void *mw_alloc(int32_t n) { return malloc((size_t) n); }

__attribute__((export_name("mw_free")))
void mw_free(void *p) { free(p); }

__attribute__((export_name("mw_pcm")))
opus_int16 *mw_pcm(void) { return pcm; }

__attribute__((export_name("mw_opus_init")))
int32_t mw_opus_init(int32_t channels) {
  int err = 0;
  if (channels < 1 || channels > 2) return -1;
  if (dec) opus_decoder_destroy(dec);
  dec = opus_decoder_create(48000, channels, &err);
  chans = channels;
  return err == OPUS_OK ? 0 : err;
}

__attribute__((export_name("mw_opus_decode")))
int32_t mw_opus_decode(const unsigned char *pkt, int32_t len) {
  if (!dec) return -100;
  return opus_decode(dec, pkt, len, pcm, MAX_FRAME, 0);
}

__attribute__((export_name("mw_abi")))
int32_t mw_abi(void) { return 2; }

__attribute__((export_name("mw_pcm_f32")))
float *mw_pcm_f32(void) { return pcmf; }

__attribute__((export_name("mw_opus_decode_f32")))
int32_t mw_opus_decode_f32(const unsigned char *pkt, int32_t len) {
  if (!dec) return -100;
  return opus_decode_float(dec, pkt, len, pcmf, MAX_FRAME, 0);
}
