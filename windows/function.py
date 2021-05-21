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

from ctypes import windll, POINTER, Array
from ctypes.wintypes import RECT, MSG, BOOL, DWORD, HANDLE, HMODULE, HWND, INT, LPARAM, LPDWORD, UINT, WPARAM, LPWSTR, \
    WCHAR
from windows.type import LRESULT, LONG_PTR, HRESULT, PVOID, WINEVENTPROC, WNDENUMPROC
from windows.definition import EVENT_MIN, EVENT_MAX


def get_message_w(
        message_pointer: POINTER(MSG),
        window_handle: HWND = None,
        message_filter_min: UINT = 0,
        message_filter_max: UINT = 0
) -> BOOL:
    """Wrapper for the "GetMessageW" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessagew for more info.
    """

    proto = windll.user32.GetMessageW
    proto.restype = BOOL
    proto.argtypes = POINTER(MSG), HWND, UINT, UINT
    return proto(message_pointer, window_handle, message_filter_min, message_filter_max)


def post_thread_message_w(
        thread_id: DWORD,
        message_type: UINT,
        parameter_w: WPARAM = 0,
        parameter_l: LPARAM = 0
) -> BOOL:
    """Wrapper for the "PostThreadMessageW" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postthreadmessagew for more info.
    """

    proto = windll.user32.PostThreadMessageW
    proto.restype = BOOL
    proto.argtypes = DWORD, UINT, WPARAM, LPARAM
    return proto(thread_id, message_type, parameter_w, parameter_l)


def translate_message(message_pointer: POINTER(MSG)) -> BOOL:
    """Wrapper for the "TranslateMessage" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-translatemessage for more info.
    """

    proto = windll.user32.TranslateMessage
    proto.restype = BOOL
    proto.argtypes = POINTER(MSG),
    return proto(message_pointer)


def dispatch_message_w(message_pointer: POINTER(MSG)) -> LRESULT:
    """Wrapper for the "DispatchMessageW" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dispatchmessagew for more info.
    """

    proto = windll.user32.DispatchMessageW
    proto.restype = BOOL
    proto.argtypes = POINTER(MSG),
    return proto(message_pointer)


def set_win_event_hook(
        callback: WINEVENTPROC,
        event_filter_min: DWORD = EVENT_MIN,
        event_filter_max: DWORD = EVENT_MAX,
        library_handle: HMODULE = None,
        process_id: DWORD = 0,
        thread_id: DWORD = 0,
        flags: DWORD = 0
) -> HANDLE:
    """Wrapper for the "SetWinEventHook" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook for more info.
    """

    proto = windll.user32.SetWinEventHook
    proto.restype = BOOL
    proto.argtypes = DWORD, DWORD, HMODULE, WINEVENTPROC, DWORD, DWORD, DWORD
    return proto(event_filter_min, event_filter_max, library_handle, callback, process_id, thread_id, flags)


def unhook_win_event(event_hook_handle: HANDLE) -> BOOL:
    """Wrapper for the "UnhookWinEvent" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unhookwinevent for more info.
    """

    proto = windll.user32.SetWinEventHook
    proto.restype = BOOL
    proto.argtypes = HANDLE,
    return proto(event_hook_handle)


def get_window_text_length_w(window_handle: HWND) -> int:
    """Wrapper for the "GetWindowTextLengthW" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtextlengthw for more info.
    """

    proto = windll.user32.GetWindowTextLengthW
    proto.restype = INT
    proto.argtypes = HWND,
    return proto(window_handle)


def get_window_text_w(window_handle: HWND, text_pointer: Array[WCHAR], max_count: INT) -> int:
    """Wrapper for the "GetWindowTextW" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtextw for more info.
    """

    proto = windll.user32.GetWindowTextW
    proto.restype = INT
    proto.argtypes = HWND, LPWSTR, INT,
    return proto(window_handle, text_pointer, max_count)


def enum_windows(callback: WNDENUMPROC, parameter_l: LPARAM = 0) -> BOOL:
    """Wrapper for the "EnumWindows" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows for more info.
    """

    proto = windll.user32.EnumWindows
    proto.restype = BOOL
    proto.argtypes = WNDENUMPROC, LPARAM,
    return proto(callback, parameter_l)


def get_desktop_window() -> HANDLE:
    """Wrapper for the "GetDesktopWindow" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdesktopwindow for more info.
    """

    proto = windll.user32.GetDesktopWindow
    proto.restype = HANDLE
    return proto()


