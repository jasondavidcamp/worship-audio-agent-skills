#!/usr/bin/env python3
"""Analyze a reference audio file for mix aimpoint work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import librosa
import numpy as np
import pyloudnorm as pyln
import soundfile as sf


BANDS = {
    "sub_20_60": (20, 60),
    "bass_60_150": (60, 150),
    "body_150_350": (150, 350),
    "low_mid_350_700": (350, 700),
    "mid_700_1500": (700, 1500),
    "presence_1500_4000": (1500, 4000),
    "edge_4000_8000": (4000, 8000),
    "air_8000_16000": (8000, 16000),
}


def _db(value: float) -> float:
    return float(20 * np.log10(max(float(value), 1e-12)))


def _to_mono(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1:
        return data.astype(np.float64)
    return data.mean(axis=1).astype(np.float64)


def _band_levels(y: np.ndarray, sr: int) -> dict[str, float]:
    d = np.abs(librosa.stft(y, n_fft=4096, hop_length=1024))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)
    levels = {}
    for name, (lo, hi) in BANDS.items():
        mask = (freqs >= lo) & (freqs < min(hi, sr / 2))
        rms = np.sqrt(np.mean(d[mask] ** 2)) if mask.any() else 1e-12
        levels[name] = round(_db(rms), 2)
    return levels


def _window_stats(y: np.ndarray, sr: int, window_s: float, hop_s: float, top_n: int) -> list[dict]:
    window = int(sr * window_s)
    hop = int(sr * hop_s)
    rows = []
    if len(y) < window:
        return rows
    for start in range(0, len(y) - window + 1, hop):
        chunk = y[start : start + window]
        rms = float(np.sqrt(np.mean(chunk * chunk)))
        peak = float(np.max(np.abs(chunk)))
        rows.append(
            {
                "start_s": round(start / sr, 3),
                "end_s": round((start + window) / sr, 3),
                "rms_dbfs": round(_db(rms), 2),
                "peak_dbfs": round(_db(peak), 2),
                "crest_db": round(_db(peak) - _db(rms), 2),
            }
        )
    return sorted(rows, key=lambda row: row["rms_dbfs"], reverse=True)[:top_n]


def _essentia_analysis(path: Path) -> dict[str, Any]:
    try:
        import essentia.standard as es  # type: ignore[import-not-found]
    except Exception as exc:
        return {
            "available": False,
            "error": f"{type(exc).__name__}: {exc}",
            "notes": "Essentia Python bindings are optional. They are commonly unavailable on native Windows Python; use WSL/Linux when needed.",
        }

    result: dict[str, Any] = {"available": True}
    try:
        loader = es.MonoLoader(filename=str(path))
        audio = loader()
        sample_rate = int(loader.paramValue("sampleRate"))
        if len(audio) == 0:
            return {"available": True, "error": "Essentia loaded zero samples."}

        def safe(name: str, func):
            try:
                result[name] = func()
            except Exception as exc:  # Keep one descriptor failure from spoiling the whole pass.
                result.setdefault("descriptor_errors", {})[name] = f"{type(exc).__name__}: {exc}"

        safe(
            "key",
            lambda: dict(zip(("key", "scale", "strength"), es.KeyExtractor()(audio), strict=False)),
        )
        def rhythm():
            bpm, _ticks, confidence, _estimates, _intervals = es.RhythmExtractor2013(method="multifeature")(audio)
            return {"bpm": float(bpm), "confidence": float(confidence)}

        safe("rhythm", rhythm)
        safe("dynamic_complexity", lambda: float(es.DynamicComplexity()(audio)[0]))

        window = es.Windowing(type="hann")
        spectrum = es.Spectrum()
        centroid = es.Centroid()
        rolloff = es.RollOff(sampleRate=sample_rate)
        flatness = es.Flatness()
        centroids = []
        rolloffs = []
        flatnesses = []
        for frame in es.FrameGenerator(audio, frameSize=2048, hopSize=1024, startFromZero=True):
            spec = spectrum(window(frame))
            centroids.append(float(centroid(spec)))
            rolloffs.append(float(rolloff(spec)))
            flatnesses.append(float(flatness(spec)))
        if centroids:
            centroid_mean = float(np.mean(centroids))
            centroid_p90 = float(np.percentile(centroids, 90))
            result["spectral"] = {
                "centroid_mean_norm": round(centroid_mean, 4),
                "centroid_p90_norm": round(centroid_p90, 4),
                "centroid_mean_hz_approx": round(centroid_mean * sample_rate / 2, 2),
                "centroid_p90_hz_approx": round(centroid_p90 * sample_rate / 2, 2),
                "rolloff_mean_hz": round(float(np.mean(rolloffs)), 2),
                "flatness_mean": round(float(np.mean(flatnesses)), 4),
            }
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def analyze(path: Path, top_windows: int = 8, include_essentia: bool = False) -> dict:
    try:
        data, sr = sf.read(path, always_2d=True, dtype="float64")
        decoder = "soundfile"
    except Exception:
        loaded, sr = librosa.load(path, sr=None, mono=False)
        if loaded.ndim == 1:
            data = loaded[:, np.newaxis].astype(np.float64)
        else:
            data = loaded.T.astype(np.float64)
        decoder = "librosa"
    y = _to_mono(data)
    meter = pyln.Meter(sr)
    peak = float(np.max(np.abs(data)))
    rms = float(np.sqrt(np.mean(y * y)))

    result = {
        "path": str(path),
        "decoder": decoder,
        "sample_rate": sr,
        "channels": data.shape[1],
        "duration_s": round(len(y) / sr, 3),
        "integrated_lufs": round(float(meter.integrated_loudness(y)), 2),
        "sample_peak_dbfs": round(_db(peak), 2),
        "rms_dbfs": round(_db(rms), 2),
        "crest_db": round(_db(peak) - _db(rms), 2),
        "bands_db": _band_levels(y, sr),
        "loudest_30s_windows": _window_stats(y, sr, 30.0, 5.0, top_windows),
        "loudest_12s_windows": _window_stats(y, sr, 12.0, 3.0, top_windows),
    }

    if include_essentia:
        result["essentia"] = _essentia_analysis(path)

    if data.shape[1] >= 2:
        left = data[:, 0]
        right = data[:, 1]
        mid = (left + right) / 2
        side = (left - right) / 2
        mid_rms = float(np.sqrt(np.mean(mid * mid)))
        side_rms = float(np.sqrt(np.mean(side * side)))
        result["stereo"] = {
            "width_ratio": round(side_rms / (mid_rms + 1e-12), 3),
            "lr_correlation": round(float(np.corrcoef(left, right)[0, 1]), 3),
        }

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze reference audio for band sound aimpoints.")
    parser.add_argument("audio_file", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    parser.add_argument("--essentia", action="store_true", help="Include optional Essentia descriptors when bindings are installed.")
    args = parser.parse_args()

    result = analyze(args.audio_file, include_essentia=args.essentia)
    text = json.dumps(result, indent=2 if args.pretty else None)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
