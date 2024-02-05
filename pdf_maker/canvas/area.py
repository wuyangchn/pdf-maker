#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - area
# ==========================================
#
#
# 
"""
from typing import List, Tuple, Union
from pdf_maker.constants._global import COLOR_PALETTE, UNIT
from pdf_maker.core.comps import Text, Line, Scatter, Rect


class Area:
    def __init__(self, width, height, show_frame: bool = False, margin_left: int = 0,
                 margin_bottom: int = 0, unit: str = "point", ppi: int = 72,
                 background_color: List[int] = COLOR_PALETTE["white"], frame_line_width: int = 1):
        self._ppi = ppi
        self._unit = unit
        self._width, self._height = self.unit_to_points(width, height, unit=unit)
        self._left_bottom = self.unit_to_points(margin_left, margin_bottom, unit=unit)
        self._frame_line_width = frame_line_width

        self._background_color: List[int] = background_color
        self._transparency: float = ...
        self._components: List[Union[Text, Line, Scatter, Rect], ...] = []
        self._show_frame: bool = ...

        if show_frame:
            self.show_frame()

    def ppi(self):
        return self._ppi

    def left_bottom(self, lb: Tuple[Union[int, float], ...] = None):
        """ note that positions of components will be changed correspondingly """
        if lb is not None:
            diff = [item - self._left_bottom[index] for index, item in enumerate(lb[:2])]
            for comp in self.components():
                self.move_comp(comp, diff=diff)
            self._left_bottom = lb

        return self._left_bottom

    def unit_to_points(self, x, y, unit: str = "pt"):
        if unit not in UNIT.keys():
            raise ValueError(f"unit mush be one of {', '.join(UNIT.keys())}, "
                             f"but got a {unit} instead.")
        if unit.lower() not in ["point", "pt"]:
            x = x * UNIT[unit] * self.ppi()
            y = y * UNIT[unit] * self.ppi()
        return x, y

    def move_comp(self, comp: Union[Text, Rect, Scatter, Line], diff: List[Union[int, float]]):
        if isinstance(comp, (Text, Scatter)):
            comp._x, comp._y = [comp._x + diff[0], comp._y + diff[1]]
        if isinstance(comp, Rect):
            comp._x, comp._y = [comp._x + diff[0], comp._y + diff[1]]
            if isinstance(comp._wind_inside_rect, tuple) and len(comp._wind_inside_rect) == 4:
                comp._wind_inside_rect = (
                    comp._wind_inside_rect[0] + diff[0], comp._wind_inside_rect[1] + diff[1],
                    *comp._wind_inside_rect[2:]
                )
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
        if self._show_frame and isinstance(self._show_frame, bool):
            self.remove_frame()
        self._show_frame = True
        if not self.has_comp("CanvasFrame"):
            rect = Rect(*self._left_bottom, width=self._width, height=self._height,
                        name="CanvasFrame", line_width=self._frame_line_width)
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
