# SuperRack Host, Latency, And CPU Planning

Use this when a Waves chain must survive the actual live host: SuperRack SoundGrid, SuperRack Performer, LV1/SuperRack-compatible workflows, or REAPER staging for later SuperRack transfer.

## Source Material Mined

- [Waves SuperRack Performer product page](https://www.waves.com/mixers-racks/superrack-performer): Performer runs natively on Mac/PC through ASIO/Core Audio and can host Waves plus supported third-party VST3 plugins.
- [Waves SuperRack SoundGrid product page](https://www.waves.com/mixers-racks/superrack?wgsf=1): SoundGrid uses SoundGrid DSP servers, SoundGrid I/O, and network switching for scalable low-latency live processing.
- [Waves Live Common Questions](https://www.waves.com/support/waves-live-common-questions-answered): SoundGrid latency includes I/O conversion, server network buffer, driver network buffer, plugin latency, and internal routing; rack/plugin latency is displayed in SuperRack.
- [Waves SuperRack Performer audio-artifact troubleshooting](https://www.waves.com/support/troubleshooting-audio-artifacts-in-superrack-performer): heavy plugins, buffer size, sample rate, cables/hubs, and interface drivers/firmware all affect crackles/dropouts.
- [Waves SuperRack Support Notes](https://www.waves.com/support/superrack-support-notes): Performer VST3 support is mono/stereo only, Apple Silicon third-party VST3 plugins must be ARM-compatible, Realtek ASIO can freeze Performer, heavy plugins can spike CPU, and yellow/red AUDIO or CPU indicators call for buffer/load reduction.
- [Waves Supported Platforms](https://www.waves.com/support/tech-specs/supported-platforms), [Plugin Latency](https://www.waves.com/support/tech-specs/plugin-latency), and [Channel Components](https://www.waves.com/support/tech-specs/channel-components) charts: compatibility, latency, and mono/stereo component availability must all pass before recommending a plugin.

## Host Choice

SuperRack SoundGrid:

- Best when the church needs the lowest practical round-trip latency, high plugin counts, redundant/scalable processing, or console/card integration.
- Plugin processing happens on SoundGrid DSP servers; the computer runs the host/control surface.
- The network, server buffer, SoundGrid I/O, and plugin latency all matter.
- Prefer for FOH, monitor, and critical in-room insert paths when SoundGrid hardware is available.

SuperRack Performer:

- Best when the church needs a native host through ASIO/Core Audio and has a stable, powerful computer/interface.
- Processing happens on the computer CPU.
- Buffer size trades latency against CPU headroom.
- Supports Waves and supported third-party VST3 plugins, but this skill should still design Waves-first chains unless the user explicitly asks for third-party VST3.
- Avoid built-in/consumer audio drivers for show-critical paths; Waves specifically warns about Realtek ASIO freeze risk.

LV1 or other Waves live hosts:

- Use the same plugin support, latency, live-mode, and channel-format rules.
- Account for LV1/internal routing and server/driver buffers when estimating latency.

REAPER staging:

- Accept REAPER as an audition/render host only when the final plugin list, order, mono/stereo format, latency class, and preset-transfer path are expected to survive SuperRack.
- Do not recommend a REAPER-only plugin or topology as a live SuperRack chain.

## Path Latency Policy

Classify the signal path before selecting plugins:

- FOH and monitors: require core-live choices by default. Prefer 0-64 samples and live/no-lookahead components.
- Broadcast/livestream: can tolerate more latency when audio/video sync is managed, but still reject unstable or artifact-prone chains.
- Offline render/reference testing: can use heavier candidates only to learn tone, not as final live recommendations.
- External inserts: add unknown latency unless the console/host can measure or manually compensate it.

Do not use sample latency alone. Also check:

- I/O conversion.
- SoundGrid server/network buffer.
- SoundGrid driver network buffer when DAW playback/recording is involved.
- ASIO/Core Audio buffer for Performer or DAW paths.
- Plugin latency and rack/latency-group behavior.
- Internal mixer/routing delays.

## CPU And Artifact Triage

If a Performer chain crackles, drops out, or feels unstable:

1. Disable suspected heavy plugins and watch CPU load. Bypass is not a valid CPU test because bypassed plugins can still consume CPU.
2. Raise the interface buffer when live latency can tolerate it.
3. Consider a lower sample rate if the production can run at 44.1/48 kHz instead of 88.2/96 kHz.
4. Connect the interface directly instead of through a hub when possible.
5. Check USB/Thunderbolt cables, adapters, dust/debris, driver versions, and interface firmware.
6. On Apple Silicon, test buffer behavior instead of assuming larger is always safer; Waves notes lower buffers may force Performance Cores.
7. If the AUDIO indicator turns yellow or CPU turns yellow/red, lighten the chain or raise buffer before adding more processors.

Heavy-plugin caution list for Performer:

- Reverbs/convolution/space: Abbey Road Chambers, Abbey Road Plates, IR-1, H-Reverb, CLA Epic.
- Vocal/specialty processors: OVox, Butch Vig Vocals, Manny Marroquin Tone Shaper.
- Channel/group tools: CLA MixHub, Scheps Parallel Particles.
- Guitar/feedback tools: PRS SuperModels, X-FDBK.
- Mastering/color: Abbey Road TG Mastering Chain.

This does not mean "never use them." It means use them after the core mix is stable, with a CPU/artifact check.

## Channel Format Gate

Before recommending a plugin, verify the rack format can show/load the correct component:

- Mono rack needs mono-capable plugins.
- Stereo rack needs stereo-capable plugins.
- Mono-to-stereo effects are usually better as FX returns than inline mono source correction.
- Some plugins are stereo or mono-to-stereo only and will not appear in mono-to-mono racks.
- Performer third-party VST3 support is limited to mono/stereo components; Apple Silicon systems require ARM-compatible VST3 plugins.

If a plugin is "supported" but missing from the menu, suspect:

- unsupported channel format,
- unsupported host/version,
- missing license,
- wrong plugin version,
- plugin not scanned,
- SoundGrid vs Performer platform mismatch.

## Output Shape

When this file applies, answer with:

```yaml
host_target: SuperRack SoundGrid | SuperRack Performer | LV1 | REAPER staging | unknown
path_class: FOH | monitor | livestream | broadcast-only | offline-test
latency_budget: core-live | conditional-live | verify-first | broadcast-only
cpu_risk: low | medium | high | unknown
format_risk: mono/stereo/component issue | none_known | unknown
chain_posture: approve | simplify | verify-in-target | reject-for-live
next_check: exact verification step before committing
```
