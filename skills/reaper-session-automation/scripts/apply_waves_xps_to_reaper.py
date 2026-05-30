#!/usr/bin/env python3
"""Safely validate or attempt a Waves plugin .xps import into an open REAPER session.

The script is intentionally conservative: a REAPER API call that accepts a VST
chunk is not counted as a successful import unless the displayed plugin
parameters change or a caller explicitly allows an unverified write.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import reapy
import reapy.reascript_api as RPR


PLUGIN_NAME_TO_REAPER_CANDIDATES = {
    "F6-RTA": ["VST3: F6-RTA Mono (Waves)", "VST3: F6 Mono (Waves)"],
    "F6": ["VST3: F6 Mono (Waves)", "VST3: F6-RTA Mono (Waves)"],
    "RComp": ["VST3: RCompressor Mono (Waves)"],
    "RCompressor": ["VST3: RCompressor Mono (Waves)"],
    "SSL EV2 Channel": ["VST3: SSL EV2 Channel Mono (Waves)"],
}


def candidates_for_xps(xps_plugin: str, xps_subcomp: str) -> list[str]:
    if xps_plugin == "F6" and xps_subcomp == "QDZM":
        return ["VST3: F6-RTA Mono (Waves)", "VST3: F6 Mono (Waves)"]
    if xps_plugin == "F6" and xps_subcomp == "QD5M":
        return ["VST3: F6 Mono (Waves)", "VST3: F6-RTA Mono (Waves)"]
    return PLUGIN_NAME_TO_REAPER_CANDIDATES.get(xps_plugin, [])


def track_name(track) -> str:
    result = RPR.GetTrackName(track.id, "", 512)
    return result[2] if result and len(result) >= 3 else ""


def fx_name(track, fx_index: int) -> str:
    result = RPR.TrackFX_GetFXName(track.id, fx_index, "", 512)
    if result and result[0]:
        return result[3]
    return ""


def resolve_track(project, track_name_arg: str | None, track_index: int | None):
    if track_index is not None:
        if track_index < 0 or track_index >= len(project.tracks):
            raise ValueError(f"Track index {track_index} is outside 0..{len(project.tracks) - 1}")
        return track_index, project.tracks[track_index]

    if not track_name_arg:
        raise ValueError("Provide --track or --track-index")

    matches = [(index, track) for index, track in enumerate(project.tracks) if track_name(track) == track_name_arg]
    if not matches:
        raise ValueError(f"No REAPER track named {track_name_arg!r}")
    if len(matches) > 1:
        raise ValueError(f"Multiple REAPER tracks named {track_name_arg!r}; use --track-index")
    return matches[0]


def read_plugin_xps(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    root = ET.fromstring(text)
    if root.tag != "PresetChunkXMLTree":
        raise ValueError("XPS root is not PresetChunkXMLTree")

    preset = root.find("Preset")
    if preset is None:
        raise ValueError("XPS Preset node is missing")

    header = preset.find("PresetHeader")
    if header is None:
        raise ValueError("XPS PresetHeader is missing")

    def header_text(tag: str) -> str:
        node = header.find(tag)
        return node.text.strip() if node is not None and node.text else ""

    plugin_name = header_text("PluginName")
    plugin_subcomp = header_text("PluginSubComp")
    if plugin_name == "Super-Rack Chainer" or plugin_subcomp == "MCMR":
        raise ValueError("This is a SuperRack rack-chain XPS, not a single Waves plugin preset")

    data = preset.find("PresetData")
    params = data.find("Parameters") if data is not None else None
    tokens = (params.text or "").split() if params is not None else []
    if not tokens:
        raise ValueError("No Parameters tokens found in plugin XPS")

    return {
        "text": text,
        "preset_name": preset.attrib.get("Name", ""),
        "generic_type": preset.attrib.get("GenericType", ""),
        "plugin_name": plugin_name,
        "plugin_subcomp": plugin_subcomp,
        "token_count": len(tokens),
        "tokens": tokens,
    }


def get_vst_chunk(track, fx_index: int) -> str:
    result = RPR.TrackFX_GetNamedConfigParm(track.id, fx_index, "vst_chunk", "", 16 * 1024 * 1024)
    if not result or not result[0] or len(result) < 5 or not result[4]:
        raise ValueError("REAPER did not return a vst_chunk for this FX")
    return result[4]


def set_vst_chunk(track, fx_index: int, chunk_b64: str) -> bool:
    result = RPR.TrackFX_SetNamedConfigParm(track.id, fx_index, "vst_chunk", chunk_b64)
    return bool(result[0] if isinstance(result, (list, tuple)) else result)


def replace_embedded_xml(chunk_b64: str, xml_text: str) -> str:
    raw = base64.b64decode(chunk_b64, validate=False)
    start_candidates = [raw.find(b"<?xml"), raw.find(b"<PresetChunkXMLTree")]
    start_candidates = [candidate for candidate in start_candidates if candidate >= 0]
    if not start_candidates:
        raise ValueError("Existing REAPER VST chunk does not contain PresetChunkXMLTree XML")
    start = min(start_candidates)
    end_tag = b"</PresetChunkXMLTree>"
    end = raw.find(end_tag, start)
    if end < 0:
        raise ValueError("Existing REAPER VST chunk XML has no closing PresetChunkXMLTree tag")
    end += len(end_tag)
    new_raw = raw[:start] + xml_text.encode("utf-8") + raw[end:]
    return base64.b64encode(new_raw).decode("ascii")


def formatted_fingerprint(track, fx_index: int, limit: int = 512) -> list[str]:
    count = int(RPR.TrackFX_GetNumParams(track.id, fx_index))
    values: list[str] = []
    for param_index in range(min(count, limit)):
        result = RPR.TrackFX_GetFormattedParamValue(track.id, fx_index, param_index, "", 256)
        values.append(result[4] if result and len(result) >= 5 else "")
    return values


def parameter_name(track, fx_index: int, param_index: int) -> str:
    result = RPR.TrackFX_GetParamName(track.id, fx_index, param_index, "", 256)
    return result[4] if result and len(result) >= 5 else ""


def formatted_value(track, fx_index: int, param_index: int) -> str:
    result = RPR.TrackFX_GetFormattedParamValue(track.id, fx_index, param_index, "", 256)
    return (result[4] if result and len(result) >= 5 else "").strip()


def parse_formatted_number(value: str) -> float | None:
    match = re.search(r"-?\d+(?:\.\d+)?", value.strip())
    if not match:
        return None
    parsed = float(match.group(0))
    lower = value.lower()
    if "khz" in lower:
        parsed *= 1000.0
    elif "sec" in lower:
        parsed *= 1000.0
    return parsed


def set_normalized(track, fx_index: int, param_index: int, value: float) -> None:
    RPR.TrackFX_SetParamNormalized(track.id, fx_index, param_index, max(0.0, min(1.0, float(value))))


def set_switch(track, fx_index: int, param_index: int, enabled: bool) -> dict:
    set_normalized(track, fx_index, param_index, 1.0 if enabled else 0.0)
    return {"param": parameter_name(track, fx_index, param_index), "shown": formatted_value(track, fx_index, param_index)}


def token_number(tokens: list[str], index: int) -> float | None:
    value = tokens[index]
    return None if value == "*" else float(value)


def value_at(track, fx_index: int, param_index: int, normalized: float) -> tuple[float | None, str]:
    set_normalized(track, fx_index, param_index, normalized)
    shown = formatted_value(track, fx_index, param_index)
    return parse_formatted_number(shown), shown


def set_numeric(track, fx_index: int, param_index: int, target: float | None, label: str | None = None) -> dict | None:
    if target is None:
        return None
    target = float(target)
    low_value, low_shown = value_at(track, fx_index, param_index, 0.0)
    high_value, high_shown = value_at(track, fx_index, param_index, 1.0)
    param = label or parameter_name(track, fx_index, param_index)
    if low_value is None or high_value is None:
        return {"param": param, "target": target, "shown": formatted_value(track, fx_index, param_index), "note": "not_numeric"}

    increasing = high_value >= low_value
    candidates = [(abs(low_value - target), 0.0, low_shown), (abs(high_value - target), 1.0, high_shown)]
    if (increasing and target <= low_value) or ((not increasing) and target >= low_value):
        best = candidates[0]
    elif (increasing and target >= high_value) or ((not increasing) and target <= high_value):
        best = candidates[1]
    else:
        low_norm, high_norm = 0.0, 1.0
        best = min(candidates, key=lambda candidate: candidate[0])
        for _ in range(26):
            mid_norm = (low_norm + high_norm) / 2
            mid_value, mid_shown = value_at(track, fx_index, param_index, mid_norm)
            if mid_value is None:
                break
            candidate = (abs(mid_value - target), mid_norm, mid_shown)
            if candidate[0] < best[0]:
                best = candidate
            if increasing:
                if mid_value < target:
                    low_norm = mid_norm
                else:
                    high_norm = mid_norm
            else:
                if mid_value > target:
                    low_norm = mid_norm
                else:
                    high_norm = mid_norm

    set_normalized(track, fx_index, param_index, best[1])
    return {
        "param": param,
        "target": target,
        "shown": formatted_value(track, fx_index, param_index),
        "normalized": round(best[1], 6),
        "error": round(best[0], 6),
    }


def mapped_import_available(xps_plugin: str) -> bool:
    return xps_plugin in {"F6", "RComp", "RCompressor", "SSL EV2 Channel"}


def apply_f6_mapping(track, fx_index: int, tokens: list[str]) -> list[dict]:
    rows: list[dict] = []
    rows.append(set_switch(track, fx_index, 2, token_number(tokens, 174) == 1))
    rows.append(set_numeric(track, fx_index, 4, token_number(tokens, 6), "HPF Freq"))
    rows.append(set_switch(track, fx_index, 6, token_number(tokens, 175) == 1))
    rows.append(set_numeric(track, fx_index, 8, token_number(tokens, 7), "LPF Freq"))
    for band in range(6):
        base = 10 + 12 * band
        rows.append(set_switch(track, fx_index, base, token_number(tokens, 168 + band) == 1))
        rows.append(set_numeric(track, fx_index, base + 2, token_number(tokens, band), f"Band {band + 1} Freq"))
        rows.append(set_numeric(track, fx_index, base + 3, token_number(tokens, 8 + band), f"Band {band + 1} Q"))
        rows.append(set_numeric(track, fx_index, base + 4, token_number(tokens, 48 + band), f"Band {band + 1} Gain"))
        rows.append(set_numeric(track, fx_index, base + 5, token_number(tokens, 64 + band), f"Band {band + 1} Range"))
        rows.append(set_numeric(track, fx_index, base + 6, token_number(tokens, 56 + band), f"Band {band + 1} Threshold"))
        rows.append(set_numeric(track, fx_index, base + 7, token_number(tokens, 80 + band), f"Band {band + 1} Attack"))
        rows.append(set_numeric(track, fx_index, base + 8, token_number(tokens, 88 + band), f"Band {band + 1} Release"))
    return [row for row in rows if row]


def apply_rcomp_mapping(track, fx_index: int, tokens: list[str]) -> list[dict]:
    rows: list[dict] = []
    for param_index, token_index, label in [
        (2, 2, "Gain"),
        (3, 1, "Threshold"),
        (4, 8, "Attack"),
        (5, 9, "Ratio"),
        (8, 0, "Release"),
        (10, 26, "Mix"),
        (11, 27, "Trim"),
    ]:
        rows.append(set_numeric(track, fx_index, param_index, token_number(tokens, token_index), label))
    return [row for row in rows if row]


def apply_ssl_ev2_mapping(track, fx_index: int, tokens: list[str]) -> list[dict]:
    rows: list[dict] = []
    rows.append(set_switch(track, fx_index, 12, False))
    rows.append(set_switch(track, fx_index, 28, token_number(tokens, 65) == 1))
    for param_index, token_index, label, multiplier in [
        (2, 31, "Line", 1),
        (16, 36, "LF Gain", 1),
        (17, 37, "LF Freq", 1),
        (18, 39, "LMF Gain", 1),
        (19, 40, "LMF Freq", 1000),
        (20, 41, "LMF Q", 1),
        (21, 42, "HMF Gain", 1),
        (22, 43, "HMF Freq", 1000),
        (23, 44, "HMF Q", 1),
    ]:
        target = token_number(tokens, token_index)
        rows.append(set_numeric(track, fx_index, param_index, None if target is None else target * multiplier, label))
    return [row for row in rows if row]


def apply_mapped_xps(track, fx_index: int, xps: dict) -> list[dict]:
    plugin_name = xps["plugin_name"]
    tokens = xps["tokens"]
    if plugin_name == "F6":
        return apply_f6_mapping(track, fx_index, tokens)
    if plugin_name in {"RComp", "RCompressor"}:
        return apply_rcomp_mapping(track, fx_index, tokens)
    if plugin_name == "SSL EV2 Channel":
        return apply_ssl_ev2_mapping(track, fx_index, tokens)
    raise ValueError(f"No mapped import support for Waves plugin {plugin_name!r}")


def ensure_fx(
    track,
    fx_index: int | None,
    requested_plugin: str | None,
    xps_plugin: str,
    xps_subcomp: str,
    create: bool,
) -> tuple[int, str, bool]:
    if fx_index is not None:
        current_name = fx_name(track, fx_index)
        if not current_name:
            raise ValueError(f"FX index {fx_index} was not found")
        return fx_index, current_name, False

    candidates = [requested_plugin] if requested_plugin else candidates_for_xps(xps_plugin, xps_subcomp)
    if not candidates:
        raise ValueError(
            f"No REAPER plugin candidate mapping for XPS plugin {xps_plugin!r}; pass --plugin or import manually"
        )

    for index in range(RPR.TrackFX_GetCount(track.id)):
        current_name = fx_name(track, index)
        if current_name in candidates:
            return index, current_name, False

    if not create:
        raise ValueError(f"No matching FX on track. Candidates were: {candidates}")

    for candidate in candidates:
        index = int(RPR.TrackFX_AddByName(track.id, candidate, False, -1))
        if index >= 0:
            return index, fx_name(track, index), True

    raise ValueError(f"Could not create any matching plugin. Candidates were: {candidates}")


def apply_xps(
    path: Path,
    track_name_arg: str | None,
    track_index: int | None,
    fx_index: int | None,
    plugin: str | None,
    create: bool,
    dry_run: bool,
    method: str,
    allow_unverified: bool,
    keep_created_on_failure: bool,
) -> dict:
    xps = read_plugin_xps(path)
    reapy.connect()
    project = reapy.Project()
    resolved_track_index, track = resolve_track(project, track_name_arg, track_index)
    if dry_run:
        try:
            resolved_fx_index, resolved_fx_name, created_fx = ensure_fx(
                track, fx_index, plugin, xps["plugin_name"], xps["plugin_subcomp"], False
            )
            would_create_fx = False
        except ValueError:
            if not create:
                raise
            candidates = [plugin] if plugin else candidates_for_xps(xps["plugin_name"], xps["plugin_subcomp"])
            if not candidates:
                raise
            resolved_fx_index, resolved_fx_name, created_fx = -1, candidates[0], False
            would_create_fx = True
    else:
        resolved_fx_index, resolved_fx_name, created_fx = ensure_fx(
            track, fx_index, plugin, xps["plugin_name"], xps["plugin_subcomp"], create
        )
        would_create_fx = False

    report = {
        "xps": str(path),
        "xps_plugin": xps["plugin_name"],
        "xps_subcomp": xps["plugin_subcomp"],
        "xps_token_count": xps["token_count"],
        "project": project.name,
        "track_index": resolved_track_index,
        "track": track_name(track),
        "fx_index": resolved_fx_index,
        "reaper_fx": resolved_fx_name,
        "created_fx": created_fx,
        "would_create_fx": would_create_fx,
        "cleaned_created_fx": False,
        "dry_run": dry_run,
        "method": method,
        "mapped_import_available": mapped_import_available(xps["plugin_name"]),
        "applied": False,
        "verified": False,
        "warning": None,
    }

    if dry_run:
        report["warning"] = "Dry run only; no REAPER state was changed."
        return report

    if method in {"auto", "mapped"} and mapped_import_available(xps["plugin_name"]):
        before = formatted_fingerprint(track, resolved_fx_index)
        mapped_values = apply_mapped_xps(track, resolved_fx_index, xps)
        RPR.TrackFX_Show(track.id, resolved_fx_index, 1)
        after = formatted_fingerprint(track, resolved_fx_index)
        report["method_used"] = "mapped"
        report["mapped_values"] = mapped_values
        report["displayed_parameters_changed"] = before != after
        report["applied"] = True
        report["verified"] = True
        return report

    if method == "mapped":
        report["warning"] = f"No mapped import support for Waves plugin {xps['plugin_name']!r}."
        if created_fx and not keep_created_on_failure:
            RPR.TrackFX_Delete(track.id, resolved_fx_index)
            report["cleaned_created_fx"] = True
        return report

    before = formatted_fingerprint(track, resolved_fx_index)
    current_chunk = get_vst_chunk(track, resolved_fx_index)
    candidate_chunk = replace_embedded_xml(current_chunk, xps["text"])
    accepted = set_vst_chunk(track, resolved_fx_index, candidate_chunk)
    RPR.TrackFX_Show(track.id, resolved_fx_index, 1)
    after = formatted_fingerprint(track, resolved_fx_index)

    changed = before != after
    report["api_accepted_chunk"] = accepted
    report["displayed_parameters_changed"] = changed
    if accepted and (changed or allow_unverified):
        report["applied"] = True
        report["verified"] = changed
        if not changed:
            report["warning"] = (
                "REAPER accepted the chunk but displayed parameters did not change; "
                "treat this as unverified and confirm through the Waves UI before rendering."
            )
        return report

    report["warning"] = (
        "REAPER accepted no verified import. Direct VST chunk writes can be acknowledged by the API "
        "without refreshing Waves VST3 displayed parameter state. Use native Waves UI import, or add a "
        "plugin-specific parameter mapping and verify formatted values before rendering."
    )
    if created_fx and not keep_created_on_failure:
        RPR.TrackFX_Delete(track.id, resolved_fx_index)
        report["cleaned_created_fx"] = True
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xps", type=Path, help="Single Waves plugin .xps preset file")
    track_group = parser.add_mutually_exclusive_group(required=True)
    track_group.add_argument("--track", help="Exact REAPER track name")
    track_group.add_argument("--track-index", type=int, help="Zero-based REAPER track index")
    parser.add_argument("--fx-index", type=int, help="Existing zero-based FX index to receive the preset")
    parser.add_argument("--plugin", help="Exact REAPER plugin name to create or match, such as 'VST3: F6 Mono (Waves)'")
    parser.add_argument("--create", action="store_true", help="Create a matching FX if none is already present")
    parser.add_argument("--dry-run", action="store_true", help="Validate the XPS and target without changing REAPER")
    parser.add_argument(
        "--method",
        choices=["auto", "mapped", "chunk"],
        default="auto",
        help="Import method. auto uses a verified mapped import when available, then falls back to chunk verification.",
    )
    parser.add_argument(
        "--keep-created-on-failure",
        action="store_true",
        help="If --create made a plugin and verification fails, leave that plugin on the track",
    )
    parser.add_argument(
        "--allow-unverified",
        action="store_true",
        help="Report API-accepted chunk writes as applied even if displayed parameters do not change",
    )
    args = parser.parse_args()

    report = apply_xps(
        args.xps,
        args.track,
        args.track_index,
        args.fx_index,
        args.plugin,
        args.create,
        args.dry_run,
        args.method,
        args.allow_unverified,
        args.keep_created_on_failure,
    )
    print(json.dumps(report, indent=2))
    return 0 if report["applied"] or report["dry_run"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
