---
name: mix-render-diagnostics
description: Analyze rendered audio, staged mix candidates, stems, references, and delivery exports to diagnose mix issues and guide repeatable next tests. Use when comparing source/candidate/reference WAVs, section-level worship mix renders, REAPER-staged plugin chains, vocal/band/drum/bus/livestream processing, artifact gates, loudness/spectrum/dynamics/mono/codec checks, vocal masking, transient punch, reverb tail buildup, candidate reports, Waves chain auditioning, or REAPER-to-SuperRack preset transfer.
---

# Mix Render Diagnostics

## Purpose

Use this skill to turn rendered audio evidence into repeatable diagnostic decisions: what changed, what failed, what still needs listening, and what next reversible test should be run.

REAPER remains the primary staging host for plugin-setting iteration, but it is a host adapter inside this broader skill. Keep REAPER-specific learnings in the REAPER references, and keep general mix diagnostics in `analysis-metrics.md` and scripts that work on WAV files from any source.

This skill does not score emotional impact, immersion, or worship feel. Translate subjective reports into measurable or inspectable hypotheses such as clipping, loudness drift, flattened crest factor, transient loss, high-band excess, low-mid buildup, mono loss, side-energy imbalance, phase damage, codec artifacts, excessive reverb tail, or lost intelligibility.

## Operating Rules

1. Work in a copy or disposable REAPER project unless the user explicitly asks to modify their working project.
2. Keep test chains serial. Do not use parallel FX chains unless the final target is known to support the same topology.
3. Bypass or disable ReaInsert/live I/O FX during offline rendering so hardware routing does not affect analysis.
4. Match gain before judging tone. Record input loudness, output loudness, peak headroom, and compensation used.
5. Treat metrics as gates and proxies, not aesthetic scores. Report what changed, what failed, and the next reversible test to run.
6. Preserve plugin versions, mono/stereo format, sample rate, oversampling, and latency mode in run notes.
7. Prefer exported Waves preset/settings files when transferring to SuperRack. Use REAPER normalized parameters only as a fallback or diagnostic view.
8. Before any master-mix render or listening check, verify the routing matrix has the master routed to output 1/2 (`MASTERHWOUT 0 0 1...`, stereo/MC output 1). Remove direct per-track hardware/ReaRoute outputs unless they are deliberately part of the test; keep normal track-to-master parent routing. A blank master hardware output can produce silent renders, and per-track hardware outputs can create misleading monitoring/routing behavior.
9. Store bulky audio render output outside the skill repo, preferably on a large local audio/render volume. Do not commit rendered audio, private sessions, or exported commercial plugin presets.

## Workflow

1. Define the target:
   - Source audio: dry or current mix render.
   - Reference audio: approved mix, target artist track, prior service render, or user-approved candidate.
   - Processing scope: vocal, band bus, drums, livestream, full mix, or another named target.

2. Stage in REAPER:
   - Create or locate a staging track for the target.
   - Add plugins directly to normal FX slots in the final target order.
   - Disable ReaInsert and other hardware/live-return effects for test renders.
   - Confirm the master has a stereo hardware send to output 1/2 before judging playback or printing a master render.
   - Clear unwanted per-track `HWOUT` routes in the routing matrix so the only hardware output is the master output 1/2 route; do not remove the normal diagonal parent/master sends.
   - Use time selections or regions for repeatable snippets: verse, chorus, loud section, sparse section, or problem phrase.

3. Generate candidates:
   - Change one hypothesis at a time for careful work, or batch broad sweeps when searching.
   - Keep every candidate serial and renderable offline.
   - Log plugin order, plugin display names, parameter changes, preset filenames, and notes.

