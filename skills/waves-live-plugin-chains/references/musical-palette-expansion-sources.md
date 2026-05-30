# Musical Palette Expansion Sources

Use this after `superrack-live-eligibility-gate.md`. The truth gate answers whether a plugin can survive the target Waves/SuperRack path; this file helps decide why an experienced live engineer might try it on a source.

## Source Classes

1. FOH live-chain articles:
   - Examples: Waves FOH engineer chain articles such as Sean Sullivan and John Cooper.
   - Use for instrument-to-plugin norms and topology ideas: vocal cleanup/control, drum gating/EQ/compression, bass control/translation, guitar/keys shaping, bus glue, and master/output posture.
   - Treat named chains as inspiration, not presets. Re-check modern SuperRack support, latency, component format, and artifact risk before recommending them.

2. Church and worship case studies:
   - Examples: Waves houses-of-worship stories, Vox Church livestream SuperRack workflow, Saddleback SoundGrid/MultiRack workflows, and comparable church-production case studies.
   - Use for worship-specific weighting: lyric clarity, stage bleed control, stream translation, volunteer-safe recall, and avoiding source hype that fights congregational clarity.
   - Give these more weight than generic studio advice when the target is church livestream, FOH, monitors, or broadcast.

3. Plugin product pages and manuals:
   - Examples: F6, Bass Rider, Vocal Rider, MaxxBass, RBass, Sibilance, C6/C4, CLA-2A, CLA-76, API 2500, H-Delay, H-Reverb, WLM Plus.
   - Use for first-pass settings, parameter intent, mode/component cautions, and "what problem is this plugin built to solve?"
   - Manuals and product pages do not override the truth gate. They explain musical purpose and control behavior, not final deployability.

## Palette Expansion Rules

- Build source palettes in this order: diagnosis, source type, worship aimpoint, prior local wins, FOH/church examples, plugin manual intent, then render evidence.
- For 20+ pass iterations, include at least one candidate from each relevant family before narrowing: cleanup/EQ, dynamics/control, channel strip/color, translation, harmonic color, and bus/output safety.
- Do not copy an engineer's whole chain unless the source, host, format, and aimpoint match. Extract the role instead: "dynamic vocal harshness control," "bass small-speaker translation," "snare transient control," "band-bus glue."
- When a case study uses legacy MultiRack or an older plugin version, translate the idea to current SuperRack-compatible components instead of assuming the exact setup is still deployable.
- Prefer source-native fixes before bus fixes. FOH chains often include buses and master processing; for iteration on one instrument, use the bus idea only if the task explicitly includes that bus.
- For worship and church production, reject moves that improve solo tone but reduce lyric intelligibility, mono stability, headroom, or smoothness over a long service.

## Source-To-Plugin Norms To Mine

Lead vocal:
- Bleed/noise: Primary Source Expander or careful C1.
- Corrective tone: F6, Q10, SSL/EV2, C6 when dynamic.
- Control: R-Vox/RComp for simple control; CLA-76/CLA-2A pair or one of them for more character; Vocal Rider only when phrasing survives.
- Cleanup/polish: Sibilance/DeEsser, Waves Tune Real-Time when key/scale are known, Silk Vocal Live only when the live component is suitable.
- Space: H-Delay, RVerb/H-Reverb/plates on sends or FX returns.

Bass:
- Leveling: RComp, CLA-2A, CLA-76, Bass Rider Live when latency and phrasing are acceptable.
- Tone/pocket: F6, SSL/EV2, C6/C4 for dynamic low-mid control.
- Translation: RBass or MaxxBass when small speakers need help; Submarine only as a guarded stress test.
- Color: PuigTec, SSL/CLA MixHub/API style, light tape only after headroom and clarity survive.

Drums:
- Bleed/gating: PSE/C1 first; InTrigger only when reinforcement is musically accepted.
- Kick/snare/toms: F6/Q10/SSL/API EQ, CLA-76/RComp/API 2500 for control, Smack Attack when transient shape is the actual problem.
- Overheads: F6/C6/Q10 for harshness/wash; avoid broad brightening or widening by default.
- Drum bus: F6 cleanup before SSL/API/RComp glue; saturation only after cymbal-hash checks.

Guitars, piano, keys, and pads:
- Acoustic: F6/Q10/SSL for boom/quack/harshness; light RComp/CLA-2A when strums jump.
- Electric: F6/Q10/SSL/API for harshness and low-mid crowding; CLA-76/RComp lightly when parts jump.
- Piano/keys/pads: F6/C6/Q10/GEQ/SSL for vocal pocketing and low-mid buildup; avoid wide enhancers when mono and lyric clarity matter.

Speech, pastor, crowd, and room mics:
- Speech: F6/Q10/PSE/C1, R-Vox/RComp/MV2, WLM/L2 only as output or broadcast guards.
- Crowd/room: HPF, F6/SSL-style cleanup, gentle ducking/pocketing; avoid aggressive restoration unless the path is broadcast-only and verified.

Buses and stream:
- Band/drum buses: F6/C6 pocketing before API 2500/SSL/RComp/CLA MixHub glue.
- Livestream/output: WLM Plus for measurement, L2/L3-LL/L4 for protection, MV2 only for specific low-level detail problems.
- Reverbs/delays: choose H-Delay, SuperTap, RVerb, H-Reverb, IR-Live, or plates based on send/return topology, CPU, tails, and service flow.

## Source Links To Revisit

- Waves FOH live-chain articles: <https://www.waves.com/foh-sean-sullivan-live-chains>, <https://www.waves.com/foh-john-cooper-live-chains>
- Waves houses of worship: <https://www.waves.com/houses-of-worship>
- Vox Church SuperRack livestream story: <https://www.waves.com/vox-church-streams-live-audio-waves-superrack>
- Saddleback SoundGrid/MultiRack story: <https://www.waves.com/saddleback-church-chooses-multirack-soundgrid>
- Plugin pages and manuals: <https://www.waves.com/plugins>, <https://www.waves.com/downloads/manuals>
