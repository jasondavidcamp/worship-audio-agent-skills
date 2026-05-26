import argparse
import json
import sqlite3


ORPHAN_CHECKS = {
    "plug_without_chainer": "select count(*) from plug p left join chainer c on c.obj_id=p.chainer_id where c.obj_id is null",
    "snapshot_plugin_without_plug": "select count(*) from snapshot_plugin sp left join plug p on p.id=sp.plug_id where p.id is null",
    "snapshot_plugin_without_preset": "select count(*) from snapshot_plugin sp left join plugin_preset pp on pp.id=sp.preset_id where pp.id is null",
    "snapshot_plugin_without_snapshot": "select count(*) from snapshot_plugin sp left join snapshot s on s.id=sp.snapshot_id where s.id is null",
    "plug_sidechain_without_plug": "select count(*) from plug_sidechain ps left join plug p on p.id=ps.plug_id where p.id is null",
    "routes_bad_src_type": "select count(*) from routes r left join src_routing_type t on t.id=r.src_asgn_type where t.id is null",
    "routes_bad_dst_type": "select count(*) from routes r left join dst_routing_type t on t.id=r.dst_asgn_type where t.id is null",
}


def rows(cur, sql, params=()):
    return [dict(row) for row in cur.execute(sql, params)]


def inspect(path):
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    report = {
        "integrity_check": cur.execute("pragma integrity_check").fetchone()[0],
        "foreign_key_check_count": len(cur.execute("pragma foreign_key_check").fetchall()),
        "counts": {},
        "orphan_checks": {},
    }
    for table in ["snapshot", "snapshot_chainer", "plug", "snapshot_plugin", "plugin_preset", "plug_sidechain", "routes"]:
        report["counts"][table] = cur.execute(f"select count(*) from {table}").fetchone()[0]
    for name, sql in ORPHAN_CHECKS.items():
        report["orphan_checks"][name] = cur.execute(sql).fetchone()[0]
    report["buses"] = rows(
        cur,
        """
        select sc.chainer_id, sc.snapshot_id, sc.name, sc.preset_name, ct.name as cluster_type, o.obj_index
        from snapshot_chainer sc
        join object o on o.id=sc.chainer_id
        left join cluster_type ct on ct.id=o.obj_type
        where sc.snapshot_id=-1
          and (lower(sc.name) like '%vocal%' or lower(sc.name) like '%band%' or lower(sc.name) like '%bus%')
        order by sc.chainer_id
        """,
    )
    report["plugins_by_chainer"] = rows(
        cur,
        """
        select p.chainer_id, p.id as plug_id, p.slot, p.plugin_name, p.plugin_4cc,
               p.vendor_name, p.disabled, p.recall_safe, p.side_chain, p.ignore_latency,
               sp.preset_id as active_preset_id, sp.bypass as active_bypass, sp.mute as active_mute
        from plug p
        left join snapshot_plugin sp on sp.plug_id=p.id and sp.snapshot_id=-1
        order by p.chainer_id, p.slot, p.id
        """,
    )
    report["plugin_state_summary"] = rows(
        cur,
        """
        select
          p.chainer_id,
          p.id as plug_id,
          p.slot,
          p.plugin_name,
          p.disabled,
          p.recall_safe,
          p.ignore_latency,
          sp.bypass as active_bypass,
          sp.mute as active_mute,
          case
            when p.disabled then 'disabled'
            when sp.bypass then 'bypassed'
            when sp.mute then 'muted'
            else 'active'
          end as effective_state
        from plug p
        left join snapshot_plugin sp on sp.plug_id=p.id and sp.snapshot_id=-1
        where p.disabled or p.recall_safe or p.ignore_latency or sp.bypass or sp.mute
        order by p.chainer_id, p.slot, p.id
        """,
    )
    report["snapshots"] = rows(cur, "select id, name from snapshot order by id")
    report["snapshot_plugin_counts"] = rows(
        cur,
        "select snapshot_id, count(*) as plugin_rows from snapshot_plugin group by snapshot_id order by snapshot_id",
    )
    report["sidechains"] = rows(
        cur,
        """
        select ps.*, p.chainer_id, p.slot, p.plugin_name
        from plug_sidechain ps
        join plug p on p.id=ps.plug_id
        order by p.chainer_id, p.slot
        """,
    )
    conn.close()
    return report


def main():
    parser = argparse.ArgumentParser(description="Inspect a Waves SuperRack Performer .sprk SQLite session.")
    parser.add_argument("path")
    args = parser.parse_args()
    print(json.dumps(inspect(args.path), indent=2))


if __name__ == "__main__":
    main()
