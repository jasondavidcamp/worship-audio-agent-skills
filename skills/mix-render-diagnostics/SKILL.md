---
name: mix-render-diagnostics
description: Analyze rendered audio, stems, references, and delivery exports to diagnose mix issues and guide repeatable next tests. Use when comparing existing WAV/FLAC/MP3/AAC render files, source/candidate/reference audio, section-level worship mix renders, stems, vocal/band/drum/bus/livestream files, artifact gates, loudness/spectrum/dynamics/mono/codec checks, vocal masking, transient punch, reverb tail buildup, candidate reports, or delivery-risk analysis.
---

# Mix Render Diagnostics

## Purpose

Use this skill to turn rendered audio evidence into repeatable diagnostic decisions: what changed, what failed, what still needs listening, and what next reversible test should be run.

This skill starts after audio files exist. It does not operate DAWs, modify plugin chains, manage REAPER render settings, or edit SuperRack sessions. If the source is still inside a host, first use the relevant host skill to create trustworthy WAVs or stems; for REAPER work use `reaper-session-automation`.

This skill does not own emotional target language or live-chain design. Translate subjective reports into measurable or inspectable hypotheses such as clipping, loudness drift, flattened crest factor, transient loss, high-band excess, low-mid buildup, mono loss, side-energy imbalance, phase damage, codec artifacts, excessive reverb tail, or lost intelligibility.

## Operating Rules

1. Treat input renders, references, and stems as read-only evidence.
2. Match gain before judging tone. Record input loudness, output loudness, peak headroom, and compensation used.
3. Treat metrics as gates and proxies, not aesthetic scores. Report what changed, what failed, and the next reversible test to run.
4. Compare like sections whenever possible: verse to verse, chorus to chorus, dense to dense, sparse to sparse.
5. Keep bulky render output outside the skill repo, preferably on a large local audio/render volume. Do not commit rendered audio, private sessions, or exported commercial plugin presets.
6. Reject obvious failures before taste calls: clipping, static/crackle/hash, severe loudness drift, harshness, low-mid buildup, pumping, phase damage, mono collapse, or lost intelligibility.
7. Do not learn mix-decision rules from any batch the user describes as static-y, crackly, corrupted, or horrible. Isolate the artifact source first.
8. Use user taste calls and aimpoint profiles only after the render passes basic artifact, headroom, and non-silence checks.
9. For candidate batches or repeated iterations, produce a scored run log. Each candidate needs gates, metric movement, aimpoint grade, confidence, grade reason, and next test.

## Workflow

1. Define the evidence:
   - Source audio: dry source, raw stem, or prior/current mix render.
   - Candidate audio: one or more processed renders to compare.
   - Reference audio: approved mix, target artist track, prior service render, or user-approved candidate.
   - Scope: vocal, band bus, drums, livestream, full mix, or another named target.
   - Sections: named timestamps for verse, chorus, bridge, loud section, sparse section, or problem phrase.

2. Prepare comparisons:
   - Prefer a section manifest when the same sections will be reused across candidates.
   - Rendered candidates should already be trustworthy WAVs or stems. If a file is missing, silent, the wrong duration, or host-render provenance is uncertain, send the task back to the host automation skill before analysis.
   - Always include a known-good baseline when screening a candidate batch.
   - For delivery-risk checks, run a codec roundtrip only after the WAV passes basic render/artifact/headroom checks.

3. Analyze:
   - Use `scripts/analyze_wav.py` for quick dependency-free WAV peak/RMS/crest checks.
   - Use `scripts/artifact_gate.py` to compare candidate snippets against known-good baseline snippets before A/B comparison.
   - For section-aware diagnostics, vocal masking, transient/punch, reverb/tail, stereo/mono, codec, or candidate report work, read `references/diagnostic-modules.md` and run `scripts/render_diagnostic_report.py`.
   - Compare source, candidate, and reference with the metrics in `references/analysis-metrics.md`.
   - For deeper reference/candidate descriptors, use `band-sound-aimpoint/scripts/analyze_reference_audio.py --essentia` when Essentia is available; otherwise rely on the existing librosa/LUFS fields.

