---
name: behringer-wing-snap
description: Inspect and analyze Behringer WING .snap mixer snapshot JSON files. Use when working with WING/W-LIVE/USB/card routing, channel and bus names, external inserts, source patching, stereo pair swaps, mains/matrices, mute/fader state, snapshot sanity checks, or comparing a WING .snap file against a Waves SuperRack .sprk session.
---

# Behringer WING Snap

## Safety Workflow

Treat `.snap` files as mixer snapshots that may represent a live console state.

1. Work read-only unless the user explicitly asks for edits.
2. Confirm the file is JSON and starts with a top-level `type` such as `snapshot.11`.
3. Parse with a JSON parser; do not use ad hoc text replacement for analysis.
4. Summarize topology before judging it: channel inputs, bus inserts, output patch, clock/sample rate, and card settings.
5. Flag issues as "confirmed" only when the file provides direct evidence. Mark inferred items as assumptions.
6. When comparing to SuperRack, analyze both files independently first, then compare channel numbers/names/routing.

## Quick Start

Use `scripts/inspect_wing_snap.py` for a compact report:

```powershell
& "<python>" scripts/inspect_wing_snap.py "<path-to-snapshot.snap>"
```

When comparing to SuperRack:

```powershell
& "<python>" scripts/inspect_wing_snap.py "<path-to-snapshot.snap>" --superrack "<path-to-session.sprk>"
```

Read `references/wing-snap-structure.md` when you need field notes, learned path meanings, or comparison cautions.

Use the focused references below when the question is more specific:

- `references/wing-source-routing-playbook.md`: source patching, channel source vs channel processing, alternate sources, user signals, stereo pair risks.
- `references/wing-recording-virtual-soundcheck.md`: USB/W-LIVE/card routing, recording/playback, virtual soundcheck, stream/record feeds.
- `references/wing-snapshot-scope-recall.md`: snapshot scopes, recall safety, scope mismatch, scene hygiene.
- `references/wing-superrack-soundgrid-routing.md`: AoIP-WSG/SoundGrid, SuperRack external inserts, FX SEND lanes, 64x64 checks.
- `references/wing-output-bus-matrix-checks.md`: buses, mains, matrices, local/AES50/card outputs, livestream and lobby/feed sanity checks.

## Analysis Checklist

For standalone WING snapshots, inspect:

- Metadata: model, firmware, created timestamp, active scene/show.
- Snapshot scopes when present: `scopes.ch`, `aux`, `bus`, `main`, `mtx`, `fx`, `routin`, `routout`, `cfg`, `area`, and `data`.
- Global audio state: `ae_globals.clkrate`, `clksrc`, USB/card config.
- Input channels: names, source `grp/in`, alt source, mute, fader, inserts.
- Source patching: distinguish source labels from channel names; inspect source group, source number, alt source, stereo role, and user signal/tap path when present.
- Buses, mains, and matrices: names, mono/stereo state, fader, mute, sends, insert state.
- FX external inserts: `fx[*].mdl == EXT`, return group/input, latency, mix, and matching `SEND` source pair.
- Output patches: inspect every group under `ae_data.io.out`, not only `USB`, `CRD`, `MOD`, and local outputs.
- Potential mistakes: shifted names, L/R swaps, routed-but-muted channels, fader `-144`, off sources, duplicate source assignments, unexplained external inserts, stale virtual-soundcheck alt sources, and output groups patched from the wrong tap/source.

For WING-to-SuperRack comparisons:

- Compare WING output patch numbers to SuperRack rack/channel numbers.
- Compare source names against SuperRack rack names.
- Check external insert returns, especially bus inserts returning on `MOD` channels.
- Decode `SEND.n` output sources as FX-send lanes when possible: `SEND.1/2 = FX1 L/R`, `SEND.25/26 = FX13 L/R`, etc.
- Verify sample rate compatibility.
- Verify bus names and intended insert paths without assuming house-specific bus numbers: e.g. `<bus/main name> -> FX slot -> card/module return -> SuperRack rack name`.
- Keep Waves plugin-chain judgments in `waves-live-plugin-chains` and SuperRack file judgments in `superrack-session-files`; use this skill for WING topology and mixer-state evidence.
- If SoundGrid routing is involved, read `references/wing-superrack-soundgrid-routing.md` before judging insert send/return pairs.

## Documentation Anchors

Use official Behringer/WING docs as anchors, then validate against the actual `.snap` file:

- WING product documentation confirms the console architecture: 40 stereo input channels, 8 stereo aux input channels, 16 aux stereo buses, 4 mains, 8 matrices, 16 true-stereo FX engines, integrated 48x48 USB audio, and optional 64-channel AoIP cards.
- The AoIP-WSG quick start guide documents 64 channels from console to SoundGrid and 64 return channels back to WING. It also documents EXTERNAL FX insertion on channels/buses and routing FX SEND L/R lanes through selected SoundGrid channels.
- WING remote/OSC documentation describes snapfiles as JSON trees and defines snapshot scopes for saved/recallable parameter groups.
- WING source-channel architecture separates source capture from channel processing; do not assume channel numbers equal physical input numbers.
- W-LIVE/USB/card routing can carry recording, playback, virtual soundcheck, broadcast, or insert paths; identify the source group and tap before calling a route wrong.

## Learned Pattern

- WING `.snap` is JSON.
- WING sample rate is often `48000`, but confirm from the file.
- WING external inserts commonly appear as `FX` rows with `mdl: EXT`.
- In SoundGrid-card workflows, an inserted bus or main may follow `<bus/main path> <name> -> FXn -> <card group>.<return channel> -> SuperRack <rack name>`.
- The matching card output should often be sourced from the FX SEND lane for that FX slot, but the exact group/channel numbers are deployment-specific.

Re-detect every time. Do not treat example FX, bus, or card channel numbers as constants.
