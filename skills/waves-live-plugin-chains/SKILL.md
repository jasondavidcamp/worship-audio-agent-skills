---
name: waves-live-plugin-chains
description: Choose live-safe, SuperRack-compatible Waves plugin chains for worship, church livestream, and live broadcast workflows. Use when the user specifically has Waves plugins, SuperRack SoundGrid, SuperRack Performer, LV1/SuperRack-compatible Waves processing, or REAPER-staged Waves chain testing and needs source-specific plugin selection, serial chain order, latency/safety checks, F6/PSE/RVox/Sibilance/CLA/API/SSL selection, or help translating an audio diagnosis into Waves plugin moves that should survive SuperRack deployment.
---

# Waves Live Plugin Chains

## Purpose

Use this skill as the Waves-specific plugin decision layer. It translates an audio diagnosis into live-safe, SuperRack-compatible Waves plugin choices, chain order, and validation checks.

Keep `live-worship-mix-engineering` Waves-neutral. Use this skill only after the user says Waves, SuperRack, LV1/SuperRack, or a Waves plugin is available or desired.

## Operating Rules

1. Define the audible problem before naming a plugin.
2. Prefer one clear job per plugin.
3. Keep chains serial unless the final host supports the same routing and latency behavior.
4. Only recommend chain plugins that are confirmed for SuperRack SoundGrid or SuperRack Performer by official Waves compatibility data or verified in the target SuperRack instance.
5. Filter choices through live suitability: latency, CPU, stability, recall behavior, mono compatibility, and SoundGrid/Performer support.
6. Treat "Live" plugin components or modes as different from full/lookahead/studio modes; choose the live component when the source is heard in the venue.
7. Mark high-latency AI cleanup, heavy restoration, mastering, or analysis plugins as broadcast-only/verify-first unless official Waves data says they are suitable for the target live path.
8. Treat installed plugins as candidates, not automatic recommendations.
9. Loudness-match insert/bypass and candidate renders before ranking.
10. Reject clipping, crackle, hash, pumping, obvious tuning artifacts, over-expanded phrases, or lost lyric intelligibility before asking for taste.
11. If the task becomes `.sprk` or `.xps` file inspection/patching, switch to `superrack-session-files`.

## Chain Decision Flow

1. Start from the diagnosis:
   - Vocal buried, sharp, inconsistent, processed, or distant.
   - Band cloudy, small, masking, or not lifting.
   - Drums pokey, buried, harsh, or disconnected from bass.
   - Livestream quiet, crunchy, harsh, dry, or too different from the room.

2. Choose the role:
   - Cleanup: PSE, C1/EMO-D5, HPF/EQ, F6, de-esser.
   - Control: RComp, RVox, CLA-76, CLA-2A, C6/C4, SSL/API bus compression.
   - Polish: saturation, exciter, delay, reverb, subtle widening, tuning.
   - Protection/measurement: L2/L3-LL/L4, WLM, meters.

3. Pick the simplest live-safe chain:
   - Remove noise, bleed, and masking before adding brightness or loudness.
   - Add compression only after the source lane is clear enough to compress safely.
   - Add ambience or width only after lyric clarity and mono translation survive.
   - If any proposed plugin fails the SuperRack/latency gate, replace it or label it as a verified-only exception.

4. Document transfer constraints:
   - Host: SuperRack SoundGrid or SuperRack Performer. LV1/REAPER references are acceptable only when the same chain is expected to transfer to SuperRack.
   - Mono/stereo format.
   - Sidechain needs.
   - Snapshot/recall requirements.
   - Latency and CPU risk.

## Reference Files

- Read `references/superrack-live-eligibility-gate.md` first when a chain will be used live. It is the compatibility, version, latency, format, and CPU gate.
- Read `references/waves-plugin-decision-matrix.md` for source-specific plugin choices and first-line alternatives.
- Read `references/waves-superrack-operational-reference.md` for live-safety, latency posture, SoundGrid/Performer cautions, and operational metadata.
- Read `references/waves-next-move-map.md` when translating common worship-mix diagnoses into Waves-specific next moves.
- Read `references/superrack-vocal-speech-chains.md` for lead vocal, BGV/choir, and spoken-word/pastor mic chains.
- Read `references/superrack-rhythm-band-bus-chains.md` for drums, kick/bass/low-end, band bus, mix bus, and livestream bus chains.
- Read `references/superrack-fx-pocketing-workflows.md` for live-safe delay/reverb workflows and F6/C6 pocketing.
- Read `references/superrack-failure-modes.md` before recommending AI cleanup, tuning, expansion, live modes, low-end enhancers, limiters, or stereo/width tools.

## Helper Script

Generate a local installed-plugin catalog:

```powershell
& "<python>" scripts/inventory_waves_plugins.py --md-output references/local-waves-plugin-catalog.md --json-output references/local-waves-plugin-inventory.json
```

Keep generated inventories private unless intentionally sanitized. They reflect the current machine's Waves install and license state.

## Related Skills

- Use `live-worship-mix-engineering` for the general worship-mix diagnosis and non-Waves workflow.
- Use `band-sound-aimpoint` to define the desired sound or reference target.
- Use `reaper-render-reference` to render and compare Waves chain candidates in REAPER.
- Use `superrack-session-files` to inspect, validate, or patch SuperRack `.sprk` and `.xps` files.
