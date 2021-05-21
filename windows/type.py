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

from ctypes import c_int64, c_void_p, WINFUNCTYPE
from ctypes.wintypes import DWORD, HWND, LONG, LPARAM, PLONG, HANDLE, BOOL

# PVOID type mapping. Used to maintain consistency with the Windows API.
# https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types#PVOID
PVOID = c_void_p

# LRESULT type mapping. Used to maintain consistency with the Windows API.
# https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types#LRESULT
LRESULT = PLONG

# HRESULT type mapping. Used to maintain consistency with the Windows API.
# https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types#HRESULT
HRESULT = LONG

# LONG_PTR type mapping. Used to maintain consistency with the Windows API.
# https://docs.microsoft.com/en-us/windows/win32/winprog/windows-data-types#LONG_PTR
LONG_PTR = c_int64

# Callback that is called whenever a specific set of events are created.
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-wineventproc
WINEVENTPROC = WINFUNCTYPE(
    None,
    HANDLE,
    DWORD,
    HWND,
    LONG,
    LONG,
    DWORD,
    DWORD,
)

# Callback that is called whenever a Window has been found in the EnumDesktopWindows or EnumWindows function.
# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms633498(v=vs.85)
WNDENUMPROC = WINFUNCTYPE(
    BOOL,
    HWND,
    LPARAM,
)
