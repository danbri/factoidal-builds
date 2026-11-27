/* Native reference: minimp3 with the flags of the Wasm build, decoding a whole file frame by
   frame (the decoder finds each frame in the rest of the file), floats written as they are. */
#include <stdio.h>
#include <stdlib.h>
#define MINIMP3_IMPLEMENTATION
#define MINIMP3_NO_SIMD
#define MINIMP3_FLOAT_OUTPUT
#include "minimp3.h"
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long n = ftell(f); fseek(f, 0, SEEK_SET);
  unsigned char *b = malloc(n); fread(b, 1, n, f); fclose(f);
  FILE *o = fopen(argv[2], "wb");
  mp3dec_t d; mp3dec_init(&d); mp3dec_frame_info_t info; float pcm[MINIMP3_MAX_SAMPLES_PER_FRAME];
  long off = 0, frames = 0, samples = 0;
  while (off < n) {
    int s = mp3dec_decode_frame(&d, b + off, n - off, pcm, &info);
    if (info.frame_bytes == 0) break;
    off += info.frame_bytes;
    if (s > 0) { fwrite(pcm, sizeof(float), s * info.channels, o); frames++; samples += s; }
  }
  fclose(o); printf("%s: %ld frames, %ld samples per channel, %d channels, %d Hz\n", argv[1], frames, samples, info.channels, info.hz);
  return 0;
}
