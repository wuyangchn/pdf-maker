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
from .objs import Obj, Resources, Text, Line, Rect
from .crf import Crf
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
        self.name = "PDF"
        self.page_size = (400, 800)
        self.filepath = ""

        self.content_bytes = b""
        self.content_str = ""
        self.component = []
        self.frame = []
        self.axis_area = [138, 400, 360, 270]  # x0, y0, w, h

        # self.default_text = [{
        #     "Tf": {"name": "", "index": "", "size": "12"},
        #     "Td": {"x": "100", "y": "100"},
        #     "Tj": {"text": "This is created by PDF-tool!"},
        # }]
        # self.default_resources = {
        #     "font": {"name": "F1", "index": "5"}
        # }
        self.default_page_size = [0, 0, 612, 792]

        catalog = Obj(type="catalog", index="1", pages="2")
        pages = Obj(type="pages", index="2", kids=[3])
        page = Obj(type="page", index="3", parent="2", resources=Resources(font="F1", font_index="5").to_dict(),
                   contents="4", mediabox=self.default_page_size)
        stream = Obj(type="", index="4", text=[])
        font = Obj(type="font", index="5", subtype="Type1", name="F1", basefont="arial")

        self._objs = [catalog, pages, page, stream, font]

        for key, value in options.items():
            setattr(self, key, value)

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
        if obj is None:
            obj = Obj(index=index, type=type, **options)
        if self.check_obj(obj, self._objs):
            self._objs.append(obj)
        if obj.get_type() == "Page":
            pages = self.get_obj(type="Pages")[0]
            pages.kids(obj.index())

    def add_page(self, contents_index: int = None, size: Union[tuple, list] = None, resources: dict = None):
        if size is None:
            size = [612, 792]
        if resources is None:
            resources = {}
        contents_index = "" if contents_index is not None else str(contents_index)
        pages_index = self.get_obj(type="Pages")[0].index()
        new_index = max([int(obj.index()) for obj in self._objs]) + 1
        new_page = Obj(type="page", index=f"{new_index}", parent=f"{pages_index}",
                       contents=f"{contents_index}", mediabox=[0, 0, *size], resources=resources)
        self.add_obj(obj=new_page)

    def get_obj(self, type: str = None, index: int = None):
        if type is not None:
            return [obj for obj in self._objs if obj.get_type() == type.capitalize()]
        if index is not None:
            return [obj for obj in self._objs if obj.index() == str(index)][0]

    def get_page(self, index: int):
        for num, obj in enumerate(self.get_obj(type="Page")):
            if num == index:
                return obj

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
        page.set_page_size(width=width, height=height)

    def text(self, page: int, x: int, y: int, text: str, size: int = 12, **options):
        page = self.get_page(index=page)
        font_name = page.get_font_name()
        font = self.get_obj(type="Font")[0].get_basefont()
        contents_page = self.get_obj(index=page.get_contents_index())
        contents_page.text(Text(font_name=font_name, size=size, x=x, y=y, text=text, font=font, **options))

    def line(self, page: int, start: List[int], end: List[int], width: Union[float, int] = None,
             color: Union[tuple, list, str] = None):
        if width is None:
            width = 0.5
        if color is None:
            color = "black"
        if isinstance(color, str):
            color = COLOR_PALETTE.get(color.lower(), [0, 0, 0])
        page = self.get_page(index=page)
        contents_page = self.get_obj(index=page.get_contents_index())
        contents_page.line(Line(start=start, end=end, color=color, width=width).to_dict())

    def rect(self, page: int, left_bottom: Union[list, tuple], width: int, height: int,
             line_width: Union[float, int] = None, color: Union[tuple, list, str] = None):
        if line_width is None:
            line_width = 0.5
        if color is None:
            color = "black"
        if isinstance(color, str):
            color = COLOR_PALETTE.get(color.lower(), [0, 0, 0])
        page = self.get_page(index=page)
        contents_page = self.get_obj(index=page.get_contents_index())
        contents_page.rect(Rect(
            *left_bottom, width=width, height=height, line_width=line_width, color=color).to_dict())

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
        root = 1
        for obj in self._objs:
            if obj.type() == "Catalog":
                root = obj.index()
        return f"trailer\n<<\n/Size {self._crf.size()}\n/Root {root} 0 R\n>>\nstartxref\n{self._crf.startoffset()}\n%%EOF\n"

    def update_crf(self):
        pass

    def _xmin(self):
        return float(0)

    def _xmax(self):
        return float(100)

    def _ymin(self):
        return float(0)

    def _ymax(self):
        return float(100)

    def _get_transfer_pos(self, x, y):
        x0, y0, w, h = self.axis_area
        x = (x - self._xmin()) / (self._xmax() - self._xmin()) * w + x0
        y = (y - self._ymin()) / (self._ymax() - self._ymin()) * h + y0
        return [x, y]

    def _get_isochron_line(self, point1, point2, color='1 0 0', width=1):
        line_str = ''
        if not len(point1) == len(point2) == 2:
            return line_str
        x0, y0, w, h = self.axis_area

        def _get_line_points(k, m):
            if k == 0:
                return [
                    [x0, m], [x0 + w, m]
                ]
            return [
                [x0, x0 * k + m], [x0 + w, (x0 + w) * k + m],
                [(y0 - m) / k, y0], [(y0 + h - m) / k, y0 + h]
            ]

        point_1 = self._get_transfer_pos(*point1)
        point_2 = self._get_transfer_pos(*point2)
        k = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
        m = point_2[1] - point_2[0] * k
        line = []
        for point in _get_line_points(k, m):
            if self.is_in_area(*point):
                line.append(point)
        if len(line) == 2:
            line_str = f'{width} w\r{color} RG\r{line[0][0]} {line[0][1]} m {line[1][0]} {line[1][1]} l S\r'
        return line_str

    def is_in_area(self, x, y):
        x0, y0, w, h = self.axis_area
        if x == -999:
            x = x0
        if y == -999:
            y = y0
        return x0 <= x <= x0 + w and y0 <= y <= y0 + h

    def set_axis_frame(self):
        from decimal import Decimal
        frame = ''
        x0, y0, w, h = self.axis_area
        frame += f'1 w\r0 0 0 RG\r{x0} {y0} {w} {h} re S\r'  # % 四个参数：最小x，最小y，宽度和高度

        xmin, xmax = float(self.figure.xaxis.min), float(self.figure.xaxis.max)
        nx, dx = int(self.figure.xaxis.split_number), float(self.figure.xaxis.interval)
        ymin, ymax = float(self.figure.yaxis.min), float(self.figure.yaxis.max)
        ny, dy = int(self.figure.yaxis.split_number), float(self.figure.yaxis.interval)

        for i in range(ny + 1):
            yi = y0 + i * h * dy / (ymax - ymin)
            if self.is_in_area(-999, yi):
                frame += f'{x0} {yi} m {x0 - 4} {yi} l S\r'
                frame += f'BT\r1 0 0 1 {x0 - 4 - 32} {yi - 4} Tm\r/F1 12 Tf\r0 0 0 rg\r({Decimal(str(ymin)) + i * Decimal(str(dy))}) Tj\rET\r'
        for i in range(nx + 1):
            xi = x0 + i * w * dx / (xmax - xmin)
            if self.is_in_area(xi, -999):
                frame += f'{xi} {y0} m {xi} {y0 - 4} l S\r'
                frame += f'BT\r1 0 0 1 {xi - 12} {y0 - 16} Tm\r/F1 12 Tf\r0 0 0 rg\r({Decimal(str(xmin)) + i * Decimal(str(dx))}) Tj\rET\r'
        self.frame.append(frame)
        return frame

    def set_split_line(self):
        others = []
        for i in range(200):
            if i * 50 >= self.page_size[0]:
                break
            others.append(f'[2] 0 d\n{i * 50} 0 m {i * 50} {self.page_size[1]} l S')
        for i in range(200):
            if i * 50 >= self.page_size[1]:
                break
            others.append(f'[2] 0 d\n0 {i * 50} m {self.page_size[0]} {i * 50} l S')
        self.content_str = self.content_str.replace(
            '% <flag: others>\r',
            '% <flag: others>\r' + '0.75 G\n' + '\n'.join(others),
        )

    def set_info(self):
        from datetime import datetime, timezone, timedelta
        date = str(datetime.now(tz=timezone(offset=timedelta(hours=8))))
        date = findall('(.*)-(.*)-(.*) (.*):(.*):(.*)\.(.*)', date)[0]
        date = ''.join(date[0:6])
        date = 'D:' + date + "+08'00'"
        self.content_str = self.content_str.replace(
            '% <flag: info CreationDate>',
            f"{date}",
        )
        self.content_str = self.content_str.replace(
            '% <flag: info ModDate>',
            f"{date}",
        )

        self.content_str = self.content_str.replace(
            '% <flag: info Title>',
            f'{self.sample.Info.sample.name} - {self.figure.name}'
        )
        self.content_str = self.content_str.replace(
            '% <flag: page title>\r',
            '% <flag: page title>\r' +
            f'(<This is a demo of the exported PDF.>) Tj T*\n'
            f'(<The PDFs can be freely edited in Adobe Illustrator.>) Tj\n'
        )

    def set_replace(self):
        self.content_str = self.content_str.replace(
            '% <main contents>\r',
            '% <main contents>\r' + '\r\n'.join(self.component)
        )
        self.content_str = self.content_str.replace(
            '% <frames>\r',
            '% <frames>\r' + '\r\n'.join(self.frame)
        )
        self.content_str = self.content_str.replace(
            '% <texts>\r',
            '% <texts>\r' + '\r\n'.join(self.text)
        )


