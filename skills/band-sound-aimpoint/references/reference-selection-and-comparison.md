# Reference Selection And Comparison

Use this when choosing reference tracks, deciding whether a reference is valid, or comparing a worship mix against a target without chasing the record blindly.

Mined from public sources:

- Sonarworks, Mixing and Mastering with Reference Tracks: https://www.sonarworks.com/blog/learn/mixing-and-mastering-with-reference-tracks
- Mastering.com, How to use references like a pro mixing engineer: https://mastering.com/mixing-with-reference-tracks/
- iZotope, 10 reference tracks you should be using for mixing: https://www.izotope.com/community/blog/mixing-reference-tracks

## First Principle

A reference track is a compass, not a blueprint. It should keep the mix oriented toward a clear emotional and technical target while preserving the actual church, band, room, and congregation.

## Reference Roles

Primary sound target:

- Same worship style family.
- Similar arrangement density and instrumentation.
- Similar vocal role and emotional posture.
- Best for global balance, tone, depth, and section lift.

Secondary feature target:

- Chosen for one trait: vocal warmth, acoustic transient, drum restraint, BGV blend, room energy, low-end posture, or stereo width.
- Do not let it override the primary target.

Translation check:

- A known track that sounds balanced on many systems.
- Useful for sanity-checking low end, harshness, width, and overall tonal tilt.

Negative reference:

- A track or mix the user does not want to emulate.
- Useful for naming taste boundaries: too glossy, too dry, too loud, too ambient, too band-forward, too compressed.

## Selection Checklist

Choose references that match:

- Genre and worship context.
- Arrangement density: solo/piano, acoustic band, full band, track-heavy, choir/BGV-heavy, or arena live.
- Vocal relationship: intimate lead, congregational lead, gang vocal, choir-supported, or production-vocal.
- Energy curve: restrained, gradual build, big bridge, celebratory opener, reflective closer.
- Instrument center: acoustic, piano, drums/bass, electric guitars, synth/pads/tracks, or choir.
- Era and production expectation.
- Delivery context: livestream, room, live album, studio record, rehearsal/stem reference.

Reject or downgrade references when:

- The song is much denser or sparser than the target arrangement.
- The lead vocal role is different from the user's worship goal.
- The reference is mostly a mastering loudness target rather than a mix/arrangement target.
- The user likes the song but not the sound.
- The reference depends on copyrighted stems, tracks, or production layers the local church cannot legally or practically use.

## Comparison Workflow

1. State the reference role.
2. Loudness-match before judging.
3. Compare like sections: verse to verse, chorus to chorus, bridge to bridge.
4. Compare one dimension at a time:
   - Vocal level and emotional placement.
   - Low-end weight and kick/bass relationship.
   - Band density and masking.
   - Brightness, air, cymbal edge, and vocal sibilance.
   - Depth: close vs roomy, dry vs ambient.
   - Width and mono survival.
   - Dynamics and section lift.
5. Write what to emulate, what to ignore, and what is out of reach.

## Worship-Specific Guardrails

- Do not let a polished record make the local mix less singable.
- Do not chase low end that will not translate in the room or stream.
- Do not copy ambience if it pushes lyrics away.
- Do not copy track-heavy width if the church mix is mono-first or volunteer-operated.
- Use the user's taste calls as stronger evidence than the public reference.

## Output Shape

```yaml
reference:
  title_or_label: "artist - song or user label"
  role: primary_target | feature_target | translation_check | negative_reference
  style_family: natural_congregational | acoustic_folk | modern_arena | ambient_spontaneous | track_heavy_pop | gospel_influenced | hybrid
  section: "full chorus"
emulate:
  - "lead vocal clear and warm, not hyped"
  - "drums support without modern-pop sub weight"
ignore:
  - "studio BGV width not practical for mono-first room"
check:
  - vocal_to_band
  - low_end
  - brightness
  - section_lift
```
