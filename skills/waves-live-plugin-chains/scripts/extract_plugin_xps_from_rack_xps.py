#!/usr/bin/env python3
"""Extract embedded single-plugin preset XML files from a SuperRack rack-chain .xps."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def clean_name(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip().rstrip(".") or "Unnamed"


def tag(text: str, name: str) -> str | None:
    match = re.search(fr"<{name}>(.*?)</{name}>", text, re.S)
    return match.group(1).strip() if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rack_xps", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--manifest", action="store_true", help="Also write a JSON extraction manifest into output_dir")
    args = parser.parse_args()

    data = args.rack_xps.read_text(encoding="utf-8", errors="replace")
    top_plugin = tag(data, "PluginName")
    top_subcomp = tag(data, "PluginSubComp")
    if top_plugin != "Super-Rack Chainer" and top_subcomp != "MCMR":
        raise SystemExit("Input does not look like a SuperRack rack-chain .xps")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    exports = []
    seen: dict[str, int] = {}

    for slot_match in re.finditer(r'<slot index="(\d+)">(.*?)</slot>', data, re.S):
        slot_index = int(slot_match.group(1))
        block = slot_match.group(2)
        preset_match = re.search(r'<plugin_preset Name="[^"]*"><!\[CDATA\[(.*?)\]\]></plugin_preset>', block, re.S)
        plugin_xml = preset_match.group(1).strip() if preset_match else ""
        plugin_name = tag(block, "plugin_name") or f"slot-{slot_index}"
        if not plugin_xml:
            continue

        stem = clean_name(f"{slot_index:02d} {plugin_name}")
        seen[stem] = seen.get(stem, 0) + 1
        if seen[stem] > 1:
            stem = f"{stem} {seen[stem]}"
        output_path = args.output_dir / f"{stem}.xps"
        output_path.write_text(plugin_xml + "\n", encoding="utf-8", newline="\n")
        exports.append(
            {
                "slot": slot_index,
                "plugin_name": plugin_name,
                "file": str(output_path),
            }
        )

    if args.manifest:
        manifest = {
            "source_rack_xps": str(args.rack_xps),
            "output_dir": str(args.output_dir),
            "exports": exports,
        }
        (args.output_dir / "extracted-plugin-xps-manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
    print(json.dumps({"exported": len(exports)}, indent=2))
    return 0 if exports else 1


if __name__ == "__main__":
    raise SystemExit(main())
