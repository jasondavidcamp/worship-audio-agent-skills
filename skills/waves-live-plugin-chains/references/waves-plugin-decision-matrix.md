# Waves Plugin Decision Matrix

Use this before selecting Waves plugins for a SuperRack worship-audio workflow. For the full installed list, generate a local catalog with `scripts/inventory_waves_plugins.py`.

First read `superrack-live-eligibility-gate.md`. If this matrix and the gate disagree, the gate wins. Also read `waves-superrack-operational-reference.md` for latency/live-safety notes and SuperRack-oriented decision rules.

## Selection Rules

1. Define the audible problem before choosing a plugin.
2. Prefer one clear job per plugin.
3. Keep SuperRack chains serial unless the final host supports the same routing.
4. For church deployment, mono usefulness beats stereo spectacle.
5. For drums, avoid solo-source hype that hurts vocal pocketing or live translation.
6. Treat installed plugins as candidates, not automatic recommendations. Verify uncertain plugins in the actual SuperRack target.
7. Use only official SuperRack-supported Waves plugins or plugins verified in the target SuperRack instance.
8. Prefer the live component or low-latency mode when a plugin has both live and full/studio modes.

## Drum Chain Starting Points

Preferred starting tools:

| Job | First choices | Alternatives | Avoid by default |
| --- | --- | --- | --- |
| Close-mic bleed/gating | Primary Source Expander, C1, EMO-D5 | InTrigger Drum Replacer only for reinforcement, not gating | Hard chopping that kills sustain |
| Kick EQ | F6, SSL E-Channel/EV2, API-550/560 | H-EQ, Q10, REQ | Excess click or broad sub boosts |
| Snare/tom EQ | F6, SSL E-Channel/EV2, API-550/560 | Scheps 73, H-EQ | Too much 180-350 Hz body or 5-10 kHz edge |
| Overheads | F6, H-EQ, SSL EQ | Sibilance/de-esser for harsh cymbals | Bright shelves and stereo wideners |
| Transients | Smack Attack, TransX | CLA Drums/JJP Drums with caution | Over-produced attack/sustain |
| Drum bus glue | SSLComp, API-2500, RComp, H-Comp | Abbey Road RS124, dbx-160 | Heavy bus crush |
| Drum/bus color | NLS, J37, Abbey Road Saturator, BB Tubes | KramerTape, REDD | Grain/static/cymbal hash |
| Trigger/reinforcement | InTrigger Drum Replacer in Live/low-latency mode | Torque for pitch/body correction | Obvious sample replacement unless requested |

For a controlled live drum chain, start with:

- Kick: PSE or C1 keyed/guided by Kick Hybrid feel, F6/SSL EQ for sub vs 60-120, optional very light RComp.
- Kick Hybrid: InTrigger Drum Replacer in Live/low-latency mode or direct hybrid track very low, EQ dulled above 3 kHz, used mostly for 60-120 support.
- Snare: PSE/C1, F6/SSL EQ cutting body/box and softening edge.
- Toms: PSE/C1, F6/SSL EQ, restrained sustain.
- Overheads: F6/H-EQ high-pass, low-mid cleanup, tucked 5-10 kHz.
- Drum bus: F6 cleanup, SSLComp/API-2500 light glue, optional NLS/J37 only after artifact gate.

## Vocals

Preferred starting tools:

| Job | First choices | Alternatives | Avoid by default |
| --- | --- | --- | --- |
| Stage bleed | Primary Source Expander | C1, NS1 with caution | Aggressive gates on lead vocal |
| Corrective EQ | F6, SSL E/EV2, H-EQ | Q10, REQ, Scheps 73 | Static presence boosts before low-mid cleanup |
| Compression | R-Vox, CLA-76 into CLA-2A, RComp, H-Comp | CLA-3A, VComp | Pinning every phrase |
| De-essing | Sibilance, RDeEsser, DeEsser, F6 | MannyM-TripleD | Dulling the whole vocal |
| Tuning | Waves Tune Real-Time | Waves Tune/LT offline only | Wrong key/scale or too-fast correction |
| Smart polish | Silk Vocal Live component | CLA Vocals, Butch Vig Vocals only if SuperRack-verified | Letting a one-knob plugin hide artifacts |
| Level consistency | Vocal Rider live posture, R-Vox | MV2 with caution | Rider fighting worship phrasing |
| FX | H-Delay, H-Reverb, RVerb, IRLive, CLA Epic | Space Rider | Serial wet effects that cannot transfer cleanly |

## Band/Buses

Preferred starting tools:

| Job | First choices | Alternatives | Avoid by default |
| --- | --- | --- | --- |
| Band bus pocketing | F6 sidechain/dynamic EQ | C6, H-EQ | Full-band dulling |
| Vocal bus glue | RComp, CLA-2A, H-Comp | SSLComp light | Over-compressing BGV blend |
| Band/drum bus glue | SSLComp, API-2500 | RComp, H-Comp, RS124 | Crushing section lift |
| Low-end enhancement | RBass, MaxxBass, Submarine | LoAir | Headroom loss and mono PA overload |
| Saturation | NLS, J37, Abbey Road Saturator | BB Tubes, KramerTape | Static/grain/cymbal hash |
| Master/stream limiting | L2, L3-LL, L4, WLM | L1 as simple guard | Loudness chasing during tone decisions |

## Plugins To Verify Before Trusting Live

- Clarix LB: SuperRack-compatible for live broadcast, but high latency and Titan/server requirements make it broadcast-only, not in-venue FOH/monitor processing.
- Clarity Vx family: useful restoration/noise tools in studio contexts, but do not make them default SuperRack chains unless the exact target host proves support, latency, and CPU behavior.
- Silk Vocal, Bass Rider, L4, Sibilance, and InTrigger: use the live component/mode where available; avoid full/lookahead/studio modes on in-venue sources.
- Linear-phase EQ, IR reverbs, tape emulations, and large mastering chains: useful in the right place, but require latency/CPU/artifact checks before live use.
- StudioVerse: installed, but do not rely on it for SuperRack workflows unless explicitly verified.
- Surround/immersive/headphone tools: usually irrelevant for mono-first church workflows.
- Instruments/samplers/synths: installed but not normal live mix inserts.
- Heavy mastering processors: can be useful, but may solve loudness while hiding balance problems.
