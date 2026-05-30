#!/usr/bin/env python3
"""Inspect a Waves .xps file and identify whether it is a plugin or rack preset."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def tag(text: str, name: str) -> str | None:
    match = re.search(fr"<{name}>(.*?)</{name}>", text, re.S)
    return match.group(1).strip() if match else None


def attr_preset(text: str) -> tuple[str | None, str | None]:
    match = re.search(r'<Preset Name="([^"]*)" GenericType="([^"]*)"', text)
    if not match:
        return None, None
    return match.group(1), match.group(2)


def realworld_tokens(text: str) -> list[str]:
    match = re.search(r'<Parameters Type="RealWorld">(.*?)</Parameters>', text, re.S)
    return match.group(1).split() if match else []


def inspect(path: Path) -> dict:
    data = path.read_text(encoding="utf-8", errors="replace")
    preset_name, generic_type = attr_preset(data)
    top_plugin = tag(data, "PluginName")
    top_subcomp = tag(data, "PluginSubComp")
    slots = []

    for slot_match in re.finditer(r'<slot index="(\d+)">(.*?)</slot>', data, re.S):
        slot_index = int(slot_match.group(1))
        block = slot_match.group(2)
        preset_match = re.search(r'<plugin_preset Name="[^"]*"><!\[CDATA\[(.*?)\]\]></plugin_preset>', block, re.S)
        plugin_xml = preset_match.group(1) if preset_match else ""
        embedded_name, embedded_type = attr_preset(plugin_xml) if plugin_xml else (None, None)
        slots.append(
            {
                "slot": slot_index,
                "plugin_name": tag(block, "plugin_name"),
                "plugin_id": tag(block, "plugin_id"),
                "vendor": tag(block, "plugin_vendor"),
                "bypass": tag(block, "plugin_bypass"),
                "disabled": tag(block, "plugin_disabled"),
                "side_chain": tag(block, "plugin_side_chain"),
                "ignore_latency": tag(block, "plugin_ignore_latency"),
                "recall_safe": tag(block, "slot_recall_safe"),
                "embedded_preset": embedded_name,
                "embedded_generic_type": embedded_type,
                "embedded_tokens": len(realworld_tokens(plugin_xml)) if plugin_xml else 0,
            }
        )

    shape = "rack-chain" if top_plugin == "Super-Rack Chainer" or top_subcomp == "MCMR" else "single-plugin"
    return {
        "file": str(path),
        "shape": shape,
        "preset_name": preset_name,
        "generic_type": generic_type,
        "top_plugin": top_plugin,
        "top_subcomp": top_subcomp,
        "top_tokens": len(realworld_tokens(data)),
        "slots": slots,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    report = inspect(args.path)
    print(f"file: {report['file']}")
    print(
        f"shape: {report['shape']} preset={report['preset_name']!r} "
        f"generic_type={report['generic_type']!r}"
    )
    print(f"top_plugin: {report['top_plugin']!r} subcomp={report['top_subcomp']!r}")
    if report["shape"] == "single-plugin":
        print(f"single_plugin_tokens: {report['top_tokens']}")
    for slot in report["slots"]:
        print(
            f"slot {slot['slot']}: {slot['plugin_name']} id={slot['plugin_id']} "
            f"bypass={slot['bypass']} disabled={slot['disabled']} "
            f"side_chain={slot['side_chain']} ignore_latency={slot['ignore_latency']} "
            f"recall_safe={slot['recall_safe']} embedded_tokens={slot['embedded_tokens']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