4. Render and analyze:
   - Render each candidate to a unique file path.
   - Prefer an explicit output path outside the repo, such as `<audio-render-root>/<run-name>`.
   - Do not trust generic `render_project`/default render bounds for full-song bounces. Use an explicit time selection from project media start/end, force `RENDER_SETTINGS=0` for master mix, force `RENDER_BOUNDSFLAG=2`, verify master output 1/2 routing, then verify the file exists and is non-zero before proceeding.
   - Always render a raw-control snippet before Waves/plugin candidates. If the control is silent even though the source WAV has audio, refresh the take's PCM source from the same file path or use a disposable staging track, then rerender the control before continuing.
   - Before a compare batch, render known-good baseline snippets and candidate snippets for at least three sections: loud/dense, mid-song, and late-song. Do not print full-length candidates until the multi-section snippet batch passes the artifact gate.
   - For short clip analysis, prefer a temporary 30-second media item plus "apply track/take FX to item" over full project render. Copy the resulting WAV to the analysis folder and delete the temporary track/item.
   - For section-aware diagnostics, vocal masking, transient/punch, reverb/tail, stereo/mono, codec, or candidate report work, read `references/diagnostic-modules.md` and run `scripts/render_diagnostic_report.py`.
   - For repeated section comparisons, use a section manifest instead of retyping section timestamps.
   - For delivery-risk checks, run a codec roundtrip only after the WAV passes basic render/artifact/headroom checks.
   - Compare source, candidate, and reference with the metrics in `references/analysis-metrics.md`.
   - For drum or drum-bus compares aimed at a specific artist/reference, read the relevant deployment-local aimpoint profile only for target tolerances and reference ranges. Keep those private profiles outside public skill repositories.
   - Before translating offline DSP prototypes into Waves chains, use `waves-live-plugin-chains` and any locally generated Waves plugin catalog.
   - Use `scripts/analyze_wav.py` for quick dependency-free WAV peak/RMS/crest checks.
   - Use `scripts/artifact_gate.py` to compare candidate snippets against known-good baseline snippets before A/B comparison. Treat user-reported static/crackle/hash as a hard failure for that render file, but isolate whether the issue is the candidate chain, a specific section, the full-length render, or playback before making any mix judgment.
   - For deeper reference/candidate descriptors, use `band-sound-aimpoint/scripts/analyze_reference_audio.py --essentia` when Essentia is available; otherwise rely on the librosa/LUFS fields.
   - Use `scripts/render_time_range.py` for REAPER renders when possible; it sets an explicit range, validates the range, and avoids the local "Nothing to render" / accidental full-project render trap.
   - Rank candidates by target-specific fit and reject obvious failures: clipping, static/crackle/hash, severe loudness drift, harshness, low-mid buildup, pumping, phase damage, or lost intelligibility.
   - When a render fails, prescribe one concrete next test: reduce or bypass the suspected processor, render the same time range, and compare the same metrics again.

5. Prepare handoff:
   - Export Waves plugin settings from REAPER when possible and record the exact file path.
   - Document plugin-state transfer findings in `references/reaper-superrack-transfer.md`.
   - Once a candidate is approved, use `superrack-session-files` to inspect or patch the SuperRack session; do not let this skill edit `.sprk` files directly.

## Run Log Shape

For each iteration, keep a compact run log:

```yaml
target: Vocal Bus
source_audio: C:\path\dry-vocal.wav
reference_audio: C:\path\approved-vocal.wav
sample_rate: 48000
region: chorus_1
candidates:
  - id: vocalbus-001
    render: C:\path\renders\vocalbus-001.wav
    chain:
      - plugin: Dynamic EQ
        slot: 1
        preset_export: C:\path\presets\vocalbus-001-f6.xps
        changed_controls:
          - "Band 3 frequency: 2.8 kHz"
          - "Band 3 range: -3.0 dB"
    analysis:
      lufs_i: -18.4
      true_peak_dbfs: -3.1
      gates:
        clipping: pass
        artifact_gate: pass
      notes: "Presence range closer to reference; 300 Hz remains elevated."
      next_test: "Try 1.5 dB dynamic cut around 300 Hz and rerender chorus_1."
    decision: keep_for_listening
```

## References

- Read `references/analysis-metrics.md` when choosing objective checks and comparing render candidates.
- Read `references/diagnostic-modules.md` when diagnosing section-specific failures, vocal masking, transient loss, tail buildup, stereo/mono translation, codec delivery, or candidate report shape.
- Read `references/section-manifest.md` when a song, service, or candidate set needs repeatable named sections.
- Read `references/codec-delivery.md` when checking livestream, video, podcast, social, or mastered-export codec risk.
- Read `references/reaper-render-safety.md` before rendering from REAPER, especially after changing render bounds, full-song renders, or time selections.
- Read and update `references/reaper-superrack-transfer.md` when learning how a Waves setting exported from REAPER imports into SuperRack.
- Read `references/reaper-mcp-setup.md` when checking the local REAPER MCP install, Codex config entry, or reapy connection requirements.

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

Render a known-safe REAPER time range:

```powershell
& "<python>" scripts/render_time_range.py "C:\path\candidate.wav" --start 150 --end 180
```

Extract Waves `.xps` preset files from an `.rpp` into one folder per track/channel:

```powershell
& "<python>" scripts/export_waves_xps_from_rpp.py "C:\path\project.rpp" "C:\path\preset-exports\YYYY-MM-DD.N" --skip-track "Drum Bus"
```

## Related Skills

- Use `live-worship-mix-engineering` to translate diagnostics into brand-neutral live worship mix moves.
- Use `waves-live-plugin-chains` when the question is which Waves plugin or chain to try.
- Use `superrack-session-files` after a REAPER candidate is approved and the task becomes SuperRack `.sprk` inspection, patching, or validation.
- Use `behringer-wing-snap` only when the workflow involves the WING console, church routing, SoundGrid card channels, or external insert mapping.
