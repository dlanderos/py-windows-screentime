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

from dataclasses import dataclass
from ctypes.wintypes import RECT


@dataclass(frozen=True)
class Rectangle:
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0


def rectangle_from_structure(structure: RECT):
    # noinspection PyTypeChecker
    return Rectangle(
        left=structure.left,
        top=structure.top,
        right=structure.right,
        bottom=structure.bottom
    )


def rectangle_area(rectangle: Rectangle):
    return (rectangle.right - rectangle.left) * (rectangle.bottom - rectangle.top)


def rectangle_intersection(rectangle1: Rectangle, rectangle2: Rectangle) -> Rectangle:
    return Rectangle(
        left=max(rectangle1.left, rectangle2.left),
        top=max(rectangle1.top, rectangle2.top),
        right=min(rectangle1.right, rectangle2.right),
        bottom=min(rectangle1.bottom, rectangle2.bottom)
    )


def idk_yet(rectangle1):
    pass
