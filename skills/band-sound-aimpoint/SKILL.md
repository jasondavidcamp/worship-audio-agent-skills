---
name: band-sound-aimpoint
description: Define, analyze, calibrate, and apply a target sound for church band mixes using reference tracks, user taste calls, and style vocabulary such as CityAlight-style naturalness. Use when comparing band, livestream, vocal, drum, or full-mix renders against a desired style/feel; creating mix aimpoints; describing tonal balance, dynamics, arrangement density, worship-band aesthetic, congregational clarity, reference-track matching, taste preferences, or emotional mix goals; or guiding REAPER/SuperRack plugin iteration toward a known target.
---

# Band Sound Aimpoint

## Purpose

Use this skill to keep mix decisions anchored to a named musical target instead of isolated plugin tweaks. Combine subjective language, reference-track evidence, objective metrics, and the user's taste history so Codex can make better engineering recommendations before asking for more taste calls.

## Operating Rules

1. Treat references as aimpoints, not templates to clone exactly.
2. Separate the musical goal from the measurement: name the feel first, then use metrics to check whether a candidate moved toward or away from it.
3. Loudness-match before judging tonal balance.
4. Compare similar sections when possible: intro to intro, full chorus to full chorus, sparse verse to sparse verse.
5. Preserve congregational priorities: lyric intelligibility, stable lead vocal, supportive band energy, and low fatigue matter more than record-polish alone.
6. Use copyrighted reference audio only for private analysis. Do not copy it into skill folders or generated deliverables.
7. Treat user taste calls as stronger calibration than public reference matching when they conflict.
8. Convert repeated user reactions into durable rules in the local/private taste-call log for the deployment.

## Workflow

1. Identify the aimpoint:
   - Reference track path(s).
   - Target section(s): full chorus, down verse, bridge, outro, or whole track.
   - Desired application: livestream mix, vocal bus, band bus, drum bus, mains, or rehearsal/studio render.

2. Build a qualitative profile:
   - Energy: restrained, driving, intimate, celebratory, wide, dry, roomy, polished, raw.
   - Vocal relationship: lead-forward, blended, gang-vocal, congregational.
   - Band relationship: acoustic-led, piano-led, drum-led, guitar-led, dense/full, open/sparse.
   - Low-end stance: warm/supportive, tight/controlled, modern/sub-heavy, light.
   - Top-end stance: smooth, airy, bright, aggressive, dark.

3. Analyze the reference:
   - Use `scripts/analyze_reference_audio.py` for loudness, peak/RMS, crest factor, section-level energy, and broad frequency bands.
   - Add `--essentia` when Essentia Python bindings are available and tonal/rhythm/spectral descriptors would help compare the aimpoint.
   - Save or update a reference profile in `references/`.

4. Compare our render:
   - Render the same kind of section from REAPER or another source.
   - Loudness-match our render to the reference before judging tone.
   - Compare broad bands and dynamics, then write an engineering interpretation.

5. Turn analysis into moves:
   - Recommend small, reversible changes first.
   - Tie each suggestion to the aimpoint: "more lead-forward," "less low-mid cloud," "more acoustic transient," "less cymbal edge."
   - When plugin iteration is needed, use `reaper-render-reference`.

6. Capture taste feedback:
   - Ask for small A/B taste calls when two candidates trade clarity, warmth, vocal pocket, BGV blend, ambience, or band energy.
   - Read the deployment's private taste-call log before interpreting a taste call when one exists.
   - Convert the user's reaction into a reusable rule, not just a one-off note.
   - Let `live-worship-mix-engineering` handle detailed grading, diagnosis, and plugin-chain moves.

## Calibration Sources

Use public internet or training sources for general mix principles, plugin roles, worship-mix workflows, reference vocabulary, arrangement expectations, and before/after decision patterns.

Use the user's direct taste calls for the church's acceptable vocal level, BGV blend, vocal processing amount, ambience depth, drum/band energy, mono deployment priorities, and whether CityAlight, Bethel, Churchfront, or a local hybrid should dominate a decision.

## Reference Files

- Read or update `references/aimpoint-vocabulary.md` when the user describes taste preferences.
- Read `references/training-intake.md` when deciding whether outside material is useful for aimpoint calibration or whether the question requires a user taste call.
- Add private reference profiles under `references/` only when the user has rights to analyze the source material and the repo will remain private.
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

- Use `reaper-render-reference` for REAPER staging, render iteration, and candidate ranking.
- Use `live-worship-mix-engineering` for scoring, section diagnosis, plugin-chain judgment, and next-move selection.
- Use `superrack-sprk` only after an approved candidate needs to move into a Waves SuperRack session.
