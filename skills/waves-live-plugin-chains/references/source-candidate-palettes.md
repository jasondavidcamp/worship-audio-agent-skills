# Source Candidate Palettes

Use this before Waves multi-pass iteration so the chain search does not collapse into one familiar plugin pair. A palette is not a preset list. It is the set of live-safe plugin roles worth considering for a source, filtered by diagnosis, aimpoint, prior wins, and render evidence.

## Palette Rules

- Start with the audible problem, then choose plugin roles.
- Include any prior approved/exported chain for the same source early in the batch, or state why it does not apply.
- Prefer live-safe, SuperRack-compatible mono/stereo components that match the source format.
- Keep each pass role-clear: cleanup, control, color, translation, or keeper refinement.
- Do not use all tools just because they exist. Reject candidates that add latency, artifacts, harshness, pumping, headroom loss, or workflow risk.
- For 5-pass batches, include at least two different topologies unless the user asks for refinement only.
- For 10-20 pass batches, broaden first across plugin families, then refine the best two or three.

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
- Control: RComp, CLA-2A, CLA-76, RVox only if its simple leveling fits the source.
- Color: SSL EV2 Channel, API or Scheps-style channel tone when natural warmth needs density.
- Translation: RBass or MaxxBass only when small-speaker read is the problem and headroom survives.
- Avoid unless justified: Submarine, heavy saturation, aggressive multiband compression, or enhancer chains that move the limiter more than the bass.
- 5-pass default: prior Bass export/current chain, F6+RComp, SSL EV2-centered, alternate compressor style, refined keeper.

## Lead Vocal

Common diagnoses: buried lyric, inconsistent distance, harshness/sibilance, proximity mud, processed feel.

- Cleanup: PSE for bleed/noise, F6 for HPF/body/harshness, Sibilance/de-esser.
- Control: RVox, RComp, CLA-76, CLA-2A, C6 for dynamic harshness/body.
- Color: SSL EV2/API/Scheps only after clarity and consistency are stable.
- Polish: short delay/reverb sends, doubler/widening only if mono and lyric clarity survive.
- Avoid unless justified: heavy tuning, restoration, wide stereo vocal tricks in a mono-critical live path.
- 5-pass default: current/prior vocal chain, clean F6+RVox/RComp, CLA-style control, de-ess/dynamic EQ focus, keeper refinement.

## BGVs And Choir

Common diagnoses: blend too forward, sibilant stack, inconsistent entries, cloudy harmony pad.

- Cleanup: F6, Sibilance/de-esser, PSE only if bleed/noise is the real problem.
- Control: RComp, RVox, C6/C4 for stack control.
- Color: SSL/API bus tone lightly.
- Avoid unless justified: hard gating, aggressive individual compression that destroys blend, stereo widening that hurts mono.

## Spoken/Pastor Mic

Common diagnoses: low intelligibility, proximity boom, plosives, room noise, sudden level jumps.

- Cleanup: F6, PSE, C1/EMO-D5 only when expansion will not chop words.
- Control: RComp, RVox, C6 for low-mid/harshness control.
- Safety: limiter/level guard only after gain structure is sane.
- Avoid unless justified: heavy restoration, AI cleanup, lookahead or high-latency tools in live paths.

## Kick

Common diagnoses: lost attack, sub/headroom overload, box, bleed, inconsistent hits.

- Cleanup: PSE/C1 gate, F6/SSL EV2 for HPF/box/attack.
- Control: RComp, CLA-76, SSL/API-style compression if hits wander.
- Translation: only add sub/low enhancement when PA/stream headroom survives.
- Avoid unless justified: InTrigger or replacement unless reinforcement is musically accepted.

## Snare And Toms

Common diagnoses: ring, box, cymbal spill, inconsistent hits, decay too long.

- Cleanup: PSE/C1 for spill, F6/SSL for ring/body/crack.
- Control: CLA-76/RComp for transient control, Smack Attack only when attack/sustain shape is the actual diagnosis.
- Avoid unless justified: over-gating, over-brightening cymbal spill, replacement without taste approval.

## Overheads And Cymbals

Common diagnoses: harsh edge, wash, low-mid smear, cymbal hash.

- Cleanup/control: F6 or C6 dynamic harshness and low-mid wash.
- Color: use sparingly; reject if grain or hash increases.
- Avoid unless justified: broad bright shelves, exciters, widening, heavy compression.

## Acoustic Guitar

Common diagnoses: boom, quack, string harshness, inconsistent strum, vocal masking.

- Cleanup: F6/SSL for HPF, body pocket, harshness.
- Control: RComp/CLA-2A light leveling.
- Color: SSL/API when the guitar needs density without more level.
- Avoid unless justified: stereo widening, heavy compression that flattens rhythm.

## Electric Guitar

Common diagnoses: harshness, low-mid crowding, thinness, level jumps.

- Cleanup: F6/SSL/API EQ.
- Control: RComp/CLA-76 lightly if parts jump.
- Color: channel-strip tone or saturation only if it supports the arrangement and does not fight vocal.
- Avoid unless justified: bright exciters, widening that weakens mono.

## Piano, Keys, And Pads

Common diagnoses: vocal masking, low-mid buildup, harsh top, static width.

- Cleanup: F6/C6/SSL for vocal pocketing and low-mid control.
- Control: RComp/API/SSL bus-style light movement only if dynamics need it.
- Color: channel strip lightly when keys feel small or disconnected.
- Avoid unless justified: wide enhancers or heavy compression that makes pads dominate.

## Drum Bus, Band Bus, Livestream Bus

- Drum bus: F6 cleanup before API/SSL/RComp glue; reject cymbal hash or flattened lift.
- Band bus: F6/C6 pocketing before bus glue; avoid solving source balance with bus processing.
- Livestream bus: WLM for monitoring, F6/C6/MV2 for specific issues, L2/L3-LL/L4 for protection only after source/bus balance is sane.
