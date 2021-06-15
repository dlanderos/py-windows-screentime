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

from typing import Callable, Union
from winapi import UnicodeBuffer
from ctypes import windll, HRESULT
from ctypes.wintypes import LPVOID, PWORD, LPWSTR, HINSTANCE, HICON

# https://docs.microsoft.com/en-us/windows/win32/api/shellapi/ne-shellapi-query_user_notification_state
QUNS_NOT_PRESENT = 1
QUNS_BUSY = 2
QUNS_RUNNING_D3D_FULL_SCREEN = 3
QUNS_PRESENTATION_MODE = 4
QUNS_ACCEPTS_NOTIFICATIONS = 5
QUNS_QUIET_TIME = 6
QUNS_APP = 7

# shellapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shqueryusernotificationstate
SHQueryUserNotificationState: Callable[[Union[LPVOID, any]], int] = windll.shell32.SHQueryUserNotificationState
SHQueryUserNotificationState.restype = HRESULT
SHQueryUserNotificationState.argtypes = [LPVOID]

# shellapi.h
# https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-extractassociatediconw
ExtractAssociatedIconW: Callable[[int, UnicodeBuffer, Union[PWORD, any]], int] = windll.shell32.ExtractAssociatedIconW
ExtractAssociatedIconW.restype = HICON
ExtractAssociatedIconW.argtypes = [HINSTANCE, LPWSTR, PWORD]
