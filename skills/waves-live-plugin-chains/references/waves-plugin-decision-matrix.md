# Waves Plugin Decision Matrix

Use this before selecting Waves plugins for a REAPER/SuperRack/LV1/MultiRack worship-audio workflow. For the full installed list, generate a local catalog with `scripts/inventory_waves_plugins.py`.

Also read `waves-superrack-operational-reference.md` for latency/live-safety notes and SuperRack-oriented decision rules.

## Selection Rules

1. Define the audible problem before choosing a plugin.
2. Prefer one clear job per plugin.
3. Keep SuperRack chains serial unless the final host supports the same routing.
4. For church deployment, mono usefulness beats stereo spectacle.
5. For CityAlight-style drums, avoid solo-drum hype that hurts vocal pocketing.
6. Treat installed plugins as candidates, not automatic recommendations. Verify uncertain plugins in the actual SuperRack target.

## Drums Toward CityAlight

Primary aimpoint: grounded, warm, centered, dynamic, cymbal-tucked.

Preferred starting tools:

| Job | First choices | Alternatives | Avoid by default |
| --- | --- | --- | --- |
| Close-mic bleed/gating | Primary Source Expander, C1, EMO-D5 | InTrigger Live as gate/trigger utility | Hard chopping that kills sustain |
| Kick EQ | F6, SSL E-Channel/EV2, API-550/560 | H-EQ, Q10, REQ | Excess click or broad sub boosts |
| Snare/tom EQ | F6, SSL E-Channel/EV2, API-550/560 | Scheps 73, H-EQ | Too much 180-350 Hz body or 5-10 kHz edge |
| Overheads | F6, H-EQ, SSL EQ | Sibilance/de-esser for harsh cymbals | Bright shelves and stereo wideners |
| Transients | Smack Attack, TransX | CLA Drums/JJP Drums with caution | Over-produced attack/sustain |
| Drum bus glue | SSLComp, API-2500, RComp, H-Comp | Abbey Road RS124, dbx-160 | Heavy bus crush |
| Drum warmth | NLS, J37, Abbey Road Saturator, BB Tubes | KramerTape, REDD | Grain/static/cymbal hash |
| Trigger/reinforcement | InTrigger Live, InTrigger | Torque for pitch/body correction | Obvious sample replacement unless requested |

For a warm, centered live-worship drum translation, start with:

- Kick: PSE or C1 keyed/guided by Kick Hybrid feel, F6/SSL EQ for sub vs 60-120, optional very light RComp.
- Kick Hybrid: InTrigger Live or direct hybrid track very low, EQ dulled above 3 kHz, used mostly for 60-120 support.
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
| Smart polish | Silk Vocal | CLA Vocals, Butch Vig Vocals | Letting a one-knob plugin hide artifacts |
| Level consistency | Vocal Rider | MV2/MaxxVolume with caution | Rider fighting worship phrasing |
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

- Clarity Vx family: useful restoration/noise tools, but verify target SuperRack flavor, latency, and CPU before live use.
- Linear-phase EQ, IR reverbs, tape emulations, and large mastering chains: useful in the right place, but require latency/CPU/artifact checks before live use.
- StudioVerse: installed, but do not rely on it for SuperRack workflows unless explicitly verified.
- Surround/immersive/headphone tools: usually irrelevant for mono-first church workflows.
- Instruments/samplers/synths: installed but not normal live mix inserts.
- Heavy mastering processors: can be useful, but may solve loudness while hiding balance problems.
