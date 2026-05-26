# SuperRack Current-State Database Notes

Some SuperRack Performer installs maintain a current-state SQLite database alongside normal session files. Treat this as a product-generated current/session persistence file, not as a stable public API.

Portable observations:

- The file can use the same broad schema as `.sprk` sessions, including `snapshot`, `snapshot_chainer`, `plug`, `snapshot_plugin`, `plugin_preset`, `plug_sidechain`, `routes`, and related support tables.
- The Active state may be represented with `snapshot_id=-1`, as in normal `.sprk` inspection.
- SuperRack may write UI-originated rack/plugin changes to the current-state database while the app is running.
- UI-originated plugin add/remove and plugin `IN`/bypass changes have been observed to update current-state database rows immediately, including `plug`, `plugin_preset`, `snapshot_plugin`, and sometimes `snapshot_chainer.selected_slot`.
- A controlled plugin `IN` toggle has been observed to change only one Active `snapshot_plugin.bypass` row, while SuperRack logged the rack, plugin, slot, and `IN on/off` action.
- Selecting a plugin tile has been observed to update `snapshot_chainer.selected_slot` without changing plugin audio state.
- Navigation-only UI actions such as changing the selected rack or tab may remain in process memory and not produce any current-state database diff.
- External database edits are not guaranteed to update the running UI, audio engine, or SuperRack logs. Treat DB edits as reload-time/session-file edits unless a controlled test proves otherwise for the target version.
- External edits can create a silent mismatch: the current-state DB may change while the running UI/audio engine continues using its in-memory state. Unrelated UI actions may write other current-state rows without reconciling that mismatch.
- SuperRack may keep session state in memory and later overwrite external DB edits on UI save, snapshot recall, app close, or session reload.
- When SuperRack is running, the current-state database may use SQLite WAL sidecar files. Use the SQLite backup API for coherent observation snapshots; copying only the main database file can miss live writes.

Safe observation workflow:

1. Open read-only first and run `PRAGMA integrity_check` and `PRAGMA foreign_key_check`.
2. If comparing before/after UI actions, capture both checkpoints through SQLite backup rather than plain file copy.
3. Compare row counts, plugin rows, `snapshot_plugin`, `plugin_preset`, `plug_sidechain`, `routes`, and rack parameter tables.
4. For cache hunting, also watch recently modified SuperRack/Waves files around a controlled UI action. If only the app log and SQLite WAL move, prefer the in-memory-state hypothesis over inventing a separate file cache.
5. Avoid treating changed controller or surface-state rows as durable session facts until repeated WAL-aware pairs confirm the mapping.

Safe edit-test workflow:

1. Make a timestamped backup.
2. Patch one obvious reversible Active-row flag only.
3. Ask the operator to confirm whether the running UI changed without reload.
4. If the UI did not change, restore the prior row value immediately and treat the file as a reload-time edit target only.
5. Rerun integrity and foreign-key checks after any edit.

Keep local install paths, host-specific port probes, church/session names, and operator-specific recovery SQL out of this skill. Store those in private deployment notes instead.
