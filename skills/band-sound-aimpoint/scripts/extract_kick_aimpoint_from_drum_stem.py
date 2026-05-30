#!/usr/bin/env python3
"""Extract a private kick-drum aimpoint from a full drum-kit WAV.

This is not source separation. It detects kick-dominant low-band events in a
full drum stem, profiles the strongest hit windows, and optionally writes a
short montage WAV for `mix-render-diagnostics/scripts/reference_score.py
--source kick`.
"""

from __future__ import annotations

import argparse
import json
import math
import wave
from pathlib import Path

import numpy as np


BANDS = {
    "sub_20_60": (20.0, 60.0),
    "kick_60_120": (60.0, 120.0),
    "upper_kick_120_220": (120.0, 220.0),
    "box_220_600": (220.0, 600.0),
    "knock_600_1500": (600.0, 1500.0),
    "attack_2k_5k": (2000.0, 5000.0),
    "hash_5k_10k": (5000.0, 10000.0),
    "air_10k_18k": (10000.0, 18000.0),
}


def db20(value: float) -> float:
    return 20.0 * math.log10(max(float(value), 1e-12))


def db10(value: float) -> float:
    return 10.0 * math.log10(max(float(value), 1e-24))


def read_wav(path: Path) -> tuple[np.ndarray, int, int]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frames = wav.getnframes()
        raw = wav.readframes(frames)

    if sample_width == 2:
        data = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    elif sample_width == 3:
        bytes_ = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
        values = (
            bytes_[:, 0].astype(np.int32)
            | (bytes_[:, 1].astype(np.int32) << 8)
            | (bytes_[:, 2].astype(np.int32) << 16)
        )
        values = np.where(values & 0x800000, values - 0x1000000, values)
        data = values.astype(np.float32) / 8388608.0
    elif sample_width == 4:
        data = np.frombuffer(raw, dtype="<i4").astype(np.float32) / 2147483648.0
    else:
        raise ValueError(f"Unsupported WAV bit depth: {sample_width * 8}")

    return data.reshape(-1, channels), sample_rate, sample_width


def band_energy(frame: np.ndarray, sample_rate: int) -> dict[str, float]:
    nfft = max(4096, 1 << (len(frame) - 1).bit_length())
    padded = np.zeros(nfft, dtype=np.float32)
    padded[: len(frame)] = frame.astype(np.float32)
    spectrum = np.abs(np.fft.rfft(padded * np.hanning(nfft))) ** 2
    freqs = np.fft.rfftfreq(nfft, 1.0 / sample_rate)
    output: dict[str, float] = {}
    for name, (low, high) in BANDS.items():
        mask = (freqs >= low) & (freqs < min(high, sample_rate / 2.0))
        output[name] = float(np.sum(spectrum[mask])) if np.any(mask) else 1e-24
    return output


def percentile_summary(values: list[float], percentiles: tuple[int, ...] = (10, 25, 50, 75, 90)) -> dict[str, float]:
    if not values:
        return {}
    array = np.array(values, dtype=np.float64)
    return {str(percentile): round(float(np.percentile(array, percentile)), 2) for percentile in percentiles}


