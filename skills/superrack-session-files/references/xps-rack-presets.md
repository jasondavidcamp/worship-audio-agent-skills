# SuperRack Rack Preset `.xps` Reference

SuperRack rack preset exports observed from the UI use `.xps` files containing XML:

```xml
<?xml version="1.0"?>
<PresetChunkXMLTree version="3">
  <Preset Name="..." GenericType="MCAT">
```

Observed rack-chain preset identity:

- Top-level `<PluginName>Super-Rack Chainer</PluginName>`
- Top-level `<PluginSubComp>MCMR</PluginSubComp>`
- Top-level `GenericType="MCAT"`
- Preset name is the rack-chain preset name.

## Slot Structure

Each populated slot appears under:

```xml
<slot index="N">
  <slot_data>
    <plugin_preset Name=""><![CDATA[...plugin preset XML...]]></plugin_preset>
    <plugin_current_setup Name="">setA</plugin_current_setup>
    <plugin_name>...</plugin_name>
    <plugin_id>...</plugin_id>
    <plugin_vendor>Waves</plugin_vendor>
    <plugin_bypass>false</plugin_bypass>
    <plugin_disabled>false</plugin_disabled>
    <plugin_side_chain>false</plugin_side_chain>
    <plugin_ignore_latency>false</plugin_ignore_latency>
  </slot_data>
  <slot_recall_safe>false</slot_recall_safe>
</slot>
```

The embedded `plugin_preset` CDATA contains a normal Waves plugin preset XML chunk with its own `<PluginName>`, `<PluginSubComp>`, and `<Parameters Type="RealWorld">` token stream.

## Backup Workflow

To back up a single rack chain from SuperRack:

1. Select the rack.
2. Use the rack/preset menu to save/export the rack preset chain as an `.xps`.
3. Store it outside the live session directory with a descriptive name.
4. Verify the `.xps` starts with XML and contains `Super-Rack Chainer` / `MCMR`.
5. Inspect populated slot order and bypass states before trusting the backup.

This `.xps` backup is not a full `.sprk` session backup. It preserves the rack chain and plugin states, but not the whole session's routing, buses, snapshots, or external insert assignments.

## Import Round-Trip Caveat

In a controlled import/save round trip, a generated rack-chain `.xps` imported successfully and preserved plugin order, plugin settings, bypass state, SQLite integrity, and foreign-key validity.

However, a prior rack output trim stored as:

```text
snapshot_chainer_params: snapshot_id=-1, param_id=50
```

was not present after the `.xps` import/save. Treat rack output gain as a session-level/rack parameter that may need to be verified or restored separately after importing a rack-chain `.xps`.

## Native Export Size / Setup Layout

Native SuperRack rack-chain `.xps` exports observed so far contain one top-level rack `PresetData` block with the slot chain inside its `PluginSpecificXMLData`.

Embedded plugin presets inside slot CDATA may each contain their own `SETUP_A` and `SETUP_B` blocks. Do not confuse those embedded plugin setup blocks with top-level rack setup blocks.

Early generated `.xps` files that duplicated the entire top-level rack slot list under both top-level `SETUP_A` and top-level `SETUP_B` imported successfully, but they did not match the native/minimal export shape. Future generated `.xps` exports should include the rack slot chain once, matching native exports, while preserving the embedded plugin preset XML as-is.

Native exports may include:

- a top-level `SETUP_A` containing the full slot chain
- a top-level `SETUP_B` with an empty `PluginSpecificXMLData`
- `slot_floating_window` and `slot_recall_safe` metadata even for empty slots
- multiple `ArtistInput` entries on some populated slots

Prefer preserving these native details when using an actual SuperRack export as the source. If a native export exists for the rack, the safest generated backup is often to copy that file and change only the top-level preset name.

Native UI exports can differ from saved `.sprk` preset payloads by a small number of opaque tokens or UI labels even when the audible chain appears equivalent. Treat native exported plugin preset blobs as more authoritative than regenerated blobs from the `.sprk` when making `.xps` backups.

## XPS Generation Rules

When creating a rack-chain `.xps`, prefer compatibility over prettiness:

1. Prefer adapting a native SuperRack-exported `.xps` template from the same SuperRack version whenever one is available.
2. Keep the native top-level structure:
   - `<?xml version="1.0"?>`
   - `<PresetChunkXMLTree version="3">`
   - one top-level `<Preset Name="..." GenericType="MCAT">`
   - top-level `<PluginName>Super-Rack Chainer</PluginName>`
   - top-level `<PluginSubComp>MCMR</PluginSubComp>`
   - one top-level rack `<PresetData Setup="SETUP_A">` containing the slot chain
   - preserve a native top-level empty `<PresetData Setup="SETUP_B">` if present in the template
3. Include exactly nine rack slot entries, `0` through `8`, unless later SuperRack versions prove a different native slot count.
4. Preserve populated slot metadata:
   - `plugin_name`
   - `plugin_id`
   - `plugin_vendor`
   - `plugin_bypass`
   - `plugin_disabled`
   - `plugin_side_chain`
   - `plugin_ignore_latency`
   - `slot_recall_safe`
   - floating-window metadata when known
5. Preserve embedded `plugin_preset` XML as-is whenever possible. Do not normalize numeric precision or rewrite formatting unless the token value itself intentionally changes.
6. If changing plugin parameters, modify only known-safe token positions, then leave all unrelated tokens and XML structure untouched.
7. Do not duplicate the full rack slot chain into top-level `SETUP_B`. Embedded plugin presets may still contain their own `SETUP_A`/`SETUP_B` blocks inside CDATA. A native empty top-level `SETUP_B` is acceptable and should be preserved from a template.
8. After generating, inspect the `.xps` and compare it against a known native export for:
   - top-level identity (`Super-Rack Chainer` / `MCMR`)
   - top-level rack `PresetData` count
   - slot count
   - plugin order
   - bypass/disabled/sidechain/ignore-latency states
   - embedded plugin token counts
   - known parameter values

If the generated file imports in SuperRack, inspect the saved `.sprk` afterward because SuperRack may rewrite plugin IDs, preset IDs, preset display names, or omit rack-level parameters such as rack output trim.
