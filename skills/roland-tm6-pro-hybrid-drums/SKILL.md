---
name: roland-tm6-pro-hybrid-drums
description: Choose Roland TM-6 PRO hybrid drum sounds, trigger roles, blend levels, gate-keying strategy, and live-safety settings for worship, church livestream, and live band contexts. Use when recommending kick, snare, floor tom, pad, sample-layer, TM-6 Pro kit, trigger blend, transient, EQ, compressor, decay, tuning, output, crosstalk, gate-key, or Sunday-safe choices against a worship mix aimpoint or drum reinforcement goal.
---

# Roland TM-6 PRO Hybrid Drums

## Purpose

Use this skill to choose practical TM-6 PRO trigger layers that support acoustic drums without making the kit feel fake, disconnected, or distracting. Anchor recommendations to the active worship aimpoint, the actual drum being triggered, and the deployment path: room, livestream, recording, or all three.

Treat the TM-6 PRO as a source-shaping tool. Recommend sounds by role first, then translate the role into module choices, blend level, tuning, decay, transient shape, and safety checks.

## Operating Rules

1. Preserve the acoustic kit as the primary instrument unless the user explicitly wants sample-forward hybrid drums.
2. Recommend trigger layers by musical job: sub weight, beater attack, snare body, snare crack, tom note, sustain, or effect.
3. Tie every choice to the aimpoint: natural congregational, modern arena, ambient/spontaneous, track-heavy pop, gospel-influenced, or local hybrid.
4. Start with lower sample levels than feel exciting in headphones. In worship mixes, the best trigger layer is often felt before it is identified.
5. Prefer short, controlled sounds for live rooms and longer, polished sounds for stream-only or recording paths.
6. Use exact TM-6 PRO instrument names only when the user provides a Data List, kit backup, screenshots, or on-device sound names. Otherwise recommend sound families and audition criteria.
7. Do not let the trigger layer fight bass guitar, keys left hand, tracks, vocal intelligibility, or congregational naturalness.
8. Check false triggers, missed hits, crosstalk, machine-gun effect, mono translation, and room/stream balance before approving a sound.
9. Keep user taste calls in `band-sound-aimpoint`, not in this skill. Consume aimpoint and taste rules from that skill when available.
10. Hand rendered-audio analysis to `mix-render-diagnostics`, practical mix moves to `live-worship-mix-engineering`, and WING routing questions to `behringer-wing-snap`.

## Workflow

1. Identify context:
   - Triggered drums: kick, snare, floor tom, or other pads.
   - Aimpoint and style family.
   - Deployment path: FOH only, livestream only, shared room/stream, recording, or virtual soundcheck.
   - Existing acoustic drum tone, mic capture, drummer dynamics, and stage volume.

2. Choose the trigger job:
   - Kick: low-end weight, beater definition, consistent punch, or special effect.
   - Snare: body, crack, rimshot consistency, clap/electronic layer, or gated modern punch.
   - Floor tom: note reinforcement, low sustain, cinematic hit, or decay control.

3. Select the sound family:
   - For exact on-device sound names, ask for a TM-6 PRO Data List excerpt, screen photo, kit backup notes, or the names the user is auditioning.
   - Without exact names, recommend a category such as tight acoustic kick, short modern kick, deep wood snare body, compressed snare crack, low acoustic floor tom, or cinematic low tom.
   - Avoid recommending full wet/effected sounds as a default layer under acoustic drums unless the aimpoint is intentionally sample-forward.

4. Set initial module moves:
   - Start blend quietly, then raise until the drum becomes consistent and emotionally right.
   - Tune to the drum and song key only when the layer has clear pitch or long sustain.
   - Shorten decay before cutting fader when the layer muddies the groove.
   - Use transient attack for definition and release/decay for cleanliness.
   - Keep pad EQ and compression subtle unless using direct outputs or stream-only processing.

5. Validate in the real path:
   - Test soft, normal, and hard hits.
   - Test fills and fast doubles.
   - Test kick with bass guitar and low keys.
   - Test snare under lead vocal and BGVs.
   - Test floor tom in big choruses and bridge builds.
   - Confirm the sample disappears naturally when muted or lowered; if the mix collapses, it is doing too much.

6. Return an actionable recommendation:

```yaml
drum: kick
aimpoint: modern worship, supportive but polished
trigger_job: add low-end consistency and controlled beater definition
sound_family: tight modern acoustic kick with short sub tail
initial_blend: felt-under-acoustic, usually about -15 to -9 dB relative to the close mic
tm6_moves:
  pitch: tune to the acoustic kick, avoid obvious note unless song needs it
  decay: short to medium-short
  transient: add attack only until bass/guitar timing reads clearly
  eq: trim low-mid box before adding more sub
safety_checks:
  - check kick/bass masking in full chorus
  - verify no double-triggering on fast patterns
  - mute the layer and confirm the acoustic kit still feels believable
confidence: medium
next_test: audition two tighter kicks and one warmer kick at equal blend in the same song section
```

## Reference Selection

- Read `references/worship-aimpoint-to-trigger-map.md` when the user names a style, artist direction, service type, or mix aimpoint.
- Read `references/kick-trigger-roles.md` for kick drum trigger choices.
- Read `references/snare-trigger-roles.md` for snare trigger choices.
- Read `references/floor-tom-trigger-roles.md` for floor tom trigger choices.
- Read `references/live-trigger-safety-checks.md` before approving a setup for rehearsal, Sunday, livestream, or recording use.

## TM-6 PRO Notes

The TM-6 PRO supports built-in V-Drums instruments, preloaded one-shot samples, user WAV import, pad-level EQ/transient/compression/MFX, master processing, direct outputs, USB audio, and six trigger inputs. Use these as practical constraints: the module can layer and shape sounds, but the right choice still depends on the acoustic drum, song section, room, and aimpoint.

When the user needs exact button-by-button operation, refer them to the Roland TM-6 PRO Reference Manual or ask for photos of the relevant screens. This skill should focus on what sound to choose and why, then give enough parameter direction to audition quickly.
