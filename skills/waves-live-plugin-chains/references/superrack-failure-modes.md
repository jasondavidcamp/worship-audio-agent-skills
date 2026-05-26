# SuperRack Plugin Failure Modes

Use this before recommending riskier Waves choices in a live SuperRack chain. Run `superrack-live-eligibility-gate.md` first.

## Source Material Mined

- Waves SuperRack Support Notes: SuperRack/Performer version compatibility, CPU indicators, plugin known issues, MIDI/plugin limitations, and heavy-plugin CPU spike cautions.
- Waves Plugin Latency chart: live/full mode differences for Sibilance, Bass Rider, Silk Vocal, L4, InTrigger, and high latency for Clarix LB.
- Waves Supported Platforms chart: whether a plugin is supported in SuperRack SoundGrid and SuperRack Native/Performer.
- Waves Clarix LB page: broadcast-only posture due to 47 ms latency and Titan/server requirements.

## General Rule

If the plugin choice makes the show less stable, less intelligible, harder to recall, or harder for a volunteer to troubleshoot, it is not a good live chain even if it sounds good in a render.

## Failure Modes

Over-expansion:

- Typical plugins: PSE, C1.
- Symptom: missing word starts/ends, chattering between phrases, unnatural choir/vocal holes.
- Fix: lower range, relax threshold/release, use less expansion, or remove the expander.

Over-compression:

- Typical plugins: RVox, CLA-76, CLA-2A, C6, bus compressors.
- Symptom: vocal pinned, consonants flattened, musical phrasing feels static, section lift disappears.
- Fix: reduce input/threshold/gain reduction, slow the fast stage, or use manual fader/snapshot help.

Lookahead/full-mode latency:

- Typical plugins: Sibilance full lookahead, Silk Vocal full component, L4 full mode, Bass Rider regular mode, InTrigger non-live modes.
- Symptom: chain feels late, monitor path uncomfortable, rack latency higher than expected.
- Fix: choose live/no-lookahead/low-latency mode or replace the plugin.

AI or restoration latency:

- Typical plugins: Clarix LB, Clarity-family tools.
- Symptom: excellent cleanup but unusable in the room, sync problems, CPU pressure.
- Fix: broadcast-only use, latency sync, Titan/server requirement check, or replace with F6/MV2/RVox/source cleanup.

Tuning artifacts:

- Typical plugin: Waves Tune Real-Time.
- Symptom: robotic transitions, wrong notes, worship leader sounds detached.
- Fix: verify key/scale, slower speed, less correction, bypass for spoken/prayer moments; remember SuperRack SoundGrid does not support MIDI input for plugins.

Low-end enhancer overload:

- Typical plugins: RBass, MaxxBass, Submarine.
- Symptom: limiter pumps, PA/sub overload, mono buildup, stream gets loud but less clear.
- Fix: rebalance kick/bass, high-pass non-low sources, reduce enhancer, check headroom/mono.

Limiter-as-mix-fix:

- Typical plugins: L2, L3-LL, L4.
- Symptom: loud but crunchy, smaller choruses, smeared drums, vocal less intelligible.
- Fix: lower bus level, fix balance and low end, then use limiter only for protection/final stream level.

FX left active:

- Typical plugins: H-Delay, H-Reverb, RVerb, IR-Live.
- Symptom: welcome/prayer/teaching starts wet, vocal distant, transitions messy.
- Fix: mute groups, snapshots, explicit FX return states, throw off-ramp cues.

Stereo spectacle:

- Typical plugins: wideners, stereo delays/reverbs, modulation.
- Symptom: exciting in headphones, weak or phasey in mono/room/stream.
- Fix: check mono, narrow the effect, and keep the vocal center stable.

Unsupported or missing plugin:

- Typical cause: version mismatch, license missing, mono/stereo rack mismatch, not SuperRack-compatible, third-party VST3 not scanned in Performer.
- Fix: verify Waves Supported Platforms, SuperRack version compatibility, local license, rack format, and actual plugin list before proposing the chain.

## Safe Replacement Patterns

- Studio vocal cleanup -> PSE + F6 + RVox/Sibilance.
- Heavy AI speech cleanup -> F6 + MV2/RVox, or Clarix LB only on broadcast paths.
- Full mastering chain -> F6/C6 as needed + WLM + L2/L3-LL/L4 as a guarded output limiter.
- Stereo wideners -> filtered delay/reverb returns that survive mono.
- Complex chain -> one channel strip plus one dynamics plugin plus one targeted cleanup plugin.
