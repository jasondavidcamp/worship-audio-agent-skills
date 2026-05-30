#!/usr/bin/env python3
"""Score a candidate WAV against a reference WAV using source-aware profiles.

The shared framework handles WAV loading, mono folding, sample-rate alignment,
loudness matching, comparison gates, warning/confidence handling, and JSON
output. Source profiles add metrics and scoring rules for a specific target.

Currently implemented source profile:

- bass: bass guitar stem/reference comparison.
"""

from __future__ import annotations

import argparse
import json
import math
import wave
from pathlib import Path

try:
    import numpy as np
except ImportError as exc:  # pragma: no cover - runtime environment guard
    raise SystemExit("reference_score.py requires numpy") from exc


BASS_BANDS = {
    "sub_20_40": (20.0, 40.0),
    "fund_40_80": (40.0, 80.0),
    "bass_80_160": (80.0, 160.0),
    "mud_160_300": (160.0, 300.0),
    "lowmid_300_700": (300.0, 700.0),
    "note_700_2k": (700.0, 2000.0),
    "edge_2k_5k": (2000.0, 5000.0),
    "noise_5k_10k": (5000.0, 10000.0),
}


def db(value: float) -> float:
    return 20.0 * math.log10(max(float(value), 1e-12))


def read_wav_mono(path: Path) -> tuple[np.ndarray, int, dict]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frames = wav.getnframes()
        raw = wav.readframes(frames)

    if sample_width == 1:
        data = np.frombuffer(raw, dtype=np.uint8).astype(np.float32)
        data = (data - 128.0) / 128.0
    elif sample_width == 2:
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
        raise ValueError(f"Unsupported WAV sample width: {sample_width} bytes")

    if channels > 1:
        data = data.reshape(-1, channels).mean(axis=1)

    meta = {
        "path": str(path),
        "sample_rate": sample_rate,
        "channels": channels,
        "bit_depth": sample_width * 8,
        "duration_seconds": frames / sample_rate if sample_rate else 0.0,
    }
    return data.astype(np.float32), sample_rate, meta