4. Decide:
   - Rank candidates by target-specific fit and reject objective failures first.
   - Grade each real candidate pass on the active aimpoint's 0-100 scale, and include confidence plus the reason the score changed.
   - Explain metric movement in audible terms: louder/softer, brighter/darker, more/less low-mid cloud, more/less transient punch, wider/narrower, more/less tail buildup.
   - When a render fails, prescribe one concrete next test: reduce or bypass the suspected processor, render the same time range, and compare the same metrics again.
   - When a candidate passes objective checks but the choice is subjective, ask for a focused A/B taste call.

5. Prepare handoff:
   - Keep the report tied to file paths, section names, and exact timestamps.
   - State what is evidence, what is inference, and what still needs listening.
   - Hand DAW/session changes to the relevant host skill and SuperRack file edits to `superrack-session-files`.

## Run Log Shape

For each comparison, keep a compact run log:

```yaml
target: Vocal Bus
source_audio: C:\path\dry-vocal.wav
baseline_audio: C:\path\baseline.wav
reference_audio: C:\path\approved-vocal.wav
sample_rate: 48000
sections:
  - chorus_1: 90.0-120.0
candidates:
  - id: vocalbus-001
    render: C:\path\renders\vocalbus-001.wav
    analysis:
      lufs_i: -18.4
      true_peak_dbfs: -3.1
      crest_db: 12.2
      gates:
        clipping: pass
        artifact_gate: pass
      notes: "Presence range closer to reference; 300 Hz remains elevated."
      aimpoint_grade: 71
      confidence: medium
      grade_reason: "Closer to the reference in presence and level stability, but low-mid buildup still masks the pocket."
      movement: closer
      next_test: "Try 1.5 dB less 300 Hz in the processor chain and rerender chorus_1."
    decision: keep_for_listening
```

## References

- Read `references/analysis-metrics.md` when choosing objective checks and comparing render candidates.
- Read `references/diagnostic-modules.md` when diagnosing section-specific failures, vocal masking, transient loss, tail buildup, stereo/mono translation, codec delivery, or candidate report shape.
- Read `references/section-manifest.md` when a song, service, or candidate set needs repeatable named sections.
- Read `references/codec-delivery.md` when checking livestream, video, podcast, social, or mastered-export codec risk.

## Helper Scripts

Run a quick WAV metric pass:

```powershell
& "<python>" scripts/analyze_wav.py "<render.wav>" --pretty
```

Run a static/artifact gate against a known-good snippet:

```powershell
& "<python>" scripts/artifact_gate.py "<candidate-snippet.wav>" --baseline "<known-good-snippet.wav>" --pretty
```

Generate a section-aware diagnostic report:

```powershell
& "<python>" scripts/render_diagnostic_report.py --candidate "C:\path\candidate.wav" --baseline "C:\path\baseline.wav" --reference "C:\path\reference.wav" --section "verse:45:75" --section "chorus:90:120" --md-output "C:\path\report.md" --json-output "C:\path\report.json"
```

Generate the same report from a section manifest:

```powershell
& "<python>" scripts/render_diagnostic_report.py --candidate "C:\path\candidate.wav" --baseline "C:\path\baseline.wav" --section-manifest "C:\path\sections.yaml" --md-output "C:\path\report.md"
```

Run a codec roundtrip and optional delivery-risk report:

```powershell
& "<python>" scripts/codec_roundtrip.py "C:\path\candidate.wav" --codec aac --bitrate 192k --section-manifest "C:\path\sections.yaml" --report-md "C:\path\codec-report.md" --pretty
```

## Related Skills

- Use `reaper-session-automation` when the work involves REAPER projects, tracks, FX, render settings, snippets, `.rpp` files, or REAPER-to-SuperRack exports.
- Use `live-worship-mix-engineering` to translate diagnostics into brand-neutral live worship mix moves.
- Use `band-sound-aimpoint` when subjective taste, artist reference targets, or worship style aimpoints drive the decision.
- Use `waves-live-plugin-chains` when the question is which Waves plugin or chain to try.
- Use `superrack-session-files` when the task becomes SuperRack `.sprk` inspection, patching, or validation.
