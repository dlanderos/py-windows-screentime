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

from ctypes import windll, Structure, POINTER
from ctypes.wintypes import INT, HGDIOBJ, BOOL, LPPOINT, HDC, LONG, WCHAR, BYTE, DWORD, LPVOID, HANDLE, WORD, HBITMAP, \
    UINT, LPCWSTR, HPEN, LPRECT
from typing import Callable, Union
from winapi import PVOID, UnicodeBuffer

# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdevicecaps
HORZRES = 8
VERTRES = 10
BITSPIXEL = 12
PLANES = 14
ASPECTX = 40
ASPECTY = 42
SYSTEM_FONT = 13

PS_SOLID = 0
PS_DASH = 1
PS_DOT = 2
PS_DASHDOT = 3
PS_DASHDOTDOT = 4
PS_NULL = 5
PS_INSIDEFRAME = 6
PS_USERSTYLE = 7
PS_ALTERNATE = 8

RGN_ERROR = 0
NULLREGION = 1
SIMPLEREGION = 2
COMPLEXREGION = 3


# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-textmetricw
class TEXTMETRICW(Structure):
    _fields_ = [
        ("tmHeight", LONG),
        ("tmAscent", LONG),
        ("tmDescent", LONG),
        ("tmInternalLeading", LONG),
        ("tmExternalLeading", LONG),
        ("tmAveCharWidth", LONG),
        ("tmMaxCharWidth", LONG),
        ("tmWeight", LONG),
        ("tmOverhang", LONG),
        ("tmDigitizedAspectX", LONG),
        ("tmDigitizedAspectY", LONG),
        ("tmFirstChar", WCHAR),
        ("tmLastChar", WCHAR),
        ("tmDefaultChar", WCHAR),
        ("tmBreakChar", WCHAR),
        ("tmItalic", BYTE),
        ("tmUnderlined", BYTE),
        ("tmStruckOut", BYTE),
        ("tmPitchAndFamily", BYTE),
        ("tmCharSet", BYTE)
    ]


# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmap
class BITMAP(Structure):
    _fields_ = [
        ("bmType", LONG),
        ("bmWidth", LONG),
        ("bmHeight", LONG),
        ("bmWidthBytes", LONG),
        ("bmPlanes", WORD),
        ("bmBitsPixel", WORD),
        ("bmBits", LPVOID)
    ]


# wingdi.h
COLORREF = DWORD

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getclipbox
GetClipBox: Callable[[int, Union[LPRECT, any]], int] = windll.gdi32.GetClipBox
GetClipBox.restype = INT
GetClipBox.argtypes = [HDC, LPRECT]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-textmetricw
LPTEXTMETRICW = POINTER(TEXTMETRICW)

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getstockobject
GetStockObject: Callable[[int], int] = windll.gdi32.GetStockObject
GetStockObject.restype = HGDIOBJ
GetStockObject.argtypes = [INT]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getobjectw
GetObjectW: Callable[[int, int, Union[LPVOID, any]], int] = windll.gdi32.GetObjectW
GetObjectW.restype = INT
GetObjectW.argtypes = [HANDLE, INT, LPVOID]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-selectobject
SelectObject: Callable[[int, int], int] = windll.gdi32.SelectObject
SelectObject.restype = HGDIOBJ
SelectObject.argtypes = [HDC, HGDIOBJ]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deleteobject
DeleteObject: Callable[[int], bool] = windll.gdi32.DeleteObject
DeleteObject.restype = BOOL
DeleteObject.argtypes = [HGDIOBJ]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createdcw
CreateDCW: Callable[[UnicodeBuffer, UnicodeBuffer, UnicodeBuffer, Union[PVOID, any]], int] = windll.gdi32.CreateDCW
CreateDCW.restype = HDC
CreateDCW.argtypes = [LPCWSTR, LPCWSTR, LPCWSTR, PVOID]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createcompatibledc
CreateCompatibleDC: Callable[[int], int] = windll.gdi32.CreateCompatibleDC
CreateCompatibleDC.restype = HDC
CreateCompatibleDC.argtypes = [HDC]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deletedc
DeleteDC: Callable[[int], int] = windll.gdi32.DeleteDC
DeleteDC.restype = BOOL
DeleteDC.argtypes = [HDC]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-lptodp
LPtoDP: Callable[[int, Union[LPPOINT, any], int], int] = windll.gdi32.LPtoDP
LPtoDP.restype = BOOL
LPtoDP.argtypes = [HDC, LPPOINT, INT]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-gettextmetricsw
GetTextMetricsW: Callable[[int, Union[LPTEXTMETRICW, any]], int] = windll.gdi32.GetTextMetricsW
GetTextMetricsW.restype = BOOL
GetTextMetricsW.argtypes = [HDC, LPTEXTMETRICW]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdevicecaps
GetDeviceCaps: Callable[[int, int], int] = windll.gdi32.GetDeviceCaps
GetDeviceCaps.restype = INT
GetDeviceCaps.argtypes = [HDC, INT]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-bitblt
BitBlt: Callable[[int, int, int, int, int, int, int, int, int], int] = windll.gdi32.BitBlt
BitBlt.restype = BOOL
BitBlt.argtypes = [HDC, INT, INT, INT, INT, HDC, INT, INT, DWORD]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-stretchblt
StretchBlt: Callable[[int, int, int, int, int, int, int, int, int, int, int], int] = windll.gdi32.StretchBlt
StretchBlt.restype = BOOL
StretchBlt.argtypes = [HDC, INT, INT, INT, INT, HDC, INT, INT, INT, INT, DWORD]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createbitmap
CreateBitmap: Callable[[int, int, int, int, Union[PVOID, any]], int] = windll.gdi32.CreateBitmap
CreateBitmap.restype = HBITMAP
CreateBitmap.argtypes = [INT, INT, UINT, UINT, PVOID]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-textoutw
TextOutW: Callable[[int, int, int, UnicodeBuffer, int], int] = windll.gdi32.TextOutW
TextOutW.restype = BOOL
TextOutW.argtypes = [HDC, INT, INT, LPCWSTR, INT]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-rectangle
Rectangle: Callable[[int, int, int, int, int], int] = windll.gdi32.Rectangle
Rectangle.restype = BOOL
Rectangle.argtypes = [HDC, INT, INT, INT, INT]

# wingdi.h
# https://docs.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createpen
CreatePen: Callable[[int, int, int], int] = windll.gdi32.CreatePen
CreatePen.restype = HPEN
CreatePen.argtypes = [INT, INT, COLORREF]
