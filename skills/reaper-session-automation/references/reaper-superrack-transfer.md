# REAPER To SuperRack Transfer

This file captures portable facts about moving Waves plugin state from REAPER into Waves SuperRack. Keep private preset paths, purchased preset names, and service-specific render folders out of public notes.

## Working Assumption

Exported Waves plugin settings from REAPER may be safer to import into SuperRack than reconstructing plugin state from REAPER normalized parameters. Prefer direct Waves preset/settings exports when available, then verify in SuperRack.

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

## XPS Extraction Notes

- A manual Waves plugin export is plain XML rooted at `PresetChunkXMLTree`.
- REAPER VST3 Waves state can embed the same `PresetChunkXMLTree` inside base64 records in the `.rpp`.
- Some records include an XML declaration; others start directly at `<PresetChunkXMLTree>`.
- Some plugins store state as multiple separately padded base64 records, so decode each base64 line independently and concatenate bytes rather than treating all lines as one base64 string.
- Use `scripts/export_waves_xps_from_rpp.py` to export one folder per track and one `.xps` per Waves FX slot.

## Live Compare Notes

- For short compares, applying track/take FX to a disposable media item can be more reliable than a full master render.
- Parse `.xps` `Parameters Type="RealWorld"` tokens and set corresponding exposed REAPER plugin controls when direct chunk replacement does not refresh live plugin state.
- Verify formatted parameter values before rendering.
- Prefer a native Waves/SuperRack export as the final transfer artifact when possible.
