#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - main
# ==========================================
#
#
# 
"""
from .objs import Obj, Resources, Text, Line, Rect, Scatter
from pdf_maker.canvas import PlotArea, Canvas
from .crf import Crf
from pdf_maker.constants._global import PAGE_SIZE
from typing import List, Union


COLOR_PALETTE: dict = {
    "black": [0, 0, 0],
    "red": [1, 0, 0],
    "green": [0, 1, 0],
    "blue": [0, 0, 1],
}


class NewPDF:
    def __init__(self, **options):

        self._objs: List[Obj] = []
        self._pages = []
        self._crf: Crf = ...
        self._header = "%PDF-1.7\n"
        self._body = ""

        self.title = "NewPDF"
        self.author = "PDF-Maker"
        self.producer = "https://pypi.org/project/pdf-maker/"
        self.creator = "PDF-Maker"
        self.page_size = (595, 842)
        self.filepath = ""

        self.content_bytes = b""
        self.content_str = ""
        self.component = []
        self.frame = []
        self.axis_area = [138, 400, 360, 270]  # x0, y0, w, h

        for key, value in options.items():
            setattr(self, key, value)

        if isinstance(self.page_size, str):
            self.page_size = PAGE_SIZE.get(self.page_size.lower(), (595, 842))

        # default obj: catalog
        self.add_obj(obj=Obj(type="catalog", index="1", pages="2"))
        # default obj: pages
        self.add_obj(obj=Obj(type="pages", index="2", kids=[]))
        # default obj: one page
        self.add_obj(obj=Obj(type="page", index="3", parent="2", contents="4",
                             mediabox=[0, 0, *self.page_size],
                             resources=Resources(font="F1", font_index="5")))
        # default obj: stream
        self.add_obj(obj=Obj(type="", index="4", text=[]))
        # default obj: font
        self.add_obj(obj=Obj(type="font", index="5", subtype="Type1", name="F1", basefont="arial"))
        # default obj: info
        self.add_obj(obj=Obj(type="Info", index="6", title=self.title, author="Yang",
                             producer=self.producer, creator=self.creator))

    def del_obj(self, index: int):
        found = False
        for obj in self._objs:
            if obj.index() == str(index):
                self._objs.remove(obj)
                found = True
                break
        if not found:
            return
        if obj.get_type() == "Page":
            pages = self.get_obj(type="Pages")[0]
            pages.remove_kid(obj.index())

    def add_obj(self, index: Union[str, int] = None, type: str = None, obj: Obj = None, **options):
        if index is None:
            index = (lambda objs: max([int(obj.index()) for obj in objs]) if len(objs) > 0 else 0)(self._objs) + 1
        if obj is None:
            obj = Obj(index=str(index), type=type, **options)
        if self.check_obj(obj, self._objs):
            self._objs.append(obj)
        if obj.get_type() == "Page":
            pages = self.get_obj(index=obj._parent)
            pages.kids(obj.index())
        return obj

    def add_page(self, contents_index: Union[int, str] = None, size: Union[tuple, list, str] = None,
                 resources: Resources = None):
        if size is None:
            size = "a4"
        if isinstance(size, str):
            size = PAGE_SIZE.get(size, (595, 842))
        if resources is None:
            font = self.get_obj(type="font")[0]
            resources = Resources(font=font._name, font_index=font.index())
        if contents_index is None:
            contents = self.add_obj(type="Stream")
        else:
            contents = self.get_obj(index=str(contents_index))
        pages_index = self.get_obj(type="Pages")[0].index()
        return self.add_obj(type="page", parent=f"{pages_index}", contents=f"{contents.index()}",
                            mediabox=[0, 0, *size], resources=resources)

    def get_obj(self, type: str = None, index: Union[str, int] = None):
        if type is not None:
            return [obj for obj in self._objs if obj.get_type() == type.capitalize()]
        if index is not None:
            return [obj for obj in self._objs if obj.index() == str(index)][0]
        raise ValueError("Object not found.")

    def get_page(self, index: int, base: int = 1):
        return self.get_obj(type="Page")[int(int(index) - int(base))]

    def get_page_indexes(self):
        return [obj.index() for obj in self.get_obj("Page")]

    def check_obj(self, obj, objs):
        if obj is None:
            return False
        indexes = [obj.index() for obj in objs]
        types = [obj.type() for obj in objs]
        if obj.index() in indexes:
            raise ValueError(f"Index {obj.index()} already exists")
        if obj.type() in types and obj.type() in ["Catalog", "Pages"]:
            raise ValueError(f"Type {obj.type()} already exists")
        return True

    def save(self, filepath: str = ""):
        """
        Args:
            filepath:

        Returns:

        """
        if filepath == "":
            filepath = self.filepath
        print(filepath)
        with open(filepath, 'wb') as f:
            f.write(self.get_byte())

    def get_content(self):
        """
        Returns:

        """
        self.content_str = self.header() + self.body() + self.crf() + self.trailer()
        return self.content_str

    def get_byte(self):
        self.content_bytes = self.get_content().encode('utf-8')
        return self.content_bytes

    def set_page_size(self, index: int, width: int, height: int):
        """
        Args:
            index:
            height:
            width:

        Returns:

        """
        page = [obj for obj in self._objs if obj.get_type() == "Page"][index]
        page.page_size((width, height))

    def text(self, page: int, x: int, y: int, text: str, size: int = 12, base: int = 1, **options):
        page = self.get_page(index=page, base=base)
        font_name = page.get_font_name()
        font = self.get_obj(type="Font")[0].get_basefont()
        contents_page = self.get_obj(index=page.get_contents_index())
        text = Text(font_name=font_name, size=size, x=x, y=y, text=text, font=font, **options)
        contents_page.text(text)
        return text

    def line(self, page: int, start: List[int], end: List[int], width: Union[float, int] = None,
             color: Union[tuple, list, str] = None, **options):
        if width is None:
            width = 0.5
        if color is None:
            color = "black"
        if isinstance(color, str):
            color = COLOR_PALETTE.get(color.lower(), [0, 0, 0])
        page = self.get_page(index=page)
        contents_page = self.get_obj(index=page.get_contents_index())
        line = Line(start=start, end=end, color=color, width=width, **options)
        contents_page.line(line)
        return line

    def rect(self, page: int, left_bottom: Union[list, tuple], width: int, height: int,
             line_width: Union[float, int] = None, color: Union[tuple, list, str] = None,
             **options):
        if line_width is None:
            line_width = 0.5
        if color is None:
            color = "black"
        if isinstance(color, str):
            color = COLOR_PALETTE.get(color.lower(), [0, 0, 0])
        page = self.get_page(index=page)
        contents_page = self.get_obj(index=page.get_contents_index())
        rect = Rect(*left_bottom, width=width, height=height, line_width=line_width, color=color, **options)
        contents_page.rect(rect)
        return rect

    def scatter(self, page: int, x: int, y: int, size: int = 5, fill_color: Union[tuple, list, str] = None,
                stroke_color: Union[tuple, list, str] = None, **options):
        if stroke_color is None:
            stroke_color = "black"
        if fill_color is None:
            fill_color = "grey"
        page = self.get_page(index=page)
        contents_page = self.get_obj(index=page.get_contents_index())
        scatter = Scatter(x=x, y=y, size=size, fill_color=fill_color, stroke_color=stroke_color, **options)
        contents_page.scatter(scatter)
        return scatter

    def header(self, header: str = None):
        if header is not None:
            self._header = header
        return self._header

    def objs(self):
        return self._objs

    def body(self):
        body = ""
        for obj in self._objs:
            body = body + obj.data()
            obj._offset = (self.header() + body).find(f"{obj.index()} 0 obj")
            obj._number = "00000"
            obj._state = "n"
        self._body = body
        return self._body

    def crf(self):
        self._crf = Crf(objs=[
            {"offset": obj.offset(), "number": obj.number(), "state": obj.state()} for obj in self._objs])
        data = self._crf.data()
        self._crf._startoffset = (self._header + self._body + data).find("xref")
        return data

    def trailer(self):
        def _get_obj(type):
            try:
                return f"{self.get_obj(type=type)[0].index()} 0 R"
            except (ValueError, IndexError):
                return ""
        root = _get_obj(type="Catalog")
        info = _get_obj(type="Info")
        self._trailer = f"trailer\n<<\n" \
                        f"/Size {self._crf.size()}\n" \
                        f"/Root {root}\n" \
                        f"/Info {info}\n" \
                        f">>\nstartxref\n{self._crf.startoffset()}\n%%EOF\n"
        return self._trailer

    def move_page(self, from_index: int, to_index: int, base: int = 1):
        pages = self.get_obj(type="Pages")[0]
        page = pages._kids.pop(from_index - base)
        pages._kids.insert(to_index - base, page)

    def canvas(self, page: int, margin_left: Union[int, float], margin_top: Union[int, float],
               canvas: Canvas, base: int = 1):
        """
        Args:
            margin_top:
            margin_left:
            page:
            canvas:
            base: from which indexing page number starts

        Returns:

        """
        page = self.get_page(index=page, base=base)
        canvas.left_bottom((margin_left, page.page_size()[1] - margin_top - canvas.height()))
        font_name = page.get_font_name()
        font = self.get_obj(type="Font")[0].get_basefont()
        contents_page = self.get_obj(index=page.get_contents_index())
        for comp in canvas.components():
            print(comp.name())
            if isinstance(comp, Text):
                comp._font_name = font_name
                comp._font = font
                contents_page.text(comp)
            if isinstance(comp, Rect):
                contents_page.rect(comp)
            if isinstance(comp, Scatter):
                contents_page.scatter(comp)
            if isinstance(comp, Line):
                contents_page.line(comp)
        pass



