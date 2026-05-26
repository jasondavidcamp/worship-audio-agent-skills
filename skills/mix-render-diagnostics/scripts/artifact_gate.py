#!/usr/bin/env python3
"""Screen WAV renders for static/crackle-like artifacts before listening checks.

This is a guardrail, not a replacement for listening. It catches obvious
high-frequency/hash differences and format problems, then prints PASS/WARN.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
import wave
from pathlib import Path

import numpy as np


def _iter_pcm_samples(raw: bytes, sample_width: int):
    if sample_width == 1:
        for value in raw:
            yield (value - 128) / 128.0
    elif sample_width == 2:
        count = len(raw) // 2
        for value in struct.unpack("<" + "h" * count, raw):
            yield value / float(1 << 15)
    elif sample_width == 3:
        for i in range(0, len(raw), 3):
            chunk = raw[i : i + 3]
            if len(chunk) < 3:
                break
            value = int.from_bytes(chunk + (b"\xff" if chunk[2] & 0x80 else b"\x00"), "little", signed=True)
            yield value / float(1 << 23)
    elif sample_width == 4:
        count = len(raw) // 4
        for value in struct.unpack("<" + "i" * count, raw):
            yield value / float(1 << 31)
    else:
        raise ValueError(f"Unsupported PCM sample width: {sample_width} bytes")


def _db(value: float) -> float:
    return 20.0 * math.log10(max(float(value), 1e-12))


def read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frames = wav.getnframes()
        raw = wav.readframes(frames)
    samples = np.fromiter(_iter_pcm_samples(raw, sample_width), dtype=np.float64)
    if channels > 1:
        samples = samples.reshape(-1, channels)
    else:
        samples = samples.reshape(-1, 1)
    return samples, sample_rate


def high_ratio(y: np.ndarray, sr: int) -> float:
    if len(y) < 2048:
        return 0.0
    size = min(len(y), sr * 5)
    chunk = y[:size]
    window = np.hanning(len(chunk))
    spectrum = np.abs(np.fft.rfft(chunk * window))
    freqs = np.fft.rfftfreq(len(chunk), 1 / sr)
    total = float(np.sum(spectrum * spectrum))
    high = float(np.sum(spectrum[freqs >= 8000] ** 2))
    return high / (total + 1e-12)


def zero_crossing_rate(y: np.ndarray) -> float:
    if len(y) < 2:
        return 0.0
    return float(np.mean(np.signbit(y[1:]) != np.signbit(y[:-1])))


def window_metrics(data: np.ndarray, sr: int, window_s: float) -> list[dict]:
    y = data.mean(axis=1)
    window = int(sr * window_s)
    rows = []
    for start in range(0, max(1, len(y) - window + 1), window):
        chunk = y[start : start + window]
        if len(chunk) < sr:
            continue
        diff = np.diff(chunk, prepend=chunk[:1])
        rms = float(np.sqrt(np.mean(chunk * chunk)))
        diff_rms = float(np.sqrt(np.mean(diff * diff)))
        peak = float(np.max(np.abs(chunk)))
        rows.append(
            {
                "start_s": round(start / sr, 3),
                "end_s": round((start + len(chunk)) / sr, 3),
                "rms_dbfs": round(_db(rms), 2),
                "peak_dbfs": round(_db(peak), 2),
                "diff_to_signal_db": round(_db(diff_rms / (rms + 1e-12)), 2),
                "zero_crossing_rate": round(zero_crossing_rate(chunk), 5),
                "high_8k_ratio": round(high_ratio(chunk, sr), 6),
            }
        )
    return rows


def summarize(path: Path, window_s: float) -> dict:
    data, sr = read_wav(path)
    mono = data.mean(axis=1)
    peak = float(np.max(np.abs(data)))
    rms = float(np.sqrt(np.mean(mono * mono)))
    windows = window_metrics(data, sr, window_s)
    return {
        "path": str(path),
        "sample_rate": sr,
        "channels": int(data.shape[1]),
        "duration_s": round(len(mono) / sr, 3),
        "peak_dbfs": round(_db(peak), 2),
        "rms_dbfs": round(_db(rms), 2),
        "windows": windows,
    }


def compare(candidate: dict, baseline: dict | None) -> tuple[str, list[str]]:
    warnings = []
    if candidate["peak_dbfs"] >= -0.3:
        warnings.append("Candidate is too close to clipping.")
    if not baseline:
        return ("WARN" if warnings else "PASS", warnings)

    if candidate["sample_rate"] != baseline["sample_rate"]:
        warnings.append("Sample rate differs from baseline.")
    if candidate["channels"] != baseline["channels"]:
        warnings.append("Channel count differs from baseline.")

    pairs = zip(candidate["windows"], baseline["windows"], strict=False)
    for cand, base in pairs:
        high_delta = cand["high_8k_ratio"] - base["high_8k_ratio"]
        zcr_delta = cand["zero_crossing_rate"] - base["zero_crossing_rate"]
        diff_delta = cand["diff_to_signal_db"] - base["diff_to_signal_db"]
        if high_delta > 0.015 or zcr_delta > 0.03 or diff_delta > 4.0:
            warnings.append(
                "Possible static/hash window "
                f"{cand['start_s']}-{cand['end_s']}s: "
                f"high_delta={high_delta:.5f}, zcr_delta={zcr_delta:.5f}, diff_delta={diff_delta:.2f}dB."
            )
    return ("WARN" if warnings else "PASS", warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--baseline", type=Path, help="Known-good WAV of the same section.")
    parser.add_argument("--window-s", type=float, default=5.0)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    candidate = summarize(args.candidate, args.window_s)
    baseline = summarize(args.baseline, args.window_s) if args.baseline else None
    status, warnings = compare(candidate, baseline)
    result = {
        "status": status,
        "warnings": warnings,
        "candidate": candidate,
        "baseline": baseline,
        "notes": "Automated static screening is imperfect. User-reported static invalidates a batch even when this script passes.",
    }
    print(json.dumps(result, indent=2 if args.pretty else None))
    return 1 if status == "WARN" else 0


if __name__ == "__main__":
    raise SystemExit(main())
