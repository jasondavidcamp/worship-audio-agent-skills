# REAPER MCP Setup

Use this as a generic checklist for REAPER automation through `reapy` or a REAPER MCP bridge. Local paths vary by workstation.

## Typical Setup

- Install or clone the REAPER MCP/reapy integration in a local tools directory.
- Create a Python virtual environment for the MCP server and install its dependencies.
- Register the MCP command in the agent's config.
- Run `reapy.config.configure_reaper(...)` so REAPER has the web interface and `activate_reapy_server.py` ReaScript action.
- Restart REAPER after configuration before external control tries to connect.

## Verification

- Confirm the MCP server can start and list tools without REAPER connected.
- Confirm REAPER can run the `activate_reapy_server.py` action.
- If calls fail with an API or connection warning, restart REAPER and verify the reapy server action is available/enabled.
- Keep REAPER version, MCP version, and Python environment notes in a private deployment log.

## Known Wrapper Mismatch Pattern

If this local deployment repeatedly returns `module 'reapy.reascript_api' has no attribute 'EnumProjects'` from MCP project/list helpers, treat the MCP wrapper as known-untrusted for session inspection. Do not retry the same MCP helper at the start of every mix pass.

Use direct ReaScript/ReaPy through the working Python environment or the skill scripts for:

- project/track/item/FX inspection,
- render settings and time selections,
- plugin insertion and parameter reads/writes,
- render-window cleanup and API pings.

Only revisit the MCP wrapper after the local REAPER MCP package has been updated, reconfigured, or explicitly tested. Until then, the MCP tool list can exist while specific helper implementations remain unsafe for the current REAPER/ReaPy API.

## Shell-Safe Probe Scripts

When probing REAPER through direct Python/ReaScript snippets, match the command shape to the user's active shell:

- PowerShell: use a here-string piped to Python, e.g. `@' ... '@ | python -`.
- Bash/zsh: use a heredoc, e.g. `python - <<'PY' ... PY`.
- Cmd.exe: prefer `python -c "..."` for tiny probes or write a temporary `.py` file for multiline code.

If the probe needs more than a few lines, uses many quotes/backslashes, or may be reused, prefer a small helper script over inline shell code. This avoids wasting time on shell quoting differences and makes the action easier to audit before touching REAPER state.
