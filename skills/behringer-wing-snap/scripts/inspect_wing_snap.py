#!/usr/bin/env python3
"""Inspect Behringer WING .snap JSON files and optionally compare to SuperRack."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path


def load_snap(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit("Snapshot root is not a JSON object")
    if not str(data.get("type", "")).startswith("snapshot."):
        raise SystemExit(f"Unexpected snapshot type: {data.get('type')!r}")
    return data


def physical_name(ae_data: dict, grp: str, n: int | str) -> str:
    n = str(n)
    item = ae_data.get("io", {}).get("in", {}).get(grp, {}).get(n)
    if item and item.get("name"):
        return f"{grp}.{n} {item['name']}"
    return f"{grp}.{n}"


def resolve_source(ae_data: dict, grp: str, n: int | str) -> str:
    n = str(n)
    if grp == "OFF":
        return "OFF"
    if grp == "SEND":
        idx = int(n)
        slot = (idx + 1) // 2
        side = "L" if idx % 2 else "R"
        return f"FX{slot} SEND {side}"
    if grp in ae_data.get("io", {}).get("in", {}):
        return physical_name(ae_data, grp, n)
    if grp == "CH":
        item = ae_data.get("ch", {}).get(n, {})
        return f"CH{int(n):02d} {item.get('name', '')}".strip()
    if grp == "BUS":
        item = ae_data.get("bus", {}).get(n, {})
        return f"BUS{int(n):02d} {item.get('name', '')}".strip()
    if grp == "MAIN":
        item = ae_data.get("main", {}).get(n, {})
        return f"MAIN{n} {item.get('name', '')}".strip()
    if grp == "MTX":
        item = ae_data.get("mtx", {}).get(n, {})
        return f"MTX{int(n):02d} {item.get('name', '')}".strip()
    return f"{grp}.{n}"


def mod_output_source(ae_data: dict, n: int | str) -> tuple[str, str]:
    item = ae_data.get("io", {}).get("out", {}).get("MOD", {}).get(str(n), {})
    grp = item.get("grp", "OFF")
    inn = item.get("in", 1)
    return f"{grp}.{inn}", resolve_source(ae_data, grp, inn)


def superrack_names(path: Path) -> dict[int, str]:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT o.obj_index + 1 AS ch, sc.name
        FROM snapshot_chainer sc
        JOIN object o ON o.id = sc.chainer_id
        WHERE sc.snapshot_id = -1 AND o.obj_type = 0
        ORDER BY o.obj_index
        """
    ).fetchall()
    return {int(r["ch"]): r["name"] for r in rows}


