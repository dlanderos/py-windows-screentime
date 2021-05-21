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

from collections import OrderedDict
from ctypes import pointer, create_unicode_buffer, sizeof
from ctypes.wintypes import HWND, DWORD, MAX_PATH, RECT, INT
from dataclasses import dataclass, field
from time import time
from helpers.rectangle import Rectangle, rectangle_from_structure, rectangle_area, rectangle_intersection
from windows.definition import PROCESS_QUERY_INFORMATION, PROCESS_VM_READ, WS_VISIBLE, GWL_STYLE, WS_SYSMENU, \
    DWMWA_CLOAKED, S_OK
from windows.function import get_window_thread_process_id, open_process, k32_get_process_image_file_name_w, \
    get_window_text_length_w, get_window_text_w, get_window_rect, dwm_get_window_attribute, get_window_long_ptr_w, \
    is_iconic, enum_windows, get_desktop_window
from windows.type import WNDENUMPROC


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


def window_capture_from_handle(window_handle: HWND) -> WindowCapture:
    # Retrieve the thread process ID of the window's application
    thread_process_id = DWORD(0)
    get_window_thread_process_id(window_handle, pointer(thread_process_id))

    # Retrieve the process handle
    process_handle = open_process(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, thread_process_id)

    # Read the process's file name
    process_file_name_buffer_length = MAX_PATH + 1
    process_file_name_buffer = create_unicode_buffer(process_file_name_buffer_length)
    k32_get_process_image_file_name_w(process_handle, process_file_name_buffer, DWORD(process_file_name_buffer_length))

    # Get the window's title
    window_text_buffer_length = get_window_text_length_w(window_handle) + 1
    window_text_buffer = create_unicode_buffer(window_text_buffer_length)
    get_window_text_w(window_handle, window_text_buffer, INT(window_text_buffer_length))

    # Get the windows' rectangle (RECT)
    rectangle_structure = RECT()
    get_window_rect(window_handle, pointer(rectangle_structure))

    # Return the Window data
    # noinspection PyTypeChecker
    return WindowCapture(
        handle=window_handle,
        process=process_file_name_buffer.value,
        title=window_text_buffer.value,
        rectangle=rectangle_from_structure(rectangle_structure),
        time_start=round(time() * 1000)
    )


def visible_window_captures() -> frozenset[WindowCapture]:
    # Use an ordered dictionary to preserve Z-Index order
    filtered_windows = OrderedDict()

    @WNDENUMPROC
    def window_enumerate_callback(window_handle, _):
        window_style = get_window_long_ptr_w(window_handle, GWL_STYLE)
        # Ensure the window is visible and has a normal style
        if window_style & WS_VISIBLE and window_style & WS_SYSMENU:
            # Retrieve whether or not the window is cloaked
            cloaked_value = INT(0)
            if dwm_get_window_attribute(
                    window_handle,
                    DWMWA_CLOAKED,
                    pointer(cloaked_value),
                    sizeof(INT)
            ) != S_OK:
                print("Failed to get DWMWA_CLOAKED attribute")
                return False

            # Ensure that the window has NOT been cloaked and is NOT iconic
            if cloaked_value != 0 and not is_iconic(window_handle):
                # Retrieve the window data from the handle and add it to the map
                filtered_windows[window_capture_from_handle(window_handle)] = 0
        return True

    # Enumerate through all windows.
    # This will block the thread until the callback finished.
    enum_windows(window_enumerate_callback)

    container_window = window_capture_from_handle(get_desktop_window())
    available_area = rectangle_area(container_window.rectangle)

    visible_windows = set()

    for index, window in enumerate(filtered_windows):
        # Plain desktop doesn't count!
        if index == 0 and window.process == "\\Device\\HarddiskVolume3\\Windows\\System32\\ApplicationFrameHost.exe":
            break

        # Continue iterating as long as there is available screen space left for a window to occupy.
        if available_area <= 0:
            break
        # Get the windows overall area
        window_area = rectangle_area(window.rectangle)

        # Adjust the window's area to reflect parts of it that are covered by another window above it.
        for previous_window in visible_windows:
            area = rectangle_area(
                rectangle_intersection(previous_window.rectangle, window.rectangle)
            )
            window_area -= area

        # Determine if the window is completely covered by another.
        # If it is, then it can be skipped.
        if window_area <= 0:
            continue

        # Add the window to the list of visible windows.
        available_area -= window_area
        visible_windows.add(window)

    return frozenset(visible_windows)


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
