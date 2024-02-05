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
from typing import List, Union, Tuple
import re
from datetime import datetime, timezone, timedelta
from .comps import BaseContent, Text, Scatter, Line, Rect, FONT_LIB
from fontTools.ttLib import TTFont

class Resources:
    def __init__(self, font, font_index, procset_index, **options):
        self._font = font
        self._font_index = font_index
        self._procset_index = procset_index
        self._code: str = ...

        self.code()

    def code(self):
        self._code = f"/Procset {self._procset_index} 0 R\n" + "\n".join([
            f"/{key.capitalize()} <<\n"
            f"/{val['name']} {val['index']} 0 R\n>>\n" for key, val in self.to_dict().items()])
        return self._code

    def to_dict(self):
        return {
            "font": {"name": f"{self._font}", "index": f"{self._font_index}"}
        }

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return object.__getattribute__(self, f"_{name}")


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
        self._font_name = ""
        self._encoding = "WinAnsiEncoding"
        self._font_bbox = [-166, -225, 1000, 931]
        self._flags = ""
        self._ascent = ""
        self._cap_height = ""
        self._descent = ""
        self._italic_angle = ""
        self._stemv = ""
        self._missing_width = ""
        self._procset = ""
        self._font_descriptor = ""

        for key, value in options.items():
            names = [key, f"_{key.lower()}"]
            for name in names:
                if hasattr(self, name) and not callable(getattr(self, name)):
                    setattr(self, name, value)

        if self.get_type() == "FontDescriptor":
            print(f"{self._font_name = }")
            self._OPEN_FONT = TTFont(FONT_LIB.get(str(self._font_name).lower()))
            print(self._OPEN_FONT['OS/2'].__dict__)
            print(self._OPEN_FONT['head'].__dict__)
            print(self._OPEN_FONT['hhea'].__dict__)
            print(self._OPEN_FONT['maxp'].__dict__)
            print(self._OPEN_FONT['cmap'].__dict__)
            print(self._OPEN_FONT['name'].__dict__)
            print(self._OPEN_FONT['post'].__dict__)
            print(self._OPEN_FONT['hmtx'].__dict__)

    def get_type(self):
        return self._type

    def type(self, type: str = None):
        if type is not None:
            self._type = type
        if self.get_type() in ["Page", "Pages", "Font", "Catalog", "FontDescriptor"]:
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
               f"{self.default()}" \
               f"<<\n{self.type()}{self.kids()}" \
               f"{self.parent()}{self.mediabox()}{self.contents()}{self.resources()}" \
               f"{self.length()}{self.subtype()}" \
               f"{self.name()}{self.basefont()}{self.encoding()}{self.pages()}" \
               f"{self.title()}{self.author()}{self.producer()}{self.creator()}" \
               f"{self.font_bbox()}{self.flags()}{self.ascent()}{self.descent()}" \
               f"{self.cap_height()}{self.italicangle()}{self.stemv()}{self.missingwidth()}" \
               f"{self.creation_date()}{self.mod_date()}{self.subject()}{self.keywords()}" \
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
        if self.get_type() != "Stream":
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

    def encoding(self, encoding: str = None):
        if self.get_type() != "Font":
            return ""
        if encoding is not None:
            self._encoding = encoding
        return f"/Encoding /{self._encoding}\n"

    def font_descriptor(self, font_descriptor: Union[str, int] = None):
        if self.get_type() != "Font":
            return ""
        if font_descriptor is not None:
            self._font_descriptor = font_descriptor
        return f"/FontDescriptor {self._font_descriptor} 0 R\n"

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

    def font_name(self, font_name: str = None):
        if font_name is not None:
            self._font_name = font_name
        if self.get_type() != "FontDescriptor":
            return ""
        return f"/FontName /{self._font_name}\n"

    def font_bbox(self, font_bbox: List[Union[int, str]] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        try:
            head_table = self._OPEN_FONT['head']
            self._font_bbox = [head_table.xMin, head_table.yMin, head_table.xMax, head_table.yMax]
        except AttributeError:
            self._font_bbox = [0, -205, 602, 770]
        if font_bbox is not None:
            self._font_bbox = font_bbox
        return f"/FontBBox [{' '.join([str(i) for i in self._font_bbox])}]\n"

    def flags(self, flags: Union[int, str] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        try:
            self._flags = self._OPEN_FONT['head'].flags
        except AttributeError:
            self._flags = 4
        if flags is not None:
            self._flags = flags
        return f"/Flags {self._flags}\n"

    def ascent(self, ascent: Union[int, str] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        try:
            self._ascent = self._OPEN_FONT['hhea'].ascent
        except AttributeError:
            self._ascent = 770
        if ascent is not None:
            self._ascent = ascent
        return f"/Ascent {self._ascent}\n"

    def descent(self, descent: Union[int, str] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        try:
            self._descent = self._OPEN_FONT['hhea'].descent
        except AttributeError:
            self._descent = -205
        if descent is not None:
            self._descent = descent
        return f"/Descent {self._descent}\n"

    def cap_height(self, cap_height: Union[int, str] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        try:
            self._cap_height = self._OPEN_FONT['OS/2'].sCapHeight
        except AttributeError:
            self._cap_height = 770
        if cap_height is not None:
            self._cap_height = cap_height
        return f"/CapHeight {self._cap_height}\n"

    def italicangle(self, italicangle: Union[int, str] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        try:
            self._italic_angle = self._OPEN_FONT['post'].italicAngle
        except AttributeError:
            self._italic_angle = 0
        if italicangle is not None:
            self._italic_angle = italicangle
        return f"/ItalicAngle {self._italic_angle}\n"

    def stemv(self, stemv: Union[int, str] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        self._stemv = 90
        if stemv is not None:
            self._stemv = stemv
        return f"/Stemv {self._stemv}\n"

    def missingwidth(self, missing_width: Union[int, str] = None):
        if self.get_type() != "FontDescriptor":
            return ""
        try:
            self._missing_width = self._OPEN_FONT['OS/2'].xAvgCharWidth
        except AttributeError:
            self._missing_width = 1000
        if missing_width is not None:
            self._missing_width = missing_width
        return f"/MissingWidth {self._missing_width}\n"

    def stream(self):
        if self.get_type() != "Stream":
            return ""
        contents: List[BaseContent] = sorted([*self._text, *self._line, *self._rect, *self._scatter], key=lambda obj: obj.z_index())
        code = '\n'.join([obj.code() for obj in contents])
        stream = f"stream\n{code}\nendstream\n"
        return stream

    def default(self):
        if self.get_type() == "ProcSet":
            return f"{self._procset}\n"
        else:
            return ""

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

    def page_size(self, page_size: Tuple[Union[int, float], ...] = None):
        if page_size is not None:
            self._mediabox = [0, 0, *page_size[:2]]
        return self._mediabox[2:4]

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
