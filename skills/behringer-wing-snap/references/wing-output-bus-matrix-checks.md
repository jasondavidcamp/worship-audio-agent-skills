# WING Output, Bus, Main, And Matrix Checks

Use this when a `.snap` question involves buses, mains, matrices, local outputs, AES50/stageboxes, USB/card outputs, livestream feeds, lobby/overflow feeds, or hearing-assist/broadcast routing.

## Source Material Mined

- Behringer WING product documentation: WING provides 16 stereo aux buses, 4 stereo mains, 8 stereo matrices, 16 true-stereo FX engines, 48x48 USB, and optional 64-channel AoIP card support.
- WING manual/routing material: output groups patch console sources to physical/local, AES50/stagebox, USB, card/module, or other destinations.
- WING source architecture: buses, mains, matrices, channels, and send lanes can all become output-patch sources.

## Core Principle

The destination group tells where audio leaves the console. The source field tells what signal is feeding it. Analyze both sides before judging a route.

## What To Inspect

- `ae_data.bus`, `ae_data.main`, and `ae_data.mtx`: names, mono/stereo state, mute, fader, inserts.
- Sends to buses/matrices when present.
- Main assignments from channels/buses.
- Every group under `ae_data.io.out`: local, AES50, USB, card/module, and any firmware/card-specific groups.
- Output sources: `CH`, `BUS`, `MAIN`, `MTX`, `SEND`, user signals, direct/tap paths, and `OFF`.
- Stream/lobby/recording naming: `LIVSTR`, `STREAM`, `BCAST`, `LOBBY`, `REC`, `MATRIX`, `HEARING`, etc.
- Mute/fader state of source bus/matrix as well as the output patch itself.

## Diagnostic Patterns

- Output patch is `OFF` for a named destination: confirmed no source unless another patch path exists.
- Matrix/livestream output is sourced from main LR only: not wrong, but note that stream may lack independent vocal/audience/loudness control.
- Lobby/overflow feed sourced from a post-fader bus: likely follows FOH changes; confirm intent.
- Recording output sourced from matrix rather than direct channels: likely stereo program recording, not multitrack.
- Matrix/bus feeding output is muted or fader `-144`: routed but silent.
- Destination name and source name imply swapped L/R: possible left/right error.
- Several adjacent output patches are shifted by one: possible copy/paste or routing offset error.

## Church Feed Patterns

- FOH mains: usually `MAIN` to local/AES50/system processor outputs.
- Livestream/broadcast: often matrix or dedicated main/bus to USB/card/encoder.
- Lobby/overflow: often matrix fed from mains plus speech priority.
- Hearing assist: often speech-forward matrix.
- SuperRack insert sends: often `SEND` source lanes to SoundGrid/card outputs.
- Multitrack recording: often channel/direct/user-signal outputs to USB/card.

## Recommended Output

For output findings, report:

- Destination: output group/channel.
- Source: source group/input and resolved source label.
- Upstream state: source bus/main/matrix mute/fader if available.
- Intended use inferred from name if any.
- Risk: silent route, wrong source, L/R swap, shifted patch, stream-lacks-control, or unknown intent.
