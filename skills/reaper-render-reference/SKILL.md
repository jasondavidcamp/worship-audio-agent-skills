---
name: reaper-render-reference
description: Use REAPER as an audio staging host to build serial Waves plugin chains, render candidates, compare them against source/reference audio, rank settings, and document/export plugin state for later transfer to Waves SuperRack. Use when iterating mixes, plugin settings, vocal/band/bus processing, reference matching, offline renders, REAPER MCP control, or REAPER-to-SuperRack Waves preset/state transfer.
---

# REAPER Render Reference

## Purpose

Use REAPER as a disposable staging area for fast plugin-setting iteration before committing settings to Waves SuperRack. Keep this skill focused on home/studio auditioning, render analysis, and settings capture; use `superrack-sprk` only when writing back to a `.sprk` session.

## Operating Rules

1. Work in a copy or disposable REAPER project unless the user explicitly asks to modify their working project.
2. Keep test chains serial. Do not use parallel FX chains unless the final target is known to support the same topology.
3. Bypass or disable ReaInsert/live I/O FX during offline rendering so hardware routing does not affect analysis.
4. Match gain before judging tone. Record input loudness, output loudness, peak headroom, and compensation used.
5. Treat objective metrics as triage, not final taste. Use them to narrow candidates, then ask for human taste calls on top contenders.
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
   - Add Waves plugins directly to normal FX slots in final SuperRack order.
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
   - Compare source, candidate, and reference with the metrics in `references/analysis-metrics.md`.
   - For drum or drum-bus compares aimed at a specific artist/reference, read the relevant private aimpoint profile before ranking candidates.
   - Before translating offline DSP prototypes into Waves chains, consult `live-worship-mix-engineering/references/waves-plugin-decision-matrix.md` and any locally generated plugin catalog.
   - Use `scripts/analyze_wav.py` for quick dependency-free WAV peak/RMS/crest checks.
   - Use `scripts/artifact_gate.py` to compare candidate snippets against known-good baseline snippets before scoring. Treat user-reported static/crackle/hash as a hard failure for that render file, but isolate whether the issue is the candidate chain, a specific section, the full-length render, or playback before learning mix taste.
   - For deeper reference/candidate descriptors, use `band-sound-aimpoint/scripts/analyze_reference_audio.py --essentia` when Essentia is available; otherwise rely on the librosa/LUFS fields.
   - Use `scripts/render_time_range.py` for REAPER renders when possible; it sets an explicit range, validates the range, and avoids the local "Nothing to render" / accidental full-project render trap.
   - Rank candidates by target-specific fit and reject obvious failures: clipping, static/crackle/hash, severe loudness drift, harshness, low-mid buildup, pumping, phase damage, or lost intelligibility.

5. Prepare handoff:
   - Export Waves plugin settings from REAPER when possible and record the exact file path.
   - Document plugin-state transfer findings in `references/reaper-superrack-transfer.md`.
   - Once a candidate is approved, use `superrack-sprk` to inspect or patch the SuperRack session; do not let this skill edit `.sprk` files directly.

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
      - plugin: Waves F6-RTA
        slot: 1
        preset_export: C:\path\presets\vocalbus-001-f6.xps
        changed_controls:
          - "Band 3 frequency: 2.8 kHz"
          - "Band 3 range: -3.0 dB"
    analysis:
      lufs_i: -18.4
      true_peak_dbfs: -3.1
      notes: "Closer presence match, slight 300 Hz buildup remains."
    decision: keep
```

## References

- Read `references/analysis-metrics.md` when choosing objective checks or scoring render candidates.
- Read `references/render-safety.md` before rendering from REAPER, especially after changing render bounds, full-song renders, or time selections.
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

Render a known-safe REAPER time range:

```powershell
& "<python>" scripts/render_time_range.py "C:\path\candidate.wav" --start 150 --end 180
```

Extract Waves `.xps` preset files from an `.rpp` into one folder per track/channel:

```powershell
& "<python>" scripts/export_waves_xps_from_rpp.py "C:\path\project.rpp" "C:\path\preset-exports\YYYY-MM-DD.N" --skip-track "Drum Bus"
```

## Related Skills

- Use `superrack-sprk` after a REAPER candidate is approved and the task becomes SuperRack `.sprk` inspection, patching, or validation.
- Use `behringer-wing-snap` only when the workflow involves the WING console, Church routing, SoundGrid card channels, or external insert mapping.
