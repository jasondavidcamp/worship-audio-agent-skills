#!/usr/bin/env python3
"""Analyze basic WAV render metrics without external dependencies."""

from __future__ import annotations

import argparse
import json
import math
import struct
import wave
from pathlib import Path


def _pcm_scale(sample_width: int) -> float:
    if sample_width == 1:
        return 128.0
    return float(1 << (8 * sample_width - 1))


def _iter_pcm_samples(raw: bytes, sample_width: int):
    if sample_width == 1:
        for value in raw:
            yield (value - 128) / 128.0
    elif sample_width == 2:
        count = len(raw) // 2
        for value in struct.unpack("<" + "h" * count, raw):
            yield value / _pcm_scale(sample_width)
    elif sample_width == 3:
        for i in range(0, len(raw), 3):
            chunk = raw[i : i + 3]
            if len(chunk) < 3:
                break
            value = int.from_bytes(chunk + (b"\xff" if chunk[2] & 0x80 else b"\x00"), "little", signed=True)
            yield value / _pcm_scale(sample_width)
    elif sample_width == 4:
        count = len(raw) // 4
        for value in struct.unpack("<" + "i" * count, raw):
            yield value / _pcm_scale(sample_width)
    else:
        raise ValueError(f"Unsupported PCM sample width: {sample_width} bytes")


def analyze_wav(path: Path) -> dict:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frames = wav.getnframes()
        raw = wav.readframes(frames)

    peak = 0.0
    square_sum = 0.0
    sample_count = 0
    for sample in _iter_pcm_samples(raw, sample_width):
        absolute = abs(sample)
        if absolute > peak:
            peak = absolute
        square_sum += sample * sample
        sample_count += 1

    rms = math.sqrt(square_sum / sample_count) if sample_count else 0.0
    peak_dbfs = 20.0 * math.log10(peak) if peak > 0 else None
    rms_dbfs = 20.0 * math.log10(rms) if rms > 0 else None
    crest_db = peak_dbfs - rms_dbfs if peak_dbfs is not None and rms_dbfs is not None else None

    return {
        "path": str(path),
        "channels": channels,
        "sample_rate": sample_rate,
        "bit_depth": sample_width * 8,
        "frames": frames,
        "duration_seconds": frames / sample_rate if sample_rate else 0,
        "peak_dbfs": peak_dbfs,
        "rms_dbfs": rms_dbfs,
        "crest_db": crest_db,
        "clipped_samples": None,
        "notes": "Basic PCM metrics only; use a LUFS/spectrum analyzer for final ranking.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze basic WAV render metrics.")
    parser.add_argument("wav", nargs="+", type=Path, help="WAV file(s) to inspect")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    results = [analyze_wav(path) for path in args.wav]
    print(json.dumps(results, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
