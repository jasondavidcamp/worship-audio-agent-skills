# SuperRack Vocal And Speech Chains

Use this for lead vocals, BGVs/choirs, and spoken-word/pastor mics. Run `superrack-live-eligibility-gate.md` first.

## Source Material Mined

- Waves PSE page: PSE is positioned for reducing mic bleed in live shows.
- Waves F6 page: F6 is a six-band dynamic EQ with per-band dynamics and analyzer features.
- Waves Plugin Latency and Supported Platforms charts: PSE, F6, RVox, CLA-76, CLA-2A, Sibilance, Waves Tune Real-Time, Vocal Rider, Silk Vocal Live, H-Delay, H-Reverb, RVerb, X-FDBK, and WLM/L2 family candidates are SuperRack-compatible with live-mode cautions noted in the gate.
- Waves SuperRack Support Notes: SuperRack SoundGrid does not support MIDI input for plugins that support MIDI control, including Waves Tune Real-Time.

## Lead Vocal Chains

Natural worship vocal, low spill:

1. F6 or SSL E-Channel for HPF, low-mid cleanup, and dynamic presence control.
2. RVox or CLA-2A for simple leveling.
3. Sibilance in live/no-lookahead posture if esses pull attention.
4. H-Delay and RVerb/H-Reverb on an effects return or confirmed SuperRack routing path.

High-spill vocal:

1. Primary Source Expander with conservative range; avoid hard gating.
2. F6 to remove box/harsh resonances raised by compression.
3. RVox for fast control, or CLA-76 into CLA-2A only when the singer needs more density.
4. Sibilance after compression if compression exposes esses.

High-control lead vocal:

1. PSE only if spill is part of the problem.
2. F6 cleanup.
3. CLA-76 for fast peaks, then CLA-2A or RVox for leveling.
4. Sibilance.
5. Silk Vocal Live only if it solves a specific harshness/body/air problem and the live component is confirmed.
6. H-Delay plus filtered reverb. Preserve vocal intelligibility before adding width or lushness.

Tuned live vocal:

1. Waves Tune Real-Time before downstream tone/compression.
2. Use correct key, scale, note transition, and speed before changing EQ.
3. Avoid MIDI-dependent workflows in SuperRack SoundGrid.
4. If artifacts appear, slow correction or bypass tuning before changing the compressor.

## BGV And Choir Chains

Individual BGV with spill:

1. PSE if stage bleed is driving compressor action.
2. F6 or SSL E-Channel for HPF, low-mid cleanup, and de-honk.
3. Light RVox/CLA-2A/RComp-style leveling.
4. Sibilance only if group esses distract.

BGV group:

1. F6 to carve the group under the lead vocal.
2. Gentle bus compression with CLA-2A, RComp, H-Comp, or SSL-style compression only if the group wanders.
3. De-ess the group if stacked consonants draw attention.
4. Keep BGV reverb/delay shorter or lower than lead unless the arrangement needs a choir pad.

Choir or many open vocal mics:

1. Use console/mute discipline first; do not rely on plugins to fix too many open mics.
2. PSE can help individual mics, but avoid unnatural chattering across a choir.
3. Group F6 for low-mid bloom and presence control.
4. WLM/metering belongs on stream/broadcast paths, not individual choir mics.

## Spoken Word And Pastor Mic Chains

Handheld/headset/lav speech:

1. X-FDBK or console/system feedback control only when feedback margin is the actual problem.
2. PSE only if stage/room bleed is obvious and the mic remains natural.
3. F6 or SSL E-Channel for HPF, low-mid cleanup, nasal control, and speech presence.
4. RVox or MV2 for consistency. Use MV2 carefully so breath, HVAC, and room noise are not lifted.
5. Sibilance if consonants hurt after compression.
6. L2 only on stream/output protection, not on the pastor channel to create loudness.

Broadcast speech cleanup:

- Clarix LB may be considered only for broadcast/stream voice paths that can tolerate latency and meet Waves hardware requirements.
- Do not put Clarix LB on in-venue FOH or monitor paths.
- If latency sync is uncertain, prefer F6/MV2/RVox and better source capture.

## Failure Checks

- PSE making words disappear: lower reduction, adjust threshold/release, or remove it.
- RVox pinning worship phrasing: reduce compression/output drive or switch to slower leveling.
- CLA-76 flattening consonants: slow/reduce compression or move presence control before compression.
- Sibilance dulling vocal: use less reduction or narrower targeting.
- Tune artifacts: verify key/scale/speed before downstream processing.
- Vocal Rider fighting emotion: use manual scene/fader moves or lighter rider action.
