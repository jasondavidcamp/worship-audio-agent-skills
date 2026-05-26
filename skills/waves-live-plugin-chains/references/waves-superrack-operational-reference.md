# Waves SuperRack Operational Reference

Source: user-provided structured reference, added 2026-05-25.

Use this as an operational plugin-selection guide for Waves SuperRack SoundGrid / SuperRack Performer workflows. It is not a strict licensing/version-completeness document. Cross-check with a locally generated installed-plugin catalog, and verify uncertain plugins inside the actual SuperRack target before committing a session.

## Data Model

When adding plugin knowledge, prefer this shape:

```json
{
  "plugin": "F6 Floating-Band Dynamic EQ",
  "category": "Dynamic EQ",
  "latency_class": "Low",
  "live_safe": true,
  "primary_uses": ["vocal harshness control", "ring suppression"],
  "common_sources": ["lead vocal", "acoustic guitar", "drum bus"],
  "description": "Dynamic EQ with floating parametric bands.",
  "ai_usage_hints": ["Use when static EQ is insufficient."]
}
```

## Safe Live Defaults

These are strong default candidates for church/SuperRack workflows:

- SSL E-Channel: very-low-latency channel strip for vocals, drums, and guitars.
- F6: low-latency dynamic EQ for vocal harshness, cymbal taming, acoustic resonance, drum resonance, and bus pocketing.
- R-Vox: very-low-latency vocal compressor/gate for fast vocal control.
- CLA-2A: smooth optical-style vocal/bass leveling.
- CLA-76: fast FET-style control for energetic vocals, snare, and drum punch.
- Q10: very-low-latency surgical EQ for resonance/ring removal.
- RVerb: low-latency general reverb.
- H-Delay: low-latency worship vocal/guitar delay.
- X-FDBK: very-low-latency feedback suppression utility.
- API 2500: low-latency drum/mix bus glue and punch.
- Sibilance: modern de-essing and vocal edge control.

## Channel Strips

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| Scheps Omni Channel | Low | Safe | Full channel workflow: saturation, gate, compression, EQ, filtering. Useful for vocals, drums, bass, broadcast voice. |
| CLA MixHub | Low | Safe | SSL-style console workflow and cohesive channel/bus color. |
| SSL E-Channel | Very low | Excellent | Strong default live channel strip for vocals, drums, guitars. |
| SSL G-Channel | Very low | Excellent | Smoother SSL-style channel/bus cohesion. |

## EQ And Dynamic EQ

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| F6 Floating-Band Dynamic EQ | Low | Excellent | Preferred live corrective EQ when static EQ is insufficient. Use for harshness, resonance, cymbal control, vocal pocketing. |
| Q10 | Very low | Excellent | Surgical EQ, ring removal, lightweight corrective shaping. |
| GEQ | Very low | Excellent | Monitor tuning, PA shaping, feedback-prone buses. |
| PuigTec EQP-1A | Low | Safe | Broad tonal sweetening, vocal/bass/mix-bus color; not surgical. |

## Compressors And Dynamics

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| R-Vox | Very low | Excellent | Fast route to controlled worship vocals and spoken word. |
| CLA-2A | Low | Excellent | Smooth vocal and bass leveling. |
| CLA-76 | Low | Excellent | Fast transient control and energy for vocals/snare/drums. |
| API 2500 | Low | Excellent | Drum bus and mix bus punch/glue. |
| C6 | Medium | Safe | Multiband vocal harshness, mix bus control, drum taming. |
| MV2 | Very low | Excellent | Livestream speech/vocal detail enhancement; use carefully so it does not over-lift noise. |

## Gates, Expansion, And Transients

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| C1 Gate | Very low | Excellent | Drum gating and noise suppression. |
| Primary Source Expander | Low | Excellent | First-stage bleed control on live vocals and close mics. |
| Smack Attack | Low | Excellent | Drum attack/sustain shaping when transient shape is the problem. |

## De-Essing And Vocal Cleanup

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| Sibilance | Low | Excellent | Preferred vocal de-esser for modern vocal cleanup. |
| DeEsser | Very low | Excellent | Lightweight classic de-essing. |
| Clarity Vx | Medium | Conditional | Livestream/spoken-word cleanup; avoid monitor paths and verify target SuperRack/latency/CPU behavior. |

## Reverb And Delay

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| H-Reverb | Medium | Safe | Lush modern worship spaces; watch CPU/tails. |
| RVerb | Low | Excellent | Reliable general live reverb. |
| Abbey Road Plates | Medium | Safe | Smooth dense vocal/snare plate tails. |
| H-Delay | Low | Excellent | Strong default worship delay. |
| SuperTap | Low | Safe | Rhythmic delays and larger ambient textures. |

## Saturation And Analog Color

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| J37 | Medium | Conditional | Vocal/drum/bus warmth; use sparingly and check for grain/hash. |
| Kramer Tape | Medium | Conditional | Bus warmth; prefer on buses rather than many inserts. |

## Feedback And Live Utilities

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| X-FDBK | Very low | Excellent | Feedback suppression for pastor mics, wedges, difficult rooms. |
| InPhase | Low | Safe | Drum alignment and multi-mic phase correction. |
| Torque | Low | Safe | Subtle kick/tom pitch adjustment. |

## Limiters And Loudness

| Plugin | Latency | Live posture | Use |
| --- | --- | --- | --- |
| L2 Ultramaximizer | Low | Excellent | Livestream output peak protection. |
| WLM Plus | Low | Excellent | LUFS loudness monitoring for broadcast/livestream. |

## Decision Rules

Vocal harshness:

1. F6
2. C6
3. Sibilance

Vocal consistency:

1. Vocal Rider
2. R-Vox
3. CLA-2A

Drum punch:

1. Smack Attack
2. CLA-76
3. API 2500

Worship ambience:

1. H-Reverb
2. H-Delay
3. Abbey Road Plates

Livestream cleanup:

1. Clarity Vx
2. MV2
3. L2
4. WLM Plus

## Operational Metadata To Capture

For automated chain generation, collect or infer:

- latency expectations
- mono/stereo capability
- sidechain support
- CPU intensity
- typical insert location
- live-risk score
- SuperRack SoundGrid vs Performer support

## Corroboration Against Local Inventory

Cross-check any local Waves inventory for the major live-safe tools: SSL E/G channels, Scheps Omni Channel, CLA MixHub, F6, Q10, GEQ, PuigTec, R-Vox, CLA-2A, CLA-76, API 2500, C6, MV2, C1, Smack Attack, Sibilance, DeEsser, Clarity Vx, H-Reverb, RVerb, Abbey Road Plates, H-Delay, SuperTap, J37, Kramer Tape, X-FDBK, InPhase, Torque, L2, and WLM Plus.

The list also reinforces the same caution posture already learned locally: AI/restoration, linear phase/mastering, IR/reverb-heavy, tape/saturation, and broad mastering chains need latency/CPU/artifact checks before live use.
