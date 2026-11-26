#!/usr/bin/env python3
"""The source of core's third_party/media/arpeggio-*.mp3 (CC0): a 4 s stereo C major arpeggio,
44.1 kHz, 16-bit WAV, made here. Encoded with LAME 3.100 as core's third_party/media/README.md says."""
import math, struct, wave
sr, secs = 44100, 4.0
notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 261.63, 196.00]
n = int(sr * secs); step = n // len(notes)
frames = bytearray()
for i in range(n):
    k = min(i // step, len(notes) - 1); t = (i - k * step) / sr
    env = min(1.0, t * 50) * math.exp(-3.0 * t)
    f = notes[k]
    l = 0.45 * env * math.sin(2 * math.pi * f * i / sr)
    r = 0.45 * env * math.sin(2 * math.pi * f * 1.5 * i / sr)
    frames += struct.pack("<hh", int(l * 32767), int(r * 32767))
w = wave.open("arpeggio.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(bytes(frames)); w.close()
