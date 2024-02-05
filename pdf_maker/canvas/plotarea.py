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
from .area import Area, Text, Line, Scatter, Rect, COLOR_PALETTE


class PlotArea(Area):
    def __init__(self, scale: Tuple[Union[int, float], ...], **options):
        super(PlotArea, self).__init__(**options)
        self._scale: Tuple[Union[int, float], ...] = scale

    def ppu(self, axis: str):
        def distance(x, y):
            return abs(x - y)
        if axis == "x":
            return self._width / distance(*self._scale[:2])
        elif axis == "y":
            return self._height / distance(*self._scale[2:4])
        else:
            raise KeyError(f"axis mush be one of x and y, got {axis} instead.")

    def scale(self):
        return self._scale

    def scale_to_points(self, x, y, coordinate: str = "scale"):
        if coordinate != "scale":
            return x, y
        x = (x - self._scale[0]) * self.ppu("x") + self._left_bottom[0]
        y = (y - self._scale[2]) * self.ppu("y") + self._left_bottom[1]
        return x, y

    def text(self, x, y, coordinate="scale", **options):
        x, y = self.scale_to_points(x, y, coordinate)
        return super(PlotArea, self).text(x=x, y=y, **options)

    def line(self, start: List[int], end: List[int], coordinate="scale", **options):
        start = self.scale_to_points(*start, coordinate)
        end = self.scale_to_points(*end, coordinate)
        return super(PlotArea, self).line(start=list(start), end=list(end), **options)

    def rect(self, left_bottom: Union[list, tuple], width: Union[int, float], height: Union[int, float],
             coordinate: str = "scale", **options):
        left_bottom = self.scale_to_points(*left_bottom, coordinate=coordinate)
        width = width * self.ppu(axis="x")
        height = height * self.ppu(axis="y")
        return super(PlotArea, self).rect(left_bottom=left_bottom, width=width, height=height, **options)

    def scatter(self, x: Union[int, float], y: Union[int, float], coordinate: str = "scale", **options):
        x, y = self.scale_to_points(x, y, coordinate)
        return super(PlotArea, self).scatter(x=x, y=y, **options)
