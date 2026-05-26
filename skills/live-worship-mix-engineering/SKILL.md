---
name: live-worship-mix-engineering
description: Apply and calibrate live worship audio engineering judgment for vocals, band, drums, buses, and livestream mixes using aimpoints, section-level render metrics, taste calls, REAPER staging, and Waves/SuperRack-safe plugin chains. Use when deciding what mix move to try next, critiquing or grading worship mix candidates, diagnosing why a render feels wrong, interpreting loudness/spectrum/dynamics/mono analysis, choosing serial Waves chains, adapting Worship Sound Guy or Drew Brashler-style live vocal approaches, or balancing lyric clarity, warmth, low-mid control, smooth top end, band energy, and congregational feel.
---

# Live Worship Mix Engineering

## Purpose

Use this skill as the judgment and calibration layer between measured audio data, listening impressions, taste calls, and plugin moves. It should answer: "Given this source, this aimpoint, these render metrics, and what the user prefers, what should we try next?"

## Operating Rules

1. Preserve worship priorities: lyrics first, musical support second, polish third.
2. Favor small reversible moves before large chain changes.
3. Use metrics to diagnose direction, not to overrule taste calls.
4. Loudness-match before judging tonal changes.
5. Prefer live-safe serial Waves chains that can transfer to SuperRack.
6. Avoid stacking processors just because they are respected; every plugin must have a job.
7. When testing plugin choices, use `reaper-render-reference` and rank candidates before recommending final settings.
8. When patching or validating `.sprk` sessions, switch to `superrack-sprk`.
9. Compare sections, not only whole songs: sparse verse, first chorus, biggest chorus/bridge, outro, and any user-reported problem timestamp.
10. Separate diagnosis from prescription: name the audible problem before choosing a plugin or fader move.
11. Preserve mono clarity when the deployment is mono-first.
12. Log user taste calls as reusable calibration data when they change future decisions.

## Decision Loop

1. State the aimpoint in plain language:
   - Example: "CityAlight-style vocal: lyric-forward, warm but clear, controlled, smooth top."

2. Diagnose the current render by section:
   - Dynamics: crest factor, RMS/LUFS, short-window range.
   - Tonality: sub/low/body/low-mid/presence/edge/air relative to dry or reference.
   - Mono compatibility and center stability when relevant.
   - Vocal-to-band and drum-to-band relationship when stems or buses are available.
   - Function: lead vocal, BGV, band bus, drum bus, livestream bus, mains.

3. Write a perceptual diagnosis:
   - Use concrete language: "lead vocal sits behind piano body," "chorus does not lift," "snare peak is exciting but detached."
   - Avoid vague labels like "muddy" unless the source, frequency region, and musical consequence are named.
   - Read `references/analysis-blind-spots.md` before trusting a grade or metric-driven conclusion.

4. Choose the lowest-risk move:
   - Cleanup first: HPF, PSE, low-mid dynamic EQ.
   - Control second: compression/expansion/multiband only where needed.
   - Polish third: saturation, exciter, width, reverb/delay.
   - Tuning only when appropriate and verified.
   - Use `references/next-move-map.md` when a common diagnosis needs a targeted next move.

5. Render and compare:
   - Keep candidate names meaningful.
   - Grade for the aimpoint and write a plain-English read, not just a score.
   - Use `references/rubric.md` and `references/section-analysis.md` when the user asks for ranking, scoring, or "what is weak?"
   - Reject objective failures before asking for taste: clipping, static/crackle/hash, wrong render bounds, severe loudness drift, phase damage, or lost intelligibility.

6. Apply only the winner:
   - Keep runner-up renders for taste calls.
   - Record taste calls in the deployment's private aimpoint/taste log when the user's reaction should guide future work.

## Common Diagnoses

- Clear but sharp: reduce dynamic presence/edge before cutting static high shelf; try de-esser, F6 high band, or gentler smart vocal processing.
- Warm but buried: reduce low-mid masking before boosting top.
- Big but cloudy: HPF/low-band dynamic EQ, then reassess body.
- Smooth but dull: add presence gently; do not over-compress to create excitement.
- Controlled but lifeless: back off compression or restore transient/body.
- Loud but not intelligible: fix mid/presence articulation and arrangement masking instead of only adding level.
- High score but bad taste call: trust the taste call and update the rubric.

## Calibration And Scoring

Use `references/rubric.md` for scoring dimensions and grade shape.

Use `references/section-analysis.md` when choosing comparable song sections.

Use `references/analysis-blind-spots.md` before giving a final grade or trusting a metric-heavy result.

Use `references/next-move-map.md` to translate a diagnosis into one or two targeted moves.

Public training material can teach techniques, plugin roles, and vocabulary. User taste calls decide how far to push vocal level, tuning, compression, ambience, drum energy, and mono-first compromises for the actual church.

## Chain Archetypes

Use `references/waves-superrack-operational-reference.md` for user-provided SuperRack/SoundGrid-oriented latency, live-safety, and decision-rule notes.

Use `references/waves-plugin-decision-matrix.md` for faster source-specific plugin selection after confirming the available Waves plugin catalog.

Use `scripts/inventory_waves_plugins.py` to generate a local installed-plugin catalog after Waves Central installs, license changes, or plugin upgrades. Keep generated inventories private unless they are intentionally sanitized.

## Related Skills

- `band-sound-aimpoint`: define and analyze the musical target.
- `reaper-render-reference`: stage plugins, render candidates, analyze/rank results.
- `superrack-sprk`: inspect or patch SuperRack sessions and `.xps` rack presets.
- `behringer-wing-snap`: bring WING routing/topology back into scope for Church deployment.
