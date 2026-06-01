# Snare Trigger Roles

Use this file when choosing a TM-6 PRO snare sound or shaping a snare trigger layer.

## Diagnose The Need

Choose one main job first:

- Body: the snare lacks chest, low-mid note, or authority.
- Crack: the backbeat lacks excitement or disappears in the stream.
- Consistency: rimshots and center hits vary too much for the style.
- Modern punch: the aimpoint needs a compressed, produced backbeat.
- Hybrid color: a clap, electronic layer, or stack is part of the arrangement.

## Sound Families

Deep wood/body layer:

- Use for worship mixes that need authority without obvious sample sound.
- Keep attack moderate and decay controlled.
- Works well under an acoustic snare that already has top-end crack.

Crisp crack layer:

- Use when the backbeat is not cutting through guitars, keys, or room wash.
- Keep body low and attack quick.
- Use carefully under lead vocal; snare crack can steal consonant attention.

Compressed modern snare:

- Use for modern arena or track-heavy worship.
- Choose short-to-medium decay, controlled ring, and stable rimshot impact.
- Avoid huge room tails unless routed stream-only and checked in context.

Clap or electronic stack:

- Use only when the arrangement or reference points there.
- Keep it song/section-specific.
- Blend lower than expected unless the goal is deliberately pop or electronic.

Gated or explosive snare:

- Use for big choruses, transitions, and special moments.
- Avoid as the default layer for verses or prayerful sections.
- Check that reverb tails do not mask worship leaders or BGVs.

## Initial TM-6 Moves

- Tune the body layer to support the acoustic snare note, not fight it.
- Shorten decay if the backbeat clouds the vocal.
- Add transient attack only after choosing the right sample family.
- Use compression to catch inconsistent hits, not flatten all dynamics.
- Consider separate kits or set-list changes for sparse versus big sections.

## Starting Blend

- Natural body support: start very low, often -18 to -12 dB under the snare mic.
- Modern crack/body support: audition around -15 to -9 dB under the snare mic.
- Clap/electronic stack: start low, then raise only if the arrangement clearly asks for it.

## Failure Signs

- The snare feels disconnected from the drummer's hands.
- Ghost notes become too loud or too identical.
- Lead vocal intelligibility drops on backbeats.
- The snare feels exciting in solo but abrasive in the full band.
- Rimshots trigger huge layers while normal hits vanish, or the reverse.

## Quick Recommendation Templates

Natural worship:

```yaml
trigger_job: add snare body without changing identity
sound_family: deep acoustic body layer
blend_start: very low under close snare
tm6_moves: short decay, low transient, gentle EQ cleanup
```

Modern worship:

```yaml
trigger_job: stabilize backbeat impact
sound_family: compressed acoustic snare with body and crack
blend_start: low-to-moderate under close snare
tm6_moves: tune body, control ring, moderate transient attack
```

Hybrid pop:

```yaml
trigger_job: add arrangement-specific color
sound_family: clap or electronic stack paired with acoustic snare
blend_start: low in verses, more intentional in choruses
tm6_moves: short decay, section-specific kit, check with tracks
```
