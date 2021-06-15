"""
    py-screentime: Python program that tracks window usage.
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

from ctypes import windll, Structure, WINFUNCTYPE, POINTER
from ctypes.wintypes import (
    INT,
    UINT,
    DWORD,
    HWND,
    LONG,
    LPARAM,
    WPARAM,
    HINSTANCE,
    HICON,
    HBRUSH,
    ATOM,
    BOOL,
    LPVOID,
    HMENU,
    HDC,
    RECT,
    BYTE,
    HMODULE,
    LPDWORD,
    LPWSTR,
    LPRECT,
    HMONITOR,
    MSG,
    HANDLE, HRGN, HBITMAP, MAX_PATH, WCHAR, WORD, HDESK,
)
from typing import Callable, Union

from winapi import HWINEVENTHOOK, LRESULT, HCURSOR, UnicodeBuffer, LONG_PTR, PVOID

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook
WINEVENT_OUTOFCONTEXT = 0x0000
WINEVENT_SKIPOWNPROCESS = 0x0002

# https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants
EVENT_SYSTEM_FOREGROUND = 0x0003
EVENT_SYSTEM_MOVESIZEEND = 0x000B
EVENT_SYSTEM_MINIMIZEEND = 0x0017
EVENT_SYSTEM_MINIMIZESTART = 0x0016

# https://docs.microsoft.com/en-us/windows/win32/winmsg/window-class-styles#CS_HREDRAW
CS_HREDRAW = 2

# https://docs.microsoft.com/en-us/windows/win32/winmsg/window-class-styles#CS_VREDRAW
CS_VREDRAW = 1

# https://docs.microsoft.com/en-us/windows/win32/winmsg/window-styles#WS_OVERLAPPEDWINDOW
WS_OVERLAPPEDWINDOW = 0xCF0000
WS_VSCROLL = 0x00200000
WS_VISIBLE = 0x10000000

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexw#CW_USEDEFAULT
CW_USEDEFAULT = -0x80000000

# Show window commands
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_NORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_MAXIMIZE = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10
SW_FORCEMINIMIZE = 11
SW_MAX = 11

WM_CREATE = 0x0001
WM_DESTROY = 0x0002
WM_MOVE = 0x0003
WM_SIZE = 0x0005
WM_ACTIVE = 0x0006
WM_PAINT = 0x000F
WM_CLOSE = 0x0010
WM_QUIT = 0x0012
WM_SYSCOLORCHANGE = 0x0015
WM_SHOWWINDOW = 0x0018
WM_VSCROLL = 0x0115
WM_COMMAND = 0x0111

GWL_STYLE = -0x0010

SW_SCROLLCHILDREN = 0x0001
SW_INVALIDATE = 0x0002
SW_ERASE = 0x0004
SW_SMOOTHSCROLL = 0x0010

# Scroll bar constants
SB_HORZ = 0
SB_VERT = 1
SB_CTL = 2
SB_BOTH = 3

# Scroll bar commands
SB_LINEUP = 0
SB_LINELEFT = 0
SB_LINEDOWN = 1
SB_LINERIGHT = 1
SB_PAGEUP = 2
SB_PAGELEFT = 2
SB_PAGEDOWN = 3
SB_PAGERIGHT = 3
SB_THUMBPOSITION = 4
SB_THUMBTRACK = 5
SB_TOP = 6
SB_LEFT = 6
SB_BOTTOM = 7
SB_RIGHT = 7
SB_ENDSCROLL = 8

SIF_RANGE = 0x0001
SIF_PAGE = 0x0002
SIF_POS = 0x0004
SIF_DISABLENOSCROLL = 0x0008
SIF_TRACKPOS = 0x0010
SIF_ALL = SIF_RANGE | SIF_PAGE | SIF_POS | SIF_TRACKPOS

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
SM_CXICON = 11
SM_CYICON = 12
SM_CXCURSOR = 13
SM_CYCURSOR = 14
SM_CXSMICON = 49
SM_CYSMICON = 50

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadimagew
OCR_NORMAL = 32512

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadimagew
OIC_SAMPLE = 32512

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadimagew
IMAGE_BITMAP = 0
IMAGE_ICON = 1
IMAGE_CURSOR = 2

# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-bitblt
SRCCOPY = 0x00CC0020

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadimagew
LR_LOADFROMFILE = 0x00000010
LR_SHARED = 0x00008000

# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getstockobject#WHITE_BRUSH
WHITE_BRUSH = 0

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-monitorinfo#dwFlags
MONITORINFOF_PRIMARY = 0x00000001

MAX_CLASS_NAME = 256

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-wineventproc
WINEVENTPROC = WINFUNCTYPE(None, HWINEVENTHOOK, DWORD, HWND, LONG, LONG, DWORD, DWORD)

# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms633498(v=vs.85)
WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)

# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms633573(v=vs.85)
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)

# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-monitorenumproc
MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, LPRECT, LPARAM)


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-iconinfoexw
class ICONINFOEXW(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("fIcon", BOOL),
        ("xHotspot", DWORD),
        ("yHotspot", DWORD),
        ("hbmMask", HBITMAP),
        ("hbmColor", HBITMAP),
        ("wResID", WORD),
        ("szModName", WCHAR * MAX_PATH),
        ("szResName", WCHAR * MAX_PATH)
    ]


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-wndclassexw
class WNDCLASSEXW(Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("style", UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", INT),
        ("cbWndExtra", INT),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPWSTR),
        ("lpszClassName", LPWSTR),
        ("hIconSm", HICON),
    ]


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-scrollinfo
class SCROLLINFO(Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("fMask", UINT),
        ("nMin", INT),
        ("nMax", INT),
        ("nPage", UINT),
        ("nPos", INT),
        ("nTrackPos", INT),
    ]


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-paintstruct
class PAINTSTRUCT(Structure):
    _fields_ = [
        ("hdc", HDC),
        ("fErase", BOOL),
        ("rcPaint", RECT),
        ("fRestore", BOOL),
        ("fIncUpdate", BOOL),
        ("rgbReserved", BYTE * 32),
    ]


# https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-monitorinfo
class MONITORINFO(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", DWORD),
    ]


PICONINFOEXW = POINTER(ICONINFOEXW)

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessagew
GetMessageW: Callable[
    [Union[POINTER(MSG), any], int, int, int], int
] = windll.user32.GetMessageW
GetMessageW.restype = BOOL
GetMessageW.argtypes = [POINTER(MSG), HWND, UINT, UINT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postquitmessage
PostQuitMessage: Callable[[int], None] = windll.user32.PostQuitMessage
PostQuitMessage.restype = None
PostQuitMessage.argtypes = [INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-translatemessage
TranslateMessage: Callable[
    [Union[POINTER(MSG), any]], int
] = windll.user32.TranslateMessage
TranslateMessage.restype = BOOL
TranslateMessage.argtypes = [POINTER(MSG)]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dispatchmessagew
DispatchMessageW: Callable[
    [Union[POINTER(MSG), any]], int
] = windll.user32.DispatchMessageW
DispatchMessageW.restype = LRESULT
DispatchMessageW.argtypes = [POINTER(MSG)]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postthreadmessagew
PostThreadMessageW: Callable[
    [int, int, int, int], int
] = windll.user32.PostThreadMessageW
PostThreadMessageW.restype = BOOL
PostThreadMessageW.argtypes = [DWORD, UINT, WPARAM, LPARAM]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getsystemmetrics
GetSystemMetrics: Callable[[int], int] = windll.user32.GetSystemMetrics
GetSystemMetrics.restype = INT
GetSystemMetrics.argtypes = [INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerclassexw
RegisterClassExW: Callable[
    [Union[POINTER(WNDCLASSEXW), any]], int
] = windll.user32.RegisterClassExW
RegisterClassExW.restype = ATOM
RegisterClassExW.argtypes = [POINTER(WNDCLASSEXW)]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unregisterclassw
UnregisterClassW: Callable[
    [Union[UnicodeBuffer, int], int], int
] = windll.user32.UnregisterClassW
UnregisterClassW.restype = BOOL
UnregisterClassW.argtypes = [LONG_PTR, HINSTANCE]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumwindows
EnumWindows: Callable[[WNDENUMPROC, int], int] = windll.user32.EnumWindows
EnumWindows.restype = BOOL
EnumWindows.argtypes = [WNDENUMPROC, LPARAM]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdesktopwindows
EnumDesktopWindows: Callable[[int, WNDENUMPROC, int], int] = windll.user32.EnumDesktopWindows
EnumDesktopWindows.restype = BOOL
EnumDesktopWindows.argtypes = [HDESK, WNDENUMPROC, LPARAM]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getforegroundwindow
GetForegroundWindow: Callable[[], int] = windll.user32.GetForegroundWindow
GetForegroundWindow.restype = HWND
GetForegroundWindow.argtypes = None

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexw
CreateWindowExW: Callable[
    [
        int,
        Union[UnicodeBuffer, int],
        UnicodeBuffer,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        Union[LPVOID, any],
    ],
    int,
] = windll.user32.CreateWindowExW
CreateWindowExW.restype = HWND
CreateWindowExW.argtypes = [
    DWORD,
    LONG_PTR,
    LPWSTR,
    DWORD,
    INT,
    INT,
    INT,
    INT,
    HWND,
    HMENU,
    HINSTANCE,
    LPVOID,
]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-destroywindow
DestroyWindow: Callable[[int], int] = windll.user32.DestroyWindow
DestroyWindow.restype = BOOL
DestroyWindow.argtypes = [HWND]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongptrw
GetWindowLongPtrW: Callable[[int, int], int] = windll.user32.GetWindowLongPtrW
GetWindowLongPtrW.restype = LONG_PTR
GetWindowLongPtrW.argtypes = [HWND, INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
GetWindowThreadProcessId: Callable[
    [int, Union[LPDWORD, any]], int
] = windll.user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = DWORD
GetWindowThreadProcessId.argtypes = [HWND, LPDWORD]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclassnamew
GetClassNameW: Callable[[int, UnicodeBuffer, int], int] = windll.user32.GetClassNameW
GetClassNameW.restype = INT
GetClassNameW.argtypes = [HWND, LPWSTR, INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-isiconic
IsIconic: Callable[[int], int] = windll.user32.IsIconic
IsIconic.restype = INT
IsIconic.argtypes = [INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtextw
GetWindowTextLengthW: Callable[[int], int] = windll.user32.GetWindowTextLengthW
GetWindowTextLengthW.restype = INT
GetWindowTextLengthW.argtypes = [INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowtextw
GetWindowTextW: Callable[[int, UnicodeBuffer, int], int] = windll.user32.GetWindowTextW
GetWindowTextW.restype = INT
GetWindowTextW.argtypes = [HWND, LPWSTR, INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowtextw
SetWindowTextW: Callable[[int, UnicodeBuffer], int] = windll.user32.SetWindowTextW
SetWindowTextW.restype = BOOL
SetWindowTextW.argtypes = [HWND, LPWSTR]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
ShowWindow: Callable[[int, int], int] = windll.user32.ShowWindow
ShowWindow.restype = BOOL
ShowWindow.argtypes = [HWND, INT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-updatewindow
UpdateWindow: Callable[[int], int] = windll.user32.UpdateWindow
UpdateWindow.restype = BOOL
UpdateWindow.argtypes = [HWND]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-defwindowprocw
DefWindowProcW: Callable[[int, int, int, int], int] = windll.user32.DefWindowProcW
DefWindowProcW.restype = LRESULT
DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-beginpaint
BeginPaint: Callable[
    [int, Union[POINTER(PAINTSTRUCT), any]], int
] = windll.user32.BeginPaint
BeginPaint.restype = HDC
BeginPaint.argtypes = [HWND, POINTER(PAINTSTRUCT)]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-endpaint
EndPaint: Callable[
    [int, Union[POINTER(PAINTSTRUCT), any]], int
] = windll.user32.EndPaint
EndPaint.restype = BOOL
EndPaint.argtypes = [HWND, POINTER(PAINTSTRUCT)]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook
SetWinEventHook: Callable[
    [int, int, int, WINEVENTPROC, int, int, int], int
] = windll.user32.SetWinEventHook
SetWinEventHook.restype = HWINEVENTHOOK
SetWinEventHook.argtypes = [DWORD, DWORD, HMODULE, WINEVENTPROC, DWORD, DWORD, DWORD]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unhookwinevent
UnhookWinEvent: Callable[[int], int] = windll.user32.UnhookWinEvent
UnhookWinEvent.restype = BOOL
UnhookWinEvent.argtypes = [HWINEVENTHOOK]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect
GetWindowRect: Callable[[int, Union[LPRECT, any]], int] = windll.user32.GetWindowRect
GetWindowRect.restype = BOOL
GetWindowRect.argtypes = [HWND, LPRECT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getclientrect
GetClientRect: Callable[[int, Union[LPRECT, any]], int] = windll.user32.GetClientRect
GetClientRect.restype = BOOL
GetClientRect.argtypes = [HWND, LPRECT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-enumdisplaymonitors
EnumDisplayMonitors: Callable[
    [int, Union[LPRECT, any], MONITORENUMPROC, int], int
] = windll.user32.EnumDisplayMonitors
EnumDisplayMonitors.restype = BOOL
EnumDisplayMonitors.argtypes = [HDC, LPRECT, MONITORENUMPROC, LPARAM]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmonitorinfow
GetMonitorInfoW: Callable[
    [int, Union[POINTER(MONITORINFO), any]], int
] = windll.user32.GetMonitorInfoW
GetMonitorInfoW.restype = BOOL
GetMonitorInfoW.argtypes = [HMONITOR, POINTER(MONITORINFO)]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadimagew
LoadImageW: Callable[
    [int, UnicodeBuffer, int, int, int, int], int
] = windll.user32.LoadImageW
LoadImageW.restype = HANDLE
LoadImageW.argtypes = [HINSTANCE, PVOID, UINT, INT, INT, UINT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setscrollinfo
SetScrollInfo: Callable[[int, int, Union[POINTER(SCROLLINFO), any], bool], int] = windll.user32.SetScrollInfo
SetScrollInfo.restype = INT
SetScrollInfo.argtypes = [HWND, INT, POINTER(SCROLLINFO), BOOL]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getscrollinfo
GetScrollInfo: Callable[[int, int, Union[POINTER(SCROLLINFO), any]], int] = windll.user32.GetScrollInfo
GetScrollInfo.restype = BOOL
GetScrollInfo.argtypes = [HWND, INT, POINTER(SCROLLINFO)]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-scrollwindowex
ScrollWindowEx: Callable[
    [int, int, int, Union[LPRECT, any], Union[LPRECT, any], int, Union[LPRECT, any], int], int
] = windll.user32.ScrollWindowEx
ScrollWindowEx.restype = INT
ScrollWindowEx.argtypes = [HWND, INT, INT, LPRECT, LPRECT, HRGN, LPRECT, UINT]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowdc
GetWindowDC: Callable[[int], int] = windll.user32.GetWindowDC
GetWindowDC.restype = HDC
GetWindowDC.argtypes = [HWND]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getdc
GetDC: Callable[[int], int] = windll.user32.GetDC
GetDC.restype = HDC
GetDC.argtypes = [HWND]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-releasedc
ReleaseDC: Callable[[int, int], int] = windll.user32.ReleaseDC
ReleaseDC.restype = INT
ReleaseDC.argtypes = [HWND, HDC]

# winuser.h
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-geticoninfoexw
GetIconInfoExW: Callable[[int, Union[PICONINFOEXW, any]], int] = windll.user32.GetIconInfoExW
GetIconInfoExW.restype = BOOL
GetIconInfoExW.argtypes = [HICON, PICONINFOEXW]
