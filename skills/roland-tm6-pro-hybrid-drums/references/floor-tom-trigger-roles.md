# Floor Tom Trigger Roles

Use this file when choosing a TM-6 PRO floor tom sound or shaping a tom trigger layer.

## Diagnose The Need

Choose one main job first:

- Note reinforcement: the floor tom lacks clear pitch or size.
- Low sustain: big builds need more emotional weight.
- Attack clarity: fills vanish under guitars, keys, pads, or crowd sound.
- Consistency: the tom changes too much hit-to-hit.
- Cinematic moment: a bridge, intro, or transition needs a larger-than-life low hit.

## Sound Families

Natural low tom:

- Use for most worship reinforcement.
- Choose a clear low note, realistic attack, and medium-short sustain.
- Tune to the acoustic floor tom so the layer feels like one drum.

Controlled modern tom:

- Use for modern arena and track-heavy mixes.
- Choose more attack and shorter sustain than a cinematic layer.
- Works well when fills need to speak through dense arrangements.

Cinematic low tom:

- Use for builds, bridge hits, and sparse emotional moments.
- Keep it section-specific or lower than instinct suggests.
- Shorten release if pads, piano lows, or bass guitar smear.

Low effect hit:

- Use only when the arrangement calls for a special sound.
- Keep out of normal fills unless the song is intentionally hybrid.
- Verify it does not feel surprising in the room.

## Initial TM-6 Moves

- Tune first. Floor tom layers become distracting quickly when they fight the drum note.
- Shorten decay when the song tempo is faster or the arrangement is dense.
- Keep sub content controlled; floor tom can overload the same range as kick and bass.
- Add attack for fill clarity, not for constant aggression.
- Use separate kit versions for big bridge builds versus normal groove sections when useful.

## Starting Blend

- Natural reinforcement: start around -18 to -12 dB under the close tom mic.
- Modern fill clarity: audition around -15 to -9 dB under the close tom mic.
- Cinematic support: automate, use a dedicated kit, or keep lower in FOH than stream.

## Failure Signs

- Fills blur into low-frequency wash.
- The floor tom sounds pitched against the song or acoustic drum.
- Kick, bass, and tom hits make the master bus pump.
- Sparse worship sections feel theatrical when they should feel intimate.
- The tom sample is heard more than the drummer's drum.

## Quick Recommendation Templates

Natural worship:

```yaml
trigger_job: add note and size
sound_family: natural low floor tom
blend_start: very low under close tom
tm6_moves: tune carefully, medium-short decay, minimal attack boost
```

Modern worship:

```yaml
trigger_job: make fills translate in big sections
sound_family: controlled modern low tom
blend_start: low-to-moderate under close tom
tm6_moves: tune to drum, shorten sustain, add mild attack
```

Bridge build:

```yaml
trigger_job: add emotional low impact
sound_family: cinematic low tom or low tom stack
blend_start: section-specific, lower in room than stream if possible
tm6_moves: tune to song/drum, manage tail, check kick/bass interaction
```
