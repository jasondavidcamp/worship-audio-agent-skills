# SuperRack Rhythm, Band, And Bus Chains

Use this for drums, kick/bass/low-end translation, band buses, mix buses, and livestream/output buses. Run `superrack-live-eligibility-gate.md` first.

## Source Material Mined

- Waves Supported Platforms and Plugin Latency charts: PSE, C1, F6, SSL E/EV2, CLA-76, API 2500, Smack Attack, InTrigger Drum Replacer, RBass, MaxxBass, Submarine, C6, MV2, L2, L3-LL, L4, and WLM Plus are SuperRack-compatible, with live-mode cautions for some.
- Waves SuperRack SoundGrid/Performer material: chains must be practical for real-time FOH, monitor, broadcast, and AV paths.
- Waves Live Common Questions: total latency includes I/O, buffer, plugin latency, and routing, so low-latency plugin choice does not remove the need to check rack latency.

## Drum Source Chains

Kick:

1. PSE or C1 Gate only if bleed/sustain is the problem.
2. F6 or SSL E/EV2 for HPF where appropriate, low-mid cleanup, sub/attack shaping.
3. CLA-76 or RComp-style control only when peaks are inconsistent.
4. InTrigger Drum Replacer only in Live/low-latency mode and only when reinforcement is musically acceptable.

Snare:

1. PSE/C1 for bleed control, not perfect silence.
2. F6/SSL for box, ring, body, and crack.
3. CLA-76 for transient control if the snare is inconsistent.
4. Smack Attack only when attack/sustain shape is the specific diagnosis.

Toms:

1. PSE/C1 to manage cymbal spill and unused passages.
2. F6/SSL for ring/body.
3. Light compression only if tom hits jump unpredictably.
4. Preserve decay unless the room or stream needs a tighter live sound.

Overheads/cymbals:

1. F6 for low-mid wash and dynamic harshness.
2. Sibilance/de-esser only if cymbal esses/edge behave like sibilance.
3. Avoid broad bright shelves, stereo hype, or saturation that adds cymbal hash.

Drum bus:

1. F6 cleanup before glue.
2. API 2500, SSL bus compression, RComp, or H-Comp for light movement.
3. Saturation only after artifact checks; avoid tape/color if cymbals get grainy.
4. Never use drum bus compression to hide bad close-mic balance.

## Kick, Bass, And Low-End Translation

Bass DI:

1. F6/SSL for HPF/LPF, low-mid cleanup, and articulation.
2. CLA-2A/RComp/RVox-style leveling when bass notes wander.
3. RBass/MaxxBass only if the bass needs small-speaker translation and headroom survives.

Kick and bass together:

1. Decide which source owns sub weight, mid-bass body, and attack.
2. Use F6 or C6 to control overlapping low-mid energy before adding low-end enhancers.
3. Use Submarine only if the PA/stream path can support it and mono/headroom remain stable.
4. Watch limiter gain reduction; if kick/bass drive the limiter, fix the low end before raising loudness.

## Band Bus

Cloudy band:

1. F6 dynamic low-mid control.
2. Pocket piano/acoustic/keys around the vocal before boosting vocal brightness.
3. Avoid full-band dulling unless the whole band is truly harsh.

Small band:

1. Check drums/bass/guitars/keys section balance first.
2. Add SSL/API-style bus glue lightly.
3. Use saturation sparingly; reject if cymbal hash or low-mid thickness appears.

Chorus does not lift:

1. Compare verse and chorus source levels before adding bus processing.
2. Check bus compressor release and gain reduction.
3. Use section automation or snapshots before master limiting.

## Mix Bus And Livestream Bus

Mix bus:

1. Keep processing light: F6 cleanup, gentle SSL/API/RComp glue, optional limiter guard.
2. Avoid solving balance with a limiter.
3. Keep mono compatibility and vocal intelligibility ahead of width or loudness.

Livestream/output bus:

1. WLM or WLM Plus for loudness monitoring.
2. F6/C6/MV2 only for specific tonal or detail problems.
3. L2/L3-LL/L4 for peak protection and final level. Prefer live/low-latency modes where applicable.
4. Clarix LB only for broadcast speech/noise cleanup when latency and hardware requirements are acceptable.

## Failure Checks

- Low-end enhancers eating headroom: bypass RBass/MaxxBass/Submarine and rebalance kick/bass.
- Bus glue holding down choruses: reduce ratio/threshold or change release.
- API/SSL bus compression making worship feel smaller: reduce gain reduction.
- Drum gate chatter: loosen PSE/C1 settings before adding more compression.
- Limiter making the stream loud but crunchy: back down bus level and fix source/bus balance.
