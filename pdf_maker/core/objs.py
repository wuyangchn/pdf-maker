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
from typing import List, Union, Set
import re
from fontTools.ttLib import TTFont
from ._global import FONT_LIB, COLOR_PALETTE
from datetime import datetime, timezone, timedelta
from .base import camel_to_snake, snake_to_camel


class BaseContent:
    def __init__(self, **options):
        self._z_index = 0
        for key, value in options.items():
            names = [key, f"_{key.lower()}"]
            for name in names:
                if hasattr(self, name) and not callable(getattr(self, name)):
                    setattr(self, name, value)

        self._code: str = ""

    def code(self):
        return ""

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return object.__getattribute__(self, f"_{name}")


class Text(BaseContent):
    def __init__(self, font_name, size, x, y, text, font, **options):
        self._font_name = font_name
        self._font = font
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
        self._line_height = 0

        super().__init__(**options)

        if isinstance(self._color, str):
            self._color = COLOR_PALETTE.get(self._color, [0, 0, 0])

        self.code()

    def code(self):
        self._line_height = ((abs(self._sub_Ts)) + max(
            (abs(self._sup_Ts) + self.get_text_height(self._text, self._font, self._sup_size)),
            self.get_text_height(self._text, self._font, self._size))) * self._line_space
        text_list = self.read_rich_text(self._text)
        self._code = f"BT\n{self._x} {self._y} Td\n" + "\n".join([f"/{self._font_name} {self.size(script)} Tf\n{color} rg\n{color} RG\n{self.Ts(script)} Ts\n{f'0 -{self._line_height} Td' if r == 'r' else ''}\n({item}) Tj" for (item, script, color, r) in text_list]) + "\nET"
        return self._code

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
                return [(rich_text.removeprefix(f"<{name}>").removesuffix(f"</{name}>"), ' '.join([str(i) for i in value]))]

            if f"<{name}>" in rich_text and f"</{name}>" in rich_text:
                reg = f"(<{name}>.*?</{name}>)"
                text_list = re.split(reg, rich_text)
                return [i for item in text_list for i in self.read_color(item)]

        return [(rich_text, ' '.join([str(i) for i in self._color]))]

    def read_script(self, rich_text):
        if rich_text.startswith("<sub>") and rich_text.endswith("</sub>"):
            return [(rich_text.removeprefix("<sub>").removesuffix("</sub>"), "sub")]
        if rich_text.startswith("<sup>") and rich_text.endswith("</sup>"):
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


class Line(BaseContent):
    def __init__(self, start, end, **options):
        self._start = start
        self._end = end
        self._width = 1
        self._color = COLOR_PALETTE.get('black', [0, 0, 0])

        super().__init__(**options)

        if isinstance(self._color, str):
            self._color = COLOR_PALETTE.get(self._color, [0, 0, 0])

        self.code()

    def code(self):
        color = " ".join([str(i) for i in self._color])
        start = " ".join([str(i) for i in self._start])
        end = " ".join([str(i) for i in self._end])
        self._code = f"{str(self._width)} w\n{color} RG\n{start} m\n{end} l\nS"
        return self._code


class Rect(BaseContent):
    def __init__(self, x, y, width, height, **options):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._line_width = 1
        self._color = COLOR_PALETTE.get('black', [0, 0, 0])

        super().__init__(**options)

        if isinstance(self._color, str):
            self._color = COLOR_PALETTE.get(self._color, [0, 0, 0])

        self.code()

    def code(self):
        color = " ".join([str(i) for i in self._color])
        self._code = f"{str(self._line_width)} w\n{color} RG\n{self._x} {self._y} {self._width} {self._height} re\nS"
        return self._code


class Scatter(BaseContent):
    def __init__(self, x, y, **options):
        """
        Args:
            x: center of the point
            y: center of the point
            **options: type: circle, rectangle
        """
        self._x = x
        self._y = y
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

        self.code()

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


class Resources(BaseContent):
    def __init__(self, font, font_index, **options):
        self._font = font
        self._font_index = font_index

        super().__init__(**options)

        self._code: str = ...
        self.code()

    def code(self):
        self._code = "\n".join([f"/{key.capitalize()} <<\n/{val['name']} {val['index']} 0 R\n>>\n" for key, val in self.to_dict().items()])
        return self._code

    def to_dict(self):
        return {
            "font": {"name": f"{self._font}", "index": f"{self._font_index}"}
        }


