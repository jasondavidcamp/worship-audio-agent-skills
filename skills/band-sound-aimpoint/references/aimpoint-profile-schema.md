# Aimpoint Profile Schema

Use this when creating a reusable profile for a reference track, artist family, user taste target, or local church mix identity.

Mined from public sources:

- Sonarworks, Mixing and Mastering with Reference Tracks: https://www.sonarworks.com/blog/learn/mixing-and-mastering-with-reference-tracks
- Mastering.com, How to use references like a pro mixing engineer: https://mastering.com/mixing-with-reference-tracks/
- iZotope Tonal Balance Control 3: https://www.izotope.com/products/tonal-balance-control
- iZotope, 10 reference tracks you should be using for mixing: https://www.izotope.com/community/blog/mixing-reference-tracks

## First Principle

Profile the reference as a set of observations, not a score. The same tonal balance can be excellent for one style family and wrong for another.

## Required Fields

```yaml
aimpoint_profile:
  label: ""
  source_type: artist_track | live_album | local_mix | stem | user_taste | style_family | negative_reference
  rights_boundary: public_summary | private_analysis | do_not_store
  style_family: natural_congregational | acoustic_folk | modern_arena | ambient_spontaneous | track_heavy_pop | gospel_influenced | hybrid
  role: primary_target | feature_target | translation_check | negative_reference
  deployment: room | livestream | mono_room | stereo_room | broadcast | rehearsal | render_test
  section:
    name: verse | chorus | bridge | outro | whole_song | custom
    time_range: ""
  qualitative:
    energy: restrained | intimate | driving | celebratory | anthemic | contemplative
    vocal_relationship: lead_forward | blended | gang_vocal | choir_supported | distant
    band_relationship: acoustic_led | piano_led | drum_led | guitar_led | keys_tracks_led | balanced
    low_end_stance: light | warm_supportive | tight_controlled | modern_sub_heavy
    top_end_stance: dark | smooth | airy | bright | aggressive
    depth: dry_close | natural_room | ambient | big_room
    width: mono_safe | modest | wide | width_dependent
  objective:
    integrated_loudness: unknown
    short_term_loudness: unknown
    peak_or_true_peak: unknown
    crest_factor: unknown
    broad_bands: unknown
    stereo_width: unknown
    vocal_balance: unknown
    section_lift: unknown
  emulate:
    - ""
  avoid:
    - ""
  taste_calls:
    - ""
```

## Objective Dimensions

Use metrics as descriptive evidence:

- Tonal balance: sub, bass, low mids, mids, presence, brilliance.
- Dynamics: RMS/LUFS, crest factor, loudness range, section lift.
- Vocal balance: lead vocal relative to band and BGVs.
- Low-end relationship: kick/bass role and consistency.
- Stereo width: what creates width and whether it survives mono.
- Depth: close/dry sources versus distant/ambient sources.
- Section shape: how much bigger chorus/bridge feels than verse.

Do not say "the reference is better because the curve is flatter." Say what the curve implies musically.

## Comparison Notes

When comparing a candidate render to a profile:

```yaml
comparison:
  matched_section: true
  loudness_matched: true
  moved_toward:
    - "lead vocal warmth"
  moved_away:
    - "chorus lift"
  likely_cause:
    - "piano low-mid density masking vocal body"
  next_move:
    - "reduce piano/acoustic low-mid buildup before adding vocal top"
```

## Private Vs Public Storage

Public repo:

- Store source links and generic style notes.
- Store schemas and workflows.
- Do not store copyrighted audio, lyrics, purchased stem details, or proprietary track maps.

Private deployment:

- Store user taste calls.
- Store derived measurements from legally accessible references.
- Store local church target profiles.
- Keep file paths and license-sensitive details private.

## Skill Behavior

When the user asks to "make it sound like X," create or read an aimpoint profile before giving mix moves. If the reference is too different, explain which dimensions are usable and which are not.
