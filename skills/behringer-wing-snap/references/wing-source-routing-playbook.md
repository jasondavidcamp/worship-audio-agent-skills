# WING Source Routing Playbook

Use this when a `.snap` question involves channel sources, physical inputs, stereo pairs, alternate sources, user signals, or mismatched channel labels.

## Source Material Mined

- Behringer WING documentation: WING is built around sources and channels, with 40 stereo input channels, 8 stereo aux channels, 16 stereo aux buses, 4 mains, 8 matrices, and 16 true-stereo FX engines.
- Behringer WING manual material: sources can carry metadata such as name, color, icon, gain/phantom where applicable, and may be routed into channels independently from channel processing.
- WING remote/OSC documentation: `.snap` files are JSON trees under audio-engine and control-engine data.

## Core Principle

On WING, a channel is not the same thing as a physical input. A channel is a processing strip that can pull from a source group and source number. Analysis must follow the source connection, not just the channel number.

## What To Inspect

- Channel label: `ae_data.ch.<n>.name`.
- Active source: `ae_data.ch.<n>.in.conn.grp` and `in`.
- Alternate source: `altgrp` and `altin`.
- Physical/source label: `ae_data.io.in.<grp>.<n>.name` when present.
- Stereo/side naming clues: L/R, left/right, OH L/R, keys L/R, tracks L/R, room L/R.
- Channel processing state: mute, fader, pre/post insert, sends, main assignment.
- Source duplication: the same physical source feeding multiple active channels.
- User signal/tap paths when present; these may intentionally carry post-fader or processed signals.

## Diagnostic Patterns

- Channel name and source name differ: not automatically wrong. Treat as a review item unless the names imply shifted inputs or a known mistake.
- Channel 12 uses source A.11 and channel 13 uses A.12: possible one-channel shift, especially if several adjacent names are shifted.
- Channel says "OH L" but source says "OH R": possible L/R swap.
- Active channel has source `OFF`: confirmed issue if the fader is up and the channel appears intended for live use.
- Duplicate physical source feeds two named active channels: possible split channel, parallel processing, or accidental duplicate patch. Mark as inferred.
- Alternate source points to USB/W-LIVE/card playback: possible virtual-soundcheck setup; check whether it is live-safe for the current snapshot.

## Recommended Output

For source-routing findings, report:

- Channel path: `CH## name`.
- Active source and resolved source label.
- Alternate source if present.
- Evidence level: confirmed from file or inferred from naming.
- Risk: no audio, wrong source, L/R swap, duplicated source, stale virtual-soundcheck source, or just naming inconsistency.

## Safe Language

- "The file confirms this channel is patched from..."
- "The name suggests a possible shift, but the file does not prove intent."
- "This may be intentional if the operator uses split channels."
- "Check on console before recall if this snapshot will affect live source routing."
