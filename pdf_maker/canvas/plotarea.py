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
import math
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

    def clip_line(self, start, end, x_clip=True, y_clip=True,
                  tolerance: float = 0.00000000001):
        """Clip a line segment to this plot rectangle.

        Liang-Barsky represents the segment as ``P(t) = start + t * delta``
        for ``0 <= t <= 1`` and narrows that interval against each enabled
        rectangle boundary.  ``None`` means that no part of the segment is
        inside the active clipping region.
        """
        try:
            x0, y0 = float(start[0]), float(start[1])
            x1, y1 = float(end[0]), float(end[1])
        except (TypeError, ValueError, IndexError) as error:
            raise TypeError("Line endpoints must contain two numeric values.") from error

        if not all(math.isfinite(value) for value in (x0, y0, x1, y1)):
            return None

        try:
            tolerance = float(tolerance)
            if not math.isfinite(tolerance) or tolerance < 0.0:
                tolerance = 0.0
        except (TypeError, ValueError):
            tolerance = 0.0

        if not x_clip and not y_clip:
            return (x0, y0), (x1, y1)

        xmin = min(self._margin_left, self._margin_left + self._width)
        xmax = max(self._margin_left, self._margin_left + self._width)
        ymin = min(self._margin_bottom, self._margin_bottom + self._height)
        ymax = max(self._margin_bottom, self._margin_bottom + self._height)

        dx = x1 - x0
        dy = y1 - y0
        t_enter = 0.0
        t_leave = 1.0
        parameter_tolerance = 1e-15

        constraints = []
        if x_clip:
            constraints.extend(((-dx, x0 - xmin), (dx, xmax - x0)))
        if y_clip:
            constraints.extend(((-dy, y0 - ymin), (dy, ymax - y0)))

        for p, q in constraints:
            if p == 0.0:
                # Parallel to this boundary: either always inside or invisible.
                if q < -tolerance:
                    return None
                continue

            ratio = q / p
            if p < 0:
                if ratio > t_leave + parameter_tolerance:
                    return None
                t_enter = max(t_enter, ratio)
            else:
                if ratio < t_enter - parameter_tolerance:
                    return None
                t_leave = min(t_leave, ratio)

        if t_enter > t_leave + parameter_tolerance:
            return None

        t_enter = min(max(t_enter, 0.0), 1.0)
        t_leave = min(max(t_leave, 0.0), 1.0)
        clipped_start = (x0 + t_enter * dx, y0 + t_enter * dy)
        clipped_end = (x0 + t_leave * dx, y0 + t_leave * dy)

        def clamp(value, lower, upper):
            if abs(value - lower) <= tolerance:
                return lower
            if abs(value - upper) <= tolerance:
                return upper
            return value

        if x_clip:
            clipped_start = (clamp(clipped_start[0], xmin, xmax), clipped_start[1])
            clipped_end = (clamp(clipped_end[0], xmin, xmax), clipped_end[1])
        if y_clip:
            clipped_start = (clipped_start[0], clamp(clipped_start[1], ymin, ymax))
            clipped_end = (clipped_end[0], clamp(clipped_end[1], ymin, ymax))

        return clipped_start, clipped_end

    # def is_out_side(self, x, y, tolerance: float = 0.00000000001):
    #     try:
    #         tolerance = float(tolerance)
    #         if not math.isfinite(tolerance) or tolerance < 0.0:
    #             tolerance = 0.0
    #     except (TypeError, ValueError):
    #         tolerance = 0.0
    #     xmin = min(self._margin_left, self._margin_left + self._width)
    #     xmax = max(self._margin_left, self._margin_left + self._width)
    #     ymin = min(self._margin_bottom, self._margin_bottom + self._height)
    #     ymax = max(self._margin_bottom, self._margin_bottom + self._height)
    #     return not (xmin - tolerance <= x <= xmax + tolerance and
    #                 ymin - tolerance <= y <= ymax + tolerance)

    # def clip_curve(self, x, y, func_y: MethodType, func_x: MethodType, x_clip=True, y_clip=True, tolerance: float = 0.00000000001):
    #     if not self.is_out_side(x, y, tolerance=tolerance):
    #         return x, y
    #     if func_y is None:
    #         if y_clip:
    #             if self._margin_bottom - tolerance <= y <= self._margin_bottom + self._height + tolerance:
    #                 return
    #             else:
    #                 return x, self._margin_bottom if y < self._margin_bottom else self._margin_bottom + self._height
    #     if func_x is None:
    #         if x_clip:
    #             if self._margin_left <= x <= self._margin_left + self._width + tolerance:
    #                 return
    #             else:
    #                 return self._margin_left if x < self._margin_left else self._margin_left + self._width, y
    #     if x_clip:
    #         if func_y is None and not (self._margin_left <= x <= self._margin_left + self._width + tolerance):
    #             return
    #         elif func_y is None:
    #             func_y = lambda _x: y
    #         if x > self._margin_left + self._width:
    #             x = self._margin_left + self._width
    #         if x < self._margin_left:
    #             x = self._margin_left
    #         y = func_y(x)
    #     if y_clip:
    #         if func_x is None and not (self._margin_bottom - tolerance <= y <= self._margin_bottom + self._height + tolerance):
    #             return
    #         elif func_x is None:
    #             func_x = lambda _y: x
    #         if y > self._margin_bottom + self._height:
    #             y = self._margin_bottom + self._height
    #         if y < self._margin_bottom:
    #             y = self._margin_bottom
    #         x = func_x(y)
    #     if self.is_out_side(x, self._margin_bottom, tolerance=tolerance) and x_clip:
    #         return
    #     if self.is_out_side(self._margin_left, y, tolerance=tolerance) and y_clip:
    #         return
    #     if self.is_out_side(x, y, tolerance=tolerance) and (x_clip == y_clip):
    #         return
    #     return x, y
    #
    # def _clip_line(self, x, y, start, end, x_clip=True, y_clip=True):
    #     if end[0] - start[0] != 0:
    #         func_y = lambda x: (end[1] - start[1]) / (end[0] - start[0]) * (x - start[0]) + start[1]
    #     else:
    #         func_y = None
    #     if end[1] - start[1] != 0:
    #         func_x = lambda y: (end[0] - start[0]) / (end[1] - start[1]) * (y - start[1]) + start[0]
    #     else:
    #         func_x = None
    #     return self.clip_curve(x, y, func_y=func_y, func_x=func_x, x_clip=x_clip, y_clip=y_clip)
    #
    # def clip_line(self, start, end, x_clip=True, y_clip=True):
    #     _start = self._clip_line(*start, start, end, x_clip=x_clip, y_clip=y_clip)
    #     _end = self._clip_line(*end, start, end, x_clip=x_clip, y_clip=y_clip)
    #     if _start is not None and _end is not None:
    #         return _start, _end
    #
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

    def same_point(self, a, b, tolerance=1e-12):
        return (
                abs(a[0] - b[0]) <= tolerance
                and abs(a[1] - b[1]) <= tolerance
        )

    def line(self, points: list, coordinate="scale", clip: bool = True, x_clip=True, y_clip=True, **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        points = [self.scale_to_points(*point, coordinate) for point in points]
        if clip:
            clipped_points = []

            for start, end in zip(points, points[1:]):
                clipped = self.clip_line(
                    start,
                    end,
                    x_clip=x_clip,
                    y_clip=y_clip,
                )

                if clipped is None:
                    continue

                clipped_start, clipped_end = clipped

                if not clipped_points:
                    clipped_points.extend([clipped_start, clipped_end])
                    continue

                # 相邻线段共享端点时，只追加新的终点
                if self.same_point(clipped_points[-1], clipped_start):
                    if not self.same_point(clipped_points[-1], clipped_end):
                        clipped_points.append(clipped_end)
                else:
                    # 这里表示中间存在矩形外的断开区域
                    clipped_points.extend([clipped_start, clipped_end])

            if not clipped_points:
                return

            points = clipped_points

        return super(PlotArea, self).line(points=points, **options)

    def rect(self, left_bottom: Union[list, tuple], width: Union[int, float], height: Union[int, float],
             coordinate: str = "scale", clip: bool = True, **options):
        if options.get("name", "") in KEYNAMES:
            raise ValueError(f"{options.get('name')} is reserved name that cannot be used.")
        left_bottom = self.scale_to_points(*left_bottom, coordinate=coordinate)
        width = width * self.ppu(axis="x")
        height = height * self.ppu(axis="y")
        if clip:
            left = self.clip_line(start=left_bottom, end=[left_bottom[0], left_bottom[1] + height])
            right = self.clip_line(start=[left_bottom[0] + width, left_bottom[1]], end=[left_bottom[0] + width, left_bottom[1] + height])
            if left is None or right is None:
                warnings.warn(
                    f"The rect of {left_bottom = } {width = } {height = } is on the outside of the plot area, "
                    f"and thus will have no effect.", UserWarning)
                return
            else:
                left_bottom, left_top = left
                right_bottom, right_top = right
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
        font = {}
        if isinstance(self._font, Obj):
            font = {"font_obj_name": self._font._name, "font_basefont": self._font._basefont,}
        XAXIS_BOTTOM_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "XAXIS_BOTTOM",
            "x": self._margin_left,
            "y": self._margin_bottom,
            "line_length": self._width,
        } | font | options

        return self.axis(**XAXIS_BOTTOM_CONFIG)

    def xaxis_top(self, **options):
        font = {}
        if isinstance(self._font, Obj):
            font = {"font_obj_name": self._font._name, "font_basefont": self._font._basefont,}
        XAXIS_TOP_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "XAXIS_TOP",
            "x": self._margin_left,
            "y": self._margin_bottom + self._height,
            "line_length": self._width,
        } | font | options

        return self.axis(**XAXIS_TOP_CONFIG)

    def yaxis_left(self, **options):
        font = {}
        if isinstance(self._font, Obj):
            font = {"font_obj_name": self._font._name, "font_basefont": self._font._basefont,}
        YAXIS_LEFT_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "YAXIS_LEFT",
            "x": self._margin_left,
            "y": self._margin_bottom,
            "line_length": self._height,
            "direction": 90,
            "title_rotate": 90,
            "title_offset": [-35, 0],
        } | font | options

        return self.axis(**YAXIS_LEFT_CONFIG)

    def yaxis_right(self, **options):
        font = {}
        if isinstance(self._font, Obj):
            font = {"font_obj_name": self._font._name, "font_basefont": self._font._basefont,}
        YAXIS_RIGHT_CONFIG = DEFAULT_AXIS_CONFIG | {
            "name": "YAXIS_RIGHT",
            "x": self._margin_left + self._width,
            "y": self._margin_bottom,
            "line_length": self._height,
            "direction": 90,
            "show_title": False,
            "show_ticks": False,
            "show_labels": False,
        } | font | options

        return self.axis(**YAXIS_RIGHT_CONFIG)

    def set_background(self, color=None, style=None):
        if color is not None: self._background_color = color
        if style is not None: self._background_style = style


