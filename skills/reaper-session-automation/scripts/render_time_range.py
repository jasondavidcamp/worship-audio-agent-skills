#!/usr/bin/env python3
"""Render an explicit REAPER master-mix time range safely."""

from __future__ import annotations

import argparse
import platform
import time
import wave
from pathlib import Path

import reapy
from reapy import reascript_api as RPR


MAX_DURATION_DRIFT_SECONDS = 0.5
RENDER_WINDOW_CLOSE_TIMEOUT_SECONDS = 5.0
RENDER_WINDOW_APPEAR_GRACE_SECONDS = 1.0
RENDER_WINDOW_TITLE_TERMS = (
    "render",
    "rendering",
    "finished in",
)


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


def _current_time_selection() -> tuple[float, float]:
    selection = RPR.GetSet_LoopTimeRange2(0, False, False, 0.0, 0.0, False)
    if isinstance(selection, (list, tuple)) and len(selection) >= 5:
        return float(selection[3]), float(selection[4])
    return 0.0, 0.0


def _restore_time_selection(start: float, end: float) -> None:
    if end > start:
        RPR.GetSet_LoopTimeRange2(0, True, False, float(start), float(end), False)
    else:
        RPR.GetSet_LoopTimeRange2(0, True, False, 0.0, 0.0, False)


def close_reaper_render_windows(timeout: float = RENDER_WINDOW_CLOSE_TIMEOUT_SECONDS) -> dict[str, list[str]]:
    """Close visible REAPER render progress/results windows on Windows.

    Returns a small report with closed and remaining render-window titles. On
    non-Windows hosts this is a no-op because REAPER window management differs
    by platform.
    """
    if platform.system() != "Windows":
        return {"closed": [], "remaining": []}

    import ctypes
    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    enum_proc_type = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    process_query_limited_information = 0x1000
    wm_close = 0x0010

    user32.EnumWindows.argtypes = [enum_proc_type, wintypes.LPARAM]
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.QueryFullProcessImageNameW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    ]

    def title_for(hwnd: int) -> str:
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return ""
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value

    def process_path_for(hwnd: int) -> str:
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        handle = kernel32.OpenProcess(process_query_limited_information, False, pid.value)
        if not handle:
            return ""
        try:
            size = wintypes.DWORD(4096)
            buf = ctypes.create_unicode_buffer(size.value)
            if kernel32.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size)):
                return buf.value
            return ""
        finally:
            kernel32.CloseHandle(handle)

    def render_windows() -> list[tuple[int, str]]:
        matches: list[tuple[int, str]] = []

        @enum_proc_type
        def enum_window(hwnd: int, _lparam: int) -> bool:
            if not user32.IsWindowVisible(hwnd):
                return True
            title = title_for(hwnd)
            if not title:
                return True
            process_path = process_path_for(hwnd).lower()
            title_lower = title.lower()
            is_reaper = process_path.endswith("\\reaper.exe") or process_path.endswith("/reaper")
            is_render_window = any(term in title_lower for term in RENDER_WINDOW_TITLE_TERMS)
            if is_reaper and is_render_window:
                matches.append((hwnd, title))
            return True

        user32.EnumWindows(enum_window, 0)
        return matches

    closed: list[str] = []
    started = time.monotonic()
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        windows = render_windows()
        if not windows and closed:
            break
        if not windows and time.monotonic() - started >= RENDER_WINDOW_APPEAR_GRACE_SECONDS:
            break
        if not windows:
            time.sleep(0.1)
            continue
        for hwnd, title in windows:
            user32.PostMessageW(hwnd, wm_close, 0, 0)
            closed.append(title)
        time.sleep(0.25)

    remaining = [title for _hwnd, title in render_windows()]
    return {"closed": closed, "remaining": remaining}


def render_time_range(output_path: Path, start: float, end: float) -> Path:
    if end <= start:
        raise ValueError(f"Refusing empty render range: start={start}, end={end}")

    output_path = output_path.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    reapy.connect()
    _ensure_master_output_1_2()
    previous_start, previous_end = _current_time_selection()
    try:
        RPR.GetSet_LoopTimeRange2(0, True, False, float(start), float(end), False)
        RPR.GetSetProjectInfo_String(0, "RENDER_FILE", str(output_path.parent), True)
        RPR.GetSetProjectInfo_String(0, "RENDER_PATTERN", output_path.stem, True)
        RPR.GetSetProjectInfo(0, "RENDER_SETTINGS", 0, True)  # master mix only
        RPR.GetSetProjectInfo(0, "RENDER_STARTPOS", float(start), True)
        RPR.GetSetProjectInfo(0, "RENDER_ENDPOS", float(end), True)
        RPR.GetSetProjectInfo(0, "RENDER_FORMAT", 0, True)  # WAV
        RPR.GetSetProjectInfo(0, "RENDER_FORMAT2", 2, True)  # 24-bit PCM
        RPR.GetSetProjectInfo(0, "RENDER_SRATE", 48000.0, True)
        RPR.GetSetProjectInfo(0, "RENDER_CHANNELS", 2.0, True)
        RPR.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 2.0, True)  # local time selection mode
        RPR.Main_OnCommand(41824, 0)
        cleanup_report = close_reaper_render_windows()
        if cleanup_report["remaining"]:
            raise RuntimeError(f"Render popup cleanup failed: {cleanup_report}")
        RPR.CountTracks(0)
    finally:
        _restore_time_selection(previous_start, previous_end)

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
