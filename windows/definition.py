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

# Permission to query process information.
# https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights#PROCESS_QUERY_INFORMATION
PROCESS_QUERY_INFORMATION = 0x0400

# Permission to read process memory.
# https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights#PROCESS_VM_READ
PROCESS_VM_READ = 0x0010

# Events must be asynchronous and sequentially ordered.
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook#WINEVENT_OUTOFCONTEXT
WINEVENT_OUTOFCONTEXT = 0x0000

# Ignore events originating from self.
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook#WINEVENT_SKIPOWNPROCESS
WINEVENT_SKIPOWNPROCESS = 0x0002

# Lowest possible value of an event type value.
# https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants#EVENT_MIN
EVENT_MIN = 0x00000001

# Highest possible value of an event type value.
# https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants#EVENT_MAX
EVENT_MAX = 0x7FFFFFFF

# Listen to events where a window is away from or to the foreground.
# https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants#EVENT_SYSTEM_FOREGROUND
EVENT_SYSTEM_FOREGROUND = 0x0003

# Listen to events where a window has been maximized.
# https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants#EVENT_SYSTEM_MINIMIZEEND
EVENT_SYSTEM_MINIMIZEEND = 0x0017

# Listen to events where a window has been minimized.
# https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants#EVENT_SYSTEM_MINIMIZESTART
EVENT_SYSTEM_MINIMIZESTART = 0x0016

# Tell a message queue receiver to stop listening for messages.
# https://docs.microsoft.com/en-us/windows/desktop/winmsg/wm-quit
WM_QUIT = 0x0012

# Gets or sets the windows style.
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongptrw#GWL_STYLE
GWL_STYLE = -16

# Gets or sets whether or not the window is visible.
# https://docs.microsoft.com/en-us/windows/win32/winmsg/window-styles#WS_VISIBLE
WS_VISIBLE = 0x10000000

# Gets or sets whether or not the window has a menu in its title bar.
# https://docs.microsoft.com/en-us/windows/win32/winmsg/window-styles#WS_VISIBLE
WS_SYSMENU = 0x00080000

# Gets or sets whether or not the window is cloaked (invisible/minimized).
# https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute#DWMWA_CLOAKED
DWMWA_CLOAKED = 14

# Gets the previous window (higher in Z-order).
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindow#GW_HWNDPREV
GW_HWNDPREV = 3

# If a procedure was successful
# https://docs.microsoft.com/en-us/windows/win32/seccrypto/common-hresult-values#S_OK
S_OK = 0
