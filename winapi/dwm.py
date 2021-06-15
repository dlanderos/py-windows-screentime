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

from ctypes import windll, HRESULT
from ctypes.wintypes import DWORD, HWND
from typing import Union, Callable
from winapi import PVOID

# https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
DWMWA_CLOAKED: int = 14

# dwmapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/nf-dwmapi-dwmgetwindowattribute
DwmGetWindowAttribute: Callable[[int, int, Union[PVOID, any], int], int] = windll.dwmapi.DwmGetWindowAttribute
DwmGetWindowAttribute.restype = HRESULT
DwmGetWindowAttribute.argtypes = [HWND, DWORD, PVOID, DWORD]
