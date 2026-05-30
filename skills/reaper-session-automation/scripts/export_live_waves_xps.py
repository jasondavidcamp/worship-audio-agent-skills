#!/usr/bin/env python3
"""Export Waves plugin preset XML from the open REAPER session into .xps files."""

from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime
from pathlib import Path

import reapy
import reapy.reascript_api as RPR

from export_waves_xps_from_rpp import clean_name, decode_waves_xml, make_xps, plugin_file_name


def track_name(track) -> str:
    result = RPR.GetTrackName(track.id, "", 512)
    return result[2] if result and len(result) >= 3 else ""


def fx_name(track, fx_index: int) -> str:
    result = RPR.TrackFX_GetFXName(track.id, fx_index, "", 512)
    if result and result[0]:
        return result[3]
    return ""


def get_vst_chunk(track, fx_index: int) -> str:
    result = RPR.TrackFX_GetNamedConfigParm(track.id, fx_index, "vst_chunk", "", 16 * 1024 * 1024)
    if not result or not result[0] or len(result) < 5 or not result[4]:
        raise ValueError("REAPER did not return a vst_chunk for this FX")
    return result[4]


def decode_live_waves_xml(track, fx_index: int) -> str:
    chunk_b64 = get_vst_chunk(track, fx_index)
    raw = base64.b64decode(chunk_b64, validate=False)
    xml_text = decode_waves_xml(["<VST>", base64.b64encode(raw).decode("ascii"), ">"])
    if not xml_text:
        raise ValueError("No Waves PresetChunkXMLTree found in the live REAPER VST payload")
    return xml_text


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


def export_live(track_name_arg: str | None, track_index: int | None, fx_index: int | None, output_dir: Path) -> dict:
    reapy.connect()
    project = reapy.Project()
    resolved_track_index, track = resolve_track(project, track_name_arg, track_index)
    resolved_track_name = track_name(track)
    output_dir.mkdir(parents=True, exist_ok=True)

    fx_indices = [fx_index] if fx_index is not None else list(range(RPR.TrackFX_GetCount(track.id)))
    exports: list[dict] = []
    errors: list[dict] = []
    seen_names: dict[str, int] = {}

    for current_fx_index in fx_indices:
        current_fx_name = fx_name(track, current_fx_index)
        if not current_fx_name:
            errors.append({"fx_index": current_fx_index, "error": "FX slot not found"})
            continue
        if "(Waves)" not in current_fx_name:
            continue

        preset_name = plugin_file_name(current_fx_name)
        seen_names[preset_name] = seen_names.get(preset_name, 0) + 1
        file_stem = preset_name if seen_names[preset_name] == 1 else f"{preset_name} {seen_names[preset_name]}"
        output_path = output_dir / f"{file_stem}.xps"

        try:
            xml_text = decode_live_waves_xml(track, current_fx_index)
            output_path.write_text(make_xps(xml_text, preset_name), encoding="utf-8", newline="\n")
            exports.append(
                {
                    "track_index": resolved_track_index,
                    "track": resolved_track_name,
                    "fx_index": current_fx_index,
                    "plugin": current_fx_name,
                    "file": str(output_path),
                }
            )
        except Exception as exc:
            errors.append(
                {
                    "track_index": resolved_track_index,
                    "track": resolved_track_name,
                    "fx_index": current_fx_index,
                    "plugin": current_fx_name,
                    "error": str(exc),
                }
            )

    manifest = {
        "created_at_local": datetime.now().isoformat(timespec="seconds"),
        "source": "open REAPER session",
        "project": project.name,
        "track_index": resolved_track_index,
        "track": resolved_track_name,
        "output_dir": str(output_dir),
        "exports": exports,
        "errors": errors,
    }
    (output_dir / "live-xps-export-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    track_group = parser.add_mutually_exclusive_group(required=True)
    track_group.add_argument("--track", help="Exact REAPER track name")
    track_group.add_argument("--track-index", type=int, help="Zero-based REAPER track index")
    parser.add_argument("--fx-index", type=int, help="Zero-based FX index; omit to export all Waves FX on the track")
    parser.add_argument("output_dir", type=Path, help="Directory that will receive .xps files and a manifest")
    args = parser.parse_args()

    manifest = export_live(args.track, args.track_index, args.fx_index, args.output_dir)
    print(json.dumps({"exported": len(manifest["exports"]), "errors": len(manifest["errors"])}, indent=2))
    return 1 if manifest["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
