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

## Analysis Checklist

For standalone WING snapshots, inspect:

- Metadata: model, firmware, created timestamp, active scene/show.
- Snapshot scopes when present: `scopes.ch`, `aux`, `bus`, `main`, `mtx`, `fx`, `routin`, `routout`, `cfg`, `area`, and `data`.
- Global audio state: `ae_globals.clkrate`, `clksrc`, USB/card config.
- Input channels: names, source `grp/in`, alt source, mute, fader, inserts.
- Buses, mains, and matrices: names, mono/stereo state, fader, mute, sends, insert state.
- FX external inserts: `fx[*].mdl == EXT`, return group/input, latency, mix, and matching `SEND` source pair.
- Output patches: `ae_data.io.out` for `USB`, `CRD`, `MOD`, local outputs, AES, etc.
- Potential mistakes: shifted names, L/R swaps, routed-but-muted channels, fader `-144`, off sources, duplicate source assignments, unexplained external inserts.

For WING-to-SuperRack comparisons:

- Compare WING output patch numbers to SuperRack rack/channel numbers.
- Compare source names against SuperRack rack names.
- Check external insert returns, especially bus inserts returning on `MOD` channels.
- Decode `SEND.n` output sources as FX-send lanes when possible: `SEND.1/2 = FX1 L/R`, `SEND.25/26 = FX13 L/R`, etc.
- Verify sample rate compatibility.
- Verify bus names and intended insert paths: e.g. `VOCALS -> Vocal Bus`, `BAND -> Band Bus`, `DRUMS -> Drum Bus`, `LIVSTR -> Livestream`.
- Keep SuperRack plugin judgments in the SuperRack skill; use this skill for WING topology and mixer-state evidence.

## Documentation Anchors

Use official Behringer/WING docs as anchors, then validate against the actual `.snap` file:

- WING product documentation confirms the console architecture: 40 stereo input channels, 8 stereo aux input channels, 16 aux stereo buses, 4 mains, 8 matrices, 16 true-stereo FX engines, integrated 48x48 USB audio, and optional 64-channel AoIP cards.
- The AoIP-WSG quick start guide documents 64 channels from console to SoundGrid and 64 return channels back to WING. It also documents EXTERNAL FX insertion on channels/buses and routing FX SEND L/R lanes through selected SoundGrid channels.
- WING remote/OSC documentation describes snapfiles as JSON trees and defines snapshot scopes for saved/recallable parameter groups.

## Learned Pattern

- WING `.snap` is JSON.
- WING sample rate is often `48000`, but confirm from the file.
- WING external inserts used `FX` rows with `mdl: EXT`.
- Bus insert returns may use `MOD` channels in SoundGrid-card workflows, for example:
  - `bus01 VOCALS -> FX13 -> MOD.49 -> SuperRack Vocal Bus`
  - `bus03 BAND -> FX14 -> MOD.51 -> SuperRack Band Bus`
  - `bus05 DRUMS -> FX15 -> MOD.53 -> SuperRack Drum Bus`
  - `main04 LIVSTR -> FX16 -> MOD.60 -> SuperRack Livestream`

These are examples, not universal constants. Re-detect every time.
