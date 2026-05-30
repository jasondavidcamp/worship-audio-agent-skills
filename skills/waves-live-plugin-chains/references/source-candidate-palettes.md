# Source Candidate Palettes

Use this before Waves multi-pass iteration so the chain search does not collapse into one familiar plugin pair. A palette is not a preset list. It is the set of live-safe plugin roles worth considering for a source, filtered by diagnosis, aimpoint, prior wins, and render evidence.

## Palette Rules

- Start with the audible problem, then choose plugin roles.
- Include any prior approved/exported chain for the same source early in the batch, or state why it does not apply.
- Prefer live-safe, SuperRack-compatible mono/stereo components that match the source format.
- Before recommending or applying a candidate, run the official truth gate in `superrack-live-eligibility-gate.md`: Supported Platforms, Plugin Latency, Channel Components, then SuperRack Support Notes.
- For broad or unfamiliar palette work, use `musical-palette-expansion-sources.md` after the truth gate to add FOH/church/manual-informed candidates.
- Keep each pass role-clear: cleanup, control, color, translation, or keeper refinement.
- Do not use all tools just because they exist. Reject candidates that add latency, artifacts, harshness, pumping, headroom loss, or workflow risk.
- For 5-pass batches, include at least two different topologies unless the user asks for refinement only.
- For 10-20 pass batches, broaden first across plugin families, then refine the best two or three.

## SuperRack Coverage Index

Use this checklist to keep known SuperRack-compatible tools on the table. Appearance here does not mean "use it"; it means "consider it when the diagnosis fits, then apply live eligibility, latency, CPU, format, and artifact gates."

- Expansion/gating: Primary Source Expander, C1 Compressor, C1 Gate.
- Corrective EQ/dynamic EQ: F6 Floating-Band Dynamic EQ, Q10, GEQ, C6, C4.
- Channel strips: SSL E-Channel, SSL G-Channel, SSL EV2 Channel, Scheps Omni Channel, CLA MixHub.
- Musical EQ/color EQ: PuigTec EQP-1A, API EQ, Scheps 73-style color, SSL/API channel EQ.
- Vocal control: Renaissance Vox / R-Vox, Vocal Rider, CLA-2A, CLA-76, RComp, MV2.
- Vocal cleanup/pitch: Sibilance, DeEsser, Waves Tune Real-Time, Silk Vocal Live.
- Bass control/translation: Bass Rider Live, RBass, MaxxBass, Submarine.
- Drum control/reinforcement: Smack Attack, InTrigger Live / InTrigger Drum Replacer, Torque Live, CLA-76, API 2500.
- Bus compression/glue: API 2500, SSL bus-style compression, RComp, CLA MixHub.
- Reverb/space: H-Reverb, RVerb, IR-Live, Abbey Road Plates.
- Delay/throws: H-Delay, SuperTap.
- Harmonic color: J37, Kramer Tape.
- Feedback/phase utilities: X-FDBK, InPhase.
- Output/loudness: L2 Ultramaximizer, L3-LL, L4, WLM Plus.
- Broadcast-only or verify-first cleanup: Clarix LB.

## Batch Shapes

5-pass exploration:

1. Prior winner/current chain if available, or raw/minimal correction.
2. Clean utility chain.
3. Alternate dynamics style.
4. Color/channel-strip or translation topology.
5. Refined keeper from the best direction.

10-pass exploration:

- Add separate passes for F6 vs SSL/API EQ, RComp vs CLA/RVox leveling, dynamic EQ vs static EQ, and optional translation tools.

20-pass exploration:

- Run a real shootout: source cleanup variants, compression families, channel strips, harmonic/translation tools, then 3-5 keeper refinements.

## Bass DI

Common diagnoses: low-mid cloud, uneven notes, thin stream translation, sub/headroom pressure, pitch not reading.

- Cleanup: F6, SSL EV2 Channel, C6/C4 when dynamic low-mid control is needed.
- Control: RComp, CLA-2A, CLA-76, Renaissance Vox / R-Vox only if its simple leveling fits the source; Bass Rider Live when automatic note leveling is worth the latency.
- Color: SSL EV2 Channel, SSL E/G, Scheps Omni Channel, CLA MixHub, API or PuigTec-style tone when natural warmth needs density.
- Translation: RBass, MaxxBass, or Submarine only when small-speaker read is the problem and headroom survives.
- Avoid unless justified: Submarine, heavy saturation, aggressive multiband compression, or enhancer chains that move the limiter more than the bass.
- 5-pass default: prior Bass export/current chain, F6+RComp, SSL EV2-centered, alternate compressor style, refined keeper.

## Lead Vocal

Common diagnoses: buried lyric, inconsistent distance, harshness/sibilance, proximity mud, processed feel.

