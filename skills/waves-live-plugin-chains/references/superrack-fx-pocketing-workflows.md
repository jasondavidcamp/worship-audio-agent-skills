# SuperRack FX And Pocketing Workflows

Use this for live-safe reverb/delay decisions and dynamic EQ/sidechain pocketing. Run `superrack-live-eligibility-gate.md` first.

## Source Material Mined

- Waves Plugin Latency and Supported Platforms charts: H-Delay, H-Reverb, RVerb, IR-Live, F6, C6, and Sibilance are SuperRack-compatible candidates, with low/zero-latency notes in the gate.
- Waves F6 product page: F6 provides floating dynamic EQ bands and per-band dynamics suitable for targeted control.
- Waves SuperRack material: routing, rack format, snapshots, and latency must match the real host, not only the DAW used for testing.

## Worship Delay

H-Delay default posture:

1. Use on a confirmed effects return or SuperRack path that matches the deployment.
2. Filter lows and excessive top so delay does not blur lyrics.
3. Prefer tempo-aware quarter/dotted-eighth/slap choices only when the operator can recall them safely.
4. Use throws only if snapshots/scenes or manual control can guarantee they are muted afterward.

Avoid:

- Serial delay directly on a vocal insert unless wet/dry, bypass, and scene behavior are tested.
- Long feedback into speech, prayer, or transitions.
- Stereo delay as the only thing making a mono-first vocal feel exciting.

## Worship Reverb

RVerb:

- Strong default for simple, reliable live ambience.
- Use when the team needs easy repeatability more than complex tail design.

H-Reverb:

- Use for larger live vocal or instrument space when CPU, tail behavior, and snapshots are stable.
- Keep predelay and filtering focused on lyric clarity.

IR-Live:

- Use when a specific convolution space is needed and CPU/tail behavior is tested.
- Avoid changing impulse/preset during critical live moments unless verified.

Speech/prayer:

- Reverb/delay returns should normally be muted or greatly reduced.
- If a pad or transition tail is desired, separate the background pad from the speech mic.

## Dynamic EQ Pocketing

Use F6 or C6 pocketing when a source masks the lead vocal but should not be statically dulled.

Common targets:

- Piano/acoustic low mids masking vocal body.
- Electric guitar/keys presence masking lyric consonants.
- Cymbal edge making the vocal feel sharp.
- Band bus low mids swelling when the full band enters.
- BGV group occupying the same presence lane as the lead.

Workflow:

1. Identify the masking source and the vocal range being hidden.
2. Try source-specific F6 before band-bus F6.
3. Use sidechain only if the SuperRack routing supports it reliably.
4. If sidechain routing is not confirmed, use static/source-specific EQ plus section automation.
5. Listen for the source becoming obviously ducked; if listeners can hear the pocketing work, it is probably too much.

## Snapshot And Service Flow Checks

- FX returns need a known state for worship, welcome, video, teaching, prayer, and response.
- Throws and lush reverbs should have explicit off-ramp cues.
- Delay tempo changes should be scene-safe.
- Avoid plugin chains that require a volunteer to remember hidden wet/dry, tap, or bypass details under pressure.

## Failure Checks

- Vocal feels distant: reduce FX return, shorten decay, increase predelay, or filter return lows before raising vocal level.
- Speech starts wet: fix mute group/snapshot state before changing the speech chain.
- Delay clutter: lower feedback or automate throws instead of leaving a long delay always active.
- Pocketing dulls the band: narrow the F6/C6 action or move the cut to the masking source.
- Sidechain unavailable: do not invent routing; use static EQ/section automation or host-supported sidechain only.
