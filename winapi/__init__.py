from ctypes import Array, create_unicode_buffer, cast
from ctypes.wintypes import HANDLE, HICON, LPARAM, WPARAM, WCHAR, LPVOID, LPWSTR
from typing import Callable, Union

UnicodeBuffer = Union[LPWSTR, Array[WCHAR], None]

NULL = 0
PVOID = LPVOID
LONG_PTR = LPARAM
UINT_PTR = WPARAM
LRESULT = LONG_PTR
HCURSOR = HICON
HWINEVENTHOOK = HANDLE

# https://docs.microsoft.com/en-us/windows/win32/seccrypto/common-hresult-values#S_OK
S_OK: int = 0


def _text(string: str) -> LPWSTR:
    return cast(create_unicode_buffer(string), LPWSTR)


def _loword(double_word: int) -> int:
    return double_word & 0xFFFF


def _hiword(double_word: int) -> int:
    return (double_word >> 16) & 0xFFFF


TEXT: Callable[[str], LPWSTR] = _text

# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms632659(v=vs.85)
LOWORD: Callable[[int], int] = _loword

# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms632657(v=vs.85)
HIWORD: Callable[[int], int] = _hiword
