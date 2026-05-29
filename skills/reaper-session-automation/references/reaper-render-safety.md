# REAPER Render Safety And Local Automation Lessons

Use this note before rendering through `reapy`, REAPER MCP, or any unattended REAPER automation.

## REAPER-Specific Lessons Learned

- Store bulky render output outside the skill repo, preferably on a dedicated audio/render volume. Do not commit rendered audio or generated preset exports.
- The generic MCP helper assumption that `RENDER_BOUNDSFLAG=1` means "time selection" was wrong in the active REAPER 7.61 setup.
- In the tested automation path, `RENDER_BOUNDSFLAG=2` correctly rendered the active time selection. Re-verify this after REAPER or API changes.
- `RENDER_BOUNDSFLAG=0` produced a "Nothing to render!" error when no custom render range was set.
- A project can inherit `RENDER_SETTINGS=32` / `RENDER_BOUNDSFLAG=4` from selected-media-item rendering. With no selected items this raises "Nothing to render!" even if a valid time selection was set. Force `RENDER_SETTINGS=0` for master mix and `RENDER_BOUNDSFLAG=2` for time selection before command `41824`.
- An accidental wrong render-bounds value can start a full 16-minute render even when a 30-second clip was intended.
- For requested snippets under 60 seconds, never rely on generic MCP render helpers, raw render actions, or "most recent render settings" actions. Use `scripts/render_time_range.py` or a disposable media-item apply-FX workflow, then confirm the WAV duration is close to `end - start`.
- If a render dialog says "Rendering to file..." for much longer than the requested range should take, stop/cancel the render and close any "Render Incomplete" prompt instead of waiting.
- After every render or render batch, close any REAPER render-complete, render-progress, or confirmation popup before continuing. Prefer focusing REAPER and sending `Esc`, then verify the reapy/MCP API responds. Do not leave render result windows open for the user.
- If REAPER asks "Loop/time selections locked, unlock now and remove?", cancel/escape the prompt unless the user explicitly asked to unlock or remove loop/time selections. Do not click `OK` as part of render cleanup.
- Imported or live-capture projects can have missing or unexpected master hardware outputs while tracks retain direct hardware/ReaRoute outputs. Before playback or render checks, verify the master has a stereo hardware send to output 1/2 (`I_DSTCHAN=0`, `I_SRCCHAN=0`, unity volume, unmuted), clear unwanted per-track hardware/ReaRoute outputs, keep the normal track-to-master parent sends, and set the render source to master mix. File size alone is not enough; always measure non-silence after render.
- If track items point at valid WAV files but master renders are silent or near plugin-noise level, check whether REAPER's PCM source handle is stale/offline. Rebinding the take to a fresh `PCM_Source_CreateFromFile(<same wav path>)` can restore normal rendering without copying tracks. Confirm with a short raw-control render before adding plugin candidates.
- When writing track Volume envelope points through ReaScript, do not pass raw linear volume values directly unless the envelope scaling mode has been checked. In one tested REAPER 7.61 setup, track Volume envelopes used scaling mode `1`; use `GetEnvelopeScalingMode` plus `ScaleToEnvelopeMode` before `InsertEnvelopePoint`. Passing raw values like `1.0` into a scaled Volume envelope can render the track nearly silent. After creating a Volume envelope, REAPER may move the visible fader to `0 dB`; the envelope then carries the fader-equivalent level.

## Required Render Pattern

For snippets and full-song bounces:

