---
name: live-worship-mix-engineering
description: Apply and calibrate live worship audio engineering judgment for vocals, band, drums, buses, rooms, and livestream mixes using aimpoints, section-level render metrics, taste calls, console/DAW-neutral processing, and volunteer-safe mix moves. Use when deciding what mix move to try next, critiquing or grading worship mix candidates, diagnosing why a render feels wrong, interpreting loudness/spectrum/dynamics/mono analysis, improving lyric clarity, warmth, low-mid control, smooth top end, band energy, congregational feel, room-to-stream translation, or choosing practical fader/EQ/dynamics/effects moves without assuming a specific plugin brand.
---

# Live Worship Mix Engineering

## Purpose

Use this skill as the judgment and calibration layer between measured audio data, listening impressions, taste calls, and plugin moves. It should answer: "Given this source, this aimpoint, these render metrics, and what the user prefers, what should we try next?"

## Operating Rules

1. Preserve worship priorities: lyrics first, musical support second, polish third.
2. Favor small reversible moves before large chain changes.
3. Use metrics to diagnose direction, not to overrule taste calls.
4. Loudness-match before judging tonal changes.
5. Prefer moves that transfer across common church systems: fader balance, gain staging, HPF/EQ, dynamics, buses, matrices, reverb/delay, and section automation.
6. Avoid stacking processors just because they are respected; every plugin must have a job.
7. Check source capture before processing when the issue is intelligibility, feedback, inconsistent tone, spill, or hollow speech.
8. For livestreams, treat FOH, aux/matrix stream, remote mix, and dedicated broadcast as different workflows with different tradeoffs.
9. When testing processing choices in a DAW, use `reaper-render-reference` and rank candidates before recommending final settings.
10. When the user specifically wants Waves plugin choices, switch to `waves-live-plugin-chains`; when patching or validating SuperRack session files, switch to `superrack-session-files`.
11. Compare sections, not only whole songs: sparse verse, first chorus, biggest chorus/bridge, outro, and any user-reported problem timestamp.
12. Separate diagnosis from prescription: name the audible problem before choosing a plugin or fader move.
13. Preserve mono clarity when the deployment is mono-first.
14. Log user taste calls as reusable calibration data when they change future decisions.
15. Treat room/system, stage volume, monitoring, arrangement, and service-flow causes as first-class diagnoses, not excuses to add processing.
16. When the same issue changes between room, board recording, and stream, identify the translation layer before prescribing mix moves.

## Decision Loop

1. State the aimpoint in plain language:
   - Example: "Natural worship vocal: lyric-forward, warm but clear, controlled, smooth top."

2. Diagnose the current render by section:
   - Dynamics: crest factor, RMS/LUFS, short-window range.
   - Tonality: sub/low/body/low-mid/presence/edge/air relative to dry or reference.
   - Mono compatibility and center stability when relevant.
   - Vocal-to-band and drum-to-band relationship when stems or buses are available.
   - Function: lead vocal, BGV, band bus, drum bus, livestream bus, mains.
   - Capture, system, and service context: microphone technique, stage volume, monitor/IEM method, open mics, PA/room behavior, FOH/stream split, room mics, broadcast delivery path, and speech/playback transition needs.

3. Write a perceptual diagnosis:
   - Use concrete language: "lead vocal sits behind piano body," "chorus does not lift," "snare peak is exciting but detached."
   - Avoid vague labels like "muddy" unless the source, frequency region, and musical consequence are named.
   - Read `references/analysis-blind-spots.md` before trusting a grade or metric-driven conclusion.

4. Choose the lowest-risk move:
   - Cleanup first: HPF, corrective EQ, bleed/spill reduction, and low-mid control.
   - Control second: compression, expansion, gates, or multiband only where needed.
   - Polish third: saturation, exciter, width, reverb/delay.
   - Tuning only when appropriate and verified.
   - Use `references/next-move-map.md` when a common diagnosis needs a targeted next move.
   - Use the focused playbooks below when the problem is source capture, volunteer consistency, livestream translation, target hierarchy, delivery loudness, room/system translation, stage/monitor spill, rhythm-section foundation, arrangement dynamics, or service-flow transitions.

5. Render and compare:
   - Keep candidate names meaningful.
   - Grade for the aimpoint and write a plain-English read, not just a score.
   - Use `references/rubric.md` and `references/section-analysis.md` when the user asks for ranking, scoring, or "what is weak?"
   - Reject objective failures before asking for taste: clipping, static/crackle/hash, wrong render bounds, severe loudness drift, phase damage, or lost intelligibility.

6. Apply only the winner:
   - Keep runner-up renders for taste calls.
   - Record taste calls in the deployment's local aimpoint/taste log when the user's reaction should guide future work.

## Common Diagnoses

- Clear but sharp: reduce dynamic presence/edge before cutting static high shelf; try de-essing or dynamic EQ before dulling the whole vocal.
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

Use `references/source-capture-and-intelligibility.md` when the issue may come from microphone choice, placement, handling, stage volume, feedback, off-axis spill, or inconsistent speech/vocal tone.

Use `references/volunteer-safe-consistency-playbook.md` when the task involves repeatable Sundays, volunteer operators, soundcheck routines, virtual soundcheck, team review, or low-risk console-neutral starting points.

Use `references/livestream-translation-playbook.md` when moving between room sound and online sound, choosing FOH/matrix/aux/broadcast workflows, using audience mics, or diagnosing a thin, dead, washy, or inconsistent stream.

Use `references/target-mix-hierarchy.md` when translating worship priorities into a practical fader/attention hierarchy for FOH, stream, vocals, band, BGVs, and low end.

Use `references/livestream-loudness-and-delivery.md` when checking LUFS, true peak, loudness range, encoder audio settings, or platform-delivery risk.

Use `references/room-system-translation-playbook.md` when a problem changes between headphones, board recording, stream, and the room, or when PA coverage, feedback margin, room modes, or system EQ may be driving the result.

Use `references/stage-volume-monitoring-playbook.md` when wedge/IEM choices, monitor requests, backline, drum/cymbal spill, or acoustic stage level may be limiting FOH clarity, stream balance, or performer confidence.

Use `references/rhythm-section-low-end-playbook.md` when kick, bass, drums, and low-frequency support need to lock together without masking the vocal or collapsing on stream/small speakers.

Use `references/arrangement-dynamics-diagnosis.md` when the mix feels dense, flat, tiring, or lyric-masked because parts, ranges, or section dynamics are competing before the console can solve it.

Use `references/service-flow-transition-playbook.md` when diagnosing speech/music handoffs, video playback, prayers, pastor mics, mute groups, reverbs, pads, cues, or snapshot flow across a full service.

Public training material can teach techniques, plugin roles, and vocabulary. User taste calls decide how far to push vocal level, tuning, compression, ambience, drum energy, and mono-first compromises for the actual church.

## Plugin-Specific Paths

Keep this skill brand-neutral. For plugin-specific choices, switch skills:

- Use `waves-live-plugin-chains` for Waves, SuperRack, LV1, MultiRack, or REAPER-hosted Waves chains.
- Use `superrack-session-files` only for SuperRack `.sprk`/`.xps` file inspection, validation, or patching.

## Related Skills

- `band-sound-aimpoint`: define and analyze the musical target.
- `reaper-render-reference`: stage plugins, render candidates, analyze/rank results.
- `waves-live-plugin-chains`: choose Waves plugin chains when Waves/SuperRack is part of the actual workflow.
- `superrack-session-files`: inspect or patch SuperRack sessions and `.xps` rack presets.
- `behringer-wing-snap`: bring WING routing/topology back into scope for church deployment.
