---
name: band-sound-aimpoint
description: Define, analyze, calibrate, and apply a target sound for church band mixes using reference tracks, user taste calls, and style vocabulary such as CityAlight-style naturalness. Use when comparing band, livestream, vocal, drum, or full-mix renders against a desired style/feel; creating mix aimpoints; describing tonal balance, dynamics, arrangement density, worship-band aesthetic, congregational clarity, reference-track matching, taste preferences, emotional mix goals, or plugin-chain decisions against a known target.
---

# Band Sound Aimpoint

## Purpose

Use this skill to keep mix decisions anchored to a named musical target instead of isolated plugin tweaks. Combine subjective language, reference-track evidence, objective metrics, and deployment-local taste history so Codex can make better engineering recommendations.

This skill owns taste calls: asking for them, interpreting them, resolving conflicts with references, and converting repeated reactions into deployment-local calibration rules. Other audio skills may consume an aimpoint or preference rule from this skill, but they should not maintain their own taste-call memory.

## Operating Rules

1. Treat references as aimpoints, not templates to clone exactly.
2. Separate the musical goal from the measurement: name the feel first, then use metrics to check whether a candidate moved toward or away from it.
3. Loudness-match before judging tonal balance.
4. Compare similar sections when possible: intro to intro, full chorus to full chorus, sparse verse to sparse verse.
5. Preserve congregational priorities: lyric intelligibility, stable lead vocal, supportive band energy, and low fatigue matter more than record-polish alone.
6. Use copyrighted reference audio only for private analysis. Do not copy it into skill folders or generated deliverables.
7. Treat user taste calls as stronger calibration than public reference matching when they conflict.
8. When the user asks to iterate toward an aimpoint, require a per-pass aimpoint grade with confidence, reason, and next move. Do not let ungraded plugin changes count as aimpoint iteration.
9. Convert repeated user reactions into durable rules in a deployment-local taste-call log kept outside public skill repositories.
10. Classify the style family before recommending a target: natural congregational, acoustic/folk, modern arena, ambient/spontaneous, track-heavy pop, gospel-influenced, or hybrid.
11. Keep objective profile fields separate from value judgments; a bright/wide/compressed reference may be correct for one style and wrong for another.

## Workflow

1. Identify the aimpoint:
   - Reference track path(s).
   - Target section(s): full chorus, down verse, bridge, outro, or whole track.
   - Desired application: livestream mix, vocal bus, band bus, drum bus, mains, or rehearsal/studio render.
   - Reference role: primary sound target, secondary feature target, translation check, or negative reference.

2. Build a qualitative profile:
   - Energy: restrained, driving, intimate, celebratory, wide, dry, roomy, polished, raw.
   - Vocal relationship: lead-forward, blended, gang-vocal, congregational.
   - Band relationship: acoustic-led, piano-led, drum-led, guitar-led, dense/full, open/sparse.
   - Low-end stance: warm/supportive, tight/controlled, modern/sub-heavy, light.
   - Top-end stance: smooth, airy, bright, aggressive, dark.
   - Style family and arrangement density.

3. Analyze the reference:
   - Use `scripts/analyze_reference_audio.py` for loudness, peak/RMS, crest factor, section-level energy, and broad frequency bands.
   - Add `--essentia` when Essentia Python bindings are available and tonal/rhythm/spectral descriptors would help compare the aimpoint.
   - Save or update a reference profile in `references/`.

4. Compare the candidate render:
   - Use the same kind of section from a trustworthy REAPER render, stem, or other source.
   - Loudness-match the candidate render to the reference before judging tone.
   - Compare broad bands and dynamics, then write an engineering interpretation.
   - For bass-guitar stem aimpoints such as a CityAlight-style bass reference, use `mix-render-diagnostics/scripts/reference_score.py --source bass` when the user wants no-human automated test points beyond section matching.
   - For iteration batches, assign an `aimpoint_grade` on a 0-100 scale, a confidence level, a one-sentence reason, and whether it moved closer, farther, or stayed flat versus the prior pass.

5. Turn analysis into moves:
   - Recommend small, reversible changes first.
   - Tie each suggestion to the aimpoint: "more lead-forward," "less low-mid cloud," "more acoustic transient," "less cymbal edge."
   - When host/session automation is needed, use `reaper-session-automation`; when rendered-audio comparison is needed, use `mix-render-diagnostics`.

6. Capture taste feedback:
   - Ask for small A/B taste calls when two candidates trade clarity, warmth, vocal pocket, BGV blend, ambience, or band energy.
   - Read any deployment-local taste-call log before interpreting a taste call when one exists.
   - Convert the user's reaction into a reusable rule, not just a one-off note.
   - Export the resulting aimpoint or preference rule in concrete mix language that `live-worship-mix-engineering`, `mix-render-diagnostics`, or `waves-live-plugin-chains` can consume.
   - Let `live-worship-mix-engineering` handle detailed diagnosis and practical next-move selection after the taste preference has been translated into an aimpoint.

## Taste Call Ownership

Use this skill whenever the user is choosing between subjective tradeoffs, including:

