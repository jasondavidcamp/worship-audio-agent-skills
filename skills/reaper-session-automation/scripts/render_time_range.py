#!/usr/bin/env python3
"""Render an explicit REAPER time range safely."""

from __future__ import annotations

import argparse
import wave
from pathlib import Path

import reapy
from reapy import reascript_api as RPR


MAX_DURATION_DRIFT_SECONDS = 0.5


def _media_end() -> float:
    end = 0.0
    for track_index in range(RPR.CountTracks(0)):
        track = RPR.GetTrack(0, track_index)
        for item_index in range(RPR.CountTrackMediaItems(track)):
            item = RPR.GetTrackMediaItem(track, item_index)
            pos = RPR.GetMediaItemInfo_Value(item, "D_POSITION")
            length = RPR.GetMediaItemInfo_Value(item, "D_LENGTH")
            end = max(end, pos + length)
    return end


def _ensure_master_output_1_2() -> None:
    """Ensure the master has a stereo hardware send to output 1/2."""
    master = RPR.GetMasterTrack(0)
    for send_index in range(RPR.GetTrackNumSends(master, 1)):
        dst = int(RPR.GetTrackSendInfo_Value(master, 1, send_index, "I_DSTCHAN"))
        src = int(RPR.GetTrackSendInfo_Value(master, 1, send_index, "I_SRCCHAN"))
        if dst == 0 and src == 0:
            RPR.SetTrackSendInfo_Value(master, 1, send_index, "D_VOL", 1.0)
            RPR.SetTrackSendInfo_Value(master, 1, send_index, "D_PAN", 0.0)
            RPR.SetTrackSendInfo_Value(master, 1, send_index, "B_MUTE", 0)
            return

    send_index = RPR.CreateTrackSend(master, 0)
    if send_index < 0:
        send_index = RPR.CreateTrackSend(master, None)
    if send_index < 0:
        raise RuntimeError("Could not create master hardware output send to output 1/2")

    RPR.SetTrackSendInfo_Value(master, 1, send_index, "I_SRCCHAN", 0)
    RPR.SetTrackSendInfo_Value(master, 1, send_index, "I_DSTCHAN", 0)
    RPR.SetTrackSendInfo_Value(master, 1, send_index, "D_VOL", 1.0)
    RPR.SetTrackSendInfo_Value(master, 1, send_index, "D_PAN", 0.0)
    RPR.SetTrackSendInfo_Value(master, 1, send_index, "B_MUTE", 0)


def _wav_duration_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def render_time_range(output_path: Path, start: float, end: float) -> Path:
    if end <= start:
        raise ValueError(f"Refusing empty render range: start={start}, end={end}")

    output_path = output_path.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    reapy.connect()
    _ensure_master_output_1_2()
    RPR.GetSet_LoopTimeRange2(0, True, False, float(start), float(end), False)
    RPR.GetSetProjectInfo_String(0, "RENDER_FILE", str(output_path.parent), True)
    RPR.GetSetProjectInfo_String(0, "RENDER_PATTERN", output_path.stem, True)
    RPR.GetSetProjectInfo(0, "RENDER_SETTINGS", 0, True)  # master mix
    RPR.GetSetProjectInfo(0, "RENDER_STARTPOS", float(start), True)
    RPR.GetSetProjectInfo(0, "RENDER_ENDPOS", float(end), True)
    RPR.GetSetProjectInfo(0, "RENDER_FORMAT", 0, True)  # WAV
    RPR.GetSetProjectInfo(0, "RENDER_FORMAT2", 2, True)  # 24-bit PCM
    RPR.GetSetProjectInfo(0, "RENDER_SRATE", 48000.0, True)
    RPR.GetSetProjectInfo(0, "RENDER_CHANNELS", 2.0, True)
    RPR.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 2.0, True)  # local time selection mode
    RPR.Main_OnCommand(41824, 0)

    if not output_path.exists() or output_path.stat().st_size <= 0:
        raise RuntimeError(f"Render did not produce a non-empty file: {output_path}")

    expected_duration = float(end) - float(start)
    actual_duration = _wav_duration_seconds(output_path)
    drift = abs(actual_duration - expected_duration)
    if drift > MAX_DURATION_DRIFT_SECONDS:
        raise RuntimeError(
            "Rendered WAV duration does not match requested range: "
            f"requested={expected_duration:.3f}s actual={actual_duration:.3f}s "
            f"path={output_path}"
        )
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_path", type=Path)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--end", type=float, help="End time in seconds. Defaults to the last media item end.")
    args = parser.parse_args()

    reapy.connect()
    end = _media_end() if args.end is None else args.end
    rendered = render_time_range(args.output_path, args.start, end)
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
