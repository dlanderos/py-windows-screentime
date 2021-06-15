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

from ctypes.wintypes import RECT, LONG
from dataclasses import dataclass, field
from typing import Union


@dataclass(frozen=True, eq=True)
class Rectangle:
    left: int = field(hash=True, compare=True, default=0)
    top: int = field(hash=True, compare=True, default=0)
    right: int = field(hash=True, compare=True, default=0)
    bottom: int = field(hash=True, compare=True, default=0)
    width: int = field(hash=True, compare=True, default=0)
    height: int = field(hash=True, compare=True, default=0)
    area: int = field(hash=True, compare=True, default=0)


def rectangle_from_positions(
        left: Union[int, LONG],
        top: Union[int, LONG],
        right: Union[int, LONG],
        bottom: Union[int, LONG]
):
    width = abs(right - left)
    height = abs(bottom - top)
    area = width * height
    return Rectangle(left, top, right, bottom, width, height, area)


def rectangle_from_rect(rect: RECT) -> Rectangle:
    return rectangle_from_positions(rect.left, rect.top, rect.right, rect.bottom)


def rectangle_intersection(region1: Rectangle, region2: Rectangle) -> Rectangle:
    return rectangle_from_positions(
        max(region1.left, region2.left),
        max(region1.top, region2.top),
        min(region1.right, region2.right),
        min(region1.bottom, region2.bottom),
    )
