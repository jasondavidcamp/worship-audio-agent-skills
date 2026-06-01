# Worship Aimpoint To Trigger Map

Use this file when mapping a worship style or aimpoint to TM-6 PRO trigger sound choices.

## Natural Congregational

Goal: reinforce the acoustic kit while preserving the sense that the room is hearing real drums.

- Kick: warm acoustic support, short sub tail, minimal click.
- Snare: low-level body reinforcement or soft crack layer; avoid obvious clap/electronic layers.
- Floor tom: natural tom note with controlled sustain; avoid cinematic booms unless the arrangement calls for it.
- Blend: quiet and almost invisible. The congregation should notice confidence, not electronics.
- Risk: over-polishing the kit until it disconnects from the band and room.

## Modern Arena Worship

Goal: give the kit consistent impact, clean low end, and a polished backbeat that supports big choruses.

- Kick: tight modern acoustic kick, controlled sub weight, moderate beater.
- Snare: body plus crack, possibly a short compressed layer under rimshots.
- Floor tom: deep, tuned low tom with medium sustain for builds.
- Blend: audible enough in the stream to stabilize the groove, still under the acoustic identity.
- Risk: excessive low-end tail causing bus compression or limiter movement.

## Ambient Or Spontaneous

Goal: make drums feel wide, patient, and emotional without crowding pads, verbs, and vocals.

- Kick: soft low support, rounded attack, shorter than expected.
- Snare: warm body or brush-like support; avoid sharp attack unless the song lifts.
- Floor tom: low cinematic support can work, but decay must leave room for pads and vocal reverb.
- Blend: lower than modern arena; automate or switch kits between sparse and big sections.
- Risk: long tom and kick tails smearing time and masking vocal consonants.

## Track-Heavy Pop Worship

Goal: make the acoustic kit lock with loops, tracks, and quantized low-end movement.

- Kick: tighter and more defined, with enough attack to line up with programmed elements.
- Snare: controlled crack/body layer that matches the track backbeat.
- Floor tom: shorter tuned tom, less roomy than natural worship.
- Blend: more present than natural congregational, especially in the livestream.
- Risk: phase and timing mismatch between acoustic mic bleed, trigger sample, and tracks.

## Gospel-Influenced Or High-Energy

Goal: keep fast playing articulate while making backbeats and fills translate.

- Kick: fast recovery, defined attack, little extra decay.
- Snare: crisp crack with body kept controlled; avoid slow samples on busy ghost-note work.
- Floor tom: clear note and attack; avoid long boom that blurs fast fills.
- Blend: dynamic and responsive rather than constantly loud.
- Risk: trigger settings choking nuance or making doubles sound mechanical.

## Hybrid Local Preference

When the church has a known taste rule, use it over generic style maps. For example:

- If the team prefers natural drums, keep samples as reinforcement only.
- If the livestream needs more impact than the room, use direct output or stream-specific gain where routing allows.
- If the drummer plays dynamically, protect the dynamic curve before chasing maximum consistency.

## Output Format

Return recommendations as:

```yaml
aimpoint:
deployment_path:
drum:
trigger_job:
sound_family:
blend_start:
blend_ceiling:
tm6_moves:
safety_checks:
next_test:
```
