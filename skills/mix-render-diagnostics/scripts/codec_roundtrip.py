#!/usr/bin/env python3
"""Encode/decode a WAV through a delivery codec and optionally analyze damage."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


CODEC_SETTINGS = {
    "mp3": {"extension": ".mp3", "args": ["-c:a", "libmp3lame"]},
    "aac": {"extension": ".m4a", "args": ["-c:a", "aac"]},
    "opus": {"extension": ".opus", "args": ["-c:a", "libopus"]},
}


def find_ffmpeg(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    return shutil.which("ffmpeg")


def run_ffmpeg(ffmpeg: str, args: list[str]) -> None:
    subprocess.run(
        [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", *args],
        check=True,
    )


def output_paths(input_wav: Path, output_dir: Path, codec: str) -> tuple[Path, Path]:
    settings = CODEC_SETTINGS[codec]
    stem = input_wav.stem
    encoded = output_dir / f"{stem}-{codec}{settings['extension']}"
    decoded = output_dir / f"{stem}-{codec}-decoded.wav"
    return encoded, decoded


def run_report(args: argparse.Namespace, decoded: Path) -> dict:
    if not args.report_md and not args.report_json:
        return {"status": "skipped"}

    script = Path(__file__).with_name("render_diagnostic_report.py")
    cmd = [
        sys.executable,
        str(script),
        "--candidate",
        str(args.input_wav),
        "--codec-roundtrip",
        str(decoded),
    ]
    if args.baseline:
        cmd.extend(["--baseline", str(args.baseline)])
    if args.reference:
        cmd.extend(["--reference", str(args.reference)])
    if args.section_manifest:
        cmd.extend(["--section-manifest", str(args.section_manifest)])
    for section in args.section:
        cmd.extend(["--section", section])
    if args.report_md:
        cmd.extend(["--md-output", str(args.report_md)])
    if args.report_json:
        cmd.extend(["--json-output", str(args.report_json)])

    subprocess.run(cmd, check=True)
    return {
        "status": "generated",
        "markdown": str(args.report_md) if args.report_md else None,
        "json": str(args.report_json) if args.report_json else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_wav", type=Path)
    parser.add_argument("--codec", choices=sorted(CODEC_SETTINGS), default="aac")
    parser.add_argument("--bitrate", default="192k")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--ffmpeg", help="Explicit ffmpeg executable path.")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--section", action="append", default=[], help="Section as name:start:end seconds.")
    parser.add_argument("--section-manifest", type=Path)
    parser.add_argument("--report-md", type=Path)
    parser.add_argument("--report-json", type=Path)
    parser.add_argument("--json-output", type=Path, help="Write codec roundtrip status JSON.")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    ffmpeg = find_ffmpeg(args.ffmpeg)
    output_dir = args.output_dir or args.input_wav.parent / f"{args.input_wav.stem}-codec-roundtrip"
    result = {
        "status": "untested",
        "input_wav": str(args.input_wav),
        "codec": args.codec,
        "bitrate": args.bitrate,
        "ffmpeg": ffmpeg,
        "encoded": None,
        "decoded_wav": None,
        "report": {"status": "skipped"},
        "notes": [],
    }

    if not ffmpeg:
        result["status"] = "ffmpeg_unavailable"
        result["notes"].append("Install ffmpeg or pass --ffmpeg to run codec delivery simulation.")
        text = json.dumps(result, indent=2 if args.pretty else None)
        if args.json_output:
            args.json_output.parent.mkdir(parents=True, exist_ok=True)
            args.json_output.write_text(text, encoding="utf-8")
        print(text)
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    encoded, decoded = output_paths(args.input_wav, output_dir, args.codec)
    encode_args = [
        "-i",
        str(args.input_wav),
        *CODEC_SETTINGS[args.codec]["args"],
        "-b:a",
        args.bitrate,
        str(encoded),
    ]
    decode_args = ["-i", str(encoded), "-acodec", "pcm_s16le", str(decoded)]
    run_ffmpeg(ffmpeg, encode_args)
    run_ffmpeg(ffmpeg, decode_args)

    result.update(
        {
            "status": "complete",
            "encoded": str(encoded),
            "decoded_wav": str(decoded),
            "report": run_report(args, decoded),
        }
    )
    text = json.dumps(result, indent=2 if args.pretty else None)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
