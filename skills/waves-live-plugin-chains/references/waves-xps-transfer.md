# Waves XPS Transfer

Use this reference for portable Waves `.xps` preset and rack-chain transfer decisions across REAPER, SuperRack SoundGrid, SuperRack Performer, and LV1-style staging hosts.

## Ownership Boundary

`waves-live-plugin-chains` owns Waves `.xps` vocabulary and transfer intent:

- whether an `.xps` is a single-plugin preset or a SuperRack rack-chain preset
- plugin order, mono/stereo component, and live suitability
- whether a chain should be decomposed into individual plugin presets before another host can use it
- what must be verified after any host imports a preset

Host-specific skills own host execution:

- `reaper-session-automation`: exporting current REAPER Waves FX state, attempting REAPER imports, focusing plugin windows, and verifying formatted REAPER parameter values.
- `superrack-session-files`: inspecting/patching `.sprk` sessions, validating rack-chain `.xps` shape, and checking SuperRack-specific bypass, disabled, snapshot, latency, and routing state.

## XPS Shapes

Single Waves plugin preset:

- XML root: `PresetChunkXMLTree`
- Top plugin is the actual Waves processor, such as `F6`, `RCompressor`, or `SSL EV2 Channel`
- Contains one plugin's `PresetData` and `Parameters Type="RealWorld"` token stream
- Can be used as a portable plugin-state artifact, but each host must verify that import actually changed the plugin state

SuperRack rack-chain preset:

- XML root: `PresetChunkXMLTree`
- Top plugin is `Super-Rack Chainer` with subcomponent `MCMR`
- Contains rack slots, each with slot metadata and embedded plugin preset XML in `plugin_preset` CDATA
- Represents a chain, not a single plugin. Do not import it directly into a REAPER plugin slot.

## Transfer Rules

1. Before moving an `.xps`, identify its shape.
2. For a rack-chain `.xps`, preserve slot order, bypass, disabled state, sidechain flags, ignore-latency flags, and recall-safe metadata when the destination is SuperRack.
3. For REAPER auditioning from a rack-chain `.xps`, first extract individual embedded plugin presets, then apply them to matching REAPER Waves components in the same order.
4. Match exact plugin component and channel format whenever possible: mono to mono, stereo to stereo, live component to live component.
5. Treat `Parameters Type="RealWorld"` as plugin-owned state, not a universal parameter map. Only edit token positions that are locally documented for that plugin/version.
6. When a chain is represented as a folder of separate single-plugin `.xps` files, preserve slot order in filenames with two-digit prefixes such as `01 PSE Mono.xps`, `02 F6-RTA Mono.xps`. The prefix is a chain-order hint, not part of the plugin preset identity.
7. A host API accepting a preset/chunk write is not proof of import. Verify with displayed/formatted values, a native UI check, an exported round-trip, or an audible render gate.
8. Keep exported `.xps` files out of public repos unless they are sanitized and legally safe to publish.

## Host Handoff

For REAPER:

- Prefer native Waves drag/drop when the plugin UI is visible: drag the single-plugin `.xps` file onto the matching Waves plugin UI, then verify formatted REAPER values or export a round-trip preset.
- If drag/drop is not available, use the Waves preset menu path: `Load -> Preset File`.
- Use `reaper-session-automation` to export live REAPER Waves plugin state to single-plugin `.xps` files.
- Expect REAPER-exported folders to use two-digit order prefixes so humans and later import automation can reconstruct the chain order.
- Use `reaper-session-automation` to attempt plugin `.xps` import and verify formatted values.
- If formatted values do not change after import, stop and use native Waves UI import or a plugin-specific exposed-parameter mapping.

For SuperRack:

- Use `superrack-session-files` to inspect rack-chain `.xps` files and `.sprk` sessions.
- Prefer SuperRack-native rack-chain imports for complete rack movement.
- After import, verify plugin order, bypass/disabled state, sidechains, latency, snapshots, and routing.
