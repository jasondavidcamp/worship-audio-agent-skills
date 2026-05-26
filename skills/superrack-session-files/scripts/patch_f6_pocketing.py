import argparse
import datetime as dt
import json
import re
import shutil
import sqlite3
from pathlib import Path


NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\*")
PARAMS_RE = re.compile(r'(<Parameters Type="RealWorld">\s*)(.*?)(\s*</Parameters>)', re.S)

POCKETING_UPDATES = {
    4: "2200",
    5: "4000",
    12: "1.5",
    13: "1",
    52: "0",
    53: "0",
    68: "-2",
    69: "-1.5",
    84: "20",
    85: "10",
    92: "180",
    93: "120",
    168: "0",
    169: "0",
    170: "0",
    171: "0",
    172: "1",
    173: "1",
}


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
    parser = argparse.ArgumentParser(description="Patch a SuperRack-created sidechained F6-RTA for vocal pocketing.")
    parser.add_argument("path")
    parser.add_argument("--plug-id", type=int, required=True)
    parser.add_argument("--no-backup", action="store_true")
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
    for row in rows:
        cur.execute("update plugin_preset set preset=? where id=?", (rewrite_preset(row["preset"], POCKETING_UPDATES), row["id"]))
        changed.append(row["id"])
    conn.commit()

    result = {
        "backup": str(backup) if backup else None,
        "changed_plugin_preset_ids": changed,
        "integrity_check": cur.execute("pragma integrity_check").fetchone()[0],
        "foreign_key_check": [tuple(row) for row in cur.execute("pragma foreign_key_check").fetchall()],
    }
    conn.close()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
