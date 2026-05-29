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
8. Treat render-popup cleanup as part of the render, not a courtesy afterthought. A render is not complete until the render progress/results popup has been closed and a ReaPy/MCP API ping succeeds.
9. For plugin work, verify plugin display names and formatted parameter values in REAPER. Normalized parameters are a fallback representation, not a reliable transfer format by themselves.
10. When changing parameters on a plugin, focus the exact plugin window before setting its parameters so a human shoulder-surfing REAPER can see the change. A hidden/offscreen parameter write is not enough for user-visible automation.
11. Before judging track-FX changes, verify both the individual FX enabled states and the track-wide FX chain switch (`I_FXEN`). A track can show enabled inserts while the whole FX chain is bypassed, causing rendered files to ignore every plugin parameter change.
12. While shoulder-surfing plugin settings, avoid exhaustive formatted-value searches on every parameter. Use known or locally calibrated normalized mappings for routine moves, verify only the important displayed values, and keep visible pauses short enough for the user to follow without waiting through busywork.
13. Separate plugin discovery from mix iteration. Loading plugins, checking whether they instantiate, or cycling through default inserts is discovery only; do not count it as a mix pass.
14. Count a plugin iteration only when it has a stated audible goal, a deliberate chain/settings change, a verified render or session-state artifact, and a short comparison note.
15. When the user asks to iterate toward an aimpoint, every counted REAPER pass must include or hand off enough evidence for an aimpoint grade. If no grade can be produced, label the pass as setup, discovery, or render-only.
16. Before rendering, state the render source being used: real target track, selected track/stem, selected item, master mix, or disposable staging track. Match the source to the task instead of reusing the last successful render helper by habit.
17. Default to the real target track for plugin edits and source-specific iteration when it passes a raw-control render. Use disposable staging tracks only as an explicit fallback, and state why the real track path could not be trusted.
18. For imported/live-capture projects, or any project/track that has previously produced a silent render from a valid source file, proactively refresh the target audio take source before the first raw-control render instead of waiting for another silent-render failure.
19. After an iteration chooses a keeper chain, remove rejected audition plugins from the target track instead of leaving them bypassed. Keep a disabled plugin only when it has a stated future-use reason, such as a live failover or explicit A/B request, and report that reason.
20. Treat temporary loop/time selections as borrowed state. After the final render in a run, restore the previous user selection if one existed; otherwise clear the temporary selection.
21. Keep bulky renders, private projects, and exported commercial plugin presets outside public skill folders and repos.

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
   - When source-staleness has already been seen in the project, refresh target-track audio takes that overlap the test range before the raw-control render: recreate the `PCM_Source` from the same existing file path, preserve take start offset and item timing, then log the refresh as preflight rather than as a failed iteration.

3. Make scoped changes:
   - Use serial FX chains unless the final host supports the same routing.
   - Before setting parameters on a particular FX, select the target track and call `TrackFX_Show(track, fx_index, 1)` or the host-equivalent focus/open command for that exact plugin. If setting several plugins, focus each plugin before its own parameter block.
   - Pause or update the UI briefly after focusing a plugin when the user is shoulder-surfing, then state which plugin and parameter group is being changed.
   - For track FX, confirm the track-wide FX chain is enabled (`I_FXEN=1`) before rendering or grading. If it was off and the user asked for audible plugin work, enable it and log that change.
   - Verify parameter names and formatted values after each important setting change.
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
   - For iteration requests, include a run-log row for each counted pass: iteration id, audible goal, changed plugins/parameters, plugin focus/visibility status, render section/path, verification gates, and grade/status. Also state final FX-chain cleanup and final loop/time selection cleanup status. Use `grade_pending` only when audio judgment is explicitly being handed to another skill or the user.
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
