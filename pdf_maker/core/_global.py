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


FONT_LIB = {
    "arial": r"D:\PythonProjects\pdf-tool\pdf_tool\resources\font\arial.ttf",
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


PAGE_SIZE: dict = {
    "a3": (842, 1191),
    "a4": (595, 842),
    "a5": (420, 595),
    "b5": (516, 729),
    "letter": (612, 792),
    "legal": (612, 1008),
}
