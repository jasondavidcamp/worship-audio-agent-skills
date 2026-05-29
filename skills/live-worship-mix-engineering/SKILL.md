---
name: live-worship-mix-engineering
description: Apply and calibrate live worship audio engineering judgment for vocals, band, drums, buses, rooms, and livestream mixes using aimpoints, section-level render metrics, console/DAW-neutral processing, and volunteer-safe mix moves. Use when deciding what mix move to try next, critiquing or grading worship mix candidates, diagnosing why a render feels wrong, interpreting loudness/spectrum/dynamics/mono analysis, improving lyric clarity, warmth, low-mid control, smooth top end, band energy, congregational feel, room-to-stream translation, or choosing practical fader/EQ/dynamics/effects moves without assuming a specific plugin brand.
---

# Live Worship Mix Engineering

## Purpose

Use this skill as the practical engineering layer between source context, section diagnosis, active aimpoints, render metrics, and console/DAW moves. It answers: "Given this source, this aimpoint, and this evidence, what should we try next?"

Taste-call intake, interpretation, and durable preference logging belong to `band-sound-aimpoint`. This skill consumes those aimpoints or preference rules, but does not maintain a separate taste-call memory.

## Core Rules

1. Preserve worship priorities: lyrics first, musical support second, polish third.
2. Classify the failure layer before prescribing: source, arrangement, mix, bus/master, room/system, stage/monitoring, stream/delivery, or service flow.
3. Compare sections, not only whole songs: sparse verse, first chorus, biggest chorus/bridge, outro, and any user-reported problem timestamp.
4. Check source capture, mic technique, gain structure, spill, and feedback margin before adding processing.
5. Prefer small reversible moves that transfer: fader balance, HPF/EQ, dynamics, buses, matrices, reverb/delay, and section automation.
6. Separate FOH, room, stream, and recording decisions whenever the routing allows it.
7. Reject objective failures before subjective comparison: clipping, static/crackle/hash, wrong render bounds, severe loudness drift, phase damage, mono collapse, or lost intelligibility.
8. Hand subjective A/B tradeoffs or durable preference questions to `band-sound-aimpoint`.

## Decision Loop

1. State the aimpoint and deployment path in plain language.
2. Diagnose the current section: dynamics, tonality, mono/center stability, vocal-to-band relationship, routing path, and capture/system context.
3. Name the audible problem concretely before choosing a tool: "lead vocal sits behind piano body," "chorus limiter ducks on kick/bass," "room mics smear stream consonants."
4. Choose the lowest-risk move: cleanup first, control second, polish third.
5. If comparing candidates, loudness-match, use `references/section-analysis.md` and `references/rubric.md`, and apply only the winner.

## Routing Map

- Aimpoint, reference matching, style vocabulary, taste calls, or preference memory: use `band-sound-aimpoint`.
- REAPER staging, render settings, short snippet renders, and session-state reports: use `reaper-session-automation`.
- Render diagnostics, artifact gates, codec/true-peak/crest/mid-side evidence: use `mix-render-diagnostics`.
- Waves/SuperRack-compatible plugin choices: use `waves-live-plugin-chains`; `.sprk` or `.xps` inspection/patching: use `superrack-session-files`.
- Common vocal, band, drum, effects, gate, or master next moves: read `references/next-move-map.md`.
- Scoring, ranking, or "what is weak?": read `references/rubric.md`, `references/section-analysis.md`, and `references/analysis-blind-spots.md`.
- Source capture, mic technique, spill, feedback, inconsistent tone, or hollow speech: read `references/source-capture-and-intelligibility.md`.
- Stream path, room mics, audience mics, FOH/matrix/broadcast workflow, or online translation: read `references/livestream-translation-playbook.md`.
- LUFS, true peak, loudness range, encoder settings, or platform-delivery risk: read `references/livestream-loudness-and-delivery.md`.
- Room, PA, headphones, board recording, stream, or seat-to-seat translation mismatch: read `references/room-system-translation-playbook.md`.
- Stage wash, wedges/IEMs, drummer/cymbals, amps, monitor spill, or gain-before-feedback limits: read `references/stage-volume-monitoring-playbook.md`.
- Filled-room collapse: classify first as room-acoustic change, stage-volume dominance, console balance, or stream-path contamination; then read the room/system, stage/monitoring, livestream, and volunteer-safe playbooks as needed.
- Kick, bass, drums, low keys, tracks, or low-frequency support: read `references/rhythm-section-low-end-playbook.md`.
- Dense, flat, tiring, or lyric-masked arrangements: read `references/arrangement-dynamics-diagnosis.md`.
- Speech/music handoffs, videos, prayers, mute groups, pads, reverbs, snapshots, or service-state flow: read `references/service-flow-transition-playbook.md`.
- Repeatable Sundays, volunteer workflows, virtual soundcheck, team review, and template changes: read `references/volunteer-safe-consistency-playbook.md`.

## Plugin-Specific Paths

Keep this skill brand-neutral. For plugin-specific choices, switch skills:

- Use `waves-live-plugin-chains` for Waves, SuperRack, LV1/SuperRack-compatible, or REAPER-staged Waves chains that must transfer to a live host.
- Use `superrack-session-files` only for SuperRack `.sprk`/`.xps` file inspection, validation, or patching.

## Related Skills

- `band-sound-aimpoint`: define the musical target, interpret taste calls, and maintain deployment-local preference rules.
- `reaper-session-automation`: stage plugins, manage render settings, and produce trustworthy REAPER snippets or session reports.
- `mix-render-diagnostics`: analyze rendered candidates and compare measured results after trustworthy files exist.
- `waves-live-plugin-chains`: choose Waves plugin chains when Waves/SuperRack is part of the actual workflow.
- `superrack-session-files`: inspect or patch SuperRack sessions and `.xps` rack presets.
- `behringer-wing-snap`: bring WING routing/topology back into scope for church deployment.
