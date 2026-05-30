---
name: reaper-session-automation
description: Safely operate REAPER sessions through a configured direct ReaPy/ReaScript Python path, with MCP only as an optional non-sensitive adapter. Use when inspecting or modifying REAPER projects, tracks, items, sends, routing, FX chains, plugin parameters, render settings, time selections, short snippet renders, render-window recovery, REAPER setup, .rpp extraction, or REAPER-to-SuperRack handoff.
---

# REAPER Session Automation

## Purpose

Use this skill as the REAPER host-adapter layer. It owns safe REAPER operations: project inspection, track/item/FX manipulation, routing checks, explicit time-range rendering, render-state cleanup, and REAPER-specific transfer artifacts. Direct ReaPy/ReaScript through the configured REAPER automation Python is the primary control path for any live session, FX, or render work.

This skill does not judge whether a mix sounds good. Once a trustworthy WAV, stem, screenshot, preset export, or project-state report exists, hand the audio-evidence interpretation to `mix-render-diagnostics`, `live-worship-mix-engineering`, `band-sound-aimpoint`, or `waves-live-plugin-chains` as appropriate.

## Operating Rules

1. Treat REAPER as live session state. Inspect before mutating, and preserve unrelated user changes.
2. Require a working direct ReaPy Python path for render-sensitive or FX-sensitive automation. Prefer the private local config `~/.codex/local/reaper-python.txt` when present; otherwise verify the active Python can `import reapy`, import `reapy.reascript_api`, and connect to the open REAPER project before touching live session state.
3. Prefer explicit ReaScript/ReaPy operations over generic "most recent settings" commands when safety depends on exact bounds, routing, or render source.
4. Do not trust raw MCP project/render helpers when local API behavior has already shown mismatches. Verify with direct ReaScript calls and formatted values.
5. If a local MCP helper has a known deterministic API mismatch, such as `module 'reapy.reascript_api' has no attribute 'EnumProjects'`, do not spend the first REAPER call proving it again. Start inspection, FX, and render-sensitive work through direct ReaScript/ReaPy or the skill helper scripts, and mention the MCP bypass only once.
6. Snapshot or record render settings before changing them, and restore them when a test changes user-visible render state.
7. For small sections, translate the request into explicit `start` and `end` seconds before rendering. Do not trust the current selection length unless it has been read back and reported.
8. For snippets under 60 seconds, never call raw render actions, generic MCP render helpers, or "most recent render settings" commands directly. Use `scripts/render_time_range.py` or a disposable item/take FX workflow, then verify the WAV duration is close to `end - start`.
9. If REAPER shows a render countdown much longer than the requested range, cancel the render and treat the render path as unsafe until bounds are fixed.
10. Treat render-popup cleanup as part of the render, not a courtesy afterthought. A render is not complete until the render progress/results popup has been closed and a ReaPy/MCP API ping succeeds.
11. For plugin work, verify plugin display names and formatted parameter values in REAPER. Normalized parameters are a fallback representation, not a reliable transfer format by themselves.
12. When changing parameters on a plugin, focus the exact plugin window before setting its parameters so a human shoulder-surfing REAPER can see the change. A hidden/offscreen parameter write is not enough for user-visible automation.
13. Before judging track-FX changes, verify both the individual FX enabled states and the track-wide FX chain switch (`I_FXEN`). A track can show enabled inserts while the whole FX chain is bypassed, causing rendered files to ignore every plugin parameter change.
14. While shoulder-surfing plugin settings, avoid exhaustive formatted-value searches on every parameter. Use known or locally calibrated normalized mappings for routine moves, verify only the important displayed values, and keep visible pauses short enough for the user to follow without waiting through busywork.
15. Separate plugin discovery from mix iteration. Loading plugins, checking whether they instantiate, or cycling through default inserts is discovery only; do not count it as a mix pass.
16. Count a plugin iteration only when it has a stated audible goal, a deliberate chain/settings change, a verified render or session-state artifact, and a short comparison note.
17. When the user asks to iterate toward an aimpoint, every counted REAPER pass must include or hand off enough evidence for an aimpoint grade. If no grade can be produced, label the pass as setup, discovery, or render-only.
18. Before rendering, state the render source being used: real target track, selected track/stem, selected item, master mix, or disposable staging track. Match the source to the task instead of reusing the last successful render helper by habit.
19. Default to the real target track for plugin edits and source-specific iteration when it passes a raw-control render. Use disposable staging tracks only as an explicit fallback, and state why the real track path could not be trusted.
20. For imported/live-capture projects, or any project/track that has previously produced a silent render from a valid source file, proactively refresh the target audio take source before the first raw-control render instead of waiting for another silent-render failure.
21. For multi-pass iteration, show a compact reviewer-facing thought log for each counted pass so the human can follow the goal, change, evidence, gates, grade, reasoning, and next move.
22. After an iteration chooses a keeper chain, remove rejected audition plugins from the target track instead of leaving them bypassed. Keep a disabled plugin only when it has a stated future-use reason, such as a live failover or explicit A/B request, and report that reason.
23. Treat temporary loop/time selections as borrowed state. After the final render in a run, restore the previous user selection if one existed; otherwise clear the temporary selection.
24. Keep bulky renders, private projects, and exported commercial plugin presets outside public skill folders and repos.
25. For Waves `.xps` round trips, use `waves-live-plugin-chains` for portable `.xps` shape/transfer intent, then use this skill for live REAPER execution. Exporting a Waves plugin state from a live REAPER FX chunk or `.rpp` is supported. Importing a `.xps` into REAPER is successful only when REAPER's displayed/formatted plugin parameters verify the change; an API-accepted VST chunk write alone is not proof.