def detect_kick_hits(mono: np.ndarray, sample_rate: int, percentile: float) -> list[dict]:
    nfft = 4096
    hop = 512
    window = np.hanning(nfft).astype(np.float32)
    freqs = np.fft.rfftfreq(nfft, 1.0 / sample_rate)
    indices = {name: np.flatnonzero((freqs >= low) & (freqs < min(high, sample_rate / 2.0))) for name, (low, high) in BANDS.items()}

    rows = []
    for start in range(0, len(mono) - nfft, hop):
        spectrum = np.abs(np.fft.rfft(mono[start : start + nfft] * window)) ** 2
        energy = {name: float(np.sum(spectrum[index])) if len(index) else 1e-24 for name, index in indices.items()}
        low = energy["sub_20_60"] + energy["kick_60_120"] + energy["upper_kick_120_220"]
        box = energy["box_220_600"] + energy["knock_600_1500"]
        attack = energy["attack_2k_5k"]
        high = energy["hash_5k_10k"] + energy["air_10k_18k"]
        score = db10(low) - 0.55 * db10(box) - 0.18 * db10(high) + 0.12 * db10(attack)
        rows.append((start + nfft // 2, score, energy, low, box, attack, high))

    scores = np.array([row[1] for row in rows], dtype=np.float64)
    threshold = float(np.percentile(scores, percentile))
    min_distance = int(0.24 * sample_rate)
    hits: list[dict] = []
    last_sample = -10**9
    for index in range(1, len(rows) - 1):
        sample, score, energy, low, box, attack, high = rows[index]
        if score < threshold or score < rows[index - 1][1] or score < rows[index + 1][1]:
            continue
        low_box = db10(low / (box + 1e-24))
        low_high = db10(low / (high + 1e-24))
        attack_low = db10((attack + 1e-24) / (low + 1e-24))
        if low_box < -1.0 or low_high < -9.0 or attack_low > 3.0:
            continue
        hit = {
            "sample": sample,
            "time_s": sample / sample_rate,
            "score": score,
            "low_box_db": low_box,
            "low_high_db": low_high,
            "attack_low_db": attack_low,
            "energies": energy,
        }
        if sample - last_sample < min_distance:
            if hits and score > hits[-1]["score"]:
                hits[-1] = hit
                last_sample = sample
            continue
        hits.append(hit)
        last_sample = sample
    return hits


def analyze_hit(mono: np.ndarray, hit: dict, sample_rate: int, pre: int, post: int) -> dict | None:
    center = int(hit["sample"])
    start = max(0, center - pre)
    end = min(len(mono), center + post)
    segment = mono[start:end]
    if len(segment) < int(0.12 * sample_rate):
        return None
    energy = band_energy(segment, sample_rate)
    thump = energy["kick_60_120"]
    transient = segment[pre : pre + int(0.035 * sample_rate)] if pre < len(segment) else segment[: int(0.035 * sample_rate)]
    body_start = pre + int(0.060 * sample_rate)
    body_end = pre + int(0.180 * sample_rate)
    body = segment[body_start:body_end] if body_end < len(segment) else segment[int(0.060 * sample_rate) :]
    attack_body_db = None
    if len(transient) and len(body):
        attack_body_db = db20(np.sqrt(np.mean(transient * transient))) - db20(np.sqrt(np.mean(body * body)))
    peak = float(np.max(np.abs(segment))) if len(segment) else 0.0
    rms = float(np.sqrt(np.mean(segment * segment))) if len(segment) else 0.0
    return {
        "time_s": round(hit["time_s"], 3),
        "peak_dbfs": round(db20(peak), 2),
        "rms_dbfs": round(db20(rms), 2),
        "crest_db": round(db20(peak / max(rms, 1e-12)), 2),
        "attack_body_db": round(attack_body_db, 2) if attack_body_db is not None else None,
        "ratios": {
            "sub_vs_thump_db": round(db10(energy["sub_20_60"] / thump), 2),
            "upper_vs_thump_db": round(db10(energy["upper_kick_120_220"] / thump), 2),
            "box_vs_thump_db": round(db10(energy["box_220_600"] / thump), 2),
            "attack_vs_thump_db": round(db10(energy["attack_2k_5k"] / thump), 2),
            "hash_vs_attack_db": round(db10(energy["hash_5k_10k"] / max(energy["attack_2k_5k"], 1e-24)), 2),
        },
        "score": round(float(hit["score"]), 2),
    }


def write_wav(path: Path, audio: np.ndarray, sample_rate: int, sample_width: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
    if peak > 0.95:
        audio = audio * (0.95 / peak)
    if sample_width == 3:
        values = np.clip(audio * 8388607, -8388608, 8388607).astype(np.int32)
        raw = bytearray()
        for value in values.reshape(-1):
            raw.extend(int(value).to_bytes(3, "little", signed=True))
        payload = bytes(raw)
    else:
        values = np.clip(audio * 32767, -32768, 32767).astype("<i2")
        sample_width = 2
        payload = values.tobytes()
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(audio.shape[1] if audio.ndim == 2 else 1)
        wav.setsampwidth(sample_width)
        wav.setframerate(sample_rate)
        wav.writeframes(payload)


def extract(input_wav: Path, output_json: Path, output_wav: Path | None, max_hits: int, percentile: float) -> dict:
    stereo, sample_rate, sample_width = read_wav(input_wav)
    mono = stereo.mean(axis=1)
    pre = int(0.030 * sample_rate)
    post = int(0.260 * sample_rate)
    hits = detect_kick_hits(mono, sample_rate, percentile)
    hit_rows = [row for hit in hits if (row := analyze_hit(mono, hit, sample_rate, pre, post)) is not None]
    selected = sorted(hit_rows, key=lambda row: (row["score"], row["peak_dbfs"]), reverse=True)[:max_hits]

    if output_wav:
        gap = np.zeros((int(0.08 * sample_rate), stereo.shape[1]), dtype=np.float32)
        pieces = []
        for row in sorted(selected, key=lambda item: item["time_s"]):
            center = int(round(row["time_s"] * sample_rate))
            start = max(0, center - pre)
            end = min(len(stereo), center + post)
            segment = stereo[start:end].copy()
            fade = int(0.006 * sample_rate)
            if len(segment) > fade * 2:
                ramp = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
                segment[:fade] *= ramp
                segment[-fade:] *= ramp[::-1]
            pieces.extend([segment, gap])
        montage = np.vstack(pieces) if pieces else np.zeros((1, stereo.shape[1]), dtype=np.float32)
        write_wav(output_wav, montage, sample_rate, sample_width)

    profile = {
        "source": str(input_wav),
        "method": "kick-dominant hit windows detected from low-band STFT envelope in full drum-kit stem; not source separation",
        "sample_rate": sample_rate,
        "channels": int(stereo.shape[1]),
        "duration_seconds": round(len(mono) / sample_rate, 3),
        "detected_kick_like_hits": len(hit_rows),
        "selected_reference_hits": len(selected),
        "selected_time_seconds": [row["time_s"] for row in sorted(selected, key=lambda item: item["time_s"])],
        "private_reference_extract_wav": str(output_wav) if output_wav else None,
        "aimpoint_profile": {
            "peak_dbfs_percentiles": percentile_summary([row["peak_dbfs"] for row in selected]),
            "crest_db_percentiles": percentile_summary([row["crest_db"] for row in selected]),
            "attack_body_db_percentiles": percentile_summary(
                [row["attack_body_db"] for row in selected if row["attack_body_db"] is not None]
            ),
            "sub_vs_thump_db_percentiles": percentile_summary([row["ratios"]["sub_vs_thump_db"] for row in selected]),
            "upper_vs_thump_db_percentiles": percentile_summary([row["ratios"]["upper_vs_thump_db"] for row in selected]),
            "box_vs_thump_db_percentiles": percentile_summary([row["ratios"]["box_vs_thump_db"] for row in selected]),
            "attack_vs_thump_db_percentiles": percentile_summary([row["ratios"]["attack_vs_thump_db"] for row in selected]),
            "hash_vs_attack_db_percentiles": percentile_summary([row["ratios"]["hash_vs_attack_db"] for row in selected]),
        },
        "interpretation": {
            "low_end": "Compare sub against 60-120 Hz thump; do not chase the reference by clipping the channel.",
            "box": "Keep 220-600 Hz box well below thump unless the user's taste call says otherwise.",
            "attack": "Match usable attack/read without turning the kick into a clicky or harsh source.",
            "dynamics": "Preserve transient shape; reject clipped or over-flattened candidates before taste calls.",
        },
        "hits": sorted(selected, key=lambda item: item["time_s"]),
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    return profile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drum_wav", type=Path, help="Full drum-kit WAV reference")
    parser.add_argument("--json-output", required=True, type=Path, help="Private JSON aimpoint profile")
    parser.add_argument("--extract-wav", type=Path, help="Optional private kick-hit montage WAV")
    parser.add_argument("--max-hits", type=int, default=32)
    parser.add_argument("--detection-percentile", type=float, default=91.5)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    profile = extract(args.drum_wav, args.json_output, args.extract_wav, args.max_hits, args.detection_percentile)
    print(json.dumps(profile, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
