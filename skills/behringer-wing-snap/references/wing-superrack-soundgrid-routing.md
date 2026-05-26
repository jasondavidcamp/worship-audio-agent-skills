# WING SuperRack And SoundGrid Routing

Use this when WING snapshots involve AoIP-WSG, WSG/SoundGrid card routing, Waves SuperRack inserts, external FX, or WING-to-SuperRack comparisons.

## Source Material Mined

- Behringer AoIP-WSG quick start material: the WING SoundGrid card supports 64 channels from console to SoundGrid and 64 return channels back to WING.
- Behringer AoIP-WSG material: SuperRack can be used with WING by assigning WING signals to SoundGrid card channels and returning processed audio.
- WING external FX pattern: WING FX slots can be set to external insert mode, with send and return paths routed through the expansion/card group.
- Waves SuperRack live posture: plugin-chain decisions belong in `waves-live-plugin-chains`; `.sprk` file validation belongs in `superrack-session-files`.

## Core Principle

For SuperRack workflows, the WING snapshot proves console-side topology: what signal is sent out, where processed audio returns, and which channel/bus/main/matrix uses the external insert. It does not prove the Waves plugin chain is good.

## What To Inspect

- FX rows where `mdl == EXT`.
- Insert assignments on channels, buses, mains, and matrices: `preins` and `postins`.
- External return group/input: `fx.<n>.egrp` and `ein`.
- Output patch for the return/input channel number, often the same card/module channel used for the external send.
- `SEND.n` source group decoding:
  - `SEND.1/2` = FX1 L/R.
  - `SEND.3/4` = FX2 L/R.
  - Continue by pairs through FX16.
  - `SEND.25/26` = FX13 L/R.
  - `SEND.31/32` = FX16 L/R.
- Sample rate and clock source.
- SuperRack rack/channel names if comparing with `.sprk`.

## Diagnostic Patterns

- FX slot is `EXT` but no channel/bus/main uses that FX slot as insert: possible unused external insert.
- Channel/bus uses `FX13` insert but FX13 is not `EXT`: insert is not a SoundGrid external path.
- FX return is `MOD.49`, but output patch `MOD.49` is not sourced from expected `SEND.25`: possible mismatched send/return lane.
- Insert return group is `OFF` or missing: confirmed broken external insert path.
- WING bus name and SuperRack rack name differ: possible naming drift; mark as inferred unless routing proves mismatch.
- WING sample rate differs from SuperRack/server expectations: confirmed compatibility risk if files show conflicting values.
- Only one side of a stereo insert appears: verify mono/stereo mode before calling it wrong.

## Recommended Output

For each external insert, report:

- Insert owner: channel/bus/main/matrix using `FXn`.
- FX slot: model, mix, latency, return group/input.
- Send lane: output group/channel and decoded source, e.g. `SEND.25 = FX13 SEND L`.
- Expected pair: odd/even SEND lanes for stereo inserts.
- SuperRack comparison: matching rack/channel name when a `.sprk` is provided.
- Risk: unused insert, wrong send lane, missing return, sample-rate mismatch, stereo mismatch, or name drift.

## Skill Boundaries

- Use this skill for WING evidence.
- Use `superrack-session-files` to inspect racks, snapshots, plugin order, bypass state, and `.sprk`/`.xps` internals.
- Use `waves-live-plugin-chains` to judge whether the Waves chain itself is live-safe.