- Cleanup: PSE for bleed/noise, F6/Q10 for HPF/body/harshness, Sibilance or DeEsser.
- Control: Renaissance Vox / R-Vox, Vocal Rider, RComp, CLA-76, CLA-2A, C6, MV2 when detail needs help.
- Color: SSL EV2, SSL E/G, API, Scheps Omni, CLA MixHub only after clarity and consistency are stable.
- Polish: Waves Tune Real-Time when key/scale are known, Silk Vocal Live for specific harshness/body/air problems, H-Delay/RVerb/H-Reverb/Abbey Road Plates/SuperTap on sends when topology supports it.
- Avoid unless justified: heavy tuning, restoration, wide stereo vocal tricks in a mono-critical live path.
- 5-pass default: current/prior vocal chain, clean F6+RVox/RComp, CLA-style control, de-ess/dynamic EQ focus, keeper refinement.

## BGVs And Choir

Common diagnoses: blend too forward, sibilant stack, inconsistent entries, cloudy harmony pad.

- Cleanup: F6, Sibilance/DeEsser, PSE only if bleed/noise is the real problem.
- Control: RComp, Renaissance Vox / R-Vox, Vocal Rider, C6/C4 for stack control.
- Color: SSL/API bus tone lightly.
- Avoid unless justified: hard gating, aggressive individual compression that destroys blend, stereo widening that hurts mono.

## Spoken/Pastor Mic

Common diagnoses: low intelligibility, proximity boom, plosives, room noise, sudden level jumps.

- Cleanup: F6, Q10, PSE, C1 only when expansion will not chop words.
- Control: RComp, Renaissance Vox / R-Vox, Vocal Rider, MV2, C6 for low-mid/harshness control.
- Safety: L2/L3-LL/L4 limiter guard only after gain structure is sane; WLM Plus for loudness checks.
- Broadcast: Clarix LB only for paths that can tolerate latency and hardware requirements.
- Avoid unless justified: heavy restoration, AI cleanup, lookahead or high-latency tools in live paths.

## Kick

Common diagnoses: lost attack, sub/headroom overload, box, bleed, inconsistent hits.

- Cleanup: PSE/C1 gate, F6/Q10/SSL EV2 for HPF/box/attack.
- Control: RComp, CLA-76, SSL/API-style compression if hits wander.
- Translation: only add sub/low enhancement when PA/stream headroom survives.
- Special tools: Torque Live for pitch correction, InTrigger Live for reinforcement when musically accepted.

## Snare And Toms

Common diagnoses: ring, box, cymbal spill, inconsistent hits, decay too long.

- Cleanup: PSE/C1 for spill, F6/Q10/SSL for ring/body/crack.
- Control: CLA-76/RComp for transient control, Smack Attack only when attack/sustain shape is the actual diagnosis.
- Special tools: Torque Live for tom pitch correction, InTrigger Live for reinforcement when musically accepted.
- Avoid unless justified: over-gating, over-brightening cymbal spill, replacement without taste approval.

## Overheads And Cymbals

Common diagnoses: harsh edge, wash, low-mid smear, cymbal hash.

- Cleanup/control: F6, C6, or Q10 for dynamic harshness, ring, and low-mid wash.
- Color: use sparingly; reject if grain or hash increases.
- Avoid unless justified: broad bright shelves, exciters, widening, heavy compression.

## Acoustic Guitar

Common diagnoses: boom, quack, string harshness, inconsistent strum, vocal masking.

- Cleanup: F6/Q10/SSL for HPF, body pocket, harshness.
- Control: RComp/CLA-2A light leveling.
- Color: SSL/API when the guitar needs density without more level.
- Avoid unless justified: stereo widening, heavy compression that flattens rhythm.

## Electric Guitar

Common diagnoses: harshness, low-mid crowding, thinness, level jumps.

- Cleanup: F6/Q10/SSL/API EQ.
- Control: RComp/CLA-76 lightly if parts jump.
- Color: channel-strip tone or saturation only if it supports the arrangement and does not fight vocal.
- Avoid unless justified: bright exciters, widening that weakens mono.

## Piano, Keys, And Pads

Common diagnoses: vocal masking, low-mid buildup, harsh top, static width.

- Cleanup: F6/C6/Q10/SSL/GEQ for vocal pocketing and low-mid control.
- Control: RComp/API/SSL bus-style light movement only if dynamics need it.
- Color: channel strip lightly when keys feel small or disconnected.
- Avoid unless justified: wide enhancers or heavy compression that makes pads dominate.

## Drum Bus, Band Bus, Livestream Bus

- Drum bus: F6 cleanup before API 2500/SSL/RComp/CLA MixHub glue; reject cymbal hash or flattened lift.
- Band bus: F6/C6 pocketing before API 2500/SSL/CLA MixHub glue; avoid solving source balance with bus processing.
- Livestream bus: WLM Plus for monitoring, F6/C6/MV2 for specific issues, L2/L3-LL/L4 for protection only after source/bus balance is sane.
- FX returns: H-Delay, SuperTap, RVerb, H-Reverb, IR-Live, and Abbey Road Plates are candidates when the host topology supports sends/returns and tails/CPU are safe.
- System utilities: X-FDBK for feedback-prone speech/monitor paths, InPhase for multi-mic phase alignment, GEQ for monitor/PA shaping.
- Color utilities: J37 and Kramer Tape can be tried on buses or special sources only after artifact/headroom checks.
