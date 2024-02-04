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
from ._global import ALIGN, COLOR_PALETTE
from .comps import Text, Line, Scatter, Rect, BaseContent


class Area:
    def __init__(self, width, height, show_frame: bool = False, x: int = 0, y: int = 0):
        self._left_bottom = (x, y)
        self._width = width
        self._height = height

        self._background_color: List[int] = ...
        self._transparency: float = ...
        self._components: List[Union[Text, Line, Scatter, Rect], ...] = []
        self._show_frame = show_frame

        if self._show_frame:
            self.show_frame()

    def left_bottom(self, lb: Tuple[Union[int, float], ...] = None):
        """ note that positions of components will be changed correspondingly """
        if lb is not None:
            diff = [item - self._left_bottom[index] for index, item in enumerate(lb[:2])]
            for comp in self.components():
                self.move_comp(comp, diff=diff)
            self._left_bottom = lb

        return self._left_bottom

    def move_comp(self, comp: Union[Text, Rect, Scatter, Line], diff: List[Union[int, float]]):
        if isinstance(comp, (Text, Rect, Scatter)):
            comp._x, comp._y = [comp._x + diff[0], comp._y + diff[1]]
        if isinstance(comp, Line):
            comp._start = [comp._start[0] + diff[0], comp._start[1] + diff[1]]
            comp._end = [comp._end[0] + diff[0], comp._end[1] + diff[1]]
        return comp

    def height(self):
        return self._height

    def width(self):
        return self._width

    def components(self):
        return self._components

    def add_component(self, comp: Union[Text, Line, Scatter, Rect]):
        if isinstance(comp, (Text, Line, Scatter, Rect)):
            self._components.append(comp)
        else:
            raise TypeError(f"The component is not an instance of Text, Line, Scatter, "
                            f"or Rect, got a {type(comp)} instead.")

    def del_component(self, comp: Union[Text, Line, Scatter, Rect]):
        if isinstance(comp, (Text, Line, Scatter, Rect)):
            self._components.remove(comp)
        else:
            raise TypeError(f"The component is not an instance of Text, Line, Scatter, "
                            f"or Rect, got a {type(comp)} instead.")

    def has_comp(self, comp_name):
        for comp in self.components():
            if comp.name() == comp_name:
                return True
        return False

    def get_comp(self, comp_name):
        for comp in self.components():
            if comp.name() == comp_name:
                return comp

    def show_frame(self):
        self._show_frame = True
        if not self.has_comp("CanvasFrame"):
            rect = Rect(*self._left_bottom, width=self._width, height=self._height, name="CanvasFrame")
            self._components.append(rect)

    def remove_frame(self):
        self._show_frame = False
        self.del_component(comp=self.get_comp(comp_name="CanvasFrame"))

    def text(self, x: int, y: int, text: str, size: int = 12, font: str = "arial", **options):
        text = Text(font_name="", size=size, x=x, y=y, text=text, font=font, **options)
        self._components.append(text)
        return text

    def line(self, start: List[int], end: List[int], width: Union[float, int] = None,
             color: Union[tuple, list, str] = None, **options):
        if width is None:
            width = 0.5
        if color is None:
            color = "black"
        if isinstance(color, str):
            color = COLOR_PALETTE.get(color.lower(), [0, 0, 0])
        line = Line(start=start, end=end, color=color, width=width, **options)
        self._components.append(line)
        return line

    def rect(self, left_bottom: Union[list, tuple], width: int, height: int,
             line_width: Union[float, int] = None, color: Union[tuple, list, str] = None,
             **options):
        if line_width is None:
            line_width = 0.5
        if color is None:
            color = "black"
        if isinstance(color, str):
            color = COLOR_PALETTE.get(color.lower(), [0, 0, 0])
        rect = Rect(*left_bottom, width=width, height=height, line_width=line_width, color=color, **options)
        self._components.append(rect)
        return rect

    def scatter(self, x: int, y: int, size: int = 5, fill_color: Union[tuple, list, str] = None,
                stroke_color: Union[tuple, list, str] = None, **options):
        if stroke_color is None:
            stroke_color = "black"
        if fill_color is None:
            fill_color = "grey"
        scatter = Scatter(x=x, y=y, size=size, fill_color=fill_color, stroke_color=stroke_color, **options)
        self._components.append(scatter)
        return scatter


class Canvas(Area):
    def __init__(self, scale: Tuple[Union[int, float], ...], **options):
        super(Canvas, self).__init__(**options)
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
        return super(Canvas, self).text(x=x, y=y, **options)

    def line(self, start: List[int], end: List[int], coordinate="scale", **options):
        start = self.scale_to_points(*start, coordinate)
        end = self.scale_to_points(*end, coordinate)
        return super(Canvas, self).line(start=list(start), end=list(end), **options)

    def rect(self, left_bottom: Union[list, tuple], width: Union[int, float], height: Union[int, float],
             coordinate: str = "scale", **options):
        left_bottom = self.scale_to_points(*left_bottom, coordinate=coordinate)
        width = width * self.ppu(axis="x")
        height = height * self.ppu(axis="y")
        return super(Canvas, self).rect(left_bottom=left_bottom, width=width, height=height, **options)

    def scatter(self, x: Union[int, float], y: Union[int, float], coordinate: str = "scale", **options):
        x, y = self.scale_to_points(x, y, coordinate)
        return super(Canvas, self).scatter(x=x, y=y, **options)