## Workflow

1. Inspect session state:
   - Resolve the REAPER automation interpreter: read `~/.codex/local/reaper-python.txt` if it exists, otherwise use the active Python only after it passes the direct ReaPy probe in `references/reaper-mcp-setup.md`.
   - Prefer `scripts/resolve_reaper_python.py --verify` for that preflight when shell access is available; it reports the configured interpreter without exposing workstation paths in public skill files.
   - If no direct ReaPy Python can connect to the open REAPER project, stop render-sensitive or FX-sensitive automation and report the missing setup. Do not use a failing MCP wrapper as a substitute for counted mix iteration.
   - Confirm the open project path, track count, target track names, current solo/mute states, existing FX, and item media paths.
   - If this deployment has a known MCP/ReaPy wrapper mismatch, especially the `EnumProjects` attribute error, skip MCP project/list helpers for the initial inspection and use direct ReaScript/ReaPy immediately.
   - If direct ReaPy fails, read `references/reaper-mcp-setup.md` and fix or configure the REAPER automation Python before continuing. Do not explore MCP workarounds for render-sensitive or FX-sensitive tasks.
   - When running direct probe scripts from a shell, use the active shell's native multiline syntax or a helper script; do not assume Bash heredocs work in PowerShell.

2. Prepare safe automation:
   - For track or FX edits, identify exact track index and plugin display names from REAPER's installed FX cache or current session.
   - If probing plugin availability, label the work as discovery, capture exact plugin names/parameter lists, and remove or bypass trial inserts that are not part of the chosen chain.
   - Before claiming an iteration, list the intended chain, the parameter or preset changes from the previous pass, and the evidence that will be rendered or inspected.
   - Before multi-pass Waves plugin iteration, ask `waves-live-plugin-chains` for a source-specific candidate palette and include topology variety unless the user explicitly asks for refinement only. Prior approved/exported/native chains for the same source are evidence anchors, not taste defaults; import, verify, render, and score at least one early when available, or state why none applies.
   - For render work, read `references/reaper-render-safety.md` before starting.
   - For REAPER-to-SuperRack artifacts, read `references/reaper-superrack-transfer.md` before exporting or interpreting Waves state.
   - For Waves `.xps` work, ask `waves-live-plugin-chains` to identify the artifact shape and transfer intent. Use this skill for live REAPER export/import attempts, and `superrack-session-files` only for SuperRack-specific `.sprk` or rack-chain validation.
   - When exporting a chain as separate single-plugin Waves `.xps` files, preserve chain order in the filenames with two-digit prefixes such as `01 F6-RTA Mono.xps`, `02 RCompressor Mono.xps`. The preset name inside the file can remain the plugin/preset display name; the filename carries slot order for humans and later imports.
   - When source-staleness has already been seen in the project, refresh target-track audio takes that overlap the test range before the raw-control render: recreate the `PCM_Source` from the same existing file path, preserve take start offset and item timing, then log the refresh as preflight rather than as a failed iteration.

