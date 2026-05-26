#!/usr/bin/env python3
"""Drum-focused reference analysis for worship mix aimpoints."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import librosa
import numpy as np
import pyloudnorm as pyln
import soundfile as sf


DRUM_BANDS = {
    "sub_20_60": (20, 60),
    "kick_bass_60_120": (60, 120),
    "upper_kick_120_220": (120, 220),
    "snare_body_180_350": (180, 350),
    "box_350_700": (350, 700),
    "crack_700_2000": (700, 2000),
    "presence_2k_5k": (2000, 5000),
    "cymbal_5k_10k": (5000, 10000),
    "air_10k_18k": (10000, 18000),
}


def db20(value: float) -> float:
    return float(20 * np.log10(max(float(value), 1e-12)))


def db10(value: float) -> float:
    return float(10 * np.log10(max(float(value), 1e-24)))


def read_audio(path: Path) -> tuple[np.ndarray, int, str]:
    try:
        data, sr = sf.read(path, always_2d=True, dtype="float64")
        return data, int(sr), "soundfile"
    except Exception:
        loaded, sr = librosa.load(path, sr=None, mono=False)
        if loaded.ndim == 1:
            data = loaded[:, np.newaxis].astype(np.float64)
        else:
            data = loaded.T.astype(np.float64)
        return data, int(sr), "librosa"


def to_mono(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1:
        return data.astype(np.float64)
    return data.mean(axis=1).astype(np.float64)


def band_energy_share(y: np.ndarray, sr: int) -> dict[str, dict[str, float]]:
    spectrum = np.abs(librosa.stft(y, n_fft=8192, hop_length=2048)) ** 2
    freqs = librosa.fft_frequencies(sr=sr, n_fft=8192)
    total_mask = (freqs >= 20) & (freqs < min(18000, sr / 2))
    total = float(np.sum(spectrum[total_mask]))
    rows: dict[str, dict[str, float]] = {}
    for name, (lo, hi) in DRUM_BANDS.items():
        mask = (freqs >= lo) & (freqs < min(hi, sr / 2))
        energy = float(np.sum(spectrum[mask])) if mask.any() else 1e-24
        rows[name] = {
            "share_pct": round(100 * energy / (total + 1e-24), 2),
            "relative_db": round(db10(energy / (total + 1e-24)), 2),
        }
    return rows


def window_rows(y: np.ndarray, data: np.ndarray, sr: int, window_s: float, hop_s: float) -> list[dict[str, Any]]:
    meter = pyln.Meter(sr)
    window = int(window_s * sr)
    hop = int(hop_s * sr)
    rows: list[dict[str, Any]] = []
    if len(y) < int(0.4 * sr):
        return rows
    for start in range(0, max(1, len(y) - window + 1), hop):
        seg = y[start : start + window]
        dseg = data[start : start + len(seg)]
        if len(seg) < int(0.4 * sr):
            continue
        peak = float(np.max(np.abs(dseg)))
        rms = float(np.sqrt(np.mean(seg * seg)))
        try:
            lufs = float(meter.integrated_loudness(seg))
        except Exception:
            lufs = math.nan
        onset_env = librosa.onset.onset_strength(y=seg.astype(np.float32), sr=sr, hop_length=512)
        onsets = librosa.onset.onset_detect(
            onset_envelope=onset_env,
            sr=sr,
            hop_length=512,
            units="time",
            backtrack=False,
        )
        centroid = librosa.feature.spectral_centroid(y=seg.astype(np.float32), sr=sr)[0]
        rows.append(
            {
                "start_s": round(start / sr, 2),
                "end_s": round((start + len(seg)) / sr, 2),
                "rms_dbfs": round(db20(rms), 2),
                "peak_dbfs": round(db20(peak), 2),
                "crest_db": round(db20(peak) - db20(rms), 2),
                "lufs": round(lufs, 2) if math.isfinite(lufs) else None,
                "onsets_per_s": round(len(onsets) / max(len(seg) / sr, 1e-9), 2),
                "centroid_hz": round(float(np.mean(centroid)), 1),
                "centroid_p90_hz": round(float(np.percentile(centroid, 90)), 1),
            }
        )
    return rows


def activity_bounds(data: np.ndarray, sr: int) -> dict[str, Any]:
    peak_trace = np.max(np.abs(data), axis=1)
    bounds: dict[str, Any] = {}
    for threshold_db in (-80, -70, -60, -50, -40, -30, -20, -10):
        threshold = 10 ** (threshold_db / 20)
        idx = np.flatnonzero(peak_trace > threshold)
        if idx.size:
            bounds[str(threshold_db)] = {
                "first_s": round(float(idx[0] / sr), 3),
                "last_s": round(float(idx[-1] / sr), 3),
                "span_s": round(float((idx[-1] - idx[0] + 1) / sr), 3),
            }
        else:
            bounds[str(threshold_db)] = None
    return bounds


def summarize_windows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    active = [row for row in rows if row["rms_dbfs"] > -100]
    if not active:
        return {"window_count": len(rows), "active_window_count": 0}
    rms = np.array([row["rms_dbfs"] for row in active])
    onsets = np.array([row["onsets_per_s"] for row in active])
    centroid = np.array([row["centroid_hz"] for row in active])
    return {
        "window_count": len(rows),
        "active_window_count": len(active),
        "active_rms_dbfs_percentiles": {str(k): round(float(np.percentile(rms, k)), 2) for k in (5, 10, 25, 50, 75, 90, 95)},
        "active_onsets_per_s_percentiles": {str(k): round(float(np.percentile(onsets, k)), 2) for k in (10, 25, 50, 75, 90)},
        "active_centroid_hz_percentiles": {str(k): round(float(np.percentile(centroid, k)), 1) for k in (10, 25, 50, 75, 90)},
        "p90_minus_p25_rms_db": round(float(np.percentile(rms, 90) - np.percentile(rms, 25)), 2),
        "p90_minus_median_rms_db": round(float(np.percentile(rms, 90) - np.percentile(rms, 50)), 2),
    }


def analyze(path: Path, window_s: float = 10.0, hop_s: float = 5.0) -> dict[str, Any]:
    data, sr, decoder = read_audio(path)
    y = to_mono(data)
    duration = len(y) / sr
    meter = pyln.Meter(sr)
    peak = float(np.max(np.abs(data)))
    rms = float(np.sqrt(np.mean(y * y)))
    onset_env = librosa.onset.onset_strength(y=y.astype(np.float32), sr=sr, hop_length=512)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, hop_length=512, units="time")
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, hop_length=512, units="time")
    windows = window_rows(y, data, sr, window_s, hop_s)

    result: dict[str, Any] = {
        "path": str(path),
        "decoder": decoder,
        "sample_rate": sr,
        "channels": int(data.shape[1]),
        "duration_s": round(duration, 3),
        "integrated_lufs": round(float(meter.integrated_loudness(y)), 2),
        "rms_dbfs": round(db20(rms), 2),
        "sample_peak_dbfs": round(db20(peak), 2),
        "crest_db": round(db20(peak) - db20(rms), 2),
        "tempo_estimate_bpm": round(float(np.atleast_1d(tempo)[0]), 2),
        "beat_count": int(len(beats)),
        "onset_count": int(len(onsets)),
        "onsets_per_s_full": round(len(onsets) / duration, 2),
        "activity_bounds_by_peak_threshold_dbfs": activity_bounds(data, sr),
        "band_energy_share_full": band_energy_share(y, sr),
        "window_summary": summarize_windows(windows),
        "loudest_windows": sorted(windows, key=lambda row: row["rms_dbfs"], reverse=True)[:12],
        "quietest_windows": sorted(windows, key=lambda row: row["rms_dbfs"])[:8],
        "all_windows": windows,
    }
    if data.shape[1] >= 2:
        left = data[:, 0]
        right = data[:, 1]
        mid = (left + right) / 2
        side = (left - right) / 2
        result["stereo"] = {
            "lr_correlation": round(float(np.corrcoef(left, right)[0, 1]), 3),
            "width_ratio": round(float(np.sqrt(np.mean(side * side)) / (np.sqrt(np.mean(mid * mid)) + 1e-12)), 3),
            "mid_dbfs": round(db20(np.sqrt(np.mean(mid * mid))), 2),
            "side_dbfs": round(db20(np.sqrt(np.mean(side * side))), 2),
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a drum reference for worship mix aimpoint work.")
    parser.add_argument("audio_file", type=Path)
    parser.add_argument("--window-s", type=float, default=10.0)
    parser.add_argument("--hop-s", type=float, default=5.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    result = analyze(args.audio_file, window_s=args.window_s, hop_s=args.hop_s)
    text = json.dumps(result, indent=2 if args.pretty else None)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
