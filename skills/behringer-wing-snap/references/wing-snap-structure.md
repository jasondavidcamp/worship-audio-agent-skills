# Behringer WING .snap Structure

## Format

Observed `.snap` files are JSON:

```json
{
  "type": "snapshot.11",
  "creator_fw": "...",
  "creator_model": "wing-fullsize",
  "active_show": "...",
  "active_scene": "...",
  "ae_data": {},
  "ce_data": {},
  "ae_globals": {},
  "ce_globals": {}
}
```

Use `json.load`; do not parse with regex.

## Important Top-Level Areas

- `scopes`: optional snapshot recall/save scope tree. Some observed `.snap` files omit it; do not fail analysis if absent.
- `ae_globals`: audio engine globals such as `clkrate`, `clksrc`, `usbacfg`.
- `ae_data.io.in`: physical/source input names by group (`A`, `B`, `C`, `LCL`, etc.).
- `ae_data.io.out`: output patch by group (`USB`, `CRD`, `MOD`, `LCL`, etc.).
- `ae_data.ch`: input channels.
- `ae_data.bus`: buses.
- `ae_data.main`: mains.
- `ae_data.mtx`: matrices.
- `ae_data.fx`: FX and external insert definitions.
- `ae_data.cards`: W-LIVE/W-MADI/card settings.
- `ce_data.user`: user keys/layers.

## Snapshot Scopes

WING remote/OSC documentation describes snapshot scopes as Boolean groups that say what was saved and what recall will affect. Treat them as recall-safety metadata rather than ordinary audio routing.

Known scope groups:

- `ch`: channels `1..40`
- `aux`: auxes `1..8`
- `bus`: buses `1..16`
- `main`: mains `1..4`
- `mtx`: matrices `1..8`
- `fx`: FX slots `1..16`
- `routin`: input routing groups `1..13`
- `routout`: output routing groups `1..11`
- `cfg`: `groups`, `audio`, `surface`, `custom`
- `area`: `L`, `C`, `R`
- `data`: `1..9`

If scopes are missing, continue structural analysis from `ae_data` and `ce_data`.

## Common Channel Fields

Input channels live at `ae_data.ch.<n>`:

- `name`: user-facing channel label.
- `mute`: channel mute.
- `fdr`: fader; `-144` is effectively off.
- `in.conn.grp` and `in.conn.in`: active source.
- `in.conn.altgrp` and `in.conn.altin`: alternate source.
- `preins`: pre-insert assignment, often `{"on": true, "ins": "FX1"}`.
- `postins`: post-insert assignment.
- `send`: bus sends.
- `main`: main assignments.

## External Insert Pattern

An external insert appears as an FX row like:

```json
"13": {
  "mdl": "EXT",
  "fxmix": 100,
  "egrp": "MOD",
  "ein": 49,
  "emode": "M",
  "lat": 5,
  "trim": 0
}
```

Interpretation observed:

- The channel/bus uses `preins.ins = "FX13"`.
- `fx.13.mdl = "EXT"` means external insert.
- `egrp/ein` indicates the return point, e.g. `MOD.49`.
- `lat` is insert latency compensation in milliseconds or a WING latency unit displayed as a number. Treat as console-provided compensation, not plugin latency.

For bus inserts, also check the corresponding `io.out.MOD.<ein>` source to see what signal is sent to the external processor.

## FX SEND Source Pattern

The WING AoIP-WSG guide explains that the FX SENDS source group contains send channels for all 16 FX rack slots. Each slot has an L/R pair:

- `SEND.1` / `SEND.2` = FX1 L/R
- `SEND.3` / `SEND.4` = FX2 L/R
- ...
- `SEND.25` / `SEND.26` = FX13 L/R
- `SEND.31` / `SEND.32` = FX16 L/R

When a `.snap` output patch says:

```json
"MOD": {
  "49": {"grp": "SEND", "in": 25}
}
```

interpret it as `MOD.49` carrying the left side of `FX13`'s external send, not as an arbitrary unnamed send. If only the odd channel is present for a stereo external insert, verify whether the related WING FX mode is mono or whether the even return/send is omitted by design.

## Output Patch Notes

`ae_data.io.out` maps an output group/channel to a source:

```json
"MOD": {
  "49": {"grp": "SEND", "in": 25}
}
```

Observed groups include:

- `USB`: USB output patch.
- `CRD`: card/W-LIVE output patch.
- `MOD`: module/card routing, sometimes used for SuperRack insert paths in SoundGrid workflows.
- `LCL`: local outputs.
- `A`, `B`, `C`: AES50/stagebox groups or physical port groups depending on console setup.

Do not hard-code this list. The analyzer should inspect all groups under `ae_data.io.out` because firmware, expansion cards, and user configuration can expose different group names.

## Issue Heuristics

Flag these for human review:

- Channel label differs from the source name and SuperRack rack name.
- Sequential channels appear shifted by one or more positions.
- Left/right source names are reversed relative to channel labels or SuperRack names.
- Stereo external inserts have only one side of an expected L/R FX SEND pair routed, unless the insert mode is explicitly mono.
- A channel/bus is routed through an external insert but the matching SuperRack rack name does not line up.
- External insert is on but return source is `OFF`.
- Routed channel is muted or fader is `-144` where live use is expected.
- WING sample rate differs from the connected audio/plugin host session.
- Duplicate physical sources feed multiple active channels unexpectedly.
- Snapshot scopes exclude the area being judged, for example output routing omitted when the user expects a routing snapshot.
- Virtual-soundcheck or playback routes are still active in a live-service snapshot.

Do not assume every mismatch is wrong. Some WING channels intentionally use different labels from physical patch names.

## Source References

- Behringer WING product documentation page: documents WING channel/bus count, USB 48x48, optional AoIP cards, and WING Manual / Remote Protocol / Waves SoundGrid QSG links.
- Behringer AoIP-WSG Quick Start Guide: documents 64x64 SoundGrid routing, WSG source/output groups, WING USER SIGNAL tap/post-fader sends, SuperRack rack routing, and EXTERNAL FX insertion.
- WING OSC/Remote Control Documentation: documents `.snap` JSON tree structure and `scopes` groups.
