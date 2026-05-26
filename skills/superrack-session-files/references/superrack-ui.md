# SuperRack UI Reference

Visual notes learned from SuperRack Performer v15.14.136.660 screenshots.

## Rack View

- The large title at top left shows the selected rack/bus. In the observed session it reads `Band Bus`.
- The selected plugin tile in the left chain is outlined yellow.
- The sidechain source dropdown appears above the plugin editor, labeled `SIDE CHAIN`.
- For the observed vocal-pocketing setup, that dropdown displays `Vocal Bus`.
- The plugin tile for the sidechained F6-RTA shows an orange/red `SC` badge.
- The same plugin tile shows `IN`, meaning the plugin instance is inserted and enabled.

## Overview View

- The `49-64` layer shows bus-style strips.
- In the observed session:
  - `Vocal Bus` input is numbered `49`.
  - `Band Bus` input is numbered `51`.
  - `Drum Bus` input is numbered `53`.
  - `Livestream` input is numbered `60`.
- Band Bus visible chain order:
  1. `NLS Buss`
  2. `F6-RTA` sidechained pocketing instance
  3. `SSL Cmp`
  4. `TGMstrL`
  5. Existing late-chain `F6-RTA`
- This matches the database pattern where Band Bus is `chainer_id=51`, the pocketing F6-RTA is slot `2`, and the old late-chain F6-RTA remains slot `5`.

## F6-RTA Visual Cues

- A flat EQ line is expected when static gain is `0`; dynamic ducking is not visible as a static EQ curve.
- The graph may still show numbered markers `1-6` even when the intent is to use only selected dynamic bands.
- In the observed pocketing setup, bands 5 and 6 are the active vocal-pocketing bands:
  - Band 5: `2200 Hz`, range `-2 dB`, attack `20 ms`, release `180 ms`.
- Band 6: `4000 Hz`, range `-1.5 dB`, attack `10 ms`, release `120 ms`.
- The selected band's lower controls show its frequency, Q, gain, range, threshold, attack, release, and sidechain mode.
- The rack-level sidechain dropdown and the plugin-level F6 `SC SOURCE` controls are separate visual checks.
- In the screenshot, the rack-level sidechain dropdown displays `Vocal Bus`, and the plugin tile shows `SC`.
- In the same screenshot, the selected F6 band's `SC SOURCE` area appears to show `INT` selected, not `EXT`.
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
- To see action, audio must be passing through Band Bus and Vocal Bus at the same time.
- Watch the F6 band's dynamic movement or gain-reduction behavior while vocals are active.
- If the user is confused by all six markers, disable unused visible bands in the preset state rather than relying on explanation alone.

## Silk Vocal Visual Cues

Observed Blue Vocal screenshot after adding Silk Vocal Live:

- Rack title: `Blue Vocal`; top subtitle showed `PRESET*`, indicating unsaved or modified preset/session state.
- Left chain order:
  1. `SilkVocl`
  2. `F6-RTA`
  3. `DeEsser`
  4. `RVox`
  5. `API-550B`
- The selected Silk tile is outlined yellow and shows `IN`.
- Silk tile latency displayed `LT 1.3ms`; rack output latency area displayed `Latency 2.7ms` for the whole Blue Vocal rack.
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
