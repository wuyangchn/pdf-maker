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
from .area import Area, COLOR_PALETTE
from .plotarea import PlotArea


class Canvas(Area):
    def __init__(self,
                 plot_area: Tuple[Union[int, float], ...] = (0, 0, 0, 0),
                 plot_scale: Tuple[Union[int, float], ...] = None,
                 clip_outside_plotarea: bool = True,
                 **options):
        super(Canvas, self).__init__(**options)
        # self._background_color = COLOR_PALETTE["white"]
        self._plot_area: PlotArea = ...
        plot_width, plot_height = self._width * plot_area[2], self._height * plot_area[3]
        margin_left = self._left_bottom[0] + self._width * plot_area[0]
        margin_bottom = self._left_bottom[1] + self._height * plot_area[1]
        if plot_area is not None and plot_scale is not None:
            self._plot_area = PlotArea(
                margin_left=margin_left, margin_bottom=margin_bottom, show_frame=True,
                width=plot_width, height=plot_height, scale=plot_scale, unit="pt", frame_line_width=1)
        if clip_outside_plotarea:
            self.rect(left_bottom=(0, 0), width=self._width, height=self._height, wind_style="WIND_EVEN_ODD",
                      wind=True, wind_inside_rect=(margin_left, margin_bottom, plot_width, plot_height),)

    def plot_area(self):
        return self._plot_area

    def text(self, x, y, unit="pt", **options):
        x, y = self.unit_to_points(x, y, unit)
        return super(Canvas, self).text(x=x, y=y, **options)

    def line(self, start: List[int], end: List[int], unit="pt", **options):
        start = self.unit_to_points(*start, unit)
        end = self.unit_to_points(*end, unit)
        return super(Canvas, self).line(start=list(start), end=list(end), **options)

    def rect(self, left_bottom: Union[list, tuple], width: Union[int, float], height: Union[int, float],
             unit: str = "pt", **options):
        left_bottom = self.unit_to_points(*left_bottom, unit=unit)
        width, height = self.unit_to_points(width, height, unit=unit)
        return super(Canvas, self).rect(left_bottom=left_bottom, width=width, height=height, **options)

    def scatter(self, x: Union[int, float], y: Union[int, float], unit: str = "pt", **options):
        x, y = self.unit_to_points(x, y, unit)
        return super(Canvas, self).scatter(x=x, y=y, **options)

    def all_components(self):
        return self.components() + self.plot_area().components() if isinstance(self.plot_area(), PlotArea) else []

    def left_bottom(self, lb: Tuple[Union[int, float], ...] = None):
        """
        note that positions of all components including components of the plot area
        will be changed correspondingly
        Args:
            lb:

        Returns:
        """
        if lb is not None:
            diff = [item - self._left_bottom[index] for index, item in enumerate(lb[:2])]
            for comp in self.all_components():
                self.move_comp(comp, diff=diff)
            self._left_bottom = lb

        return self._left_bottom