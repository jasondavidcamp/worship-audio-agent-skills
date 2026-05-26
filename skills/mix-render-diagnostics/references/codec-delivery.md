# Codec Delivery

Use codec delivery checks for livestream exports, video uploads, podcast-style distribution, social clips, or any mastered file that will be encoded before listeners hear it.

## When To Run

Run `scripts/codec_roundtrip.py` when:

- the mix is near-final,
- true peak or high-band harshness is already close to the edge,
- stereo width or phase is part of the sound,
- cymbals, esses, ambience, or limiters feel fragile,
- the user reports that the uploaded/streamed version sounds worse than the WAV.

## What It Does

The helper script uses `ffmpeg` when available:

1. Encode the WAV to a delivery codec such as AAC, MP3, or Opus.
2. Decode that file back to WAV.
3. Optionally run `render_diagnostic_report.py` with the original as `--candidate` and the decoded file as `--codec-roundtrip`.

If `ffmpeg` is unavailable, report codec delivery as `ffmpeg_unavailable` or `untested`. Do not infer delivery safety from the original WAV alone.

## What To Watch

- decoded peak or clipping risk,
- high-band smear or changed 5-10 kHz energy,
- changed air-band energy,
- mono/stereo translation changes,
- distortion-like difference on loud choruses, cymbals, esses, or reverbs.

## Usage

```powershell
& "<python>" scripts/codec_roundtrip.py "C:\path\candidate.wav" --codec aac --bitrate 192k --section-manifest "C:\path\sections.yaml" --report-md "C:\path\codec-report.md" --report-json "C:\path\codec-report.json" --pretty
```

## Guardrails

- Treat this as delivery-risk evidence, not mastering advice.
- Do not run it before basic render, artifact, and headroom checks pass.
- Do not overreact to tiny band deltas. Focus on audible-risk sections: loud chorus, dense bridge, cymbals, esses, and reverb tails.
- Use the codec and bitrate closest to the actual delivery path when known.