def trim_to_overlap(candidate: np.ndarray, reference: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    length = min(len(candidate), len(reference))
    return candidate[:length], reference[:length]


def resample_linear(audio: np.ndarray, source_rate: int, target_rate: int) -> np.ndarray:
    if source_rate == target_rate or len(audio) == 0:
        return audio
    duration = len(audio) / float(source_rate)
    target_length = max(1, int(round(duration * target_rate)))
    source_times = np.arange(len(audio), dtype=np.float64) / float(source_rate)
    target_times = np.arange(target_length, dtype=np.float64) / float(target_rate)
    return np.interp(target_times, source_times, audio).astype(np.float32)


def basic_metrics(audio: np.ndarray) -> dict:
    peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
    rms = float(np.sqrt(np.mean(audio * audio))) if len(audio) else 0.0
    return {
        "peak_dbfs": db(peak),
        "rms_dbfs": db(rms),
        "crest_db": db(peak / max(rms, 1e-12)),
    }


def rms_match(candidate: np.ndarray, reference: np.ndarray) -> tuple[np.ndarray, float]:
    cand_rms = float(np.sqrt(np.mean(candidate * candidate))) if len(candidate) else 0.0
    ref_rms = float(np.sqrt(np.mean(reference * reference))) if len(reference) else 0.0
    gain = ref_rms / max(cand_rms, 1e-12)
    return candidate * gain, db(gain)


def band_rms_db(audio: np.ndarray, sample_rate: int, low: float, high: float) -> float:
    if len(audio) < 2:
        return -240.0
    window = np.hanning(len(audio))
    spectrum = np.fft.rfft(audio * window)
    freqs = np.fft.rfftfreq(len(audio), 1.0 / sample_rate)
    mask = (freqs >= low) & (freqs < high)
    if not np.any(mask):
        return -240.0
    rms = np.sqrt(np.mean(np.abs(spectrum[mask]) ** 2)) / max(1.0, len(audio) / 2.0)
    return db(float(rms))


def band_profile(audio: np.ndarray, sample_rate: int, bands: dict[str, tuple[float, float]]) -> dict[str, float]:
    return {name: band_rms_db(audio, sample_rate, *bounds) for name, bounds in bands.items()}


def compare_profiles(candidate: dict[str, float], reference: dict[str, float]) -> dict:
    return {
        name: {
            "candidate_db": candidate[name],
            "reference_db": reference[name],
            "delta_db": candidate[name] - reference[name],
        }
        for name in candidate
    }


def ratio_db(profile: dict[str, float], numerator: tuple[str, ...], denominator: tuple[str, ...]) -> float:
    num = np.mean([profile[name] for name in numerator])
    den = np.mean([profile[name] for name in denominator])
    return float(num - den)


def short_window_rms(audio: np.ndarray, sample_rate: int, window_ms: float = 200.0) -> np.ndarray:
    size = max(1, int(sample_rate * window_ms / 1000.0))
    if len(audio) < size:
        return np.array([], dtype=np.float32)
    count = len(audio) // size
    framed = audio[: count * size].reshape(count, size)
    rms = np.sqrt(np.mean(framed * framed, axis=1))
    active = rms[rms > max(float(np.max(rms)) * 0.08, 1e-5)]
    return active


def consistency_metrics(audio: np.ndarray, sample_rate: int) -> dict:
    rms = short_window_rms(audio, sample_rate)
    if len(rms) == 0:
        return {"active_windows": 0, "rms_std_db": None, "rms_range_db": None}
    rms_db = np.array([db(v) for v in rms])
    return {
        "active_windows": int(len(rms_db)),
        "rms_std_db": float(np.std(rms_db)),
        "rms_range_db": float(np.max(rms_db) - np.min(rms_db)),
    }


def onset_indices(audio: np.ndarray, sample_rate: int) -> list[int]:
    frame = max(1, int(sample_rate * 0.02))
    hop = frame
    if len(audio) < frame * 4:
        return []
    count = (len(audio) - frame) // hop + 1
    frames = np.array(
        [
            np.sqrt(np.mean(audio[i * hop : i * hop + frame] ** 2))
            for i in range(count)
        ]
    )
    if len(frames) < 3:
        return []
    threshold = max(float(np.median(frames) * 1.8), float(np.max(frames) * 0.18), 1e-5)
    onsets: list[int] = []
    last = -999
    for i in range(1, len(frames)):
        rising = frames[i] > threshold and frames[i] > frames[i - 1] * 1.35
        separated = (i - last) * hop > int(sample_rate * 0.18)
        if rising and separated:
            onsets.append(i * hop)
            last = i
    return onsets


def envelope_metrics(audio: np.ndarray, sample_rate: int) -> dict:
    onsets = onset_indices(audio, sample_rate)
    attack_size = int(sample_rate * 0.06)
    body_start = int(sample_rate * 0.08)
    body_end = int(sample_rate * 0.40)
    ratios: list[float] = []
    for onset in onsets:
        if onset + body_end >= len(audio):
            continue
        attack = audio[onset : onset + attack_size]
        body = audio[onset + body_start : onset + body_end]
        attack_rms = float(np.sqrt(np.mean(attack * attack))) if len(attack) else 0.0
        body_rms = float(np.sqrt(np.mean(body * body))) if len(body) else 0.0
        ratios.append(db(attack_rms / max(body_rms, 1e-12)))
    if not ratios:
        return {"onsets": len(onsets), "attack_to_body_db": None}
    return {"onsets": len(ratios), "attack_to_body_db": float(np.median(ratios))}


def build_base_comparison(candidate_path: Path, reference_path: Path, bands: dict[str, tuple[float, float]]) -> dict:
    candidate, cand_sr, cand_meta = read_wav_mono(candidate_path)
    reference, ref_sr, ref_meta = read_wav_mono(reference_path)

    resampled = False
    if cand_sr != ref_sr:
        candidate = resample_linear(candidate, cand_sr, ref_sr)
        cand_meta["original_sample_rate"] = cand_sr
        cand_meta["analysis_sample_rate"] = ref_sr
        resampled = True
        cand_sr = ref_sr

    candidate_original_duration = len(candidate) / cand_sr if cand_sr else 0.0
    reference_original_duration = len(reference) / ref_sr if ref_sr else 0.0
    candidate, reference = trim_to_overlap(candidate, reference)
    candidate_matched, gain_db = rms_match(candidate, reference)

    cand_basic = basic_metrics(candidate)
    ref_basic = basic_metrics(reference)
    cand_profile = band_profile(candidate_matched, cand_sr, bands)
    ref_profile = band_profile(reference, ref_sr, bands)
    deltas = compare_profiles(cand_profile, ref_profile)
    comparison_duration = len(candidate) / cand_sr if cand_sr else 0.0

    return {
        "candidate_audio": candidate,
        "reference_audio": reference,
        "candidate_matched_audio": candidate_matched,
        "candidate_sample_rate": cand_sr,
        "reference_sample_rate": ref_sr,
        "candidate_profile": cand_profile,
        "reference_profile": ref_profile,
        "result": {
            "candidate": cand_meta,
            "reference": ref_meta,
            "candidate_resampled_to_reference_rate": resampled,
            "comparison_duration_seconds": comparison_duration,
            "comparison_gates": {
                "duration_mismatch": abs(candidate_original_duration - reference_original_duration) > 0.5,
                "short_comparison": comparison_duration < 10.0,
                "low_reference_level": ref_basic["rms_dbfs"] < -60.0,
                "low_candidate_level": cand_basic["rms_dbfs"] < -60.0,
            },
            "loudness_match_gain_db": gain_db,
            "basic": {
                "candidate": cand_basic,
                "reference": ref_basic,
            },
            "loudness_matched_band_deltas": deltas,
        },
    }


def gate_warnings(result: dict) -> list[str]:
    warnings: list[str] = []
    gates = result.get("comparison_gates", {})
    if gates.get("duration_mismatch"):
        warnings.append("candidate/reference durations differ; compare already matched excerpts for a stronger score")
    if gates.get("short_comparison"):
        warnings.append("comparison is shorter than 10 seconds; confidence is low")
    if gates.get("low_reference_level"):
        warnings.append("reference comparison segment is very quiet; score may be misleading")
    if gates.get("low_candidate_level"):
        warnings.append("candidate comparison segment is very quiet; score may be misleading")
    return warnings


def confidence_from_gates(result: dict) -> str:
    gates = result.get("comparison_gates", {})
    if (
        gates.get("duration_mismatch")
        or gates.get("short_comparison")
        or gates.get("low_reference_level")
        or gates.get("low_candidate_level")
    ):
        return "low"
    return "medium"


def add_bass_metrics(context: dict) -> None:
    result = context["result"]
    cand_profile = context["candidate_profile"]
    ref_profile = context["reference_profile"]
    candidate_matched = context["candidate_matched_audio"]
    reference = context["reference_audio"]
    cand_sr = context["candidate_sample_rate"]
    ref_sr = context["reference_sample_rate"]
    deltas = result["loudness_matched_band_deltas"]
    cand_basic = result["basic"]["candidate"]
    ref_basic = result["basic"]["reference"]

    candidate_ratios = {
        "fund_to_bass_40_80_vs_80_160": ratio_db(cand_profile, ("fund_40_80",), ("bass_80_160",)),
        "bass_to_mud_80_160_vs_160_300": ratio_db(cand_profile, ("bass_80_160",), ("mud_160_300",)),
        "mud_to_lowmid_160_300_vs_300_700": ratio_db(cand_profile, ("mud_160_300",), ("lowmid_300_700",)),
    }
    reference_ratios = {
        "fund_to_bass_40_80_vs_80_160": ratio_db(ref_profile, ("fund_40_80",), ("bass_80_160",)),
        "bass_to_mud_80_160_vs_160_300": ratio_db(ref_profile, ("bass_80_160",), ("mud_160_300",)),
        "mud_to_lowmid_160_300_vs_300_700": ratio_db(ref_profile, ("mud_160_300",), ("lowmid_300_700",)),
    }
    result["ratio_deltas"] = {
        key: {
            "candidate_db": candidate_ratios[key],
            "reference_db": reference_ratios[key],
            "delta_db": candidate_ratios[key] - reference_ratios[key],
        }
        for key in candidate_ratios
    }

    candidate_consistency = consistency_metrics(candidate_matched, cand_sr)
    reference_consistency = consistency_metrics(reference, ref_sr)
    result["note_consistency"] = {
        "candidate": candidate_consistency,
        "reference": reference_consistency,
    }
    result["attack_body_envelope"] = {
        "candidate": envelope_metrics(candidate_matched, cand_sr),
        "reference": envelope_metrics(reference, ref_sr),
    }

    translation_candidate = {
        "note_700_2k_vs_fund_40_160": ratio_db(
            cand_profile, ("note_700_2k",), ("fund_40_80", "bass_80_160")
        ),
        "lowmid_300_700_vs_fund_40_160": ratio_db(
            cand_profile, ("lowmid_300_700",), ("fund_40_80", "bass_80_160")
        ),
    }
    translation_reference = {
        "note_700_2k_vs_fund_40_160": ratio_db(
            ref_profile, ("note_700_2k",), ("fund_40_80", "bass_80_160")
        ),
        "lowmid_300_700_vs_fund_40_160": ratio_db(
            ref_profile, ("lowmid_300_700",), ("fund_40_80", "bass_80_160")
        ),
    }
    result["translation_proxy"] = {
        key: {
            "candidate_db": translation_candidate[key],
            "reference_db": translation_reference[key],
            "delta_db": translation_candidate[key] - translation_reference[key],
        }
        for key in translation_candidate
    }

    excess_mud = max(
        0.0,
        np.mean(
            [
                deltas["mud_160_300"]["delta_db"],
                deltas["lowmid_300_700"]["delta_db"],
            ]
        ),
    )
    result["mud_penalty"] = {
        "excess_mud_db": float(excess_mud),
        "penalty_points": float(min(12.0, excess_mud * 2.0)),
    }

    sub_excess = max(0.0, deltas["sub_20_40"]["delta_db"])
    headroom_penalty = max(0.0, cand_basic["peak_dbfs"] + 2.0) * 2.0
    result["sub_headroom_risk"] = {
        "sub_excess_db": float(sub_excess),
        "candidate_peak_dbfs": cand_basic["peak_dbfs"],
        "reference_peak_dbfs": ref_basic["peak_dbfs"],
        "penalty_points": float(min(14.0, sub_excess * 1.5 + headroom_penalty)),
    }

    crest_delta = cand_basic["crest_db"] - ref_basic["crest_db"]
    cand_std = candidate_consistency.get("rms_std_db")
    ref_std = reference_consistency.get("rms_std_db")
    std_delta = (cand_std - ref_std) if cand_std is not None and ref_std is not None else 0.0
    comp_penalty = 0.0
    if crest_delta < -3.0:
        comp_penalty += min(8.0, abs(crest_delta + 3.0) * 1.5)
    if std_delta < -2.5:
        comp_penalty += min(5.0, abs(std_delta + 2.5))
    result["compression_pumping_proxy"] = {
        "crest_delta_db": float(crest_delta),
        "short_window_rms_std_delta_db": float(std_delta),
        "penalty_points": float(comp_penalty),
    }


def score_bass(result: dict) -> tuple[int, list[str]]:
    warnings = gate_warnings(result)
    score = 100.0

    spectral_abs = [abs(v["delta_db"]) for v in result["loudness_matched_band_deltas"].values()]
    score -= min(28.0, float(np.mean(spectral_abs)) * 2.0)

    for ratio_name, payload in result["ratio_deltas"].items():
        delta = abs(payload["delta_db"])
        score -= min(6.0, delta * 1.5)
        if delta > 4.0:
            warnings.append(f"{ratio_name} differs from reference by {delta:.1f} dB")

    mud = result["mud_penalty"]
    score -= mud["penalty_points"]
    if mud["excess_mud_db"] > 2.0:
        warnings.append(f"excess mud/low-mid energy: {mud['excess_mud_db']:.1f} dB")

    sub = result["sub_headroom_risk"]
    score -= sub["penalty_points"]
    if sub["sub_excess_db"] > 3.0:
        warnings.append(f"sub buildup risk: {sub['sub_excess_db']:.1f} dB over reference")
    if sub["candidate_peak_dbfs"] > -2.0:
        warnings.append("candidate peak headroom below 2 dB")

    comp = result["compression_pumping_proxy"]
    score -= comp["penalty_points"]
    if comp["crest_delta_db"] < -3.0:
        warnings.append(f"crest factor is {abs(comp['crest_delta_db']):.1f} dB flatter than reference")

    trans = result["translation_proxy"]
    for key, payload in trans.items():
        if payload["delta_db"] < -4.0:
            score -= 4.0
            warnings.append(f"{key} translation is {abs(payload['delta_db']):.1f} dB below reference")

    return int(max(0.0, min(100.0, round(score)))), warnings


def analyze_bass(candidate_path: Path, reference_path: Path) -> dict:
    context = build_base_comparison(candidate_path, reference_path, BASS_BANDS)
    result = context["result"]
    result["source_type"] = "bass"
    result["profile"] = "bass_guitar_reference_v1"
    add_bass_metrics(context)
    score, warnings = score_bass(result)
    result["reference_score"] = score
    result["bass_reference_score"] = score
    result["warnings"] = warnings
    result["confidence"] = confidence_from_gates(result)
    result["notes"] = [
        "This score excludes automatic verse/chorus/bridge matching.",
        "Use already matched excerpts when section role matters.",
        "Metrics are proxies; human listening still owns final taste calls.",
    ]
    return result


def analyze(candidate_path: Path, reference_path: Path, source: str = "bass") -> dict:
    if source == "bass":
        return analyze_bass(candidate_path, reference_path)
    raise ValueError(f"Unsupported source profile: {source}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="bass", choices=("bass",), help="Source profile to use")
    parser.add_argument("--candidate", required=True, type=Path, help="Candidate WAV")
    parser.add_argument("--reference", required=True, type=Path, help="Reference WAV")
    parser.add_argument("--json-output", type=Path, help="Optional JSON report path")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args(argv)

    result = analyze(args.candidate, args.reference, source=args.source)
    text = json.dumps(result, indent=2 if args.pretty else None)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