def get_window_rect(window_handle: HANDLE, rectangle_pointer: POINTER(RECT)) -> BOOL:
    """Wrapper for the "GetWindowRect" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect for more info.
    """

    proto = windll.user32.GetWindowRect
    proto.restype = BOOL
    proto.argtypes = HANDLE, POINTER(RECT),
    return proto(window_handle, rectangle_pointer)


def get_client_rect(window_handle: HANDLE, rectangle_pointer: POINTER(RECT)) -> BOOL:
    """Wrapper for the "GetClientRect" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclientrect for more info.
    """

    proto = windll.user32.GetClientRect
    proto.restype = BOOL
    proto.argtypes = HANDLE, POINTER(RECT),
    return proto(window_handle, rectangle_pointer)


def is_iconic(window_handle: HANDLE) -> BOOL:
    """Wrapper for the "IsIconic" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-isiconic for more info.
    """

    proto = windll.user32.IsIconic
    proto.restype = BOOL
    proto.argtypes = HANDLE,
    return proto(window_handle)


def is_window_visible(window_handle: HANDLE) -> BOOL:
    """Wrapper for the "IsWindowVisible" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswindowvisible for more info.
    """

    proto = windll.user32.IsWindowVisible
    proto.restype = BOOL
    proto.argtypes = HANDLE,
    return proto(window_handle)


def get_window(window_handle: HWND, command: UINT) -> HWND:
    """Wrapper for the "GetWindow" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindow for more info.
    """

    proto = windll.user32.GetWindow
    proto.restype = HWND
    proto.argtypes = HWND, UINT,
    return proto(window_handle, command)


def get_window_long_ptr_w(window_handle: HANDLE, value_offset: INT) -> int:
    """Wrapper for the "GetWindowLongPtrW" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongptrw for more info.
    """

    proto = windll.user32.GetWindowLongPtrW
    proto.restype = LONG_PTR
    proto.argtypes = HANDLE, INT,
    return proto(window_handle, value_offset)


def get_window_thread_process_id(window_handle: HWND, thread_process_id_pointer: LPDWORD) -> BOOL:
    """Wrapper for the "GetWindowThreadProcessId" Windows user function.
        See https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid for
        more info.
    """

    proto = windll.user32.GetWindowThreadProcessId
    proto.restype = DWORD
    proto.argtypes = HWND, LPDWORD,
    return proto(window_handle, thread_process_id_pointer)


def dwm_get_window_attribute(
        window_handle: HWND,
        attribute_flag: DWORD,
        value_pointer: POINTER,
        value_size: any
) -> HRESULT:
    """Wrapper for the "DwmGetWindowAttribute" Windows dwm function.
        See https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmgetwindowattribute for more info.
    """

    proto = windll.dwmapi.DwmGetWindowAttribute
    proto.restype = HRESULT
    proto.argtypes = HWND, DWORD, PVOID, DWORD
    return proto(window_handle, attribute_flag, value_pointer, value_size)


def get_current_thread_id() -> DWORD:
    """Wrapper for the "GetCurrentThreadId" Windows kernel function.
    See https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentthreadid for
    more info.
    """

    proto = windll.kernel32.GetCurrentThreadId
    proto.restype = DWORD
    return proto()


def open_process(access_rights: DWORD, process_id: DWORD, inherit_handle: BOOL = False) -> HANDLE:
    """Wrapper for the "OpenProcess" Windows kernel function.
    See https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess for
    more info.
    """

    proto = windll.kernel32.OpenProcess
    proto.restype = HANDLE
    proto.argtypes = DWORD, BOOL, DWORD,
    return proto(access_rights, inherit_handle, process_id)


def close_handle(object_handle: HANDLE) -> BOOL:
    """Wrapper for the "CloseHandle" Windows kernel function.
    See https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle for
    more info.
    """

    proto = windll.kernel32.CloseHandle
    proto.restype = BOOL
    proto.argtypes = HANDLE,
    return proto(object_handle)


def k32_get_process_image_file_name_w(process_handle: HANDLE, path_pointer: Array[WCHAR], path_size: DWORD) -> DWORD:
    """Wrapper for the "K32GetProcessImageFileNameW" Windows kernel function.
    See https://docs.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getprocessimagefilenamew for
    more info.
    """

    proto = windll.kernel32.K32GetProcessImageFileNameW
    proto.restype = DWORD
    proto.argtypes = HANDLE, LPWSTR, DWORD,
    return proto(process_handle, path_pointer, path_size)
