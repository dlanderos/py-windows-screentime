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

from typing import Callable, Any, Union
from winapi import UnicodeBuffer
from ctypes import windll
from ctypes.wintypes import (
    DWORD, LPCWSTR, HMODULE, HANDLE, BOOL, LPWSTR, PDWORD
)

# https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# libloaderapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulehandlew
GetModuleHandleW: Callable[[UnicodeBuffer], int] = windll.kernel32.GetModuleHandleW
GetModuleHandleW.restype = HMODULE
GetModuleHandleW.argtypes = [LPCWSTR]

# libloaderapi
# https://docs.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamew
GetModuleFileNameW: Callable[[int, UnicodeBuffer, int], int] = windll.kernel32.GetModuleFileNameW
GetModuleFileNameW.restype = DWORD
GetModuleFileNameW.argtypes = [HMODULE, LPWSTR, DWORD]

# processthreadsapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentthreadid
GetCurrentThreadId: Callable[[], int] = windll.kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = DWORD
GetCurrentThreadId.argtypes = None

# processthreadsapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess
OpenProcess: Callable[[int, bool, int], int] = windll.kernel32.OpenProcess
OpenProcess.restype = HANDLE
OpenProcess.argtypes = [DWORD, BOOL, DWORD]

# processthreadsapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
CloseHandle: Callable[[int], bool] = windll.kernel32.CloseHandle
CloseHandle.restype = BOOL
CloseHandle.argtypes = [HANDLE]

# psapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getprocessimagefilenamew
GetProcessImageFileNameW: Callable[[int, UnicodeBuffer, int], int] = windll.kernel32.K32GetProcessImageFileNameW
GetProcessImageFileNameW.restype = DWORD
GetProcessImageFileNameW.argtypes = [HANDLE, LPWSTR, DWORD]

# winbase.h
# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-queryfullprocessimagenamew
QueryFullProcessImageNameW: Callable[
    [int, int, UnicodeBuffer, Union[PDWORD, Any]], bool
] = windll.kernel32.QueryFullProcessImageNameW
QueryFullProcessImageNameW.restype = BOOL
QueryFullProcessImageNameW.argtypes = [HANDLE, DWORD, LPWSTR, PDWORD]
