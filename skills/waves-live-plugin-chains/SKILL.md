---
name: waves-live-plugin-chains
description: Choose live-safe, SuperRack-compatible Waves plugin chains for worship, church livestream, and live broadcast workflows. Use when the user specifically has Waves plugins, SuperRack SoundGrid, SuperRack Performer, LV1/SuperRack-compatible Waves processing, REAPER-staged Waves chain testing, Waves `.xps` preset/chain transfer planning, source-specific plugin selection, serial chain order, latency/safety checks, F6/PSE/RVox/Sibilance/CLA/API/SSL selection, or help translating an audio diagnosis into Waves plugin moves that should survive SuperRack deployment.
---

# Waves Live Plugin Chains

## Purpose

Use this skill as the Waves-specific plugin decision and portable preset-transfer layer. It translates an audio diagnosis into live-safe, SuperRack-compatible Waves plugin choices, chain order, validation checks, and `.xps` transfer intent that can be applied by REAPER or SuperRack host skills.

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
9. Do not count a plugin as tested just because it loaded with default settings. A useful candidate needs a source-specific role, deliberate starting settings or preset choice, and evidence from the same comparison section.
10. For multi-pass chain iteration, define what would improve the aimpoint grade before choosing settings, then require a score or `grade_pending` after the candidate is rendered.
11. Before multi-pass Waves iteration, build a source-specific candidate palette. Include prior approved/exported chains for the same source early, plus at least one alternate topology unless the user explicitly asks for refinement only.
12. Loudness-match insert/bypass and candidate renders before ranking.
13. Reject clipping, crackle, hash, pumping, obvious tuning artifacts, over-expanded phrases, or lost lyric intelligibility before asking for taste.
14. Use this skill for Waves `.xps` shape, chain, compatibility, and transfer planning. Switch to `reaper-session-automation` for live REAPER export/import execution, and to `superrack-session-files` for `.sprk` patching or SuperRack-specific session/rack validation.

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
   - If the only known fact is "this plugin is installed," stop at inventory/discovery and ask `reaper-session-automation` to verify exact names or parameters instead of presenting it as a mix candidate.

3. Build a candidate palette for iteration:
   - Read `references/source-candidate-palettes.md` for the source type.
   - Read `references/musical-palette-expansion-sources.md` when the task asks for broader exploration, 10+ passes, or a less familiar source/plugin family.
   - Check for prior approved/exported chains or presets for the same source; include one early or state why it does not apply.
   - For 5-pass iterations, include topology variety: prior/current chain, clean utility chain, alternate dynamics, color/channel-strip chain, and keeper refinement.
   - For 10-20 pass iterations, broaden into a plugin-family shootout before narrowing.
   - Name the audible hypothesis for each topology, not only the plugin list.

4. Pick the simplest live-safe chain:
   - Remove noise, bleed, and masking before adding brightness or loudness.
   - Add compression only after the source lane is clear enough to compress safely.
   - Add ambience or width only after lyric clarity and mono translation survive.
   - If any proposed plugin fails the SuperRack/latency gate, replace it or label it as a verified-only exception.
   - Include the first intentional settings to try, not only plugin names.
   - For each candidate, state the expected grade movement: what should score higher if the move works, and what tradeoff could lower the score.

5. Document transfer constraints:
   - Host: SuperRack SoundGrid or SuperRack Performer. LV1/REAPER references are acceptable only when the same chain is expected to transfer to SuperRack.
   - Mono/stereo format.
   - Sidechain needs.
   - Snapshot/recall requirements.
   - Latency and CPU risk.

6. Plan `.xps` transfer when needed:
   - Read `references/waves-xps-transfer.md`.
   - Identify whether the artifact is a single-plugin preset or a SuperRack rack-chain preset.
   - For rack-chain `.xps` files that must be auditioned in REAPER, extract embedded plugin presets first, then hand the resulting plugin `.xps` files to `reaper-session-automation`.
   - For approved REAPER chains that must leave REAPER, hand live export execution to `reaper-session-automation` and inspect the resulting `.xps` shape here before SuperRack validation.
   - Require host-specific verification after import. Do not treat `.xps` existence or API acceptance as proof that plugin state is active.

## Reference Files

- Read `references/superrack-live-eligibility-gate.md` first when a chain will be used live. It is the compatibility, version, latency, format, and CPU gate.
- Read `references/superrack-host-latency-cpu-planning.md` when choosing between SuperRack SoundGrid, SuperRack Performer, LV1, REAPER staging, broadcast-only use, or when CPU/artifact/latency risk affects the chain.
- Read `references/waves-plugin-decision-matrix.md` for source-specific plugin choices and first-line alternatives.
- Read `references/waves-superrack-operational-reference.md` for live-safety, latency posture, SoundGrid/Performer cautions, and operational metadata.
- Read `references/source-candidate-palettes.md` before multi-pass Waves iterations, especially when the user wants broader exploration across instruments, voice types, or plugin families.
- Read `references/waves-xps-transfer.md` when exporting, importing, decomposing, inspecting, or planning `.xps` preset/chain movement between REAPER and SuperRack.
- Read `references/musical-palette-expansion-sources.md` when broadening palettes from FOH live-chain examples, church/worship case studies, StudioVerse popularity patterns, or plugin manuals/product pages after the official eligibility gate passes.
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

Inspect a Waves `.xps` file and identify whether it is a single-plugin preset or a SuperRack rack-chain preset:

```powershell
& "<python>" scripts/inspect_waves_xps.py "C:\path\preset-or-rack.xps"
```

Extract embedded plugin presets from a SuperRack rack-chain `.xps` for REAPER auditioning or per-plugin comparison:

```powershell
& "<python>" scripts/extract_plugin_xps_from_rack_xps.py "C:\path\rack-chain.xps" "C:\path\extracted-plugin-presets"
```

## Related Skills

- Use `live-worship-mix-engineering` for the general worship-mix diagnosis and non-Waves workflow.
- Use `band-sound-aimpoint` to define the desired sound or reference target.
- Use `reaper-session-automation` to stage or render Waves chain candidates in REAPER, export live REAPER plugin `.xps` files, or attempt/verify plugin `.xps` import into REAPER.
- Use `mix-render-diagnostics` to compare the resulting WAVs or stems.
- Use `superrack-session-files` to inspect, validate, or patch SuperRack `.sprk` sessions and SuperRack-specific rack-chain state after this skill has handled portable Waves `.xps` intent.
