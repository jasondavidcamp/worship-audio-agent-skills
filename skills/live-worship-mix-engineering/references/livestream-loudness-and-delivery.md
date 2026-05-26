# Livestream Loudness And Delivery

Use this when evaluating stream output level, dynamic range, true peak safety, codec/encoder settings, or whether a worship stream will survive platform delivery.

Mined from public sources:

- ITU-R BS.1770-5: https://www.itu.int/rec/R-REC-BS.1770-5-202311-I/en
- EBU R 128: https://tech.ebu.ch/publications/r128
- YouTube Help, Live Encoder Settings: https://support.google.com/youtube/answer/2853702?hl=en-EN

## First Principle

Measure loudness so the stream is consistent and safe, but do not let a number outrank intelligibility, musical balance, or freedom from artifacts.

## Measurements To Prefer

Integrated loudness:

- Use for the whole service, worship set, sermon, or completed program segment.
- Good for comparing delivery level across services.
- Too broad to diagnose why a chorus, sermon transition, or video playback felt wrong.

Short-term loudness:

- Use for song sections, speaking blocks, prayer, and transitions.
- Helps catch sudden jumps that integrated loudness hides.

Loudness range:

- Use to judge whether viewers will chase volume.
- Too narrow can feel crushed; too wide can make speech and music inconsistent online.

True peak:

- Use for intersample peak safety and codec/encoder resilience.
- Do not trust sample peak alone when the stream is being encoded.

Spectral balance:

- Check low-end and high-frequency excess because encoders, limiters, and small speakers punish extreme balances.
- This is a mix diagnosis, not just a mastering diagnosis.

## Delivery Checks

Before a livestream or uploaded service:

- Confirm the encoder audio codec and sample rate match the platform workflow.
- For YouTube Live, official help currently lists AAC or MP3 audio, CBR encoding, 44.1 kHz stereo audio, and 128 kbps stereo audio among its recommended live settings.
- Run a private or unlisted test with music and speech before the real service when changing encoder, matrix, bus, limiter, sample rate, or routing.
- Monitor the stream return when possible, not only the console output.
- Check video playback, sermon mics, worship, prayer, and transitions separately.

## Practical Worship Targets

Do not hard-code a single LUFS target as universal. Platform behavior, service length, music/speech ratio, and the active church aimpoint all matter.

Useful posture:

- Keep true peak safely below clipping after limiting and encoding.
- Keep speech and worship close enough that viewers do not constantly adjust volume.
- Preserve lyrics before low-end impact.
- Leave more headroom when the stream has lots of cymbals, crowd mics, playback videos, or unpredictable speech mics.
- If the stream sounds small, fix balance and ambience before smashing the limiter.

## Common Diagnoses

Viewers turn down worship and turn up sermon:

- Music/speech loudness relationship is too wide.
- Use bus/matrix automation, speech bus control, worship bus control, or stream master dynamics.
- Do not solve by limiting worship until it loses life.

Stream is loud but lyrics are unclear:

- Loudness is not the bottleneck.
- Check vocal-to-band balance, 1.5-4 kHz masking, sibilance control, room mic wash, and limiter pumping.

Limiter pulls down the whole mix:

- Look for low-end buildup, cymbal spikes, harsh vocal peaks, or video playback overs.
- Fix the source or subgroup before driving the stream limiter harder.

Platform return sounds worse than local record:

- Compare console output, encoder input, local encoded recording, and platform playback.
- Check sample-rate conversion, bitrate, clipping before the encoder, and excessive true peaks.

## Skill Behavior

When loudness is in scope, report:

```yaml
delivery_context: YouTube Live / upload / local record / unknown
integrated_loudness: measured_or_unknown
short_term_range: measured_or_unknown
true_peak: measured_or_unknown
main_risk: clipping / too dynamic / crushed / harsh / low-heavy / speech-music mismatch
next_move: one or two delivery-safe changes
```

If no measurements are available, ask for or create a render before making confident loudness claims.
