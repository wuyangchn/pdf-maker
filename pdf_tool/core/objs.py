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
        self._resources: dict = {
            "font": {"name": "", "index": ""}
        }
        self._text: List[dict] = [{
            "Tf": {"name": "", "index": "", "size": "12"},
            "Td": {"x": "100", "y": "100"},
            "Tj": {"text": "Hello, World!"},
        }]
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
        if length is not None:
            self._length = str(length)
        if not self._length.isdigit():
            return ""
        return f"<<\n/Length {self._length}\n>>\n"

    def stream(self):
        if self.get_type() in ["Page", "Pages", "Font", "Catalog"]:
            return ""
        return f"stream\n{self.text()}endstream\n"

    def text(self, text: dict = None):
        if text is not None:
            self._text.append(text)
        if len(self._text) == 0:
            return ""
        text = "\n".join([f"/{each['Tf']['name']} {each['Tf']['size']} Tf\n{each['Td']['x']} {each['Td']['y']} Td\n({each['Tj']['text']}) Tj" for each in self._text])
        return f"BT\n{text}\nET\n"

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