3. Make scoped changes:
   - Use serial FX chains unless the final host supports the same routing.
   - Before setting parameters on a particular FX, select the target track and call `TrackFX_Show(track, fx_index, 1)` or the host-equivalent focus/open command for that exact plugin. If setting several plugins, focus each plugin before its own parameter block.
   - Pause or update the UI briefly after focusing a plugin when the user is shoulder-surfing, then state which plugin and parameter group is being changed.
   - For track FX, confirm the track-wide FX chain is enabled (`I_FXEN=1`) before rendering or grading. If it was off and the user asked for audible plugin work, enable it and log that change.
   - Verify parameter names and formatted values after each important setting change.
   - When importing a Waves plugin `.xps` back into REAPER, first validate that it is a single-plugin preset rather than a SuperRack rack-chain preset.
   - Prefer the native Waves UI import path when the plugin window is visible or can be safely focused: add/focus the Waves plugin, drag the `.xps` file from Explorer onto the Waves plugin UI, then verify formatted REAPER values or an exported round-trip before rendering. This is usually easier to automate than the menu path because Waves' OpenGL UI hides internal menu items from Windows UI Automation.
   - If drag/drop is unavailable, use the Waves preset browser/menu path: open the Waves preset menu, choose `Load -> Preset File`, select the `.xps`, then verify formatted values.
   - When the user asks to compare or iterate against an existing `.xps` chain, do not reconstruct it by hand first. Use native import when available, verify the loaded state, render the same comparison section, and score it as a real candidate before spending passes on new manual settings.
   - Use `scripts/apply_waves_xps_to_reaper.py --dry-run` before mutating the session when using automation. If native UI import is not available, use the helper's `auto` mapped import for supported Waves plugins such as F6/F6-RTA, RComp, and SSL EV2.
   - If REAPER accepts a `vst_chunk` write but formatted values do not change, report the import as unverified/failed and use native Waves UI import or a plugin-specific exposed-parameter mapping before rendering. Do not retry the same chunk path repeatedly.
   - Do not spend a shoulder-surfed iteration binary-searching every parameter to exact display values. Calibrate a small mapping when needed, set routine values directly, and verify the handful of controls that matter musically.
   - If the plugin cannot be focused or its UI cannot be made visible, say so and mark the change as non-visible automation rather than implying the human could watch it happen.
   - Do not cycle plugins on a track as a substitute for parameter work. If no setting changes were made, report "plugin discovery only" and do not advance an iteration counter.
   - Avoid long-running render commands while probing plugin parameters or project state.
   - At the end of a plugin iteration, clean the target track's FX chain so it contains the chosen keeper plugins only. Delete rejected audition plugins that are merely bypassed or disabled, unless the user asked to keep them or there is a named operational reason.

4. Render or print evidence only through safe paths:
   - For a requested short sample, choose and state concrete bounds such as `chorus_1 = 93.0-98.0s`; if the user requested "5 seconds," verify `end - start = 5.0` before rendering.
   - Snapshot the current loop/time selection before setting a temporary render range. When a useful current loop/time selection already exists, read it back first and either use those exact seconds or restore it after setting a temporary test range.
   - Use `scripts/render_time_range.py` only for explicit master-mix time ranges.
   - For single-source FX iteration, first try the real target track: selected-track/stem render, selected-item render, or master mix of only that track, as appropriate. Continue on the real track only after a raw-control render for the same section passes duration, non-silence, and popup-cleanup gates.
   - In a known stale-source session, run the target-take refresh before that raw-control render. The raw-control render should then validate the refreshed path, not rediscover the same silent-render problem.
   - Use a disposable staging track only when the real target track render fails verification, the session track path is known untrusted, or the user explicitly wants a non-mutating audition. Log the failure or reason before using staging.
   - For very short checks, prefer disposable media-item/take FX workflows when full master renders are unnecessary.
   - Immediately after every render command, close the render progress/results popup. When using custom ReaScript instead of `scripts/render_time_range.py`, copy or call that script's render-window cleanup routine before analysis or the next action.
   - After the last render in the run, restore the previous loop/time selection if one existed; if the selection was created only for the render, clear it with `GetSet_LoopTimeRange2(..., 0.0, 0.0, ...)`.
   - Verify output file existence, non-zero size, duration, non-silence, popup cleanup, and loop/time selection cleanup before offering it as a listening or analysis artifact.
   - For plugin-iteration batches, compare candidate files against a baseline or prior pass at least with a simple sample-difference check. If multiple candidates are byte-identical after deliberate FX moves, stop and inspect render source, track-wide FX enable, plugin bypass/offline state, and routing before continuing.