- Clarity versus warmth.
- Vocal-forward versus blended.
- Dry/intimate versus ambient/spacious.
- Natural drums versus sample-forward impact.
- Smooth top versus bright excitement.
- Congregational/natural versus polished/modern.
- Mono-first stability versus stereo width.

Record taste calls as:

- Exact user language.
- Candidate or reference context.
- Inferred durable preference.
- Confidence level: one-off reaction, repeated pattern, or confirmed rule.
- Deployment scope: this song, this service, this church, or general preference.

Do not let render metrics overrule a confirmed taste rule unless the render has an objective failure such as clipping, artifacts, lost intelligibility, mono collapse, or unsafe delivery headroom.

## Aimpoint Iteration Grade

For any multi-pass request using words such as "iterate," "try N times," "get closer," "candidate batch," or "toward the aimpoint," keep a compact score for every real pass:

```yaml
iteration: 3
target: Bass Guitar
section: chorus_1 142.5-147.5s
aimpoint_grade: 71
confidence: medium
movement: closer
reason: "Low-mid cloud improved and bass supports the downbeat better, but note attack still feels too soft."
next_move: "Keep the EQ cut; try slightly faster compression release and rerender the same section."
```

Use a 0-100 grade where `100` means the pass fully serves the active aimpoint for the evaluated scope. Prefer whole numbers unless a decimal is genuinely useful. Anchor scores roughly as: `90-100` excellent/near-target, `80-89` strong, `70-79` usable but clearly improvable, `60-69` noticeably off, and below `60` a poor fit or failed pass.

Use `low` confidence when the grade is based only on metrics or session-state evidence. Use `medium` or `high` only when trustworthy audio, a reference/baseline, and either listening notes or strong diagnostic evidence support the call.

## Calibration Sources

Use public internet or training sources for general mix principles, plugin roles, worship-mix workflows, reference vocabulary, arrangement expectations, and before/after decision patterns.

Use the user's direct taste calls for the church's acceptable vocal level, BGV blend, vocal processing amount, ambience depth, drum/band energy, mono deployment priorities, and whether CityAlight, Bethel, Churchfront, or a local hybrid should dominate a decision.

## Reference Files

- Read `references/reference-selection-and-comparison.md` when choosing, vetting, or comparing reference tracks.
- Read `references/worship-style-families.md` when the user names an artist/style or needs a broader target than a single reference track.
- Read `references/congregational-arrangement-aimpoints.md` when the target depends on singability, team size, multitracks/stems, key/tempo, or arrangement density.
- Read `references/aimpoint-profile-schema.md` when creating or updating a reusable reference profile.
- Read `references/worship-mix-hierarchy-examples.md` when turning a style target into practical vocal/band/BGV/low-end priorities.
- Read or update `references/aimpoint-vocabulary.md` when the user describes taste preferences.
- Read `references/training-intake.md` when deciding whether outside material is useful for aimpoint calibration or whether the question requires a user taste call.
- Keep private reference profiles, purchased-stem notes, and deployment-specific taste logs outside public repos; include only sanitized schemas or public summaries here.
- Keep copyrighted reference audio and purchased stem analysis out of public repos unless the analysis is intentionally licensed for sharing.

## Helper Script

Run a reference analysis:

```powershell
& "<python>" scripts/analyze_reference_audio.py "<audio-file>" --pretty
```

Run an optional Essentia pass:

```powershell
& "<python>" scripts/analyze_reference_audio.py "<audio-file>" --essentia --pretty
```

Run a drum-focused pass:

```powershell
& "<python>" scripts/analyze_drum_reference.py "<drum-stem-or-render.wav>" --pretty
```

The script accepts formats readable by the installed audio stack, including WAV and many M4A/AAC files when backend support is present.

If Python cannot decode an M4A/AAC reference, use REAPER as a private decoder: create a temporary item from the source, apply/glue it to WAV, copy the WAV to a scratch analysis folder, and delete the temporary REAPER track/item. Do not store copyrighted reference audio inside the skill folder.

Essentia note: native Windows Python often cannot install Essentia bindings. Use the normal librosa/LUFS analysis on Windows, or run the same script in WSL/Linux when Essentia descriptors are needed. A typical WSL call looks like:

```powershell
wsl.exe -d Ubuntu -- /path/to/venv/bin/python "/mnt/c/path/to/skills/band-sound-aimpoint/scripts/analyze_reference_audio.py" "/mnt/c/path/to/audio.wav" --essentia --pretty
```

## Related Skills

- Use `reaper-session-automation` for REAPER staging, snippet renders, and session-state reports.
- Use `mix-render-diagnostics` for rendered-audio diagnostics and candidate ranking after trustworthy files exist.
- Use `live-worship-mix-engineering` for section diagnosis, plugin-chain judgment, and next-move selection after the aimpoint or taste rule is known.
- Use `waves-live-plugin-chains` when the aimpoint needs to become Waves plugin-chain choices.
- Use `superrack-session-files` only after an approved candidate needs to move into a Waves SuperRack session file.
