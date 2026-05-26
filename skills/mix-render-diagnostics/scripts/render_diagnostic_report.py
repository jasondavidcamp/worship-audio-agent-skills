#!/usr/bin/env python3
"""Generate section-aware mix render diagnostic reports from WAV files."""

from __future__ import annotations

import argparse
import json
import math
import struct
import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np


BANDS = [
    ("sub", 20, 60),
    ("bass", 60, 250),
    ("low_mids", 250, 500),
    ("mids", 500, 1500),
    ("presence", 1500, 5000),
    ("sibilance_edge", 5000, 10000),
    ("air", 10000, 20000),
]


@dataclass(frozen=True)
class Section:
    name: str
    start: float | None
    end: float | None


def db(value: float) -> float:
    return 20.0 * math.log10(max(float(value), 1e-12))


def ratio_db(numerator: float, denominator: float) -> float:
    return db(max(numerator, 1e-12) / max(denominator, 1e-12))


def iter_pcm_samples(raw: bytes, sample_width: int):
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
            sign = b"\xff" if chunk[2] & 0x80 else b"\x00"
            value = int.from_bytes(chunk + sign, "little", signed=True)
            yield value / float(1 << 23)
    elif sample_width == 4:
        count = len(raw) // 4
        for value in struct.unpack("<" + "i" * count, raw):
            yield value / float(1 << 31)
    else:
        raise ValueError(f"Unsupported PCM sample width: {sample_width} bytes")


def read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()
        sample_width = wav.getsampwidth()
        frames = wav.getnframes()
        raw = wav.readframes(frames)
    samples = np.fromiter(iter_pcm_samples(raw, sample_width), dtype=np.float64)
    if channels > 1:
        samples = samples.reshape(-1, channels)
    else:
        samples = samples.reshape(-1, 1)
    return samples, sample_rate


def parse_section(value: str) -> Section:
    parts = value.split(":")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Sections must use name:start:end")
    name, start, end = parts
    try:
        start_f = float(start)
        end_f = float(end)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Section start/end must be numbers") from exc
    if end_f <= start_f:
        raise argparse.ArgumentTypeError("Section end must be greater than start")
    return Section(name=name, start=start_f, end=end_f)


def slice_section(data: np.ndarray, sr: int, section: Section) -> np.ndarray:
    start = int(max(section.start or 0.0, 0.0) * sr)
    end = int((section.end if section.end is not None else len(data) / sr) * sr)
    end = min(max(end, start), len(data))
    return data[start:end]


def rms(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(values * values)))


def peak(values: np.ndarray) -> float:
    if values.size == 0:
        return 0.0
    return float(np.max(np.abs(values)))


def band_levels(mono: np.ndarray, sr: int) -> dict[str, float | None]:
    if len(mono) < 128:
        return {name: None for name, _, _ in BANDS}
    window = np.hanning(len(mono))
    spectrum = np.fft.rfft(mono * window)
    freqs = np.fft.rfftfreq(len(mono), 1 / sr)
    levels: dict[str, float | None] = {}
    for name, low, high in BANDS:
        mask = (freqs >= low) & (freqs < min(high, sr / 2))
        if not np.any(mask):
            levels[name] = None
            continue
        band_power = float(np.mean(np.abs(spectrum[mask]) ** 2))
        levels[name] = round(10.0 * math.log10(max(band_power, 1e-24)), 2)
    return levels


def stereo_metrics(data: np.ndarray) -> dict[str, float | None]:
    if data.shape[1] < 2:
        return {
            "correlation": None,
            "side_to_mid_db": None,
            "mono_delta_db": 0.0,
        }
    left = data[:, 0]
    right = data[:, 1]
    if len(left) < 2 or rms(left) == 0 or rms(right) == 0:
        correlation = None
    else:
        correlation = float(np.corrcoef(left, right)[0, 1])
    mid = (left + right) * 0.5
    side = (left - right) * 0.5
    stereo_rms = rms(data)
    mono_rms = rms(mid)
    return {
        "correlation": round(correlation, 4) if correlation is not None else None,
        "side_to_mid_db": round(ratio_db(rms(side), rms(mid)), 2),
        "mono_delta_db": round(ratio_db(mono_rms, stereo_rms), 2),
    }


