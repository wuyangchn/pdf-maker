#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - comps
# ==========================================
#
#
# 
"""
import re
from fontTools.ttLib import TTFont
from pdf_maker.constants._global import FONT_LIB, COLOR_PALETTE, LINE_STYLE, WIND
from typing import Tuple, Union, List, Mapping
from xml.etree import ElementTree
from math import sin, cos, pi as PI, acos, asin


class BaseContent:
    def __init__(self, name: str = "", z_index: int = 0, x: int = 0, y: int = 0,
                 width: int = 0, height: int = 0, **options):
        self._name = name
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._z_index = z_index
        self._h_align: str = "left"
        self._v_align: str = "bottom"
        self._rotate: int = 0

        for key, value in options.items():
            names = [key, f"_{key.lower()}"]
            for name in names:
                if hasattr(self, name) and not callable(getattr(self, name)):
                    setattr(self, name, value)

        self._code: str = ""

    def code(self):
        return ""

    def name(self):
        return self._name

    def z_index(self):
        return self._z_index

    def align(self):
        self._x, self._y = self._align(self._x, self._y, self._h_align,
                                       self._v_align, self._width, self._height, self._rotate)

    @staticmethod
    def _align(x, y, h_align, v_align, width, height, rotate):
        """
        This function is used to set actual position of the left_bottom.
            For example, align(x=5, y=10, h_align='middle', v_align='center', width=10, height=10, rotate=0),
                will return (2.5 = 5 - 5 / 2, 5 = 10 - 10 / 2), which is the position of the left bottom.
                The left bottom position is required by pdf sepc to draw the item.
        Args:
            x: target position x, e.g., 3 in this example
            y: target position y, e.g., 5 in this example
            h_align: horizontal alignment, means the x is at left, middle, or right
            v_align: vertical alignment, means the y is at bottom, center, or top
            width: total width of the item
            height: total height of the item
            rotate: rotate degree integer between 0 to 360

        Returns:

        """
        if v_align == "bottom":
            height = 0
        elif v_align == "center":
            height = height / 2
        elif v_align == "top":
            height = height
        else:
            raise ValueError(f"Vertical alignment must be bottom, center, or top, but got {v_align} instead.")
        if h_align == "left":
            width = 0
        elif h_align == "middle":
            width = width / 2
        elif h_align == "right":
            width = width
        else:
            raise ValueError(f"Horizontal alignment must be left, middle, or right, but got {h_align} instead.")

        l = (width ** 2 + height ** 2) ** .5
        if l == 0:
            return x, y
        b = asin(height / l)
        a = int(rotate) / 180 * PI
        x = x - l * cos(a + b)
        y = y - l * sin(a + b)
        return x, y


class Text(BaseContent):
    def __init__(self, font_name, size, text, font, **options):
        self._font_name = font_name  # font name defined in page resources, like F0, F1, ...
        self._font = font  # real font name, lick Arial, Times, ...
        self._size = size
        self._text = text
        self._sub_size = int(self._size * 2. / 3.)
        self._sup_size = int(self._size * 2. / 3.)
        self._sub_Ts = -int(self._size * 1. / 4.)
        self._sup_Ts = int(self._size * 1. / 3.)
        self._color = COLOR_PALETTE.get('black', [0, 0, 0])
        self._line_space = 1.3
        self._line_height = 0
        self._font_widths: Mapping[int, int] = ...
        self._units_per_em: int = 2048
        self._dpi = 96    # points per inch, usually 72
        self._rotate = 0

        super().__init__(**options)

        if isinstance(self._color, str):
            self._color = COLOR_PALETTE.get(self._color, [0, 0, 0])

        # self.code()

    def code(self):
        text_list = self.read_rich_text(self._text)
        text_in_lines = [""]
        for text in text_list:
            if text[3] == "r":
                text_in_lines.append("")
            text_in_lines[-1] = text_in_lines[-1] + text[0]
        # line_height = self.get_char_width("M")
        line_height = int(FONT_LIB.get(self._font.lower())['line_height'] * self._size) * self._line_space
        line_width = max([sum([self.get_char_width(char) for char in text]) for text in text_in_lines])
        self._width = line_width
        self._height = line_height
        angle = PI * int(self._rotate) / 180
        self.align()
        pos = f'{round(cos(angle), 2)} {round(sin(angle), 2)} {round(-sin(angle), 2)} {round(cos(angle), 2)} ' \
              f'{round(self._x, 6)} {round(self._y, 6)}'
        self._code = f"BT\n{pos} Tm\n" + "\n".join([
            f"/{self._font_name} {self.size(script)} Tf\n"
            f"{color} rg\n{color} RG\n"
            f"{self.Ts(script)} Ts\n"
            f"{f'0 -{self.get_line_height()} Td' if r == 'r' else ''}\n"
            f"({item}) Tj" for (item, script, color, r) in text_list]) + "\nET"
        return self._code

    def get_line_height(self):
        # font_height = self.get_font_height(self._text, self._font)
        font_height = FONT_LIB.get(self._font.lower())['line_height']
        self._line_height = ((abs(self._sub_Ts)) + max(
            (abs(self._sup_Ts) + int(font_height * self._sup_size)), int(font_height * self._size))) * self._line_space
        return self._line_height

    def get_char_width(self, char: str):
        if not isinstance(self._font_widths, dict):
            return 0
        # why we need to multiply 2
        width = float(self._font_widths.get(ord(char), 0)) / float(self._units_per_em) * float(self._size) * 2
        # print(f"{char = }, {width = }, size = {self._size}")
        return width

    def size(self, flag: str):
        if flag == "sub": return self._sub_size
        if flag == "sup": return self._sup_size
        return self._size

    def Ts(self, flag: str):
        if flag == "sub": return self._sub_Ts
        if flag == "sup": return self._sup_Ts
        return 0

    def read_rich_text(self, text):
        # rich_text_list = self.read_script(text)
        # rich_text_list = [(color[0], script[1], color[1]) for script in rich_text_list for color in self.read_color(script[0])]
        # rich_text_list = [(r[0], script, color, r[1]) for (item, script, color) in rich_text_list for r in self.read_break(item)]
        rich_text_list = self.read_color(text)
        rich_text_list = [(script[0], script[1], color) for (item, color) in rich_text_list for script in self.read_script(item)]
        rich_text_list = [(r[0], script, color, r[1]) for (item, script, color) in rich_text_list for r in self.read_break(item)]
        return rich_text_list

    def read_color(self, rich_text):
        for name, value in COLOR_PALETTE.items():
            if rich_text.startswith(f"<{name}>") and rich_text.endswith(f"</{name}>"):
                return [(rich_text.removeprefix(f"<{name}>").removesuffix(f"</{name}>"), ' '.join([str(i) for i in value]))]
            if f"<{name}>" in rich_text and f"</{name}>" in rich_text:
                reg = f"(<{name}>.*?</{name}>)"
                text_list = re.split(reg, rich_text)
                return [i for item in text_list for i in self.read_color(item)]
        return [(rich_text, ' '.join([str(i) for i in self._color]))]

    def read_script(self, rich_text):
        if rich_text.startswith("<sub>") and rich_text.endswith("</sub>"):
            if not self._is_rich_text(rich_text.removeprefix("<sub>").removesuffix("</sub>")):
                return [(rich_text.removeprefix("<sub>").removesuffix("</sub>"), "sub")]
        if rich_text.startswith("<sup>") and rich_text.endswith("</sup>"):
            if not self._is_rich_text(rich_text.removeprefix("<sup>").removesuffix("</sup>")):
                return [(rich_text.removeprefix("<sup>").removesuffix("</sup>"), "sup")]
        if "<sub>" in rich_text and "</sub>" in rich_text:
            text_list = re.split(r"(<sub>.*?</sub>)", rich_text)
            return [i for item in text_list for i in self.read_script(item)]
        if "<sup>" in rich_text and "</sup>" in rich_text:
            text_list = re.split(r"(<sup>.*?</sup>)", rich_text)
            return [i for item in text_list for i in self.read_script(item)]
        return [(rich_text, "normal")]

    def read_break(self, rich_text: str):
        if "<r>" in rich_text:
            text = rich_text.split("<r>")
            return [(text[0], ""), (text[1], "r")]
        return [(rich_text, "")]

    @staticmethod
    def _is_rich_text(text: str):
        for reg in [r"(<sup>.*?</sup>)", r"(<sub>.*?</sub>)"]:
            if len(re.findall(reg, text)) > 0:
                return True
        return False

    @staticmethod
    def to_chr(code: str):
        return "".join([chr(int(f"0x{each}", 16)) for each in code.lstrip("FEFF").split(" ")])

    @staticmethod
    def get_font_width(text: str, font: str, size: int):
        font = TTFont(FONT_LIB.get(str(font).lower())['file'])
        cmap = font['cmap']
        t = cmap.getcmap(3, 1).cmap
        s = font.getGlyphSet()
        pixels_per_em = font['head'].unitsPerEm
        total = 0
        for c in text:
            if ord(c) in t and t[ord(c)] in s:
                total += s[t[ord(c)]].width
            else:
                total += s['.notdef'].width
        total = total * float(size) / pixels_per_em
        return int(total)

    @staticmethod
    def get_font_height(text: str, font: str):
        tree = ElementTree.parse(FONT_LIB.get(font.lower())['file'])
        root = tree.getroot()
        head_obj = root.find('head')
        OS_2_obj = root.find('OS_2')
        pixels_per_em = head_obj.find("unitsPerEm").attrib['value']
        ascender = OS_2_obj.find("sTypoAscender").attrib['value']
        descender = OS_2_obj.find("sTypoDescender").attrib['value']
        line_gap = OS_2_obj.find("sTypoLineGap").attrib['value']
        line_height = (float(ascender) + float(descender) + float(line_gap)) / float(pixels_per_em)
        return line_height


class Line(BaseContent):
    def __init__(self, start, end, line_style: str = "solid", **options):
        self._start = start
        self._end = end
        self._width = 1
        self._line_style = line_style
        self._color = COLOR_PALETTE.get('black', [0, 0, 0])

        super().__init__(**options)

        if isinstance(self._color, str):
            self._color = COLOR_PALETTE.get(self._color, [0, 0, 0])

        # self.code()

    def code(self, start=None, end=None, lt: str = None):
        if start is None or end is None:
            start, end = self._start, self._end
        if lt is None:
            lt = self._line_style
        distance = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** .5
        if distance == 0:
            return ""
        if lt == "solid":
            color = " ".join([str(i) for i in self._color])
            start = " ".join([str(i) for i in start])
            end = " ".join([str(i) for i in end])
            code = f"{str(self._width)} w\n{color} RG\n{start} m\n{end} l\nS"
        elif lt in ["dashed", "dotted", "densely_dotted", "densely_dashed", "loosely_dashed", "loosely_dotted"]:
            dash_length = LINE_STYLE[lt][0]
            blank_length = LINE_STYLE[lt][1]
            step_x = (dash_length + blank_length) / distance * (end[0] - start[0])
            step_y = (dash_length + blank_length) / distance * (end[1] - start[1])
            add_x = dash_length / distance * (end[0] - start[0])
            add_y = dash_length / distance * (end[1] - start[1])
            code = "\n".join([self.code(
                start=[start[0] + i * step_x, start[1] + i * step_y],
                end=[start[0] + i * step_x + add_x, start[1] + i * step_y + add_y],
                lt="solid") for i in range(int(distance // (dash_length + blank_length) + 1))]
            )
        elif lt == "dashdot":
            step_x = sum(LINE_STYLE[lt]) / distance * (end[0] - start[0])
            step_y = sum(LINE_STYLE[lt]) / distance * (end[1] - start[1])
            add_x_1 = LINE_STYLE[lt][0] / distance * (end[0] - start[0])
            add_y_1 = LINE_STYLE[lt][0] / distance * (end[1] - start[1])
            add_x_2 = sum(LINE_STYLE[lt][:2]) / distance * (end[0] - start[0])
            add_y_2 = sum(LINE_STYLE[lt][:2]) / distance * (end[1] - start[1])
            add_x_3 = sum(LINE_STYLE[lt][:3]) / distance * (end[0] - start[0])
            add_y_3 = sum(LINE_STYLE[lt][:3]) / distance * (end[1] - start[1])
            code = "\n".join(
                ["\n".join([
                    self.code(
                        start=[start[0] + i * step_x, start[1] + i * step_y],
                        end=[start[0] + i * step_x + add_x_1, start[1] + i * step_y + add_y_1],
                        lt="solid"),
                    self.code(
                        start=[start[0] + i * step_x + add_x_2, start[1] + i * step_y + add_y_2],
                        end=[start[0] + i * step_x + add_x_3, start[1] + i * step_y + add_y_3],
                        lt="solid"),
                ]) for i in range(int(distance // sum(LINE_STYLE[lt]) + 1))]
            )
        else:
            raise ValueError(f"line style must be one of f{', '.join(LINE_STYLE.keys())}, but got {lt} instead.")
        return code


class Rect(BaseContent):
    def __init__(self, **options):
        self._line_width = 1
        self._color = COLOR_PALETTE.get('black', [0, 0, 0])
        self._fill: bool = False
        self._wind: bool = False
        self._wind_color = COLOR_PALETTE.get('white', [1, 1, 1])
        self._wind_style = "WIND_NON_ZERO"
        self._wind_inside_rects: List[Tuple[Union[float, int], ...]] = ...

        super().__init__(**options)

        if isinstance(self._color, str):
            self._color = COLOR_PALETTE.get(self._color, [0, 0, 0])

        # self.code()

    def code(self):
        wind = ""
        if self._wind and len(self._wind_inside_rects) > 0:
            rects = '\n'.join([' '.join([str(i) for i in rect]) + ' re' for rect in self._wind_inside_rects])
            wind = f"\n{rects} f{'*' if self._wind_style == 'WIND_EVEN_ODD' else ''}"
        self._code = f"{str(self._line_width)} w\n" \
                     f"{' '.join([str(i) for i in self._color])} RG\n" \
                     f"{(' '.join([str(i) for i in self._wind_color]) + ' rg') if self._wind else ''}\n" \
                     f"{self._x} {self._y} {self._width} {self._height} re {wind}\nS"
        return self._code


class Scatter(BaseContent):
    def __init__(self, **options):
        """
        Args:
            x: center of the point
            y: center of the point
            **options: type: circle, rectangle
        """
        self._size = 5
        self._line_width = 1
        self._fill_color = COLOR_PALETTE.get('black', [0, 0, 0])
        self._stroke_color = COLOR_PALETTE.get('black', [0, 0, 0])
        self._scale_factor = 1
        self._type = "circle"

        super().__init__(**options)

        if isinstance(self._fill_color, str):
            self._fill_color = COLOR_PALETTE.get(self._fill_color, [0, 0, 0])
        if isinstance(self._stroke_color, str):
            self._stroke_color = COLOR_PALETTE.get(self._stroke_color, [0, 0, 0])

        # self.code()

    def code(self):
        stroke_color = f"{' '.join([str(i) for i in self._stroke_color])} RG"
        fill_color = f"{' '.join([str(i) for i in self._fill_color])} rg"
        line_width = f"{self._line_width} w"
        line = ""
        if self._type.lower()[:3] == "rec":
            x = self._x - self._size
            y = self._y - self._size * self._scale_factor
            line = f"{x} {y} {self._size * 2} {self._size * self._scale_factor * 2} re b"
        if self._type.lower()[:3] == "cir":
            r = 0.55228 * self._size
            s = (str(self._x - self._size), str(self._y))
            k1 = (str(self._x - self._size), str(r + self._y))
            k2 = (str(self._x - r), str(self._y + self._size))
            e1 = (str(self._x), str(self._y + self._size))
            k3 = (str(self._x + r), str(self._y + self._size))
            k4 = (str(self._x + self._size), str(r + self._y))
            e2 = (str(self._x + self._size), str(self._y))
            k5 = (str(self._x + self._size), str(self._y - r))
            k6 = (str(self._x + r), str(self._y - self._size))
            e3 = (str(self._x), str(self._y - self._size))
            k7 = (str(self._x - r), str(self._y - self._size))
            k8 = (str(self._x - self._size), str(self._y - r))
            e4 = s
            # line = f"{self._x} {self._y} {self._size} 0 360 arc"
            line = f"{' '.join(s)} m\n{' '.join(k1)} {' '.join(k2)} {' '.join(e1)} c\n" \
                   f"{' '.join(k3)} {' '.join(k4)} {' '.join(e2)} c\n" \
                   f"{' '.join(k5)} {' '.join(k6)} {' '.join(e3)} c\n" \
                   f"{' '.join(k7)} {' '.join(k8)} {' '.join(e4)} c\nh B"
        self._code = f"{line_width}\n{stroke_color}\n{fill_color}\n{line}"
        return self._code
