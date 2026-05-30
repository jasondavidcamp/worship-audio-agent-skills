#!/usr/bin/env python3
"""Compatibility wrapper for bass reference scoring.

Prefer `reference_score.py --source bass` for new source-aware scoring work.
This wrapper preserves the original bass-specific command and import surface.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reference_score import analyze as analyze_reference


def analyze(candidate_path: Path, reference_path: Path) -> dict:
    return analyze_reference(candidate_path, reference_path, source="bass")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path, help="Candidate bass WAV")
    parser.add_argument("--reference", required=True, type=Path, help="Reference bass WAV")
    parser.add_argument("--json-output", type=Path, help="Optional JSON report path")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    result = analyze(args.candidate, args.reference)
    text = json.dumps(result, indent=2 if args.pretty else None)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
