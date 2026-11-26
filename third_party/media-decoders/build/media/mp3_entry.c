/*
 * mp3_entry.c: the entry point of the minimp3 decoder build that runs in the Lean WasmVM
 * engine (records: docs/designissues/2026-11-08-media-wasmvm.md and
 * docs/designissues/2026-11-26-foafnaut-audio-plan.md in danbri/factoidal-core).
 *
 * Built by build-media.sh into a standalone Wasm module (WASI imports only, no
 * JavaScript). The host (Lean) reads the MP3 stream (ID3 tags, frame headers, the
 * Xing/LAME header) and gives exactly one MPEG audio frame per call, in stream order, so
 * the decoder never searches for a frame itself: minimp3 accepts a buffer that is one
 * whole frame starting at offset 0. The bit reservoir of layer III is kept between calls.
 * Exports:
 *
 *   mw_abi() -> 2                     version of this interface
 *   mw_alloc(n) -> ptr, mw_free(ptr)
 *   mw_mp3_init() -> 0                a new decoder state (call before a stream and
 *                                     after a seek)
 *   mw_mp3_decode(frame, len) -> n    samples per channel of the frame, written to
 *                                     mw_pcm_f32() as interleaved 32-bit floats and to
 *                                     mw_pcm() as interleaved little-endian int16;
 *                                     0: the bytes were not one decodable frame
 *   mw_mp3_info(i) -> value           of the last call: 0 frame bytes used, 1 channels,
 *                                     2 sample rate in Hz, 3 layer, 4 bit rate in kbit/s
 *   mw_pcm_f32() -> ptr, mw_pcm() -> ptr   1152 samples per channel, 2 channels at most
 *
 * minimp3 (CC0-1.0) is built with MINIMP3_NO_SIMD (the engine has no SIMD) and
 * MINIMP3_FLOAT_OUTPUT; the int16 output is minimp3's own conversion of the floats.
 */
#include <stdint.h>
#include <stdlib.h>
#define MINIMP3_IMPLEMENTATION
#define MINIMP3_NO_SIMD
#define MINIMP3_FLOAT_OUTPUT
#include "minimp3.h"

static mp3dec_t dec;
static mp3dec_frame_info_t info;
static float pcmf[MINIMP3_MAX_SAMPLES_PER_FRAME];
static int16_t pcm16[MINIMP3_MAX_SAMPLES_PER_FRAME];

__attribute__((export_name("mw_abi")))
int32_t mw_abi(void) { return 2; }

__attribute__((export_name("mw_alloc")))
void *mw_alloc(int32_t n) { return malloc((size_t) n); }

__attribute__((export_name("mw_free")))
void mw_free(void *p) { free(p); }

__attribute__((export_name("mw_pcm_f32")))
float *mw_pcm_f32(void) { return pcmf; }

__attribute__((export_name("mw_pcm")))
int16_t *mw_pcm(void) { return pcm16; }

__attribute__((export_name("mw_mp3_init")))
int32_t mw_mp3_init(void) {
  mp3dec_init(&dec);
  info.frame_bytes = info.channels = info.hz = info.layer = info.bitrate_kbps = 0;
  return 0;
}

__attribute__((export_name("mw_mp3_decode")))
int32_t mw_mp3_decode(const uint8_t *frame, int32_t len) {
  if (len <= 0) return 0;
  int n = mp3dec_decode_frame(&dec, frame, len, pcmf, &info);
  if (n <= 0 || info.channels < 1 || info.channels > 2) return 0;
  mp3dec_f32_to_s16(pcmf, pcm16, n * info.channels);
  return n;
}

__attribute__((export_name("mw_mp3_info")))
int32_t mw_mp3_info(int32_t i) {
  switch (i) {
    case 0: return info.frame_bytes;
    case 1: return info.channels;
    case 2: return info.hz;
    case 3: return info.layer;
    case 4: return info.bitrate_kbps;
    default: return -1;
  }
}