def build_report(data: dict, sr_names: dict[int, str] | None = None) -> dict:
    ae = data.get("ae_data", {})
    report: dict = {
        "metadata": {
            "type": data.get("type"),
            "creator_model": data.get("creator_model"),
            "creator_fw": data.get("creator_fw"),
            "created": data.get("created"),
            "active_scene": data.get("active_scene"),
        },
        "audio": data.get("ae_globals", {}),
        "cards": ae.get("cards", {}),
    }
    if data.get("scopes"):
        report["scopes_summary"] = summarize_scopes(data["scopes"])

    channels = []
    for key, ch in sorted(ae.get("ch", {}).items(), key=lambda kv: int(kv[0])):
        conn = ch.get("in", {}).get("conn", {})
        channels.append(
            {
                "ch": int(key),
                "name": ch.get("name", ""),
                "input": f"{conn.get('grp')}.{conn.get('in')}",
                "input_name": resolve_source(ae, conn.get("grp", "OFF"), conn.get("in", 1)),
                "alt": f"{conn.get('altgrp')}.{conn.get('altin')}",
                "mute": ch.get("mute"),
                "fader": ch.get("fdr"),
                "preins": ch.get("preins", {}),
                "postins": ch.get("postins", {}),
            }
        )
    report["channels"] = channels

    buses = []
    for section in ("bus", "main", "mtx"):
        for key, obj in sorted(ae.get(section, {}).items(), key=lambda kv: int(kv[0])):
            buses.append(
                {
                    "path": f"{section}{int(key):02d}",
                    "name": obj.get("name", ""),
                    "mono": obj.get("busmono"),
                    "mute": obj.get("mute"),
                    "fader": obj.get("fdr"),
                    "preins": obj.get("preins", {}),
                    "postins": obj.get("postins", {}),
                }
            )
    report["mix_outputs"] = buses

    external_inserts = []
    for key, fx in sorted(ae.get("fx", {}).items(), key=lambda kv: int(kv[0])):
        if fx.get("mdl") == "EXT":
            ein = fx.get("ein")
            out_ref, out_name = mod_output_source(ae, ein) if fx.get("egrp") == "MOD" else ("", "")
            external_inserts.append(
                {
                    "fx": f"FX{key}",
                    "return": f"{fx.get('egrp')}.{ein}",
                    "send_source": out_ref,
                    "send_source_name": out_name,
                    "lat": fx.get("lat"),
                    "mix": fx.get("fxmix"),
                }
            )
    report["external_inserts"] = external_inserts

    output_patches = {}
    for group in ("USB", "CRD", "MOD", "LCL"):
        rows = []
        for key, item in sorted(ae.get("io", {}).get("out", {}).get(group, {}).items(), key=lambda kv: int(kv[0])):
            if item.get("grp") != "OFF":
                rows.append(
                    {
                        "out": int(key),
                        "source": f"{item.get('grp')}.{item.get('in')}",
                        "source_name": resolve_source(ae, item.get("grp", "OFF"), item.get("in", 1)),
                    }
                )
        output_patches[group] = rows
    report["output_patches"] = output_patches

    if sr_names:
        comparisons = []
        for row in output_patches.get("MOD", []):
            ch = row["out"]
            if ch in sr_names:
                comparisons.append(
                    {
                        "channel": ch,
                        "wing_source_name": row["source_name"],
                        "superrack_name": sr_names[ch],
                    }
                )
        report["superrack_compare_mod"] = comparisons

    issues = []
    for row in channels:
        if row["mute"] and row["fader"] != -144:
            issues.append({"severity": "note", "kind": "muted_with_fader_up", "path": f"ch{row['ch']:02d}", "name": row["name"]})
        if row["input"].startswith("OFF") and row["name"] and row["fader"] != -144:
            issues.append({"severity": "warning", "kind": "named_channel_input_off", "path": f"ch{row['ch']:02d}", "name": row["name"]})
        if is_lr_opposite(row["name"], row["input_name"]):
            issues.append(
                {
                    "severity": "warning",
                    "kind": "possible_lr_swap",
                    "path": f"ch{row['ch']:02d}",
                    "name": row["name"],
                    "input_name": row["input_name"],
                }
            )
    for row in external_inserts:
        if row["send_source"].startswith("SEND."):
            send_n = int(row["send_source"].split(".")[1])
            fx_n = int(row["fx"][2:])
            expected = 2 * fx_n - 1
            if send_n not in (expected, expected + 1):
                issues.append(
                    {
                        "severity": "warning",
                        "kind": "external_insert_unexpected_send_pair",
                        "fx": row["fx"],
                        "return": row["return"],
                        "send_source": row["send_source"],
                        "expected": f"SEND.{expected}/SEND.{expected + 1}",
                    }
                )
    if sr_names:
        for row in report.get("superrack_compare_mod", []):
            if is_lr_opposite(row["wing_source_name"], row["superrack_name"]):
                issues.append(
                    {
                        "severity": "warning",
                        "kind": "possible_superrack_lr_swap",
                        "channel": row["channel"],
                        "wing_source_name": row["wing_source_name"],
                        "superrack_name": row["superrack_name"],
                    }
                )
    report["heuristic_issues"] = issues
    return report


def summarize_scopes(scopes: dict) -> dict:
    summary = {}
    for group, values in scopes.items():
        if isinstance(values, dict):
            enabled = [key for key, val in values.items() if val is True]
            disabled = [key for key, val in values.items() if val is False]
            summary[group] = {
                "enabled_count": len(enabled),
                "disabled_count": len(disabled),
                "enabled": enabled[:80],
                "disabled": disabled[:80],
            }
        else:
            summary[group] = values
    return summary


def is_lr_opposite(label_a: str, label_b: str) -> bool:
    a = (label_a or "").lower()
    b = (label_b or "").lower()

    def side(text: str) -> str | None:
        normalized = re.sub(r"[^a-z0-9]+", " ", text)
        if re.search(r"\b(left|overhead l|ovh l|oh l|choir l|crowd l)\b", normalized) or re.search(
            r"\bl\b", normalized
        ):
            return "L"
        if re.search(r"\b(right|overhead r|ovh r|oh r|choir r|crowd r)\b", normalized) or re.search(
            r"\br\b", normalized
        ):
            return "R"
        return None

    sa = side(a)
    sb = side(b)
    return sa is not None and sb is not None and sa != sb


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snap", type=Path)
    parser.add_argument("--superrack", type=Path, help="Optional SuperRack .sprk file for channel-name comparison")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    data = load_snap(args.snap)
    sr = superrack_names(args.superrack) if args.superrack else None
    report = build_report(data, sr)
    print(json.dumps(report, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
