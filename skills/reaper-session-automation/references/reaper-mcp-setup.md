# REAPER Direct ReaPy And MCP Setup

Use this as a generic checklist for REAPER automation through direct `reapy` first, with a REAPER MCP bridge treated as optional. Local paths vary by workstation.

## Typical Setup

- Install `python-reapy` into a dedicated or default Python environment used for REAPER automation.
- Store the working interpreter path in a private local config such as `~/.codex/local/reaper-python.txt`. Do not commit workstation-specific Python paths to the public skill repo.
- Install or clone the REAPER MCP/reapy integration in a local tools directory.
- Create a Python virtual environment for the MCP server and install its dependencies.
- Register the MCP command in the agent's config.
- Run `reapy.config.configure_reaper(...)` so REAPER has the web interface and `activate_reapy_server.py` ReaScript action.
- Restart REAPER after configuration before external control tries to connect.

## Verification

- Verify direct ReaPy before render-sensitive work:

```powershell
$py = if (Test-Path "$env:USERPROFILE\.codex\local\reaper-python.txt") { Get-Content "$env:USERPROFILE\.codex\local\reaper-python.txt" -Raw } else { "python" }
& $py.Trim() -c "import reapy, reapy.reascript_api as RPR; print('reapy ok', reapy.Project().name); print('EnumProjects', hasattr(RPR, 'EnumProjects'))"
```

Or from this skill folder:

```powershell
& "python" scripts/resolve_reaper_python.py --verify --pretty
```

- Confirm the MCP server can start and list tools without REAPER connected.
- Confirm REAPER can run the `activate_reapy_server.py` action.
- If calls fail with an API or connection warning, restart REAPER and verify the reapy server action is available/enabled.
- Keep REAPER version, MCP version, and Python environment notes in a private deployment log.

For live session mutation, FX edits, parameter reads/writes, render settings, time selections, or popup cleanup, direct ReaPy is required. MCP helper calls may be used only when they have been verified for the current setup and the task is not render-sensitive or FX-sensitive.

## Known Wrapper Mismatch Pattern

If this local deployment repeatedly returns `module 'reapy.reascript_api' has no attribute 'EnumProjects'` from MCP project/list helpers, treat the MCP wrapper as known-untrusted for session inspection. Do not retry the same MCP helper at the start of every mix pass, especially when direct ReaPy has already verified that `EnumProjects` exists in the configured automation Python.

Use direct ReaScript/ReaPy through the working Python environment or the skill scripts for:

- project/track/item/FX inspection,
- render settings and time selections,
- plugin insertion and parameter reads/writes,
- render-window cleanup and API pings.

Only revisit the MCP wrapper after the local REAPER MCP package has been updated, reconfigured, or explicitly tested. Until then, the MCP tool list can exist while specific helper implementations remain unsafe for the current REAPER/ReaPy API.

## MCP Repair Order

When MCP fails but direct ReaPy works:

1. Verify the MCP server's own virtual environment can import `reapy` and that `reapy.reascript_api.EnumProjects` exists.
2. If the venv is healthy but the already-running MCP tool still reports old API errors, restart the MCP server or restart the host app so the tool process reloads its environment.
3. Re-test one harmless MCP read tool only after the restart. If it still fails, leave MCP disabled for sensitive work and continue through direct ReaPy.
4. Do not patch public skills with workstation-specific MCP paths; keep local process IDs, venv paths, and restart notes in private deployment notes.

## Shell-Safe Probe Scripts

When probing REAPER through direct Python/ReaScript snippets, match the command shape to the user's active shell:

- PowerShell: use a here-string piped to Python, e.g. `@' ... '@ | python -`.
- Bash/zsh: use a heredoc, e.g. `python - <<'PY' ... PY`.
- Cmd.exe: prefer `python -c "..."` for tiny probes or write a temporary `.py` file for multiline code.

If the probe needs more than a few lines, uses many quotes/backslashes, or may be reused, prefer a small helper script over inline shell code. This avoids wasting time on shell quoting differences and makes the action easier to audit before touching REAPER state.