5. Handoff:
   - Return concise session facts: project path, target track, FX chain, settings changed, render path, and any REAPER warnings.
   - For iteration requests, state the winning iteration explicitly in the summary before or after the per-pass logs: winner id/name, grade, and whether it was applied to the target track.
   - For iteration requests, include a run-log row for each counted pass: iteration id, audible goal, changed plugins/parameters, plugin focus/visibility status, render section/path, verification gates, and grade/status. Prefer this reviewer-facing shape for each pass:

```text
Iteration 2
Goal: tighter bass support without masking vocal/piano
Change: F6 cut 180 Hz -2.0 dB; RComp 3:1, slower release
Focus: F6 visible, RComp visible
Render: bass_check_02 = 142.500-147.500s
Gates: duration pass, non-silent pass, clipping pass, popup closed, selection restored/cleared
Aimpoint grade: 68/100, medium confidence
Why: low-mid cloud improved, but attack is still soft and level jumps on chorus push
Next: add gentler leveling before EQ; avoid more low-end boost
```

   - Also state final FX-chain cleanup and final loop/time selection cleanup status. Use `grade_pending` only when audio judgment is explicitly being handed to another skill or the user.
   - Send rendered WAV comparison and artifact analysis to `mix-render-diagnostics`.
   - Send live Waves chain design to `waves-live-plugin-chains`.
   - Send approved SuperRack `.sprk` inspection or patching to `superrack-session-files`.

## References

- Read `references/reaper-render-safety.md` before any unattended render, time selection, snippet render, routing-sensitive render, or render-window cleanup.
- Read `references/reaper-mcp-setup.md` when checking the local direct ReaPy install, optional REAPER MCP bridge, Codex config entry, ReaPy connection, or API mismatch.
- Read `references/reaper-superrack-transfer.md` when exporting Waves settings from REAPER, extracting `.xps` files from `.rpp`, or translating REAPER plugin state into SuperRack. Read `waves-live-plugin-chains/references/waves-xps-transfer.md` first when the question is about portable `.xps` shape, chain intent, or REAPER/SuperRack transfer planning.

## Helper Scripts

Resolve the configured REAPER automation Python, optionally verifying the open project:

```powershell
& "python" scripts/resolve_reaper_python.py --verify --pretty
```

Render a known-safe REAPER time range:

```powershell
& "<reaper-python>" scripts/render_time_range.py "C:\path\candidate.wav" --start 150 --end 180
```

Extract Waves `.xps` preset files from an `.rpp` into one folder per track/channel:

```powershell
& "<reaper-python>" scripts/export_waves_xps_from_rpp.py "C:\path\project.rpp" "C:\path\preset-exports\YYYY-MM-DD.N" --skip-track "Drum Bus"
```

Exports use ordered filenames such as `01 PSE Mono.xps`, `02 F6-RTA Mono.xps`.

Export the current Waves FX state from the open REAPER session:

```powershell
& "<reaper-python>" scripts/export_live_waves_xps.py --track "Bass" "C:\path\preset-exports\Bass"
```

The live export helper also uses two-digit REAPER FX order prefixes by default.

Validate or attempt a single-plugin Waves `.xps` import into REAPER. Treat a non-zero result as a safety stop, not a shell failure to work around:

```powershell
& "<reaper-python>" scripts/apply_waves_xps_to_reaper.py "C:\path\F6 Mono.xps" --track "Bass" --fx-index 0 --dry-run
& "<reaper-python>" scripts/apply_waves_xps_to_reaper.py "C:\path\F6 Mono.xps" --track "Bass" --fx-index 0 --method auto
```

When a human can see the plugin UI, the preferred `.xps` import is the native Waves drag/drop path: focus the exact FX window, drag the `.xps` file onto the Waves plugin UI, then read back the important formatted parameters. The Waves menu path (`Load -> Preset File`) is the second native option.

## Related Skills

- Use `mix-render-diagnostics` after REAPER has produced trustworthy WAVs or stems.
- Use `waves-live-plugin-chains` when choosing Waves/SuperRack-compatible live plugin chains or planning portable Waves `.xps` preset/chain transfer.
- Use `superrack-session-files` when the task becomes SuperRack `.sprk` or `.xps` file inspection, validation, or patching.
- Use `behringer-wing-snap` when the workflow depends on WING console snapshots, routing, inserts, or SoundGrid card channel mapping.
