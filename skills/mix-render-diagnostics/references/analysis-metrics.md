# Analysis Metrics

Use metrics to narrow the search before making listening or A/B decisions. Always note whether a metric is measured, estimated from a tool, or inferred.

## Baseline Checks

- Integrated loudness: compare source, candidate, and reference LUFS.
- Short-term loudness: inspect the loudest phrase and the quietest useful phrase.
- True peak and sample peak: reject candidates that clip or lose required headroom.
- Loudness compensation: compare tonal changes at matched perceived loudness when possible.
- Crest factor / dynamic range: flag candidates that flatten transients or pump audibly.
- Artifact gate: compare a short candidate snippet against a known-good baseline with `scripts/artifact_gate.py`; do not make mix judgments if static/crackle/hash is suspected or reported.
- Section report: use `scripts/render_diagnostic_report.py` when a single integrated value may hide verse/chorus/bridge differences. Use `--section-manifest` for repeatable named sections.

## Spectral Checks

- Low end: check sub buildup, kick/bass masking, and rumble.
- Low mids: watch roughly 180-500 Hz for mud or boxiness.
- Presence: watch roughly 1.5-5 kHz for intelligibility versus harshness.
- Sibilance/edge: watch roughly 5-10 kHz for vocal bite, cymbal hash, and de-essing side effects.
- Air: check high-band openness without hiss or brittle top.

## Diagnostic Module Checks

Use `references/diagnostic-modules.md` when the problem is bigger than a single metric:

- Section-aware diagnostics: compare the same candidate across sparse, dense, loud, late-song, and problem timestamp sections.
- Vocal masking: compare vocal and band stems when available; otherwise call findings mix-level proxies.
- Transient/punch: inspect crest, attack-to-body proxy, transient density, and baseline deltas.
- Reverb/tail buildup: inspect quiet-floor-to-body ratio and sparse-section wash risk.
- Stereo/mono translation: inspect correlation, mono delta, and side-to-mid energy by band.
- Codec delivery: compare a decoded codec round-trip when available; use `scripts/codec_roundtrip.py` when `ffmpeg` is available, and mark codec untested when unavailable.
- Candidate report: produce JSON/Markdown with warnings and one next test per section.

## Optional Essentia Checks

Use Essentia descriptors when bindings are available, especially under WSL/Linux:

- Key/scale and strength: useful for tuning setup and reference sanity checks, but confirm by ear/piano when stakes are high.
- BPM and confidence: useful for comparing song sections and delay/reverb timing.
- Spectral centroid/rolloff/flatness: useful for brightness, cymbal hash, and dense-arrangement comparisons. The current Essentia centroid field is reported as normalized plus approximate Hz.
- Dynamic complexity / EBU loudness fields: useful for identifying over-flattened candidates.

Essentia Python bindings are usually not available in native Windows Python. Use a Linux or WSL Python environment when Essentia descriptors are needed. Do not block a mix pass on Essentia; fall back to the existing librosa, pyloudnorm, and render metrics.

## Task-Specific Scoring

For vocal or speech:

- Intelligibility at matched loudness.
- Sibilance control.
- Low-mid cleanup without thinning.
- Stable dynamics across loud and soft phrases.

For band, drums, or livestream buses:

- Translation against reference.
- Punch and transient preservation.
- Bass/kick relationship.
- Vocal pocket and masking behavior.
- Stereo image stability.

For bass guitar against a reference stem, use `scripts/bass_reference_score.py` when a no-human automated pass is needed. It intentionally does not pick or match song sections; feed it already comparable files or excerpts when section role matters. The score should include:

- Loudness-matched spectral distance across sub, fundamental, bass, mud, low-mid, note/read, edge, and noise bands.
- Low-end balance ratios: `40-80 / 80-160`, `80-160 / 160-300`, and `160-300 / 300-700`.
- Note consistency from short-window RMS variation, with both too-uneven and over-flattened behavior treated as risks.
- Attack/body envelope from onset-adjacent energy, used as a proxy for whether notes speak or feel soft.
- Small-speaker translation proxies: `700 Hz-2 kHz / 40-160 Hz` and `300-700 Hz / 40-160 Hz`.
- Mud penalty for excess `160-300 Hz` and `300-700 Hz` after loudness matching.
- Sub/headroom risk for excess `20-40 Hz`, poor peak headroom, or low-end growth without useful read.
- Compression/pumping proxy from crest-factor loss and short-window RMS over-stability.
- A candidate-reference score on a 0-100 scale plus warnings that can feed the aimpoint grade.

## Ranking Guidance

Prefer candidates that solve the named problem with the least collateral damage. If two candidates score similarly, keep the simpler chain or the one that is easier to reproduce in the user's target delivery environment.

## Training Intake Biases

Training notes from mix education can reinforce useful analysis biases:

- Check gain staging and bus headroom before interpreting tone metrics.
- Grade the static balance separately from plugin tone. A poor fader relationship can masquerade as EQ, compression, or limiter trouble.
- Penalize bus/master compression that reduces chorus lift, transient life, or vocal intelligibility even when loudness and peak numbers look controlled.
- Penalize reverb/delay that improves size while moving the lead lyric backward.
- For mono-first church playback, treat clipping, fatigue, and blurred center information as hard failures.
- Treat user-reported static/crackle as a hard technical failure even when peak, LUFS, spectrum, and mono metrics look normal.