def band_mid_side(data: np.ndarray, sr: int) -> dict[str, float | None]:
    if data.shape[1] < 2:
        return {name: None for name, _, _ in BANDS}
    left = data[:, 0]
    right = data[:, 1]
    mid = (left + right) * 0.5
    side = (left - right) * 0.5
    mid_levels = band_levels(mid, sr)
    side_levels = band_levels(side, sr)
    result: dict[str, float | None] = {}
    for name, _, _ in BANDS:
        if mid_levels[name] is None or side_levels[name] is None:
            result[name] = None
        else:
            result[name] = round(float(side_levels[name]) - float(mid_levels[name]), 2)
    return result


def transient_metrics(mono: np.ndarray, sr: int) -> dict[str, float]:
    if len(mono) < sr // 2:
        return {
            "attack_to_body_db": 0.0,
            "transient_density_per_s": 0.0,
        }
    window = max(int(sr * 0.02), 64)
    hop = max(window // 2, 1)
    values = []
    for start in range(0, len(mono) - window + 1, hop):
        chunk = mono[start : start + window]
        values.append(rms(chunk))
    env = np.array(values, dtype=np.float64)
    if env.size < 3:
        return {
            "attack_to_body_db": 0.0,
            "transient_density_per_s": 0.0,
        }
    body = float(np.percentile(env, 60))
    attacks = np.diff(env, prepend=env[0])
    threshold = max(float(np.percentile(attacks, 90)), body * 0.15, 1e-6)
    events = int(np.sum(attacks > threshold))
    duration = len(mono) / sr
    return {
        "attack_to_body_db": round(ratio_db(float(np.percentile(env, 95)), body), 2),
        "transient_density_per_s": round(events / max(duration, 1e-9), 2),
    }


def tail_metrics(mono: np.ndarray, sr: int) -> dict[str, float]:
    if len(mono) < sr:
        return {
            "quiet_floor_dbfs": db(rms(mono)),
            "tail_floor_to_body_db": -120.0,
        }
    window = max(int(sr * 0.2), 256)
    values = []
    for start in range(0, len(mono) - window + 1, window):
        values.append(rms(mono[start : start + window]))
    env = np.array(values, dtype=np.float64)
    quiet = float(np.percentile(env, 20))
    body = float(np.percentile(env, 70))
    return {
        "quiet_floor_dbfs": round(db(quiet), 2),
        "tail_floor_to_body_db": round(ratio_db(quiet, body), 2),
    }


def analyze_section(data: np.ndarray, sr: int, section: Section) -> dict:
    chunk = slice_section(data, sr, section)
    mono = chunk.mean(axis=1) if chunk.size else np.array([], dtype=np.float64)
    peak_value = peak(chunk)
    rms_value = rms(mono)
    peak_dbfs = db(peak_value)
    rms_dbfs = db(rms_value)
    return {
        "section": section.name,
        "start_s": section.start,
        "end_s": section.end,
        "duration_s": round(len(mono) / sr, 3) if sr else 0,
        "peak_dbfs": round(peak_dbfs, 2),
        "rms_dbfs": round(rms_dbfs, 2),
        "crest_db": round(peak_dbfs - rms_dbfs, 2),
        "bands_db": band_levels(mono, sr),
        "stereo": stereo_metrics(chunk),
        "side_to_mid_by_band_db": band_mid_side(chunk, sr),
        "transients": transient_metrics(mono, sr),
        "tail": tail_metrics(mono, sr),
    }


def analyze_file(path: Path, sections: list[Section]) -> dict:
    data, sr = read_wav(path)
    duration = len(data) / sr if sr else 0
    effective_sections = sections or [Section("full", 0.0, duration)]
    return {
        "path": str(path),
        "sample_rate": sr,
        "channels": int(data.shape[1]),
        "duration_s": round(duration, 3),
        "sections": [analyze_section(data, sr, section) for section in effective_sections],
    }


def delta(candidate: float | None, other: float | None) -> float | None:
    if candidate is None or other is None:
        return None
    return round(float(candidate) - float(other), 2)


def compare_section(candidate: dict, other: dict | None, label: str) -> dict:
    if other is None:
        return {}
    band_deltas = {}
    for name, _, _ in BANDS:
        band_deltas[name] = delta(candidate["bands_db"].get(name), other["bands_db"].get(name))
    return {
        f"{label}_rms_delta_db": delta(candidate["rms_dbfs"], other["rms_dbfs"]),
        f"{label}_crest_delta_db": delta(candidate["crest_db"], other["crest_db"]),
        f"{label}_band_deltas_db": band_deltas,
        f"{label}_attack_to_body_delta_db": delta(
            candidate["transients"]["attack_to_body_db"],
            other["transients"]["attack_to_body_db"],
        ),
        f"{label}_tail_floor_delta_db": delta(
            candidate["tail"]["tail_floor_to_body_db"],
            other["tail"]["tail_floor_to_body_db"],
        ),
        f"{label}_mono_delta_change_db": delta(
            candidate["stereo"]["mono_delta_db"],
            other["stereo"]["mono_delta_db"],
        ),
        f"{label}_side_to_mid_change_db": delta(
            candidate["stereo"]["side_to_mid_db"],
            other["stereo"]["side_to_mid_db"],
        ),
    }


def section_lookup(analysis: dict | None) -> dict[str, dict]:
    if not analysis:
        return {}
    return {section["section"]: section for section in analysis["sections"]}


def vocal_masking(
    vocal_analysis: dict | None,
    band_analysis: dict | None,
    section_name: str,
) -> dict:
    if not vocal_analysis or not band_analysis:
        return {
            "status": "untested",
            "notes": "Provide matching vocal and band stems for source-level masking analysis.",
        }
    vocal = section_lookup(vocal_analysis).get(section_name)
    band = section_lookup(band_analysis).get(section_name)
    if not vocal or not band:
        return {
            "status": "untested",
            "notes": "Stem sections did not match candidate sections.",
        }
    presence_gap = delta(vocal["bands_db"].get("presence"), band["bands_db"].get("presence"))
    low_mid_gap = delta(vocal["bands_db"].get("low_mids"), band["bands_db"].get("low_mids"))
    warnings = []
    if presence_gap is not None and presence_gap < -3:
        warnings.append("Band energy may mask vocal articulation in 1.5-5 kHz.")
    if low_mid_gap is not None and low_mid_gap < -3:
        warnings.append("Band low-mid energy may crowd vocal warmth/body.")
    return {
        "status": "measured",
        "vocal_minus_band_presence_db": presence_gap,
        "vocal_minus_band_low_mids_db": low_mid_gap,
        "warnings": warnings,
    }


def codec_compare(candidate: dict, roundtrip: dict | None, section_name: str) -> dict:
    if not roundtrip:
        return {
            "status": "untested",
            "notes": "Provide a decoded codec round-trip WAV to test delivery damage.",
        }
    cand = section_lookup(candidate).get(section_name)
    rt = section_lookup(roundtrip).get(section_name)
    if not cand or not rt:
        return {
            "status": "untested",
            "notes": "Codec round-trip sections did not match candidate sections.",
        }
    high_delta = delta(rt["bands_db"].get("sibilance_edge"), cand["bands_db"].get("sibilance_edge"))
    air_delta = delta(rt["bands_db"].get("air"), cand["bands_db"].get("air"))
    peak_delta = delta(rt["peak_dbfs"], cand["peak_dbfs"])
    warnings = []
    if peak_delta is not None and rt["peak_dbfs"] >= -0.3:
        warnings.append("Decoded codec round-trip is close to clipping.")
    if high_delta is not None and abs(high_delta) > 2.5:
        warnings.append("Codec round-trip changed 5-10 kHz energy noticeably.")
    if air_delta is not None and abs(air_delta) > 3.0:
        warnings.append("Codec round-trip changed air band energy noticeably.")
    return {
        "status": "measured",
        "roundtrip_peak_delta_db": peak_delta,
        "roundtrip_sibilance_edge_delta_db": high_delta,
        "roundtrip_air_delta_db": air_delta,
        "warnings": warnings,
    }


def warnings_for_section(section: dict, baseline_delta: dict, reference_delta: dict) -> list[str]:
    warnings = []
    if section["peak_dbfs"] >= -0.3:
        warnings.append("Clipping or near-clipping risk.")
    if section["crest_db"] < 8.0:
        warnings.append("Low crest factor; possible over-compression or limiter flattening.")
    if section["stereo"]["correlation"] is not None and section["stereo"]["correlation"] < 0.15:
        warnings.append("Low stereo correlation; check mono compatibility.")
    if section["stereo"]["mono_delta_db"] is not None and section["stereo"]["mono_delta_db"] < -4.5:
        warnings.append("Large mono fold-down loss.")
    if section["tail"]["tail_floor_to_body_db"] > -18.0:
        warnings.append("High quiet-floor-to-body ratio; possible tail or ambience buildup.")

    crest_drop = baseline_delta.get("baseline_crest_delta_db")
    if crest_drop is not None and crest_drop < -2.0:
        warnings.append("Crest factor dropped more than 2 dB from baseline.")

    attack_drop = baseline_delta.get("baseline_attack_to_body_delta_db")
    if attack_drop is not None and attack_drop < -2.0:
        warnings.append("Attack-to-body proxy dropped; possible transient/punch loss.")

    low_mid_delta = baseline_delta.get("baseline_band_deltas_db", {}).get("low_mids")
    if low_mid_delta is not None and low_mid_delta > 2.0:
        warnings.append("Low-mid energy rose more than 2 dB from baseline.")

    ref_presence = reference_delta.get("reference_band_deltas_db", {}).get("presence")
    if ref_presence is not None and ref_presence < -2.0:
        warnings.append("Presence band is below reference; lyric clarity may lag.")

    return warnings


def next_test(warnings: list[str]) -> str:
    if not warnings:
        return "Keep this candidate for listening; compare against the target aimpoint."
    joined = " ".join(warnings).lower()
    if "clipping" in joined:
        return "Lower the offending source or bus before the limiter, rerender the same section, and recheck peak/crest."
    if "crest" in joined or "transient" in joined or "attack" in joined:
        return "Reduce compression, clipping, sustain lift, or parallel blend; rerender the same dense section."
    if "low-mid" in joined:
        return "Find the source raising 180-500 Hz and try a small fader/EQ/dynamic-EQ move before adding brightness."
    if "mono" in joined or "correlation" in joined:
        return "Narrow or filter the side-heavy source/effect, rerender stereo and mono checks, then compare center impact."
    if "tail" in joined or "ambience" in joined:
        return "Shorten, filter, duck, or automate the ambience return, then rerender a sparse vocal section."
    if "presence" in joined:
        return "Check whether vocal or band masking changed in 1.5-5 kHz; try a small vocal/band pocketing move."
    return "Change one suspected processor or balance move, rerender this same section, and compare the same metrics."


def build_report(args: argparse.Namespace) -> dict:
    sections = args.section
    candidate = analyze_file(args.candidate, sections)
    baseline = analyze_file(args.baseline, sections) if args.baseline else None
    reference = analyze_file(args.reference, sections) if args.reference else None
    vocal = analyze_file(args.vocal_stem, sections) if args.vocal_stem else None
    band = analyze_file(args.band_stem, sections) if args.band_stem else None
    codec_roundtrip = analyze_file(args.codec_roundtrip, sections) if args.codec_roundtrip else None

    baseline_sections = section_lookup(baseline)
    reference_sections = section_lookup(reference)
    candidates = []
    for section in candidate["sections"]:
        name = section["section"]
        baseline_delta = compare_section(section, baseline_sections.get(name), "baseline")
        reference_delta = compare_section(section, reference_sections.get(name), "reference")
        vocal_info = vocal_masking(vocal, band, name)
        codec_info = codec_compare(candidate, codec_roundtrip, name)
        warnings = warnings_for_section(section, baseline_delta, reference_delta)
        warnings.extend(vocal_info.get("warnings", []))
        warnings.extend(codec_info.get("warnings", []))
        candidates.append(
            {
                "section": name,
                "metrics": section,
                "deltas": {
                    **baseline_delta,
                    **reference_delta,
                },
                "vocal_masking": vocal_info,
                "codec_delivery": codec_info,
                "warnings": warnings,
                "next_test": next_test(warnings),
            }
        )
    return {
        "summary": {
            "candidate": str(args.candidate),
            "baseline": str(args.baseline) if args.baseline else None,
            "reference": str(args.reference) if args.reference else None,
            "vocal_stem": str(args.vocal_stem) if args.vocal_stem else None,
            "band_stem": str(args.band_stem) if args.band_stem else None,
            "codec_roundtrip": str(args.codec_roundtrip) if args.codec_roundtrip else None,
            "section_count": len(candidates),
        },
        "candidate_file": candidate,
        "baseline_file": baseline,
        "reference_file": reference,
        "sections": candidates,
    }


def markdown(report: dict) -> str:
    lines = [
        "# Mix Render Diagnostic Report",
        "",
        "## Inputs",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Section Findings")
    lines.append("")
    for section in report["sections"]:
        metrics = section["metrics"]
        lines.append(f"### {section['section']}")
        lines.append("")
        lines.append(f"- peak: {metrics['peak_dbfs']} dBFS")
        lines.append(f"- rms proxy: {metrics['rms_dbfs']} dBFS")
        lines.append(f"- crest: {metrics['crest_db']} dB")
        lines.append(f"- stereo correlation: {metrics['stereo']['correlation']}")
        lines.append(f"- side-to-mid: {metrics['stereo']['side_to_mid_db']} dB")
        lines.append(f"- mono delta: {metrics['stereo']['mono_delta_db']} dB")
        lines.append(f"- attack-to-body: {metrics['transients']['attack_to_body_db']} dB")
        lines.append(f"- transient density: {metrics['transients']['transient_density_per_s']} per second")
        lines.append(f"- tail floor/body: {metrics['tail']['tail_floor_to_body_db']} dB")
        deltas = section["deltas"]
        if deltas:
            lines.append(
                "- baseline deltas: "
                f"rms {deltas.get('baseline_rms_delta_db')}, "
                f"crest {deltas.get('baseline_crest_delta_db')}, "
                f"low-mids {deltas.get('baseline_band_deltas_db', {}).get('low_mids')}, "
                f"presence {deltas.get('baseline_band_deltas_db', {}).get('presence')}"
            )
            lines.append(
                "- reference deltas: "
                f"rms {deltas.get('reference_rms_delta_db')}, "
                f"crest {deltas.get('reference_crest_delta_db')}, "
                f"low-mids {deltas.get('reference_band_deltas_db', {}).get('low_mids')}, "
                f"presence {deltas.get('reference_band_deltas_db', {}).get('presence')}"
            )
        vocal = section["vocal_masking"]
        lines.append(f"- vocal masking: {vocal['status']}")
        if vocal["status"] == "measured":
            lines.append(f"  - vocal minus band presence: {vocal['vocal_minus_band_presence_db']} dB")
            lines.append(f"  - vocal minus band low-mids: {vocal['vocal_minus_band_low_mids_db']} dB")
        codec = section["codec_delivery"]
        lines.append(f"- codec delivery: {codec['status']}")
        if codec["status"] == "measured":
            lines.append(f"  - roundtrip peak delta: {codec['roundtrip_peak_delta_db']} dB")
            lines.append(f"  - roundtrip 5-10 kHz delta: {codec['roundtrip_sibilance_edge_delta_db']} dB")
            lines.append(f"  - roundtrip air delta: {codec['roundtrip_air_delta_db']} dB")
        if section["warnings"]:
            lines.append("- warnings:")
            for warning in section["warnings"]:
                lines.append(f"  - {warning}")
        else:
            lines.append("- warnings: none")
        lines.append(f"- next test: {section['next_test']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--vocal-stem", type=Path)
    parser.add_argument("--band-stem", type=Path)
    parser.add_argument("--codec-roundtrip", type=Path, help="Decoded WAV after the intended codec encode/decode path.")
    parser.add_argument("--section", action="append", type=parse_section, default=[], help="Section as name:start:end seconds.")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--md-output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    report = build_report(args)
    text = json.dumps(report, indent=2 if args.pretty else None)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(text, encoding="utf-8")
    if args.md_output:
        args.md_output.parent.mkdir(parents=True, exist_ok=True)
        args.md_output.write_text(markdown(report), encoding="utf-8")
    if not args.json_output and not args.md_output:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