class Obj:
    def __init__(self, index, type, **options):
        self._pages: str = ""
        self._basefont = ""
        self._name = ""
        self._index: int = index
        self._type: str = type
        self._kids: List[str] = []
        self._parent: Union[int, str] = ""
        self._contents: Union[int, str] = ""
        self._length: Union[int, str] = ""
        self._mediabox: Union[tuple, list] = [0, 0, 612, 792]
        self._title: str = ""
        self._author: str = ""
        self._producer: str = ""
        self._creator: str = ""
        self._subject: str = ""
        self._keywords: str = ""
        self._creation_date: str = ""
        self._mod_date: str = ""
        self._resources: Resources = ...
        self._text: List[Text] = []
        self._line: List[Line] = []
        self._rect: List[Rect] = []
        self._scatter: List[Scatter] = []
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
        # attributes = [
        #     "Type", "Kids", "Parent", "Mediabox", "Contents",
        #     "Resources", "Length", "Subtype", "Name", "Basefont",
        #     "Pages", "Title", "Author", "Producer", "Creator",
        #     "CreateDate", "ModDate", "Subject", "Keywords"
        #
        # ]
        return f"{self.index()} 0 obj\n" \
               f"<<\n{self.type()}{self.kids()}" \
               f"{self.parent()}{self.mediabox()}{self.contents()}{self.resources()}" \
               f"{self.length()}{self.subtype()}" \
               f"{self.name()}{self.basefont()}{self.pages()}" \
               f"{self.title()}{self.author()}{self.producer()}{self.creator()}{self.creation_date()}{self.mod_date()}{self.subject()}{self.keywords()}" \
               f">>\n" \
               f"{self.stream()}" \
               f"endobj\n"

    """ Attributes of objects """
    def pages(self, pages: int = None):
        if self.get_type() != "Catalog":
            return ""
        if pages is not None:
            pass
        if self.get_type() != "Catalog" or not self._pages.isdigit():
            return ""
        return f"/Pages {self._pages} 0 R\n"

    def kids(self, kids: Union[list, int, str] = None):
        if self.get_type() != "Pages":
            return ""
        if kids is not None:
            if isinstance(kids, (int, str)):
                kids = [kids]
            kids = [str(i) for i in kids]
        else:
            kids = []
        for kid in kids:
            self._kids.append(kid)
        kids = ' '.join([f"{i} 0 R" for i in self._kids])
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

    def resources(self, resources: Resources = None):
        if self.get_type() != "Page":
            return ""
        if resources is not None:
            self._resources = resources
        if not isinstance(self._resources, Resources):
            return ""
        resources = self._resources.code()
        return f"/Resources <<\n{resources}>>\n"

    def length(self, length: int = None):
        if self.get_type() != "" or self.get_type() != "Stream":
            return ""
        content = self.stream()
        content = content.rstrip("\n")
        self._length = len(content)
        if length is not None:
            self._length = str(length)
        if not str(self._length).isdigit():
            return ""
        return f"/Length {self._length}\n"

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

    def title(self, title: str = None):
        if self.get_type() != "Info":
            return ""
        if title is not None:
            self._title = title
        return f"/Title ({self._title})\n"

    def author(self, author: str = None):
        if self.get_type() != "Info":
            return ""
        if author is not None:
            self._author = author
        return f"/Author ({self._author})\n"

    def producer(self, producer: str = None):
        if self.get_type() != "Info":
            return ""
        if producer is not None:
            self._producer = producer
        return f"/Producer ({self._producer})\n"

    def subject(self, subject: str = None):
        if self.get_type() != "Info":
            return ""
        if subject is not None:
            self._subject = subject
        return f"/subject ({self._subject})\n"

    def keywords(self, keywords: str = None):
        if self.get_type() != "Info":
            return ""
        if keywords is not None:
            self._keywords = keywords
        return f"/keywords ({self._keywords})\n"

    def creator(self, creator: str = None):
        if self.get_type() != "Info":
            return ""
        if creator is not None:
            self._creator = creator
        return f"/Creator ({self._creator})\n"

    def creation_date(self, creation_date: str = None):
        date = str(datetime.now(tz=timezone(offset=timedelta(hours=8))))
        date = ("D:" + "".join(re.findall(r"(\d*|\+)", date)))[:-2] + "'00'"
        self._creation_date = date
        if self.get_type() != "Info":
            return ""
        if creation_date is not None:
            self._creation_date = creation_date
        return f"/CreationDate ({self._creation_date})\n"

    def mod_date(self, mod_date: str = None):
        date = str(datetime.now(tz=timezone(offset=timedelta(hours=8))))
        date = ("D:" + "".join(re.findall(r"(\d*|\+)", date)))[:-2] + "'00'"
        self._mod_date = date
        if self.get_type() != "Info":
            return ""
        if mod_date is not None:
            self._mod_date = mod_date
        return f"/ModDate ({self._mod_date})\n"

    def stream(self):
        if self.get_type() in ["Page", "Pages", "Font", "Catalog", "Info"]:
            return ""
        contents: List[BaseContent] = sorted([*self._text, *self._line, *self._rect, *self._scatter], key=lambda obj: obj.z_index)
        code = '\n'.join([obj.code() for obj in contents])
        stream = f"stream\n{code}\nendstream\n"
        return stream

    """ Functions """
    def text(self, text: Text):
        self._text.append(text)

    def line(self, line: Line):
        self._line.append(line)

    def rect(self, rect: Rect):
        self._rect.append(rect)

    def scatter(self, scatter: Scatter):
        self._scatter.append(scatter)

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
        if self.get_type() == "Page":
            return self._resources.font
        elif self.get_type() == "Font":
            return self._name

    def remove_kid(self, index: Union[str, int]):
        if str(index) in self._kids:
            self._kids.remove(str(index))

    def get_basefont(self):
        return self._basefont