1. Compute or choose explicit `start` and `end` seconds.
2. Reject the render if `end <= start`.
3. Set REAPER's loop/time selection with `GetSet_LoopTimeRange2(..., start, end, ...)`.
4. Set output directory with `RENDER_FILE` and filename stem with `RENDER_PATTERN`.
5. Set `RENDER_SETTINGS=0` for master mix and `RENDER_BOUNDSFLAG=2` for the time selection.
6. Render with command `41824`.
7. Verify the expected file exists and has non-zero size.
8. Verify the rendered WAV duration is close to `end - start`; if a 5-second request produces a long render or long file, delete/reject it and fix render bounds before continuing.
9. Verify it is non-silent with peak/RMS analysis before offering it as a listening sample.
10. If the raw-control render is silent while the source WAV is not, refresh/rebind the media sources or create a disposable staging track from the same file, then rerender the control.
11. Analyze peak/LUFS before making further gain moves.
12. Close render-complete/progress/confirmation popups, then run a quick API ping before starting the next render or returning control to the user.

For a "full project" render, do not use an ambiguous whole-project bounds mode. Instead, find the max media-item end time and render `0` to that value as a time selection.

## Short Section Selection Pattern

For user requests like "render 5 seconds," "just the chorus hit," or "a quick bass check":

1. Convert the musical request into concrete seconds before touching render commands.
2. If using the edit cursor, marker, item edge, or existing loop/time selection as the anchor, read back the actual position in seconds.
3. Compute `end = start + requested_duration`; for "5 seconds," reject any range whose measured duration is not `5.0` seconds before render.
4. State or log the exact range before rendering: e.g. `bass_check_01 = 142.500-147.500s`.
5. Set the loop/time selection through ReaScript/ReaPy, then immediately read it back and verify the same `start`/`end`.
6. After rendering, verify the WAV duration matches the requested duration within a small tolerance before opening, analyzing, or offering the file.
7. If any render window countdown implies a longer range, cancel immediately and fix the bounds.

## Headroom Rule

After any bus/master/plugin gain change:

- Render at least one loud 30-second section.
- Reject the pass if sample peak reaches `0.0 dBFS` or visible clipping appears.
- Prefer preserving at least `2 dB` sample-peak headroom unless the user explicitly asks for a mastered loud file.
- Avoid controlling final loudness through unknown normalized limiter parameters unless the parameter mapping has been verified by render analysis.

## Artifact Rule

If the user reports static, crackle, hash, or gritty corruption while peak/LUFS metrics look clean:

- Treat the render as invalid.
- Compare against a known-good rerendered baseline.
- Check whether the render was printed faster-than-realtime or through a plugin chain that behaves badly during render.
- If render speed cannot be reliably controlled by API, use a manual/GUI-confirmed render mode or a short user-confirmed spot check before printing full-length candidates.
- Do not offer A/B listening decisions from a render batch that may have been printed faster-than-realtime.
- Do not learn mix-decision rules from any batch the user describes as static-y, crackly, corrupted, or horrible.

## Required Compare-Batch Gate

For future A/B compare batches:

1. Choose at least three 20-30 second sections: dense chorus/loud section, mid-song section, and late-song section. Add a sparse vocal section when vocal noise or ambience is being judged.
2. Render a known-good baseline snippet through the exact same render path for each section.
3. Render only candidate snippets first.
4. Run `scripts/analyze_wav.py`, deeper LUFS/spectrum analysis, and `scripts/artifact_gate.py` on each snippet.
5. If the candidate snippets pass automated checks, ask for short spot-checks when the user is available or clearly mark the snippets as "unverified by ear."
6. Only render full-length candidates after all required snippet sections are clean.
7. After a full-length render, spot-check the full rendered file at the same timestamps used for the snippets plus any quiet/open sections. Snippet files can be clean while the full-length render or playback path still has artifacts.
8. If any candidate in a batch has shared static/crackle, invalidate the compare batch and isolate source/FX/bus/plugin render behavior before continuing.

For unattended work, prefer preparing short snippets and a targeted listening checklist over rendering multiple full-length candidates that have not passed a human or audible-artifact sanity check.

If short verified snippets are clean but a full-length render is reported as static-y or corrupted, do not conclude that the candidate chain is bad from full-render feedback alone. Isolate full-render playback, untested sections, and long-render behavior separately.
