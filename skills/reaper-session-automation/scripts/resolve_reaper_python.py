#!/usr/bin/env python3
"""Resolve and optionally verify the Python interpreter for REAPER automation.

The preferred interpreter can be stored privately in:

    ~/.codex/local/reaper-python.txt

This helper avoids assuming that the shell's default `python` is the same
environment used for REAPER/ReaPy automation.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def private_config_path() -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / ".codex" / "local" / "reaper-python.txt"


def resolve_python() -> tuple[str, str]:
    env_path = os.environ.get("REAPER_PYTHON")
    if env_path:
        return env_path.strip(), "REAPER_PYTHON"

    config = private_config_path()
    if config.exists():
        value = config.read_text(encoding="utf-8").strip()
        if value:
            return value, str(config)

    return sys.executable, "current_python"


def verify_python(python_path: str) -> dict:
    probe = (
        "import json, reapy, reapy.reascript_api as RPR; "
        "project = reapy.Project(); "
        "print(json.dumps({"
        "'ok': True, "
        "'project_name': project.name, "
        "'has_enum_projects': hasattr(RPR, 'EnumProjects'), "
        "'has_get_project_name': hasattr(RPR, 'GetProjectName')"
        "}))"
    )
    completed = subprocess.run(
        [python_path, "-c", probe],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if completed.returncode == 0:
        try:
            payload = json.loads(completed.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            payload = {"ok": False, "error": "Probe returned non-JSON output."}
    else:
        payload = {"ok": False, "error": completed.stderr.strip() or completed.stdout.strip()}
    payload["returncode"] = completed.returncode
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Verify ReaPy import and current project connection.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    python_path, source = resolve_python()
    result = {
        "python": python_path,
        "source": source,
        "config_path": str(private_config_path()),
    }
    if args.verify:
        result["verification"] = verify_python(python_path)

    print(json.dumps(result, indent=2 if args.pretty else None))
    verification = result.get("verification")
    return 0 if verification is None or verification.get("ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
