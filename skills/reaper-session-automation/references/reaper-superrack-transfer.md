# REAPER To SuperRack Transfer

This file captures portable facts about moving Waves plugin state from REAPER into Waves SuperRack. Keep private preset paths, purchased preset names, and service-specific render folders out of public notes.

For host-neutral Waves `.xps` vocabulary, shape detection, and transfer intent, read `waves-live-plugin-chains/references/waves-xps-transfer.md` first. This file covers the REAPER-specific execution edge of that transfer.

## Working Assumption

Exported Waves plugin settings from REAPER may be safer to import into SuperRack than reconstructing plugin state from REAPER normalized parameters. Prefer direct Waves preset/settings exports when available, then verify in SuperRack.

Direction matters:

- REAPER live/plugin state -> plugin `.xps`: this REAPER skill executes the export through `scripts/export_live_waves_xps.py`.
- REAPER `.rpp` saved state -> plugin `.xps`: this REAPER skill executes the extraction through `scripts/export_waves_xps_from_rpp.py`.
- Plugin `.xps` -> REAPER live plugin: this REAPER skill executes guarded import attempts through `scripts/apply_waves_xps_to_reaper.py`.
- SuperRack rack-chain `.xps` -> REAPER live plugin: not a direct import. Use the Waves skill to decompose embedded plugin presets first, then use this skill to apply and verify them in REAPER.

## Capture Checklist

When testing a plugin-state transfer, record:

- Plugin name as shown in REAPER.
- Plugin name as shown in SuperRack.
- Plugin format in REAPER: VST3, VST2, mono/stereo, Waves shell version if visible.
- SuperRack flavor: SoundGrid, Performer, or other.
- Sample rate.
- Export method used in REAPER.
- Exported file extension and path.
- Import method used in SuperRack.
- Whether values match visually and audibly after import.
- Controls that do not transfer, such as sidechain source, external key assignment, oversampling, tempo sync, or analyzer display state.

## Known Risks

- REAPER normalized parameter values may not map cleanly to SuperRack preset payloads.
- Menu controls, hidden parameters, sidechain routing, and plugin version differences can break naive translation.
- SuperRack SoundGrid compatibility matters; a Waves plugin available in REAPER is not automatically a valid live SoundGrid plugin.
- Plugin bypass, disabled state, latency, and snapshot recall behavior are SuperRack session concerns and should be handled by `superrack-session-files`.
- REAPER `TrackFX_SetNamedConfigParm(..., "vst_chunk", ...)` can return success for a Waves VST3 chunk write without refreshing the visible plugin parameters. Do not treat that as a successful `.xps` import unless formatted values prove the plugin state changed.

## XPS Extraction Notes

- A manual Waves plugin export is plain XML rooted at `PresetChunkXMLTree`.
- REAPER VST3 Waves state can embed the same `PresetChunkXMLTree` inside base64 records in the `.rpp`.
- Some records include an XML declaration; others start directly at `<PresetChunkXMLTree>`.
- Some plugins store state as multiple separately padded base64 records, so decode each base64 line independently and concatenate bytes rather than treating all lines as one base64 string.
- Use `scripts/export_waves_xps_from_rpp.py` to export one folder per track and one `.xps` per Waves FX slot.
- Use `scripts/export_live_waves_xps.py` when the open REAPER session has unsaved plugin changes that need to become `.xps` files.

## Live Compare Notes

- For short compares, applying track/take FX to a disposable media item can be more reliable than a full master render.
- Parse `.xps` `Parameters Type="RealWorld"` tokens and set corresponding exposed REAPER plugin controls when direct chunk replacement does not refresh live plugin state. Add those mappings deliberately per plugin; do not invent token positions while mixing.
- Verify formatted parameter values before rendering.
- Prefer a native Waves/SuperRack export as the final transfer artifact when possible.

## REAPER Import Gate

When importing a single-plugin `.xps` into REAPER:

1. Confirm the file is a plugin preset, not a SuperRack rack-chain preset. The top-level plugin must not be `Super-Rack Chainer` / `MCMR`.
2. Match the target REAPER plugin by exact display name and mono/stereo component.
3. Focus the target plugin window so the operator can see the import attempt.
4. Snapshot formatted parameter values before the write.
5. Attempt the import only with a guarded helper or native Waves UI import.
6. Read formatted parameter values after the write.
7. Count the import only if the visible/formatted values verify the expected state. If the API reports success but values do not change, stop and report the import as unverified.
