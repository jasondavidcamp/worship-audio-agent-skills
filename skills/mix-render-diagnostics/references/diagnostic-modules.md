# Diagnostic Modules

Use these modules when a render sounds wrong but basic peak/RMS checks do not explain why. The modules are evidence generators for `live-worship-mix-engineering`; they do not replace listening, taste calls, or source-context judgment.

## 1. Section-Aware Mix Diagnostics

Compare multiple short regions before full-length judgment:

- sparse vocal section,
- first chorus,
- biggest chorus or bridge,
- late-song section,
- user-reported problem timestamp.

For each section, capture loudness proxy, peak, crest factor, spectral bands, mid/side balance, mono delta, transient proxy, and artifact status. Flag section-specific failures instead of averaging them away.

Use `references/section-manifest.md` and `render_diagnostic_report.py --section-manifest` when the same sections will be reused across candidates.

## 2. Vocal Intelligibility And Masking

Best evidence comes from a full mix plus vocal and band stems for the same section.

Check:

- vocal-to-band relationship in 1.5-5 kHz for lyric articulation,
- band or keys/guitars masking the vocal in 180-500 Hz,
- sibilance/edge pressure in 5-10 kHz,
- vocal presence loss after bus compression, limiting, reverb, or stereo processing.

When stems are unavailable, report only mix-level proxies and avoid claiming source-level masking with certainty.

## 3. Transient And Punch Analysis

Use this for drums, drum bus, band bus, low-end changes, clippers, limiters, transient designers, sample reinforcement, and parallel compression.

Check:

- crest factor by section,
- attack-to-body proxy,
- transient density,
- candidate vs baseline transient loss,
- whether loudness increased while punch decreased.

Do not call a drum change better just because RMS or low end increased.

## 4. Reverb Tail And Space Buildup

Use this when vocals feel distant, consonants smear, prayers/welcome are too wet, or late-song ambience piles up.

Check:

- quiet-floor-to-body ratio,
- energy between phrases or in sparse sections,
- late-song wash compared with early sections,
- high-mid/air tail brightness that keeps drawing attention.

Prefer reporting "tail/gap-fill risk" unless a dry stem or FX return is available.

## 5. Stereo And Mono Translation By Band

Use this for livestream, mono PA zones, center vocal stability, wide reverbs/delays, stereo tracks, pads, synths, and audience mics.

Check:

- side-to-mid energy overall and by frequency band,
- left/right correlation,
- mono fold-down level loss,
- which bands change most when folded to mono.

Treat weak center information, negative correlation, or large mono loss as hard deployment risks for church playback.

## 6. Codec And Delivery Simulation

Use this for livestream, podcast, video, social clips, or mastered exports.

Check a codec round-trip when possible:

- encode/decode the candidate with the expected delivery codec,
- compare decoded audio against the WAV,
- flag high-band smear, sample-peak overs, mono/stereo shifts, and distortion-like difference energy.

If the script receives only WAV input, mark codec risk as untested instead of assuming delivery safety.

Use `references/codec-delivery.md` and `scripts/codec_roundtrip.py` when a real encode/decode check is needed.

## 7. Candidate Report Generation

Every candidate report should include:

- source files and sections analyzed,
- pass/warn gates,
- deltas against baseline and reference,
- likely issue labels,
- unknowns that require stems or listening,
- one concrete next test.

Prefer Markdown for human review and JSON for later automation. Keep rendered audio and private session data out of the public repo.
