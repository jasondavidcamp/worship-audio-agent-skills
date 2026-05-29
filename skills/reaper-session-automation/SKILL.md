---
name: reaper-session-automation
description: Safely operate REAPER sessions through MCP, ReaPy, or ReaScript. Use when inspecting or modifying REAPER projects, tracks, items, sends, routing, FX chains, plugin parameters, render settings, time selections, short snippet renders, render-window recovery, REAPER MCP setup, .rpp extraction, or REAPER-to-SuperRack handoff.
---

# REAPER Session Automation

## Purpose

Use this skill as the REAPER host-adapter layer. It owns safe REAPER operations: project inspection, track/item/FX manipulation, routing checks, explicit time-range rendering, render-state cleanup, and REAPER-specific transfer artifacts.

This skill does not judge whether a mix sounds good. Once a trustworthy WAV, stem, screenshot, preset export, or project-state report exists, hand the audio-evidence interpretation to `mix-render-diagnostics`, `live-worship-mix-engineering`, `band-sound-aimpoint`, or `waves-live-plugin-chains` as appropriate.

## Operating Rules

1. Treat REAPER as live session state. Inspect before mutating, and preserve unrelated user changes.
2. Prefer explicit ReaScript/ReaPy operations over generic "most recent settings" commands when safety depends on exact bounds, routing, or render source.
3. Do not trust raw MCP project/render helpers when local API behavior has already shown mismatches. Verify with direct ReaScript calls and formatted values.
4. Snapshot or record render settings before changing them, and restore them when a test changes user-visible render state.
5. For small sections, translate the request into explicit `start` and `end` seconds before rendering. Do not trust the current selection length unless it has been read back and reported.
6. For snippets under 60 seconds, never call raw render actions, generic MCP render helpers, or "most recent render settings" commands directly. Use `scripts/render_time_range.py` or a disposable item/take FX workflow, then verify the WAV duration is close to `end - start`.
7. If REAPER shows a render countdown much longer than the requested range, cancel the render and treat the render path as unsafe until bounds are fixed.
8. Close render progress, render complete, and confirmation popups before continuing automation. Verify the MCP/ReaPy API responds before the next operation.
9. For plugin work, verify plugin display names and formatted parameter values in REAPER. Normalized parameters are a fallback representation, not a reliable transfer format by themselves.
10. Separate plugin discovery from mix iteration. Loading plugins, checking whether they instantiate, or cycling through default inserts is discovery only; do not count it as a mix pass.
11. Count a plugin iteration only when it has a stated audible goal, a deliberate chain/settings change, a verified render or session-state artifact, and a short comparison note.
12. When the user asks to iterate toward an aimpoint, every counted REAPER pass must include or hand off enough evidence for an aimpoint grade. If no grade can be produced, label the pass as setup, discovery, or render-only.
13. Before rendering, state the render source being used: master mix, selected track/stem, selected item, or disposable staging track. Match the source to the task instead of reusing the last successful render helper by habit.
14. Keep bulky renders, private projects, and exported commercial plugin presets outside public skill folders and repos.

## Workflow

1. Inspect session state:
   - Confirm the open project path, track count, target track names, current solo/mute states, existing FX, and item media paths.
   - If MCP tools fail with ReaPy attribute or connection errors, read `references/reaper-mcp-setup.md` and probe direct `reapy.reascript_api` availability before changing the project.
   - When running direct probe scripts from a shell, use the active shell's native multiline syntax or a helper script; do not assume Bash heredocs work in PowerShell.

2. Prepare safe automation:
   - For track or FX edits, identify exact track index and plugin display names from REAPER's installed FX cache or current session.
   - If probing plugin availability, label the work as discovery, capture exact plugin names/parameter lists, and remove or bypass trial inserts that are not part of the chosen chain.
   - Before claiming an iteration, list the intended chain, the parameter or preset changes from the previous pass, and the evidence that will be rendered or inspected.
   - For render work, read `references/reaper-render-safety.md` before starting.
   - For REAPER-to-SuperRack artifacts, read `references/reaper-superrack-transfer.md` before exporting or interpreting Waves state.

3. Make scoped changes:
   - Use serial FX chains unless the final host supports the same routing.
   - Verify parameter names and formatted values after each important setting change.
   - Do not cycle plugins on a track as a substitute for parameter work. If no setting changes were made, report "plugin discovery only" and do not advance an iteration counter.
   - Avoid long-running render commands while probing plugin parameters or project state.

4. Render or print evidence only through safe paths:
   - For a requested short sample, choose and state concrete bounds such as `chorus_1 = 93.0-98.0s`; if the user requested "5 seconds," verify `end - start = 5.0` before rendering.
   - When a useful current loop/time selection already exists, read it back first and either use those exact seconds or preserve/restore it after setting a temporary test range.
   - Use `scripts/render_time_range.py` only for explicit master-mix time ranges.
   - For single-source FX iteration, prefer a selected-track/stem render or a disposable staging track from the source media unless the real master path has already produced a non-silent raw control for the same section.
   - For very short checks, prefer disposable media-item/take FX workflows when full master renders are unnecessary.
   - Verify output file existence, non-zero size, duration, and non-silence before offering it as a listening or analysis artifact.

5. Handoff:
   - Return concise session facts: project path, target track, FX chain, settings changed, render path, and any REAPER warnings.
   - For iteration requests, include a run-log row for each counted pass: iteration id, audible goal, changed plugins/parameters, render section/path, verification gates, and grade/status. Use `grade_pending` only when audio judgment is explicitly being handed to another skill or the user.
   - Send rendered WAV comparison and artifact analysis to `mix-render-diagnostics`.
   - Send live Waves chain design to `waves-live-plugin-chains`.
   - Send approved SuperRack `.sprk` inspection or patching to `superrack-session-files`.

## References

- Read `references/reaper-render-safety.md` before any unattended render, time selection, snippet render, routing-sensitive render, or render-window cleanup.
- Read `references/reaper-mcp-setup.md` when checking the local REAPER MCP install, Codex config entry, ReaPy connection, or API mismatch.
- Read `references/reaper-superrack-transfer.md` when exporting Waves settings from REAPER, extracting `.xps` files from `.rpp`, or translating REAPER plugin state into SuperRack.

## Helper Scripts

Render a known-safe REAPER time range:

```powershell
& "<python>" scripts/render_time_range.py "C:\path\candidate.wav" --start 150 --end 180
```

Extract Waves `.xps` preset files from an `.rpp` into one folder per track/channel:

```powershell
& "<python>" scripts/export_waves_xps_from_rpp.py "C:\path\project.rpp" "C:\path\preset-exports\YYYY-MM-DD.N" --skip-track "Drum Bus"
```

## Related Skills

- Use `mix-render-diagnostics` after REAPER has produced trustworthy WAVs or stems.
- Use `waves-live-plugin-chains` when choosing Waves/SuperRack-compatible live plugin chains.
- Use `superrack-session-files` when the task becomes SuperRack `.sprk` or `.xps` file inspection, validation, or patching.
- Use `behringer-wing-snap` when the workflow depends on WING console snapshots, routing, inserts, or SoundGrid card channel mapping.
