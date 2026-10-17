#!/usr/bin/env python3
"""Alpha-20 sonification renderer. Stdlib-only (wave, struct, math)."""
import json
import math
import struct
import sys
import wave
from pathlib import Path

SR = 44100

def adsr(n, a, d, s, r):
    na, nd, nr = int(a * n), int(d * n), int(r * n)
    ns = max(n - na - nd - nr, 0)
    out = []
    out += [i / max(na, 1) for i in range(na)]
    out += [1 - (1 - s) * (i / max(nd, 1)) for i in range(nd)]
    out += [s] * ns
    out += [s * (1 - i / max(nr, 1)) for i in range(nr)]
    return out[:n]

def render_event(ev):
    dur_ms = ev["t_end_ms"] - ev["t_start_ms"]
    n = int(SR * dur_ms / 1000)
    env = adsr(n, *ev["adsr"])
    samples = []
    if ev.get("freq_start") and ev.get("freq_end"):
        f0, f1 = ev["freq_start"], ev["freq_end"]
        phase = 0.0
        for i in range(n):
            f = f0 + (f1 - f0) * i / n
            phase += 2 * math.pi * f / SR
            samples.append(math.sin(phase) * env[i])
    else:
        f = ev.get("freq_hz") or 440
        for i in range(n):
            samples.append(math.sin(2 * math.pi * f * i / SR) * env[i])
    return samples

def main(src, dst):
    data = json.loads(Path(src).read_text())
    total_n = int(SR * data["duration_ms"] / 1000)
    buf = [0.0] * total_n
    for ev in data["events"]:
        start = int(SR * ev["t_start_ms"] / 1000)
        for i, s in enumerate(render_event(ev)):
            if start + i < total_n:
                buf[start + i] += s
    peak = max((abs(x) for x in buf), default=1.0) or 1.0
    with wave.open(dst, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(32767 * s / peak)) for s in buf))
    print("wrote " + dst + " (" + str(data["duration_ms"]) + " ms, " + str(total_n) + " samples @ " + str(SR) + " Hz)")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
