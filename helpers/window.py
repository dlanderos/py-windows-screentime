"""
    py-windows-screentime: Python program that tracks window usage.
    Copyright (C) 2021 dxboats

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from ctypes import create_unicode_buffer, sizeof, byref
from ctypes.wintypes import DWORD, MAX_PATH, RECT, INT
from dataclasses import dataclass, field
from time import time

from helpers.rectangle import Rectangle, rectangle_from_rect, rectangle_intersection
from winapi import (
    S_OK, NULL
)
from winapi.dwm import DwmGetWindowAttribute, DWMWA_CLOAKED
from winapi.kernel import OpenProcess, PROCESS_QUERY_LIMITED_INFORMATION, GetProcessImageFileNameW
from winapi.user import GetWindowThreadProcessId, GetWindowTextLengthW, GetWindowTextW, WNDENUMPROC, \
    GetWindowLongPtrW, GWL_STYLE, WS_VISIBLE, IsIconic, EnumWindows, GetClientRect, GetClassNameW, MAX_CLASS_NAME


@dataclass(frozen=True)
class WindowCapture:
    handle: int = field(hash=True)
    process: str = field(hash=True)
    title: str = field(hash=True)
    rectangle: Rectangle = field(hash=True)
    time_start: int = field(hash=False)


@dataclass(frozen=True)
class WindowState:
    """
    Represents a state a Window was in. Includes the title, the rectangle, and the duration the window was in that state
    """
    title: str = field(hash=True)
    rectangle: Rectangle = field(hash=True)
    duration: int = field(hash=True)


@dataclass(frozen=True)
class WindowResult:
    """
    Represents a single window and the results of its analysis.
    """
    handle: int = field(hash=True)
    process: str = field(hash=True)
    states: frozenset[WindowState] = field(hash=True)


IGNORED_CLASS_NAMES = frozenset(
    {
        "Shell_TrayWnd",
        "Internet Explorer_Hidden",
        "Progman",
        "WorkerW",
    }
)


def visible_window_captures() -> frozenset[WindowCapture]:
    previous_rectangles: set[Rectangle] = set()
    captures: set[WindowCapture] = set()

    @WNDENUMPROC
    def enumerate_windows2(handle: int, _unused_parameter: int) -> bool:

        # Ensure the window has the visible style.
        style = GetWindowLongPtrW(handle, GWL_STYLE)
        if not style & WS_VISIBLE:
            return True

        # Ensure the window is not cloaked.
        cloaked = INT(0)
        if DwmGetWindowAttribute(handle, DWMWA_CLOAKED, byref(cloaked), sizeof(INT)) != S_OK:
            # TODO: debug for when this fails?
            return True
        if cloaked:
            return True

        # Ensure the window is not iconic.
        if IsIconic(handle):
            return True

        # Ensure the window has a valid class name.
        buffer_class_name_length = MAX_CLASS_NAME + 1
        buffer_class_name = create_unicode_buffer(buffer_class_name_length)
        if not GetClassNameW(handle, buffer_class_name, buffer_class_name_length):
            # TODO: debug for when this fails?
            return True
        if buffer_class_name.value in IGNORED_CLASS_NAMES:
            return True

        # Attempt to retrieve the process and thread id of the window.
        process_id = DWORD(0)
        thread_id = GetWindowThreadProcessId(handle, byref(process_id))
        if not process_id or not thread_id:
            # TODO: debug for when this fails?
            return True

        # Attempt to retrieve the window's text (current title).
        buffer_text_length = GetWindowTextLengthW(handle) + 1
        buffer_text = create_unicode_buffer(buffer_text_length)
        if not GetWindowTextW(handle, buffer_text, buffer_text_length):
            # TODO: debug for when this fails?
            return True

        # Attempt to retrieve the window's client area (rectangle)
        rect = RECT()
        if not GetClientRect(handle, byref(rect)):
            # TODO: debug for when this fails?
            return True
        rectangle = rectangle_from_rect(rect)

        # Ensure the window has some portions that are visible
        area = rectangle.area
        for previous_rectangle in previous_rectangles:
            area -= rectangle_intersection(rectangle, previous_rectangle).area
        if area <= 0:
            return True

        # Retrieve the process handle
        process_handle = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, thread_id)

        # Read the process's file name
        process_file_name_buffer_length = MAX_PATH + 1
        process_file_name_buffer = create_unicode_buffer(process_file_name_buffer_length)
        GetProcessImageFileNameW(process_handle, process_file_name_buffer, process_file_name_buffer_length)

        previous_rectangles.add(rectangle)
        captures.add(WindowCapture(
            handle=handle,
            process=process_file_name_buffer.value,
            title=buffer_text.value,
            rectangle=rectangle,
            time_start=round(time() * 1000)
        ))

        return True

    EnumWindows(enumerate_windows2, NULL)

    return frozenset(captures)


def capture_to_state(capture: WindowCapture) -> WindowState:
    return WindowState(
        title=capture.title,
        rectangle=capture.rectangle,
        duration=round(time() * 1000) - capture.time_start
    )


def update_capture_state(
        captures: dict[tuple[int, str], WindowCapture],
        states: dict[tuple[int, str], set[WindowState]]
):
    visible_captures = set()
    for capture in visible_window_captures():
        capture_key = (capture.handle, capture.process)
        visible_captures.add(capture_key)
        if capture_key in captures:
            old_capture = captures[capture_key]
            # Determine if the capture has mutated. If it has, we need to begin capturing future changes.
            # Note: this window is still visible, so future changes need to be continuously checked.
            if old_capture is not capture:
                if capture_key not in states:
                    states[capture_key] = set()
                # This capture can now be added to the states
                states[capture_key].add(capture_to_state(old_capture))

                # The capture for this key is now the new one... waiting to be finalized
                captures[capture_key] = capture
        else:
            captures[capture_key] = capture

    remove_them_keys = set()
    for key, value in captures.items():
        if key not in visible_captures:
            if key not in states:
                states[key] = set()

            # This capture can now be added to the states since it wasn't in the visible ones above.
            states[key].add(capture_to_state(value))

            # Remove this from captures since we gotta wait for it to become visible again
            remove_them_keys.add(key)

    # Remove the keys that need to be removed
    for key in remove_them_keys:
        captures.pop(key)


def finalize_capture_state(
        captures: dict[tuple[int, str], WindowCapture],
        states: dict[tuple[int, str], set[WindowState]]
) -> frozenset[WindowResult]:
    for key, value in captures.items():
        if key not in states:
            states[key] = set()
        states[key].add(capture_to_state(value))

    result_set = set()
    for key, value in states.items():
        result_set.add(WindowResult(
            handle=key[0],
            process=key[1],
            states=frozenset(value)
        ))

    return frozenset(result_set)
