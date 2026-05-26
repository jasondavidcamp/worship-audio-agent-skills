import argparse
import datetime as dt
import json
import re
import shutil
import sqlite3
from pathlib import Path


NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\*")
PARAMS_RE = re.compile(r'(<Parameters Type="RealWorld">\s*)(.*?)(\s*</Parameters>)', re.S)

def fmt_number(value):
    return f"{value:g}"


def build_pocketing_updates(args):
    updates = {
        4: fmt_number(args.band5_freq),
        5: fmt_number(args.band6_freq),
        12: fmt_number(args.band5_q),
        13: fmt_number(args.band6_q),
        52: "0",
        53: "0",
        60: fmt_number(args.band5_threshold),
        61: fmt_number(args.band6_threshold),
        68: fmt_number(args.band5_range),
        69: fmt_number(args.band6_range),
        84: fmt_number(args.band5_attack),
        85: fmt_number(args.band6_attack),
        92: fmt_number(args.band5_release),
        93: fmt_number(args.band6_release),
        172: "1",
        173: "1",
    }
    if not args.keep_bands_1_to_4:
        updates.update({168: "0", 169: "0", 170: "0", 171: "0"})
    if args.set_external_sidechain:
        updates.update({148: "1", 149: "1"})
    return updates


def rewrite_params(params, updates):
    matches = list(NUMBER_RE.finditer(params))
    if len(matches) != 272:
        raise ValueError(f"Expected 272 F6 params, found {len(matches)}")
    out = []
    pos = 0
    for i, match in enumerate(matches):
        out.append(params[pos:match.start()])
        out.append(updates.get(i, match.group(0)))
        pos = match.end()
    out.append(params[pos:])
    return "".join(out)


def rewrite_preset(preset, updates):
    match = PARAMS_RE.search(preset)
    if not match:
        raise ValueError("Preset has no F6 RealWorld parameter block")
    return preset[: match.start(2)] + rewrite_params(match.group(2), updates) + preset[match.end(2) :]


def main():
    parser = argparse.ArgumentParser(description="Patch known F6-RTA RealWorld tokens for a conservative sidechain/dynamic-EQ pocketing pattern.")
    parser.add_argument("path")
    parser.add_argument("--plug-id", type=int, required=True)
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--band5-freq", type=float, default=2200.0)
    parser.add_argument("--band6-freq", type=float, default=4000.0)
    parser.add_argument("--band5-q", type=float, default=1.5)
    parser.add_argument("--band6-q", type=float, default=1.0)
    parser.add_argument("--band5-threshold", type=float, default=0.0)
    parser.add_argument("--band6-threshold", type=float, default=0.0)
    parser.add_argument("--band5-range", type=float, default=-2.0)
    parser.add_argument("--band6-range", type=float, default=-1.5)
    parser.add_argument("--band5-attack", type=float, default=20.0)
    parser.add_argument("--band6-attack", type=float, default=10.0)
    parser.add_argument("--band5-release", type=float, default=180.0)
    parser.add_argument("--band6-release", type=float, default=120.0)
    parser.add_argument("--keep-bands-1-to-4", action="store_true", help="Do not disable visible F6 bands 1-4.")
    parser.add_argument("--set-external-sidechain", action="store_true", help="Set known band 5/6 SC SOURCE flags to EXT. Verify this mapping for the target SuperRack/F6 version first.")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise FileNotFoundError(path)
    backup = None
    if not args.no_backup:
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.stem}.backup-{stamp}{path.suffix}")
        shutil.copy2(path, backup)

    conn = sqlite3.connect(path)
    conn.execute("pragma foreign_keys=on")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    plug = cur.execute("select * from plug where id=? and plugin_name='F6-RTA' and side_chain=1", (args.plug_id,)).fetchone()
    if plug is None:
        raise RuntimeError("Expected sidechained F6-RTA plug was not found; create it in SuperRack first")

    rows = cur.execute(
        """
        select distinct pp.id, pp.preset
        from snapshot_plugin sp
        join plugin_preset pp on pp.id=sp.preset_id
        where sp.plug_id=?
        order by pp.id
        """,
        (args.plug_id,),
    ).fetchall()
    if not rows:
        raise RuntimeError("No plugin_preset rows found for selected plug")

    changed = []
    updates = build_pocketing_updates(args)
    for row in rows:
        cur.execute("update plugin_preset set preset=? where id=?", (rewrite_preset(row["preset"], updates), row["id"]))
        changed.append(row["id"])
    conn.commit()

    result = {
        "backup": str(backup) if backup else None,
        "changed_plugin_preset_ids": changed,
        "updated_token_indices": sorted(updates),
        "integrity_check": cur.execute("pragma integrity_check").fetchone()[0],
        "foreign_key_check": [tuple(row) for row in cur.execute("pragma foreign_key_check").fetchall()],
    }
    conn.close()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
