---
name: superrack-session-files
description: Inspect, validate, and safely modify Waves SuperRack session files and rack preset exports. Use when working with SuperRack/SoundGrid or SuperRack Performer `.sprk` SQLite session databases, `.xps` rack presets, racks, buses, plugin ordering, sidechains, routing, snapshots, recall-safe state, bypass/disable state, latency flags, or file-level SuperRack troubleshooting.
---

# SuperRack Session Files

## Safety Workflow

Treat `.sprk` files as fragile live session databases.

1. Work read-only first. Confirm the file starts with `SQLite format 3`.
2. Create an untouched backup before any edit.
3. Inspect `PRAGMA integrity_check` and `PRAGMA foreign_key_check`.
4. Identify buses and plugins through database rows, not assumptions from names alone.
5. Preserve routing, plugin IDs, plugin ordering, snapshot bindings, recall-safe state, bypass/disable state, and latency flags unless explicitly instructed.
6. Prefer SuperRack-generated rows as templates. Do not invent opaque plugin state serialization.
7. After edits, rerun integrity checks and orphan checks.

If plugin state serialization cannot be safely regenerated, stop and document manual SuperRack UI steps.

If SuperRack is open with the session already loaded, warn that saving from the UI can overwrite external database edits from the app's in-memory session state. For reliable DB patching, close the session/app or reload the modified `.sprk` after the patch before making further UI changes.

## Scope Boundary

Keep this skill focused on SuperRack files and session structure.

- Use `waves-live-plugin-chains` for Waves plugin selection, live-safe chain design, and SoundGrid/Performer plugin suitability.
- Use this skill when the task is to inspect, validate, compare, back up, or carefully patch `.sprk` or `.xps` file content.
- Do not invent plugin preset serialization. Prefer SuperRack-generated rows or native `.xps` exports as templates.

## Core Tables

- `snapshot_chainer`: rack/bus names per snapshot.
- `object` plus `cluster_type`: chainer object type and index.
- `plug`: plugin instances, chain membership, slots, sidechain flag.
- `snapshot_plugin`: snapshot-to-plugin preset bindings.
- `plugin_preset`: plugin preset XML/text payloads.
- `plug_sidechain`: plugin sidechain source assignment.
- `routes`: audio/control routing.

Use [sprk-schema.md](references/sprk-schema.md) for learned mappings and F6 notes.
Use [superrack-ui.md](references/superrack-ui.md) for visual/UI cues from SuperRack screenshots.
Use [superrack-docs.md](references/superrack-docs.md) for official Waves documentation anchors and interpretation rules.
Use [current-session-db.md](references/current-session-db.md) for portable notes about SuperRack's current-state SQLite database behavior.
Use [xps-rack-presets.md](references/xps-rack-presets.md) for SuperRack rack-chain preset `.xps` backups/exports.

## Helper Scripts

Use `scripts/inspect_sprk.py` for a compact report:

```powershell
& "<python>" scripts/inspect_sprk.py "<path-to-session.sprk>"
```

Use `scripts/patch_f6_pocketing.py` only when the session already contains a SuperRack-created sidechained F6-RTA instance to patch:

```powershell
& "<python>" scripts/patch_f6_pocketing.py "<path-to-session.sprk>" --plug-id 225
```

The patch script makes a timestamped backup, edits only `plugin_preset` rows for the selected plug, and validates SQLite integrity.

Use `scripts/inspect_xps.py` to inspect a SuperRack rack-chain `.xps` export:

```powershell
& "<python>" scripts/inspect_xps.py "<path-to-rack-preset.xps>"
```

## Analysis Checklist

When reviewing a session, distinguish:

- Plugin order: rack signal flow is top to bottom by slot.
- Plugin `IN`/bypass: bypass keeps the plugin in the processing chain.
- Plugin disabled: removes the plugin from processing and latency/CPU calculations while keeping settings.
- Plugin removed: deletes the slot/settings/control assignments.
- Sidechain assignment: rack-level sidechain source and plugin-specific detector/source controls can both matter.
- Recall Safe: snapshot recall may not affect safe racks/plugins even when snapshot rows exist.
- Latency: plugin latency, rack total latency, ignored-latency flags, and link/latency group settings can change live behavior.
- Snapshots: stored snapshot state can differ from Active state; always compare Active against recallable snapshots when snapshot use matters.

## Session Patterns

Treat all rack IDs, chainer IDs, object indices, plugin IDs, slots, and sidechain handles as session-specific. Re-detect them for every `.sprk` file and prefer SuperRack-created rows as templates for any edit.

## Screenshot Learning

When the user provides SuperRack screenshots, extract durable UI facts and add them to
`references/superrack-ui.md`. Prefer short visual-to-database mappings over long prose.
