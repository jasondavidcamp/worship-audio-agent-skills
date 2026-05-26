# Congregational Arrangement Aimpoints

Use this when the aimpoint depends on singability, key/tempo, band size, tracks/stems, arrangement density, or whether the congregation should feel invited rather than impressed.

Mined from public sources:

- CityAlight About: https://cityalight.com/about/
- WorshipFuel/CCLI, Getting Started with Multitracks in Worship: https://www.worshipfuel.com/equip/getting-started-with-multitracks-in-worship/
- PraiseCharts, Top MultiTracks for Your Worship Team: https://www.praisecharts.com/song-lists/top-multi-tracks
- CCLI/CCS Pocket Guide to Copyright Licenses for Churches: https://www.worshipfuel.com/wp-content/uploads/2023/06/pocket-guide-ccli-ccs-r2.pdf
- Church Production, Mixing Techniques: https://www.churchproduction.com/education/mixing_techniques/

## First Principle

An aimpoint is not only tone. It is also how easy the song feels to join. A mix can sound impressive and still fail the congregation if the melody, lyric, arrangement, or production density feels out of reach.

## Arrangement Density Scale

Sparse:

- Voice plus piano/acoustic/pad.
- Best for prayer, response, scripture-heavy songs, and exposed lyrics.
- Mix target: intimate, clear, no distracting ambience or low-mid bloom.

Small band:

- Vocal, acoustic/piano, bass, light drums/cajon, simple keys.
- Best for local-church singability and flexible teams.
- Mix target: melody-forward, supportive rhythm, no attempt to fake arena scale.

Full band:

- Drums, bass, guitars, keys, BGVs, possible tracks.
- Best for medium/high energy and section lift.
- Mix target: vocal still leads; band density supports without crowding.

Track-heavy:

- Loops, synths, stems, programmed elements, click/cues, and possibly missing live parts.
- Best when the team rehearses with tracks and the congregation accepts the production feel.
- Mix target: tracks fill holes without replacing local leadership.

Choir/BGV-heavy:

- BGVs, choir, gang vocals, call-and-response.
- Best for congregational invitation and emotional support.
- Mix target: lead lyric remains primary; group vocals tell the congregation when to sing.

## Singability Checks

Before adopting a reference target, ask:

- Is the melody easy for non-musicians to follow?
- Is the range comfortable for the congregation after transposition?
- Does the arrangement give the congregation clear entrances?
- Is the chorus memorable without the record's production layers?
- Does the band need tracks to carry the hook or can live musicians carry it?
- Are repeats, tags, or bridges worshipful for this church or just copied from the recording?
- Does the energy serve congregational singing or turn the moment into a performance?

## Tracks And Stems

Use multitracks/stems as arrangement tools, not as automatic polish.

Helpful uses:

- Fill missing parts when the local band is small.
- Provide click/cues and tempo stability.
- Add pads, simple loops, or production details that support the live team.
- Rehearse with isolated parts or customized arrangements.

Risks:

- Arrangement becomes too large for the congregation.
- Volunteers cannot balance tracks against live musicians.
- The track carries the emotional lift while the local team feels secondary.
- The mix becomes stereo-width dependent and fails mono or livestream translation.
- Copyright/licensing assumptions are wrong.

## Copyright And Public Skill Boundary

Do not store copyrighted reference audio, stems, lyrics, or purchased track analysis inside a public skill repository.

In a private deployment, store only the derived observations needed for future decisions:

- Style family.
- Section role.
- Instrumental density.
- Vocal relationship.
- Low-end/top-end/depth notes.
- User taste calls.

Avoid copying lyrics or detailed proprietary arrangement maps.

## Aimpoint Output

```yaml
arrangement_aimpoint:
  density: sparse | small_band | full_band | track_heavy | choir_bgv_heavy
  congregation_role: lead_singing | response | listening | prayer | celebration
  melody_support: strong | moderate | weak
  track_dependency: none | optional | important | dominant
  risks:
    - "tracks may make local band feel small"
    - "bridge repeats may outlast congregational energy"
  mix_implications:
    - "lead vocal should stay more forward than reference"
    - "keep pads wide but mono-safe"
```
