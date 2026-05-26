---
name: waves-live-plugin-chains
description: Choose live-safe Waves plugin chains for worship, church livestream, and SuperRack/LV1/REAPER workflows. Use when the user specifically has Waves plugins, SuperRack SoundGrid, SuperRack Performer, LV1, MultiRack, or REAPER-hosted Waves processing and needs source-specific plugin selection, serial chain order, latency/safety checks, F6/PSE/RVox/Sibilance/CLA/API/SSL style decisions, or help translating a general worship-mix diagnosis into Waves plugin moves.
---

# Waves Live Plugin Chains

## Purpose

Use this skill as the Waves-specific plugin decision layer. It translates a general worship-mix diagnosis into live-safe Waves plugin choices, chain order, and validation checks.

Keep `live-worship-mix-engineering` Waves-neutral. Use this skill only after the user says Waves, SuperRack, LV1, MultiRack, or a Waves plugin is available or desired.

## Operating Rules

1. Define the audible problem before naming a plugin.
2. Prefer one clear job per plugin.
3. Keep chains serial unless the final host supports the same routing and latency behavior.
4. Filter choices through live suitability: latency, CPU, stability, recall behavior, mono compatibility, and SoundGrid/Performer support.
5. Treat installed plugins as candidates, not automatic recommendations.
6. Loudness-match insert/bypass and candidate renders before ranking.
7. Reject clipping, crackle, hash, pumping, obvious tuning artifacts, over-expanded phrases, or lost lyric intelligibility before asking for taste.
8. If the task becomes `.sprk` or `.xps` file inspection/patching, switch to `superrack-session-files`.

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

4. Document transfer constraints:
   - Host: SuperRack SoundGrid, SuperRack Performer, LV1, MultiRack, REAPER, or other.
   - Mono/stereo format.
   - Sidechain needs.
   - Snapshot/recall requirements.
   - Latency and CPU risk.

## Reference Files

- Read `references/waves-plugin-decision-matrix.md` for source-specific plugin choices and first-line alternatives.
- Read `references/waves-superrack-operational-reference.md` for live-safety, latency posture, SoundGrid/Performer cautions, and operational metadata.
- Read `references/waves-next-move-map.md` when translating common worship-mix diagnoses into Waves-specific next moves.

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
