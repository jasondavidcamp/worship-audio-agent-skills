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

## Shell-Safe Probe Scripts

When probing REAPER through direct Python/ReaScript snippets, match the command shape to the user's active shell:

- PowerShell: use a here-string piped to Python, e.g. `@' ... '@ | python -`.
- Bash/zsh: use a heredoc, e.g. `python - <<'PY' ... PY`.
- Cmd.exe: prefer `python -c "..."` for tiny probes or write a temporary `.py` file for multiline code.

If the probe needs more than a few lines, uses many quotes/backslashes, or may be reused, prefer a small helper script over inline shell code. This avoids wasting time on shell quoting differences and makes the action easier to audit before touching REAPER state.
