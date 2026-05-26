# Backlog

## Mix Render Diagnostics

### Optional external feedback experiment

Evaluate whether `mix-render-diagnostics` should support an opt-in external feedback step using Mix Analyzer and/or Waves Online Mastering.

Why:

- Mix Analyzer offers limited free full analyses, currently 3 per month, so use it only on high-value candidates.
- Its frequency, dynamics, stereo, clarity, transient, voice, instrument, and AI-insight modules may provide useful second-opinion evidence.
- Waves Online Mastering may be useful as a black-box mastered-reference comparison, not as primary mix coaching.

First experiment:

1. Choose one near-final stereo worship mix candidate with a known local diagnostic report.
2. Run Mix Analyzer once on the candidate, and only run a second analysis on the reference if the first report is clearly useful.
3. Compare external feedback against local `render_diagnostic_report.py` output.
4. Capture where the external tool agreed, found a new issue, or gave advice that was too generic for live worship.
5. Decide whether to add a formal `external-feedback` reference/workflow to `mix-render-diagnostics`.

Guardrails:

- Make this opt-in only.
- Do not upload private, unreleased, sensitive, spoken-word, or congregation-identifiable audio without explicit approval.
- Do not treat external scores as taste or worship-fit truth.
- Do not let mastering-style advice override lyric clarity, congregational translation, or live-deployment constraints.
