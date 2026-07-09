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
from typing import List, Union
from types import MethodType
from .area import Area, KEYNAMES
from .._utils.warns import custom_warn
from ..core.objs import Obj
import warnings
warnings.showwarning = custom_warn

DEFAULT_AXIS_CONFIG = {
    "name": "NAME",
    "x": 0,
    "y": 0,
    "line_length": 300,
    "major_ticks_inc": 10,
    "major_tick_direction": -1,
    "major_width": 1,
    "line_width": 1,
    "major_labels": [],
    "font_name": "",
    "font": "",
    "label_h_align": "middle",
    "label_v_align": "top",
    "label_offset": [0, 0],
    "title_offset": [0, -20],
    "title_rotate": 0,
    "title": "Title",
    "from": 0,
    "to": 100,
    "direction": 0,
    "show_title": True,
    "show_ticks": True,
    "show_labels": True,
    "show_major_ticks": True,
    "show_minor_ticks": False,
    "show_major_labels": True,
    "show_minor_labels": False,
}


class PlotArea(Area):
    def __init__(self, name: str, scale: List[Union[int, float, str]], **options):
        self._name = name
        self._scale: List[Union[int, float, str]] = [float(i) for i in scale]
        self._clip_outside = True
        self._background_color = 'none'
        self._background_style = 'none'            # background color mode
        self._font: Obj = ...
        super(PlotArea, self).__init__(**options)

    def ppu(self, axis: str):
        def distance(x, y):
            return abs(x - y)
        if axis == "x":
            return self._width / distance(*self._scale[:2])
        elif axis == "y":
            return self._height / distance(*self._scale[2:4])
        else:
            raise KeyError(f"axis mush be given as one of x or y, got {axis} instead.")

    def scale(self, scale: List[Union[int, float]] = None):
        if scale is not None:
            self._scale = scale
        return self._scale

    def scale_to_points(self, x, y, coordinate: str = "scale"):
        x = float(x)
        y = float(y)
        if coordinate != "scale":
            return x, y
        x = (x - self._scale[0]) * self.ppu("x") + self._margin_left
        y = (y - self._scale[2]) * self.ppu("y") + self._margin_bottom
        return x, y

    def clip_curve(self, x, y, func_y: MethodType, func_x: MethodType, x_clip=True, y_clip=True, tolerance: float = 0.00000000001):
        if not self.is_out_side(x, y, tolerance=tolerance):
            return x, y
        if func_y is None:
            if y_clip:
                if self._margin_bottom - tolerance <= y <= self._margin_bottom + self._height + tolerance:
                    return
                else:
                    return x, self._margin_bottom if y < self._margin_bottom else self._margin_bottom + self._height
        if func_x is None:
            if x_clip:
                if self._margin_left <= x <= self._margin_left + self._width + tolerance:
                    return
                else:
                    return self._margin_left if x < self._margin_left else self._margin_left + self._width, y
        if x_clip:
            if func_y is None and not (self._margin_left <= x <= self._margin_left + self._width + tolerance):
                return
            elif func_y is None:
                func_y = lambda _x: y
            if x > self._margin_left + self._width:
                x = self._margin_left + self._width
            if x < self._margin_left:
                x = self._margin_left
            y = func_y(x)
        if y_clip:
            if func_x is None and not (self._margin_bottom - tolerance <= y <= self._margin_bottom + self._height + tolerance):
                return
            elif func_x is None:
                func_x = lambda _y: x
            if y > self._margin_bottom + self._height:
                y = self._margin_bottom + self._height
            if y < self._margin_bottom:
                y = self._margin_bottom
            x = func_x(y)
        if self.is_out_side(x, self._margin_bottom, tolerance=tolerance) and x_clip:
            return
        if self.is_out_side(self._margin_left, y, tolerance=tolerance) and y_clip:
            return
        if self.is_out_side(x, y, tolerance=tolerance) and (x_clip == y_clip):
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

    def is_out_side(self, x, y, tolerance: float = 0.00000000001):
        return not (self._margin_left - tolerance <= x <= self._margin_left + tolerance + self._width and
                    self._margin_bottom - tolerance <= y <= self._margin_bottom + tolerance + self._height)

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

    def line(self, points: list, coordinate="scale", clip: bool = True, x_clip=True, y_clip=True, **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        points = [self.scale_to_points(*point, coordinate) for point in points]
        if clip:
            for i in range(len(points) - 1):
                try:
                    points[i:i+2] = self.clip_line(points[i], points[i+1], x_clip=x_clip, y_clip=y_clip)
                except TypeError:
                    warnings.warn(f"The line from {points[i]} to {points[i+1]} is on the outside of the plot area, "
                                  f"and thus will have no effect.", UserWarning)
                    return
        return super(PlotArea, self).line(points=points, **options)

    def rect(self, left_bottom: Union[list, tuple], width: Union[int, float], height: Union[int, float],
             coordinate: str = "scale", clip: bool = True, **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        left_bottom = self.scale_to_points(*left_bottom, coordinate=coordinate)
        width = width * self.ppu(axis="x")
        height = height * self.ppu(axis="y")
        if clip:
            try:
                left_bottom, left_top = self.clip_line(start=left_bottom, end=[left_bottom[0], left_bottom[1] + height])
                right_bottom, right_top = self.clip_line(start=[left_bottom[0] + width, left_bottom[1]], end=[left_bottom[0] + width, left_bottom[1] + height])
            except TypeError:
                warnings.warn(f"The rect of {left_bottom = } {width = } {height = } is on the outside of the plot area, "
                              f"and thus will have no effect.", UserWarning)
                return
            else:
                width = abs(right_bottom[0] - left_bottom[0])
                height = abs(left_top[1] - left_bottom[1])

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

    def axis(self, **options):
        return super(PlotArea, self).axis(**options)

    def xaxis_bottom(self, **options):

        XAXIS_BOTTOM_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "XAXIS_BOTTOM",
            "x": self._margin_left,
            "y": self._margin_bottom,
            "line_length": self._width,
            "font_name": self._font._name,
            "font": self._font._basefont,
        } | options

        return self.axis(**XAXIS_BOTTOM_CONFIG)

    def xaxis_top(self, **options):

        XAXIS_TOP_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "XAXIS_TOP",
            "x": self._margin_left,
            "y": self._margin_bottom + self._height,
            "line_length": self._width,
            "font_name": self._font._name,
            "font": self._font._basefont,
        } | options

        return self.axis(**XAXIS_TOP_CONFIG)

    def yaxis_left(self, **options):

        YAXIS_LEFT_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "YAXIS_LEFT",
            "x": self._margin_left,
            "y": self._margin_bottom,
            "line_length": self._height,
            "font_name": self._font._name,
            "font": self._font._basefont,
            "direction": 90,
            "title_rotate": 90,
            "title_offset": [-35, 0],
        } | options

        return self.axis(**YAXIS_LEFT_CONFIG)

    def yaxis_right(self, **options):

        YAXIS_RIGHT_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "YAXIS_RIGHT",
            "x": self._margin_left + self._width,
            "y": self._margin_bottom,
            "line_length": self._height,
            "font_name": self._font._name,
            "font": self._font._basefont,
            "direction": 90,
            "show_title": False,
            "show_ticks": False,
            "show_labels": False,
        } | options

        return self.axis(**YAXIS_RIGHT_CONFIG)

    def set_background(self, color=None, style=None):
        if color is not None: self._background_color = color
        if style is not None: self._background_style = style


