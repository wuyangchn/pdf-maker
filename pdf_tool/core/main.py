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
from .objs import Obj
from .crf import Crf
from typing import List, Union


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
        self.component = []
        self.text = []
        self.frame = []
        self.axis_area = [138, 400, 360, 270]  # x0, y0, w, h

        self.all_types = ["Catalog", "Pages", "Page", "Font"]
        self.all_fonts = ["Helvetica"]
        self.default_text = [{
            "Tf": {"name": "", "index": "", "size": "12"},
            "Td": {"x": "100", "y": "100"},
            "Tj": {"text": "This is created by PDF-tool!"},
        }]
        self.default_resources = {
            "font": {"name": "F1", "index": "5"}
        }
        self.default_page_size = [0, 0, 612, 792]

        catalog = Obj(type="catalog", index="1", pages="2")
        pages = Obj(type="pages", index="2", kids=[3])
        page = Obj(type="page", index="3", parent="2", resources=self.default_resources,
                   contents="4", mediabox=self.default_page_size)
        stream = Obj(type="", index="4", text=self.default_text)
        font = Obj(type="font", index="5", subtype="Type1", name="F1", basefont="Helvetica")

        self._objs = [catalog, pages, page, stream, font]

        for key, value in options.items():
            setattr(self, key, value)

    def add_obj(self, index: Union[str, int] = None, type: str = None, obj: Obj = None, **options):
        if obj is None:
            obj = Obj(index=index, type=type, **options)
        if self.check_obj(obj, self._objs):
            self._objs.append(obj)
        if obj.get_type() == "Page":
            pages = self.get_obj(type="Pages")
            pages.kids(obj.index())

    def get_obj(self, type: str = None, index: int = None):
        if type is not None:
            return [obj for obj in self._objs if obj.get_type() == type.capitalize()][0]
        if index is not None:
            return [obj for obj in self._objs if obj.index() == str(index)][0]

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

    def set_text(self):
        text = ''
        x0, y0, w, h = self.axis_area
        # Figure Title
        text += f'BT\r1 0 0 1 {x0 + 10} {y0 - 20 + h} Tm\n/F1 12 Tf\r({self.sample.Info.sample.name}) Tj\rET\r'
        if self.figure._type == 'isochron':
            xaxis_title_number = ''.join(list(filter(str.isdigit, self.figure.xaxis.title.text)))
            yaxis_title_number = ''.join(list(filter(str.isdigit, self.figure.yaxis.title.text)))
            # X axis title
            x_title_length = 5 * 12  # length * font point size
            text += '\n'.join([
                'BT', f'1 0 0 1 {x0 + w / 2 - x_title_length / 2} {y0 - 30} Tm',
                # % 使用Tm将文本位置设置为（35,530）前四个参数是cosx, sinx, -sinx, cosx表示逆时针旋转弧度
                '/F1 8 Tf', '5 Ts', f'({xaxis_title_number[:2]}) Tj', '/F1 12 Tf', '0 Ts', '(Ar / ) Tj',
                '/F1 8 Tf', '5 Ts', f'({xaxis_title_number[2:4]}) Tj', '/F1 12 Tf', '0 Ts', '(Ar) Tj', 'ET',
            ])
            # Y axis title
            y_title_length = 5 * 12  # length * font point size
            text += '\n'.join([
                'BT', f'0 1 -1 0 {x0 - 40} {y0 + h / 2 - y_title_length / 2} Tm',
                # % 使用Tm将文本位置设置为（35,530）前四个参数是cosx, sinx, -sinx, cosx表示逆时针旋转弧度
                '/F1 8 Tf', '5 Ts', f'({yaxis_title_number[:2]}) Tj', '/F1 12 Tf', '0 Ts', '(Ar / ) Tj',
                '/F1 8 Tf', '5 Ts', f'({yaxis_title_number[2:4]}) Tj', '/F1 12 Tf', '0 Ts', '(Ar) Tj', 'ET',
            ])

        elif self.figure._type == 'spectra':
            # X axis title
            x_title_length = 13 * 12  # length * font point size
            text += '\n'.join([
                'BT', f'1 0 0 1 {x0 + w / 2 - x_title_length / 2} {y0 - 30} Tm',
                '/F1 12 Tf', '0 Ts', '(Cumulative ) Tj', '/F1 8 Tf', '5 Ts', f'(39) Tj',
                '/F1 12 Tf', '0 Ts', '(Ar Released (%)) Tj', 'ET',
            ])
            # Y axis title
            y_title_length = 9 * 12  # length * font point size
            text += '\n'.join([
                'BT', f'0 1 -1 0 {x0 - 40} {y0 + h / 2 - y_title_length / 2} Tm',
                '/F1 12 Tf', '0 Ts', f'(Apparent Age (Ma)) Tj', 'ET',
            ])
            # Text 1
            info = self.figure.set1.info
            if len(info) == 8 and self.figure.text1.text != '':
                sum39 = findall('∑{sup|39}Ar = (.*)', self.figure.text1.text)[1]
                text += '\n'.join([
                    'BT', f'1 0 0 1 {x0 + w / 4} {y0 + h / 2} Tm',
                    '/F1 12 Tf', '0 Ts', f'(t) Tj', '/F1 8 Tf', '-2 Ts', f'(p) Tj',
                    '/F1 12 Tf', '0 Ts',
                    f'( = {info[4]:.2f} <261> {info[6]:.2f} Ma, MSMD = {info[3]:.2f}, ∑) Tj',
                    '/F1 8 Tf', '5 Ts', f'(39) Tj',
                    '/F1 12 Tf', '0 Ts',
                    f'(Ar = {sum39}) Tj',
                    'ET',
                ])
            # Text 2
            text2 = findall('∑{sup|39}Ar = (.*)', self.figure.text2.text)[1]

        self.text.append(text)
        return text

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

    def get_pdf(self):
        self.do_function(
            self.set_main_content,
            self.set_axis_frame,
            self.set_text,
            self.set_info,
            self.set_replace,
            # self.set_split_line,
            self.toByte,
            self.save,
        )

    def get_contents(self):
        self.do_function(
            self.set_main_content,
            self.set_axis_frame,
            self.set_text,
        )
        return {
            'component': self.component,
            'frame': self.frame,
            'text': self.text,
        }

    def toByte(self):
        self.content_bytes = self.content_str.encode('utf-8')
        return self.content_bytes

    def do_function(self, *handlers):
        for handler in handlers:
            try:
                handler()
            except Exception:
                print(traceback.format_exc())
                continue
