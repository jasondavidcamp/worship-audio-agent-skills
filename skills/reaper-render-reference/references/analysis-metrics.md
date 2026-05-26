# Analysis Metrics

Use metrics to narrow the search before asking for taste calls. Always note whether a metric is measured, estimated from a tool, or inferred.

## Baseline Checks

- Integrated loudness: compare source, candidate, and reference LUFS.
- Short-term loudness: inspect the loudest phrase and the quietest useful phrase.
- True peak and sample peak: reject candidates that clip or lose required headroom.
- Loudness compensation: compare tonal changes at matched perceived loudness when possible.
- Crest factor / dynamic range: flag candidates that flatten transients or pump audibly.
- Artifact gate: compare a short candidate snippet against a known-good baseline with `scripts/artifact_gate.py`; do not score taste if static/crackle/hash is suspected or reported.

## Spectral Checks

- Low end: check sub buildup, kick/bass masking, and rumble.
- Low mids: watch roughly 180-500 Hz for mud or boxiness.
- Presence: watch roughly 1.5-5 kHz for intelligibility versus harshness.
- Sibilance/edge: watch roughly 5-10 kHz for vocal bite, cymbal hash, and de-essing side effects.
- Air: check high-band openness without hiss or brittle top.

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

## Ranking Guidance

Prefer candidates that solve the named problem with the least collateral damage. If two candidates score similarly, keep the simpler chain or the one that transfers more safely to SuperRack.

## Training Intake Biases

Training notes from mix education can reinforce useful analysis biases:

- Check gain staging and bus headroom before interpreting tone metrics.
- Grade the static balance separately from plugin tone. A poor fader relationship can masquerade as EQ, compression, or limiter trouble.
- Penalize bus/master compression that reduces chorus lift, transient life, or vocal intelligibility even when loudness and peak numbers look controlled.
- Penalize reverb/delay that improves size while moving the lead lyric backward.
- For mono-first church playback, treat clipping, fatigue, and blurred center information as hard failures.
- Treat user-reported static/crackle as a hard technical failure even when peak, LUFS, spectrum, and mono metrics look normal.
