#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - canvas
# ==========================================
#
#
# 
"""
from typing import List, Tuple, Union
from types import MethodType
from .area import Area, Text, Line, Scatter, Rect, COLOR_PALETTE, KEYNAMES
from .._utils.warns import custom_warn
import warnings
warnings.showwarning = custom_warn


class PlotArea(Area):
    def __init__(self, name: str, scale: Tuple[Union[int, float], ...], **options):
        super(PlotArea, self).__init__(**options)
        self._name = name
        self._scale: Tuple[Union[int, float], ...] = scale
        self._clip_outside = True

    def ppu(self, axis: str):
        def distance(x, y):
            return abs(x - y)
        if axis == "x":
            return self._width / distance(*self._scale[:2])
        elif axis == "y":
            return self._height / distance(*self._scale[2:4])
        else:
            raise KeyError(f"axis mush be given as one of x or y, got {axis} instead.")

    def scale(self, scale: Tuple[Union[int, float], ...] = None):
        if scale is not None:
            self._scale = scale
        return self._scale

    def scale_to_points(self, x, y, coordinate: str = "scale"):
        if coordinate != "scale":
            return x, y
        x = (x - self._scale[0]) * self.ppu("x") + self._margin_left
        y = (y - self._scale[2]) * self.ppu("y") + self._margin_bottom
        return x, y

    def clip_curve(self, x, y, func_y: MethodType, func_x: MethodType, x_clip=True, y_clip=True):
        if not self.is_out_side(x, y):
            return x, y
        if func_y is None:
            if y_clip:
                if self._margin_bottom <= y <= self._margin_bottom + self._height:
                    return
                else:
                    return x, self._margin_bottom if y < self._margin_bottom else self._margin_bottom + self._height
        if func_x is None:
            if x_clip:
                if self._margin_left <= x <= self._margin_left + self._width:
                    return
                else:
                    return self._margin_left if x < self._margin_left else self._margin_left + self._width, y
        if x_clip:
            if func_y is None and not (self._margin_left <= x <= self._margin_left + self._width):
                return
            elif func_y is None:
                func_y = lambda _x: y
            if x > self._margin_left + self._width:
                x = self._margin_left + self._width
            if x < self._margin_left:
                x = self._margin_left
            y = func_y(x)
        if y_clip:
            if func_x is None and not (self._margin_bottom <= y <= self._margin_bottom + self._height):
                return
            elif func_x is None:
                func_x = lambda _y: x
            if y > self._margin_bottom + self._height:
                y = self._margin_bottom + self._height
            if y < self._margin_bottom:
                y = self._margin_bottom
            x = func_x(y)
        if self.is_out_side(x, self._margin_bottom) and x_clip:
            return
        if self.is_out_side(self._margin_left, y) and y_clip:
            return
        if self.is_out_side(x, y) and (x_clip == y_clip):
            return
        return x, y

    def _clip_line(self, x, y, start, end, x_clip=True, y_clip=True):
        if end[0] - start[0] != 0:
            func_y = lambda x: (end[1] - start[1]) / (end[0] - start[0]) * (x - start[0]) + start[1]
        else:
            func_y = None
        if end[1] - start[1] != 0:
            func_x = lambda y: (end[0] - start[0]) / (end[1] - start[1]) * (y - start[1]) + start[0]
        else:
            func_x = None
        return self.clip_curve(x, y, func_y=func_y, func_x=func_x, x_clip=x_clip, y_clip=y_clip)

    def clip_line(self, start, end, x_clip=True, y_clip=True):
        _start = self._clip_line(*start, start, end, x_clip=x_clip, y_clip=y_clip)
        _end = self._clip_line(*end, start, end, x_clip=x_clip, y_clip=y_clip)
        if _start is not None and _end is not None:
            return _start, _end

    def is_out_side(self, x, y):
        return not (self._margin_left <= x <= self._margin_left + self._width and
                    self._margin_bottom <= y <= self._margin_bottom + self._height)

    def text(self, x, y, coordinate="scale", clip: bool = True, **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        x, y = self.scale_to_points(x, y, coordinate)
        if clip:
            if self.is_out_side(x, y):
                warnings.warn(f"The given text at {x, y} is on the outside of the plot area, "
                              f"and thus will have no effect.", UserWarning)
                return
        return super(PlotArea, self).text(x=x, y=y, **options)

    def line(self, start: List[int], end: List[int], coordinate="scale", clip: bool = True,
             x_clip=True, y_clip=True, **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        start = self.scale_to_points(*start, coordinate)
        end = self.scale_to_points(*end, coordinate)
        if clip:
            try:
                start, end = self.clip_line(start, end, x_clip=x_clip, y_clip=y_clip)
            except TypeError:
                warnings.warn(f"The line from {start} to {end} is on the outside of the plot area, "
                              f"and thus will have no effect.", UserWarning)
                return
        return super(PlotArea, self).line(start=list(start), end=list(end), **options)

    def rect(self, left_bottom: Union[list, tuple], width: Union[int, float], height: Union[int, float],
             coordinate: str = "scale", **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        left_bottom = self.scale_to_points(*left_bottom, coordinate=coordinate)
        width = width * self.ppu(axis="x")
        height = height * self.ppu(axis="y")
        return super(PlotArea, self).rect(left_bottom=left_bottom, width=width, height=height, **options)

    def scatter(self, x: Union[int, float], y: Union[int, float], coordinate: str = "scale", **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        x, y = self.scale_to_points(x, y, coordinate)
        if self.is_out_side(x, y):
            warnings.warn(f"The scatter at {x, y} is on the outside of the plot area, "
                          f"and thus will have no effect.", UserWarning)
        else:
            return super(PlotArea, self).scatter(x=x, y=y, **options)
