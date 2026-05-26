# SuperRack UI Reference

Portable visual notes learned from SuperRack Performer screenshots. Treat rack names, bus numbers, plugin order, and parameter values as examples only; re-detect them from the user's screenshot or `.sprk` file every time.

## Rack View

- The large title at top left shows the selected rack/bus, such as a vocal, band, drum, livestream, or speech rack.
- The selected plugin tile in the left chain is outlined yellow.
- SuperRack logs may identify UI-originated plugin selections and `IN on/off` actions by rack name, plugin name, and UI slot number.
- Windows UI Automation can expose top-bar controls such as rack navigation and view tabs, but rack/plugin tiles may require screenshot or coordinate-driven interaction.
- The sidechain source dropdown appears above the plugin editor, labeled `SIDE CHAIN`.
- The sidechain dropdown displays the selected detector/source rack, for example a vocal rack feeding a band-bus dynamic EQ.
- The plugin tile for the sidechained F6-RTA shows an orange/red `SC` badge.
- The same plugin tile shows `IN`, meaning the plugin instance is inserted and enabled.

## Overview View

- The overview layers show rack/bus strips and their visible numbering. Treat those numbers as session-specific evidence, not universal bus IDs.
- Visible plugin order in the rack should match `plug.slot` order in the database after accounting for zero-based database slots versus one-based UI/log wording.
- When a screenshot and database disagree, verify whether the screenshot is showing Active state, a stored snapshot, a different rack layer, or an unsaved current-state change.

## F6-RTA Visual Cues

- A flat EQ line is expected when static gain is `0`; dynamic ducking is not visible as a static EQ curve.
- The graph may still show numbered markers `1-6` even when the intent is to use only selected dynamic bands.
- In a conservative two-band sidechain/pocketing example, bands 5 and 6 may be the only active dynamic bands:
  - Band 5: `2200 Hz`, range `-2 dB`, attack `20 ms`, release `180 ms`.
  - Band 6: `4000 Hz`, range `-1.5 dB`, attack `10 ms`, release `120 ms`.
- The selected band's lower controls show its frequency, Q, gain, range, threshold, attack, release, and sidechain mode.
- The rack-level sidechain dropdown and the plugin-level F6 `SC SOURCE` controls are separate visual checks.
- In a screenshot, the rack-level sidechain dropdown and the plugin tile `SC` badge can prove that a sidechain source is assigned at rack/plugin level.
- The selected F6 band's `SC SOURCE` area can still show `INT`; that means the rack-level assignment alone is not enough to prove the band is using external detection.
- For true vocal-triggered ducking, verify each active F6 band is set to the intended detector source. Do not assume the rack-level `Vocal Bus` assignment alone proves the selected band is using external detection.
- A Band 6 `INT` to `EXT` save changed Active preset token `149` from `0` to `1`.
- A reverse `EXT` to `INT` save changed only token `149` back from `1` to `0`.
- Token `149` is confirmed for Band 6 `SC SOURCE`: `0=INT`, `1=EXT`.
- Band 5 `INT` to `EXT` changed token `148` from `0` to `1`.
- Band 5 reverse `EXT` to `INT` changed only token `148` from `1` to `0`.
- Token group `144-149` is the confirmed six-band `SC SOURCE` flag group for Bands 5-6 and likely ordered Bands 1-6.
- Token `198` has changed when editing different bands and appears to reflect selected/current band UI state.
- Band 6 `SC MODE` reverse test changed only token `133` from `1` to `0` when returning to `Split`; source flags stayed unchanged.
- Token `133` is confirmed for Band 6 `SC MODE`: `0=Split`, `1=likely Wide`.
- Band 5 `SC MODE` changed token `132` from `0` to `1`; source flags stayed unchanged.
- Band 5 reverse back to `Split` changed only token `132` from `1` to `0`.
- Token group `128-133` is confirmed for Bands 5-6 and likely ordered Bands 1-6.
- Band 6 shape `Bell` to `High Shelf` changed token `141` from `1` to `2`; token `198` also followed the selected/current band.
- Band 6 reverse `High Shelf` to `Bell` changed only token `141` from `2` to `1`.
- Band 6 `Bell` to `Low Shelf` changed only token `141` from `1` to `0`.
- Token `141` is confirmed for Band 6 shape/type: `0=Low Shelf`, `1=Bell`, `2=High Shelf`.
- Token group `136-141` is likely the six-band shape/type flag group.
- Plugin tile bypass/IN is stored in `snapshot_plugin.bypass`, not in the F6 RealWorld tokens.
- For the pocketing F6-RTA, Active `snapshot_plugin.bypass` changed `0 -> 1` when bypassed; stored snapshots stayed `0`.
- Band 6 Solo on changed token `21` from `0` to `1`, making `16-21` a likely six-band Solo flag group.
- The same Solo experiment also re-enabled the plugin tile, changing Active `snapshot_plugin.bypass` from `1` back to `0`; isolate reverse Solo before treating token `21` as confirmed.
- Band 6 Solo off changed only token `21` from `1` to `0`.
- Token `21` is confirmed for Band 6 Solo: `0=off`, `1=on`.
- Band 6 threshold change from `0` to `-10` changed only token `61`; `72-77` did not change and are not threshold in this observed stream.
- Band 6 threshold reverse from `-10` to `0` changed only token `61`.
- Band 5 threshold change from `0` to `-10` changed token `60`; token `198` followed selected/current band UI state.
- Band 5 threshold reverse from `-10` to `0` changed only token `60`.
- Tokens `60` and `61` are confirmed for Band 5 and Band 6 threshold; token group `56-61` is likely ordered Bands 1-6.

## Practical Teaching Notes

- Explain that the sidechain supplies the detector signal; it does not draw a permanent EQ curve.
- To see sidechain action, audio must pass through both the processed rack and the detector/source rack at the same time.
- Watch the F6 band's dynamic movement or gain-reduction behavior while vocals are active.
- If the user is confused by all six markers, disable unused visible bands in the preset state rather than relying on explanation alone.

## Silk Vocal Visual Cues

A vocal-rack screenshot after adding Silk Vocal Live can expose useful UI/database mappings:

- Rack title showed the selected vocal rack name; top subtitle showed `PRESET*`, indicating unsaved or modified preset/session state.
- Left chain order is session-specific; use it to cross-check visible slot order against `plug.slot`, not as a recommended vocal chain.
- The selected Silk tile is outlined yellow and shows `IN`.
- Silk tile latency displayed `LT 1.3ms`; rack output latency area displayed `Latency 2.7ms` for the whole rack.
- The plugin window title/logo reads `Silk Vocal Live` even though the database header observed `<PluginName>Silk Vocal</PluginName>` and the plug row name is `SilkVocl`.
- Visible current Silk settings from the screenshot:
  - Voice type dropdown: `Male`
  - Low focus enabled/selected, value `45`
  - Mid focus enabled/selected, value `35`
  - High focus enabled/selected, value `50`
  - Dynamic mode indicator `Dyn` is lit
  - Output fader readout `0.0`
  - Curve Freeze knob is visible at upper right
  - Two curve-type buttons are visible; the left/blue button appears selected
- Treat this screenshot as a UI baseline only. The Silk Vocal token map is not yet learned, so do not edit Silk RealWorld tokens without controlled UI save comparisons.
