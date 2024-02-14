#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - global
# ==========================================
#
#
# 
"""
import os
from typing import List, Mapping, Union


SOURCE_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")


FONT_LIB = {
    # Note the names should be postScriptName, such as ArialMT not Arial
    "ArialMT".lower(): {
        "file": os.path.join(SOURCE_ROOT, "font/arial.xml"),  # do not use "font\\xxx.xx"
                                                              # because this cannot be recognized in unix system
        # "ttf_file": os.path.join(SOURCE_ROOT, "font/arial.ttf"),
        "ttf_file": os.path.join(SOURCE_ROOT, "subset/arial-subset.ttf"),
        "type": "TrueType",
        "line_height": 0.66748046875,
        "units_per_em": 2048,
        "flags": "32",
        "font_bbox": ['-1361', '-665', '4096', '2129'],
        "italic_angle": 0, "ascent": 1854, "descent": -434, "cap_height": 1467, "font_weight": 400,
        "stemv": 95, "avg_char_width": 904, "max_char_width": 904, "first_char": 0, "last_char": 255,
        "x_height": 1062, "missing_width": 452,
    },
    "Calibri".lower(): {
        "file": os.path.join(SOURCE_ROOT, "font/calibri.xml"),
        "ttf_file": os.path.join(SOURCE_ROOT, "subset/calibri-subset.ttf"),
        # "ttf_file": os.path.join(SOURCE_ROOT, "font/calibri.ttf"),
        "type": "TrueType", "postScriptName": "Calibri",
        "line_height": 0.66748046875,
        "units_per_em": 2048,
        "flags": "32",
        "font_bbox": ['-1361', '-665', '4096', '2129'],
        "italic_angle": 0, "ascent": 1854, "descent": -434, "cap_height": 1467, "font_weight": 400,
        "stemv": 95, "avg_char_width": 904, "max_char_width": 904, "first_char": 0, "last_char": 255,
        "x_height": 1062, "missing_width": 452,
    },
    "Helvetica".lower(): {
        "file": os.path.join(SOURCE_ROOT, "font/helvetica.xml"),
        "ttf_file": os.path.join(SOURCE_ROOT, "subset/helvetica-subset.ttf"),
        "type": "TrueType", "postScriptName": "Helvetica",
        "line_height": 0.60986328125,
        "units_per_em": 2048,
        "flags": "31",
        "font_bbox": ['-76', '-461', '1976', '1946'],
        "italic_angle": 0.0, "ascent": 1577, "descent": -471, "cap_height": 1469, "font_weight": 400,
        "stemv": 95, "avg_char_width": 1079, "max_char_width": 1079, "first_char": 0, "last_char": 255,
        "x_height": 1071, "missing_width": 539,
    },
    "TimesNewRomanPSMT".lower(): {
        "file": os.path.join(SOURCE_ROOT, "font/times.xml"),
        "ttf_file": os.path.join(SOURCE_ROOT, "subset/times-subset.ttf"),
        # "ttf_file": os.path.join(SOURCE_ROOT, "font/times.ttf"),
        "type": "TrueType", "postScriptName": "TimesNewRomanPSMT",
        "line_height": 0.62744140625,
        "units_per_em": 2048,
        # "flags": "00001000 00011001",
        "flags": "32",
        "font_bbox": ['-1164', '-628', '4190', '2129'],
        "italic_angle": 0.0, "ascent": 1825, "descent": -443, "cap_height": 1356, "font_weight": 400,
        "stemv": 95, "avg_char_width": 821, "max_char_width": 821, "first_char": 0, "last_char": 255,
        "x_height": 916, "missing_width": 410,
    },
    "MicrosoftSansSerif".lower(): {
        "file": os.path.join(SOURCE_ROOT, "font/micross.xml"),
        "ttf_file": os.path.join(SOURCE_ROOT, "subset/micross-subset.ttf"),
        # "ttf_file": os.path.join(SOURCE_ROOT, "font/micross.ttf"),
        "type": "TrueType", "postScriptName": "MicrosoftSansSerif",
        "line_height": 0.64892578125,
        "units_per_em": 2048,
        # "flags": "00000000 00011011",
        "flags": "32",
        "font_bbox": ['-1188', '-526', '3017', '2055'],
        "italic_angle": 0.0, "ascent": 1888, "descent": -430, "cap_height": 1466, "font_weight": 400,
        "stemv": 95, "avg_char_width": 901, "max_char_width": 901, "first_char": 0, "last_char": 255,
        "x_height": 1061, "missing_width": 450,
    },
    "EWGWZO+Untitled1".lower(): {
        "file": os.path.join(SOURCE_ROOT, "font/arial.xml"),
        "ttf_file": os.path.join(SOURCE_ROOT, "font/arial.ttf"),
        "type": "TrueType",
        "line_height": 0.66748046875,
        "units_per_em": 2048,
        "flags": "32",
        "font_bbox": ['33', '-20', '1271', '1370'],
        "italic_angle": 0, "ascent": 800, "descent": -200, "cap_height": 1349, "font_weight": 400,
        "stemv": 0, "avg_char_width": 904, "max_char_width": 904, "first_char": 65, "last_char": 68,
        "x_height": 1062, "missing_width": 452,
    },
}


COLOR_PALETTE: dict = {
    "black": [0, 0, 0],
    "red": [1, 0, 0],
    "green": [0, 1, 0],
    "blue": [0, 0, 1],
    "white": [1, 1, 1],
    "yellow": [1, 1, 0],
    "magenta": [1, 0, 1],
    "cyan": [0, 1, 1],
    "grey": [0.5, 0.5, 0.5],

    "myColor1": [0.145, 0.54, 0.745],  # #2596be rgb(37, 150, 190)
    "myColor2": [0.671, 0.859, 0.89],  # #abdbe3 rgb(171,219,227)
}

COLOR_MAP_1: list = [
    # 3399FF, 33FF99, FFFF66, FF6666,
    [0.200, 0.600, 1.000], [0.200, 1.000, 0.600], [1.000, 1.000, 0.400], [1.000, 0.400, 0.400],
    # 00FFFF, 00994C, FF8000, 7F00FF
    [0.000, 1.000, 1.000], [0.000, 0.600, 0.298], [1.000, 0.502, 0.000], [0.498, 0.000, 1.000],
    # 3333FF, FF3399
    [1.000, 0.200, 0.600], [0.200, 0.200, 1.000],
]


PAGE_SIZE: dict = {
    "a3": (842, 1191),
    "a4": (595, 842),  # pixels/points at 72 ppi
    "a5": (420, 595),
    "b5": (516, 729),
    "letter": (612, 792),
    "legal": (612, 1008),
}

VALIGN: List[str] = [
    "bottom", "center", "top",
]

HALIGN: List[str] = [
    "left", "middle", "right",
]

UNIT: Mapping[str, Union[int, float]] = {
    "cm": 0.393701, "inch": 1.0, "mm": 0.0393701, "point": 1, "pt": 1,
}

LINE_STYLE: Mapping[str, Union[int, float]] = {
    "solid": ...,
    "dotted": (1, 1),
    "dashed": (5, 5),
    "dashdot": (5, 2, 1, 2),
    "densely_dashed": (5, 1),
    "loosely_dashed": (5, 10),
    "densely_dotted": (1, 10),
    "loosely_dotted": (1, 1),
}

WIND = ["WIND_EVEN_ODD", "WIND_NON_ZERO"]

KEYNAMES = [
    "__ClipOutsidePlotAreas", "__CanvasFrame"
]
