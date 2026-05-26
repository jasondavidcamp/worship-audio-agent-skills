# WING Recording And Virtual Soundcheck

Use this when a `.snap` question involves USB, W-LIVE, card routing, playback, virtual soundcheck, stream recording, or multitrack capture.

## Source Material Mined

- Behringer WING product documentation: WING includes integrated 48x48 USB audio and supports optional 64-channel audio networking cards.
- WING documentation and user material: W-LIVE/USB/card routing can be used for multitrack recording, playback, and virtual soundcheck style workflows.
- WING source architecture: channel active and alternate sources can differ, which matters when a show uses live inputs plus playback/recording returns.

## Core Principle

Recording and virtual soundcheck are routing states, not just storage features. A snapshot can tell you whether USB/card/W-LIVE paths are patched, but it may not tell you the operator's intent. Separate live source, recording send, playback return, and stream feed.

## What To Inspect

- Global audio: `ae_globals.clkrate`, `clksrc`, USB/audio config fields such as `usbacfg` when present.
- Card state: `ae_data.cards`.
- Output patch groups: `USB`, `CRD`, `MOD`, W-LIVE/card-specific groups, and any other group under `ae_data.io.out`.
- Input source groups used by channels and alt sources: live stagebox/local groups vs USB/card/playback groups.
- Whether channel alt sources are consistent across adjacent channels.
- Whether a stream/record feed is patched from mains, matrix, bus, or channel/direct sources.
- Whether W-LIVE/USB playback sources are still assigned to active channels in a live-service snapshot.

## Diagnostic Patterns

- `USB` or `CRD` outputs are sourced from direct channels: likely multitrack recording.
- `USB` or `CRD` outputs are sourced from mains/matrices: likely stereo broadcast/record feed.
- Channel alt sources point to USB/card playback: likely virtual soundcheck.
- Active channel sources point to USB/card playback during a live snapshot: possible accidental virtual-soundcheck state.
- Stream feed comes from main LR only: may miss broadcast-specific vocal, audience, or loudness treatment.
- Recording feed uses post-fader/user signals: useful for stem-style capture, but not the same as raw preamp capture.

## Review Questions

- Is this snapshot intended for live inputs, playback/virtual soundcheck, recording, or streaming?
- Are the capture sends preamp/direct, post-processing, post-fader, or matrix/bus feeds?
- Does the recording path need raw multitrack, broadcast mix, or both?
- Are live and playback sources separated clearly enough for volunteers?
- Is sample rate compatible with the connected recorder/interface/plugin host?

## Recommended Output

For recording/virtual-soundcheck findings, report:

- Capture path: output group/channel and resolved source.
- Playback path: active or alternate source groups on channels.
- Live risk: accidental playback source, missing capture channel, sample-rate mismatch, wrong tap point, or unlabeled route.
- Human check: what to confirm on the console before service.
