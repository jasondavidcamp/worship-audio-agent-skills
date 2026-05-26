#!/usr/bin/env python3
"""Extract Waves plugin preset XML from a REAPER .rpp into .xps files.

This mirrors a manual Waves plugin export convention: one folder per REAPER
track, one .xps file per Waves FX slot named by plugin display name.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import textwrap
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr


def clean_name(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip().rstrip(".") or "Unnamed"


def plugin_file_name(reaper_name: str) -> str:
    name = re.sub(r"^VST3?:\s*", "", reaper_name)
    name = re.sub(r"\s*\(Waves\)\s*$", "", name)
    return clean_name(name)


def track_chunks(lines: list[str]):
    starts = [i for i, line in enumerate(lines) if line.strip().startswith("<TRACK")]
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        yield lines[start:end]


def track_name(chunk: list[str]) -> str:
    for line in chunk:
        stripped = line.strip()
        if stripped.startswith("NAME "):
            match = re.match(r'NAME\s+"(.*)"', stripped)
            return match.group(1) if match else stripped[5:].strip()
    return "Unnamed Track"


def vst_blocks(chunk: list[str]):
    index = 0
    while index < len(chunk):
        stripped = chunk[index].strip()
        if stripped.startswith("<VST "):
            match = re.match(r'<VST\s+"([^"]+)"', stripped)
            block = [chunk[index]]
            index += 1
            while index < len(chunk):
                block.append(chunk[index])
                if chunk[index].strip() == ">":
                    break
                index += 1
            yield {"reaper_name": match.group(1) if match else "Unknown VST", "lines": block}
        index += 1


def decode_waves_xml(block_lines: list[str]) -> str | None:
    raw_parts: list[bytes] = []
    for line in block_lines[1:]:
        stripped = line.strip()
        if stripped == ">":
            break
        if re.fullmatch(r"[A-Za-z0-9+/=]+", stripped):
            try:
                # REAPER may store this as separately padded base64 records.
                raw_parts.append(base64.b64decode(stripped, validate=False))
            except Exception:
                continue
    if not raw_parts:
        return None

    raw = b"".join(raw_parts)
    start = raw.find(b"<?xml")
    if start < 0:
        start = raw.find(b"<PresetChunkXMLTree")
    end_tag = b"</PresetChunkXMLTree>"
    end = raw.find(end_tag)
    if start < 0 or end < 0:
        return None
    return raw[start : end + len(end_tag)].decode("utf-8", errors="replace")


def make_xps(xml_text: str, preset_name: str) -> str:
    root = ET.fromstring(xml_text)
    preset = root.find("Preset")
    if preset is None:
        raise ValueError("Preset node missing")
    generic_type = preset.attrib.get("GenericType", "")

    header = preset.find("PresetHeader")
    if header is None:
        raise ValueError("PresetHeader missing")

    def header_text(tag: str, default: str = "") -> str:
        node = header.find(tag)
        return node.text if node is not None and node.text is not None else default

    active_setup = header_text("ActiveSetup", "CURRENT")
    data_nodes = preset.findall("PresetData")
    chosen = next((node for node in data_nodes if node.attrib.get("Setup") == active_setup), None)
    if chosen is None and data_nodes:
        chosen = data_nodes[0]
    if chosen is None:
        raise ValueError("PresetData missing")

    params = chosen.find("Parameters")
    if params is None:
        raise ValueError("Parameters missing")
    params_type = params.attrib.get("Type", "RealWorld")
    params_text = (params.text or "").strip()

    plugin_specific = chosen.find("PluginSpecificXMLData")
    if plugin_specific is None or (
        not list(plugin_specific) and not (plugin_specific.text or "").strip()
    ):
        plugin_specific_xml = "            <PluginSpecificXMLData />"
    else:
        plugin_specific_xml = textwrap.indent(
            ET.tostring(plugin_specific, encoding="unicode"), "            "
        ).rstrip()

    return (
        '<?xml version="1.0"?>\n'
        '<PresetChunkXMLTree version="3">\n'
        f'    <Preset Name={quoteattr(preset_name)} GenericType={quoteattr(generic_type)}>\n'
        "        <PresetHeader>\n"
        f"            <PluginName>{escape(header_text('PluginName'))}</PluginName>\n"
        f"            <PluginSubComp>{escape(header_text('PluginSubComp'))}</PluginSubComp>\n"
        f"            <PluginVersion>{escape(header_text('PluginVersion'))}</PluginVersion>\n"
        "            <ReadOnly>false</ReadOnly>\n"
        "        </PresetHeader>\n"
        '        <PresetData Setup="CURRENT">\n'
        f"            <Parameters Type={quoteattr(params_type)}>\n"
        f"{params_text}\n"
        "</Parameters>\n"
        f"{plugin_specific_xml}\n"
        "        </PresetData>\n"
        "    </Preset>\n"
        "</PresetChunkXMLTree>\n"
    )


def export_waves_xps(project: Path, output_root: Path, skip_tracks: set[str]) -> dict:
    output_root.mkdir(parents=True, exist_ok=True)
    lines = project.read_text(encoding="utf-8", errors="replace").splitlines()
    exports: list[dict] = []
    errors: list[dict] = []

    for chunk in track_chunks(lines):
        current_track = track_name(chunk)
        if current_track in skip_tracks:
            continue
        blocks = [block for block in vst_blocks(chunk) if "(Waves)" in block["reaper_name"]]
        if not blocks:
            continue

        track_dir = output_root / clean_name(current_track)
        track_dir.mkdir(parents=True, exist_ok=True)
        seen_names: dict[str, int] = {}

        for slot, block in enumerate(blocks, start=1):
            preset_name = plugin_file_name(block["reaper_name"])
            seen_names[preset_name] = seen_names.get(preset_name, 0) + 1
            file_stem = preset_name if seen_names[preset_name] == 1 else f"{preset_name} {seen_names[preset_name]}"
            output_path = track_dir / f"{file_stem}.xps"
            try:
                xml_text = decode_waves_xml(block["lines"])
                if not xml_text:
                    raise ValueError("No Waves PresetChunkXMLTree found in REAPER VST payload")
                output_path.write_text(make_xps(xml_text, preset_name), encoding="utf-8", newline="\n")
                exports.append(
                    {
                        "track": current_track,
                        "slot": slot,
                        "plugin": block["reaper_name"],
                        "file": str(output_path),
                    }
                )
            except Exception as exc:
                errors.append(
                    {
                        "track": current_track,
                        "slot": slot,
                        "plugin": block["reaper_name"],
                        "error": str(exc),
                    }
                )

    manifest = {
        "created_at_local": datetime.now().isoformat(timespec="seconds"),
        "source_project": str(project),
        "output_root": str(output_root),
        "convention": "one folder per REAPER track/channel; one Waves .xps preset file per FX slot named by plugin display name",
        "skipped_tracks": sorted(skip_tracks),
        "exports": exports,
        "errors": errors,
    }
    (output_root / "export-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="REAPER .rpp file")
    parser.add_argument("output_root", type=Path, help="Root folder for track subfolders")
    parser.add_argument("--skip-track", action="append", default=[], help="Track name to skip")
    args = parser.parse_args()

    manifest = export_waves_xps(args.project, args.output_root, set(args.skip_track))
    print(json.dumps({"exported": len(manifest["exports"]), "errors": len(manifest["errors"])}, indent=2))
    return 1 if manifest["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
