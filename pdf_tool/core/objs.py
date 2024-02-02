#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - objs
# ==========================================
#
#
# 
"""
from typing import List, Union
import re
from fontTools.ttLib import TTFont
from ._global import FONT_LIB, COLOR_PALETTE


class Text:
    def __init__(self, font_name, size, x, y, text, font, **options):
        self._font_name = font_name
        self._size = size
        self._x = x
        self._y = y
        self._text = text
        self._sub_size = int(self._size * 2. / 3.)
        self._sup_size = int(self._size * 2. / 3.)
        self._sub_Ts = -int(self._size * 1. / 4.)
        self._sup_Ts = int(self._size * 1. / 3.)
        self._color = COLOR_PALETTE.get('black', [0, 0, 0])
        self._line_space = 1.3

        for key, value in options.items():
            names = [key, f"_{key.lower()}"]
            for name in names:
                if hasattr(self, name) and not callable(getattr(self, name)):
                    setattr(self, name, value)

        self._line_height = ((abs(self._sub_Ts)) + max(
            (abs(self._sup_Ts) + self.get_text_height(self._text, font, self._sup_size)),
            self.get_text_height(self._text, font, self._size))) * self._line_space

        text_list = self.read_rich_text(text)
        self._rich = "\n".join([f"/{self._font_name} {self.size(script)} Tf\n{color} rg\n{color} RG\n{self.Ts(script)} Ts\n{f'0 -{self._line_height} Td' if r == 'r' else ''}\n({item}) Tj" for (item, script, color, r) in text_list])

    def to_dict(self):
        return {
            "Tf": {"name": f"{self._font_name}", "size": f"{self._size}"},
            "Td": {"x": f"{self._x}", "y": f"{self._y}"},
            "Tj": {"text": f"{self._text}"},
            "rich": self._rich
        }

    def size(self, flag: str):
        if flag == "sub": return self._sub_size
        if flag == "sup": return self._sup_size
        return self._size

    def Ts(self, flag: str):
        if flag == "sub": return self._sub_Ts
        if flag == "sup": return self._sup_Ts
        return 0

    def read_rich_text(self, text):
        rich_text_list = self.read_script(text)
        rich_text_list = [(color[0], script[1], color[1]) for script in rich_text_list for color in self.read_color(script[0])]
        rich_text_list = [(r[0], script, color, r[1]) for (item, script, color) in rich_text_list for r in self.read_break(item)]
        return rich_text_list

    def read_color(self, rich_text):
        for name, value in COLOR_PALETTE.items():
            if rich_text.startswith(f"<{name}>") and rich_text.endswith(f"</{name}>"):
                return [(rich_text.lstrip(f"<{name}>").rstrip(f"</{name}>"), ' '.join([str(i) for i in value]))]

            if f"<{name}>" in rich_text and f"</{name}>" in rich_text:
                reg = f"(<{name}>.*?</{name}>)"
                text_list = re.split(reg, rich_text)
                return [i for item in text_list for i in self.read_color(item)]

        return [(rich_text, ' '.join([str(i) for i in self._color]))]

    def read_script(self, rich_text):
        if rich_text.startswith("<sub>") and rich_text.endswith("</sub>"):
            return [(rich_text.lstrip("<sub>").rstrip("</sub>"), "sub")]
        if rich_text.startswith("<sup>") and rich_text.endswith("</sup>"):
            return [(rich_text.lstrip("<sup>").rstrip("</sup>"), "sup")]
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
    def to_chr(code: str):
        return "".join([chr(int(f"0x{each}", 16)) for each in code.lstrip("FEFF").split(" ")])

    @staticmethod
    def get_text_width(text: str, font: str, size: int):
        font = TTFont(FONT_LIB.get(str(font).lower()))
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
    def get_text_height(text: str, font: str, size: int):
        font = TTFont(FONT_LIB.get(str(font).lower()))
        pixels_per_em = font['head'].unitsPerEm
        ascender = font['OS/2'].sTypoAscender
        descender = font['OS/2'].sTypoDescender
        line_gap = font['OS/2'].sTypoLineGap
        line_height = (ascender + descender + line_gap) / pixels_per_em * size
        return int(line_height)


class Line:
    def __init__(self, start, end, width, color):
        self._start = start
        self._end = end
        self._width = width
        self._color = color
        if isinstance(self._color, list):
            self._color = " ".join([str(i) for i in self._color])
        if isinstance(self._start, list):
            self._start = " ".join([str(i) for i in self._start])
        if isinstance(self._end, list):
            self._end = " ".join([str(i) for i in self._end])

    def to_dict(self):
        return {
            "width": self._width, "color": self._color, "start": self._start , "end": self._end
        }


class Rect:
    def __init__(self, x, y, width, height, line_width, color):
        self._x = x
        self._y = y
        self._line_width = line_width
        self._width = width
        self._height = height
        self._color = color
        if isinstance(self._color, list):
            self._color = " ".join([str(i) for i in self._color])

    def to_dict(self):
        return {
            "x": self._x, "y": self._y,
            "width": self._width, "height": self._height,
            "line_width": self._line_width, "color": self._color,
        }


class Resources:
    def __init__(self, font, font_index):
        self._font = font
        self._font_index = font_index

    def to_dict(self):
        return {
            "font": {"name": f"{self._font}", "index": f"{self._font_index}"}
        }


class Obj:
    def __init__(self, type, **options):
        self._pages: str = ""
        self._basefont = ""
        self._name = ""
        self._index: int = 0
        self._type: str = type
        self._kids: List[int] = []
        self._parent: Union[int, str] = ""
        self._contents: Union[int, str] = ""
        self._length: Union[int, str] = ""
        self._mediabox: Union[tuple, list] = [0, 0, 612, 792]
        self._resources: dict = {}
        self._text: List[Text] = []
        self._line: List[dict] = []
        self._rect: List[dict] = []
        self._subtype = ""
        self._offset: Union[str, int] = ""
        self._number: Union[str, int] = ""
        self._state: str = "n"

        for key, value in options.items():
            names = [key, f"_{key.lower()}"]
            for name in names:
                if hasattr(self, name) and not callable(getattr(self, name)):
                    setattr(self, name, value)

    def get_type(self):
        return self._type.capitalize()

    def type(self, type: str = None):
        if type is not None:
            self._type = type
        if self.get_type() in ["Page", "Pages", "Font", "Catalog"]:
            return f"/Type /{self.get_type()}\n"
        return ""

    def data(self):
        return f"{self.index()} 0 obj\n<<\n{self.type()}{self.kids()}" \
               f"{self.parent()}{self.mediabox()}{self.contents()}{self.resources()}" \
               f"{self.length()}{self.subtype()}" \
               f"{self.name()}{self.basefont()}{self.pages()}" \
               f">>\n{self.stream()}" \
               f"endobj\n"

    def pages(self, pages: int = None):
        if self.get_type() != "Catalog":
            return ""
        if pages is not None:
            pass
        if self.get_type() != "Catalog" or not self._pages.isdigit():
            return ""
        return f"/Pages {self._pages} 0 R\n"

    def kids(self, kids: Union[List[int], int] = None):
        if self.get_type() != "Pages":
            return ""
        if kids is not None:
            if isinstance(kids, (int, str)):
                kids = [kids]
            self._kids = self._kids + kids
        kids = ' '.join([f'{i} 0 R' for i in self._kids])
        return f"/Kids [{kids}]\n/Count {len(self._kids)}\n"

    def parent(self, parent: int = None):
        if self.get_type() != "Page":
            return ""
        if parent is not None:
            self._parent = str(parent)
        if not self._parent.isdigit():
            return ""
        return f"/Parent {str(self._parent)} 0 R\n"

    def contents(self, contents: int = None):
        if self.get_type() != "Page":
            return ""
        if contents is not None:
            self._contents = str(contents)
        if not self._contents.isdigit():
            return ""
        return f"/Contents {str(self._contents)} 0 R\n"

    def resources(self, resources: dict = None):
        if self.get_type() != "Page":
            return ""
        if resources is not None:
            self._resources = resources
        if not isinstance(self._resources, dict):
            return ""
        resources = "\n".join([f"/{key.capitalize()} <<\n/{val['name']} {val['index']} 0 R\n>>\n" for key, val in self._resources.items()])
        return f"/Resources <<\n{resources}>>\n"

    def length(self, length: int = None):
        if self.get_type() != "":
            return ""
        content = self.stream()
        content = content.rstrip("\n")
        self._length = len(content)
        if length is not None:
            self._length = str(length)
        if not str(self._length).isdigit():
            return ""
        return f"/Length {self._length}\n"

    def stream(self):
        if self.get_type() in ["Page", "Pages", "Font", "Catalog"]:
            return ""
        return f"stream\n{self.text()}{self.line()}{self.rect()}endstream\n"

    def text(self, text: Text = None):
        if text is not None:
            self._text.append(text)
        if len(self._text) == 0:
            return ""
        content = "\n".join([f"{each._x} {each._y} Td\n{each._rich}" for each in self._text])
        return f"BT\n{content}\nET\n"

    def line(self, line: dict = None):
        if line is not None:
            self._line.append(line)
        if len(self._line) == 0:
            return ""
        line = "\n".join([f"{str(each['width'])} w\n{each['color']} RG\n{each['start']} m\n{each['end']} l\nS" for each in self._line])
        return f"{line}\n"

    def rect(self, rect: dict = None):
        if rect is not None:
            self._rect.append(rect)
        if len(self._rect) == 0:
            return ""
        rect = "\n".join([f"{str(each['line_width'])} w\n{each['color']} RG\n{each['x']} {each['y']} {each['width']} {each['height']} re\nS" for each in self._rect])
        return f"{rect}\n"

    def subtype(self, subtype: str = None):
        if self.get_type() != "Font":
            return ""
        if subtype is not None:
            self._subtype = subtype
        return f"/Subtype /{self._subtype}\n"

    def name(self, name: str = None):
        if self.get_type() != "Font":
            return ""
        if name is not None:
            self._name = name
        return f"/Name /{self._name}\n"

    def basefont(self, basefont: str = None):
        if self.get_type() != "Font":
            return ""
        if basefont is not None:
            self._basefont = basefont
        return f"/BaseFont /{self._basefont}\n"

    def mediabox(self, mediabox: Union[tuple, list] = None):
        if self.get_type() != "Page":
            return ""
        if mediabox is not None:
            self._mediabox = mediabox
        return f"/MediaBox [{' '.join([str(i) for i in self._mediabox])}]\n"

    def index(self):
        return str(self._index)

    def offset(self):
        return str(self._offset)

    def number(self):
        return str(self._number)

    def state(self):
        return str(self._state)

    def set_page_size(self, width: int, height: int):
        self._mediabox = [0, 0, width, height]

    def get_contents_index(self):
        return self._contents

    def get_font_name(self):
        return self._resources["font"]["name"]

    def remove_kid(self, index: Union[str, int]):
        kids = [str(i) for i in self._kids]
        kids.remove(str(index))
        self._kids = kids

    def get_basefont(self):
        return self._basefont
