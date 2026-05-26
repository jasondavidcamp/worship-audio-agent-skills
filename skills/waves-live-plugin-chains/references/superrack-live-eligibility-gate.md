# SuperRack Live Eligibility Gate

Use this before recommending any plugin chain for a live Waves workflow. The goal is to prevent this skill from recommending studio-only chains that sound useful in REAPER but fail in SuperRack.

## Source Material Mined

- Waves SuperRack Support Notes, updated 2025-08-13: SuperRack/plugin version compatibility, SoundGrid network notes, MIDI/plugin limits, Performer CPU warnings, and known issues.
- Waves SuperRack SoundGrid product/support page: SuperRack SoundGrid is built for FOH, monitor, broadcast, and AV use, and V15 supports V16 and V15 Waves plugins.
- Waves SuperRack Performer product/support page: SuperRack Performer supports Waves V16/V15 plugins in V15 and can run natively on Core Audio/ASIO, but this skill still limits recommendations to Waves/SuperRack-deployable chains.
- Waves Supported Platforms chart: per-plugin SuperRack SoundGrid and SuperRack Native/Performer support.
- Waves Plugin Latency chart: per-plugin latency and live/full mode differences.
- Waves Channel Components chart: per-plugin mono/stereo/rack-format availability.
- Waves Live Common Questions: SoundGrid latency is affected by I/O conversion, server buffer, driver buffer, plugin latency, and routing; rack latency is displayed in SuperRack.
- Waves SuperRack Performer audio-artifact troubleshooting: heavy plugins, buffer size, sample rate, cables/hubs, and interface drivers/firmware affect crackles/dropouts.
- Waves Clarix LB product page: SoundGrid-compatible broadcast cleanup with 47 ms latency, not intended for in-venue concert audio.

## Hard Gate

Recommend a plugin in a live chain only when all are true:

1. It is confirmed in Waves Supported Platforms as `superRackSoundGrid` or `superRackNative`, or the user confirms it appears in the target SuperRack plugin list.
2. The installed plugin version is compatible with the target SuperRack version.
3. Its live latency is acceptable for the path: FOH and monitor paths should use zero/near-zero/low-latency choices; broadcast-only paths can tolerate more latency if synced.
4. The rack format can load it. Mono racks will not show stereo-only plugins.
5. CPU/load is realistic for the show. If SuperRack Performer audio or CPU indicators turn yellow/red, lighten the chain or raise buffer.
6. The chain uses the live component or low-latency mode when the plugin has both full/studio and live modes.
7. The target host and path are named: SoundGrid, Performer, LV1, REAPER staging, FOH, monitor, livestream, or broadcast-only.

## Version Gate

- SuperRack V15: use Waves V16 or V15 plugins.
- SuperRack V14: use Waves V16, V15, or V14 plugins.
- SuperRack V13: use Waves V14 or V13 plugins.
- SuperRack V12: use Waves V13 or V12 plugins.
- Do not design new public chains around MultiRack. Waves notes that the last Waves plugin version supported in MultiRack is V10.

## Latency Classes For This Skill

- Core live: 0-64 samples at 48 kHz, or official zero/near-zero live posture. Good default for FOH, vocals, drums, buses, and many stream chains.
- Conditional live: 65-256 samples, or plugin modes that require care. Use when the job is worth the latency and the rack path can tolerate it.
- Verify-first: above 256 samples, special hardware requirements, unconfirmed support, heavy CPU, or plugin modes that can surprise volunteers.
- Broadcast-only: high-latency live-broadcast tools that are SuperRack-compatible but not suitable for in-venue FOH/monitor paths.

## Mined Live-Safe Notes

Official Waves data indicates these common candidates are SuperRack SoundGrid and SuperRack Native/Performer compatible:

| Plugin | 48 kHz latency note | Skill posture |
| --- | --- | --- |
| Primary Source Expander | 0 samples | Core live bleed control |
| F6 Floating-Band Dynamic EQ | 0 samples | Core live dynamic EQ/pocketing |
| Renaissance Vox | 64 samples | Core live vocal/speech leveling |
| CLA-76 | 0 samples | Core live fast control |
| CLA-2A | 0 samples | Core live smooth leveling |
| Sibilance | Live/full no-lookahead 0 samples; full lookahead adds latency | Use live/no-lookahead mode |
| Waves Tune Real-Time | Zero or near-zero depending on pitch | Core live when key/scale are known |
| Vocal Rider | 0 samples | Core live; verify musical phrasing |
| Silk Vocal | Live component 64 samples; full component is high latency | Use Silk Vocal Live only for venue paths |
| C1 Compressor | Comp/gate 0 samples; some sidechain variants add latency | Use simple live modules first |
| C6 | 64 samples | Core/conditional live multiband control |
| MV2 | 64 samples | Core/conditional stream/speech detail |
| H-Delay | 0 samples | Core live delay |
| H-Reverb | 0 samples | Core live but watch CPU/tails |
| RVerb | 0 samples | Core live reverb |
| IR-Live | 0 samples | Core live convolution option; verify CPU/tails |
| SSL E-Channel | 1 sample | Core live channel strip |
| SSL EV2 Channel | 59 samples | Core live/conditional channel strip |
| API 2500 | 0 samples | Core live drum/bus glue |
| Bass Rider | Live mode 240 samples at 48 kHz | Conditional live; avoid if it fights phrasing |
| RBass / MaxxBass / Submarine | 0 samples | Core live only if headroom/mono survive |
| L2 / L3-LL | 64 samples | Stream/output protection, not tone repair |
| L4 | Live mode 168 samples at 48 kHz | Conditional stream/output protection |
| WLM Plus | WLM 0, WLM Plus 80 samples | Metering/correction; prefer metering live |
| Clarix LB | 2192 samples / 47 ms | Broadcast-only; not in-venue |
| InTrigger Drum Replacer | Live 0 samples; low-latency mode 72 samples; full mode much higher | Use Live/low-latency only on venue paths |
| Torque | Torque Live 0 samples; regular component adds latency | Use Torque Live on venue paths |

## Refusal And Replacement Rules

- If a proposed plugin is not confirmed for SuperRack, do not recommend it as a chain plugin. Offer a SuperRack-safe replacement.
- If a plugin is compatible but high-latency, mark it as broadcast-only or verify-first.
- If a studio/full component has a live component, name the live component explicitly.
- If Performer crackles, drops out, or shows yellow/red audio/CPU indicators, simplify the chain and apply `superrack-host-latency-cpu-planning.md` before adding plugins.
- If the user is staging in REAPER, still design for the final SuperRack host, not for every plugin REAPER can load.
- If the plugin appears in inventory but not in the target rack, suspect version, license, format, unsupported platform, or mono/stereo mismatch before suggesting a workaround.
