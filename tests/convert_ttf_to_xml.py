#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-maker - convert_ttf_to_xml
# ==========================================
#
#
# 
"""
from xml.etree import ElementTree
from pdf_maker.constants._global import FONT_LIB, COLOR_PALETTE, LINE_STYLE, WIND
from fontTools.ttLib import TTFont


fonts = FONT_LIB.keys()
fonts = ["times-new-roman"]

# for font in fonts:
#     TTFont(r"D:\PythonProjects\pdf-maker\pdf_maker\resources\font" + f"\\{font.lower()}.ttf").saveXML(f"{font}.xml")


# def get_font_width(text: str, font: str, size: int):
#     font = TTFont(FONT_LIB.get(str(font).lower())['file'])
#     cmap = font['cmap']
#     t = cmap.getcmap(3, 1).cmap
#     s = font.getGlyphSet()
#     pixels_per_em = font['head'].unitsPerEm
#     total = 0
#     for c in text:
#         if ord(c) in t and t[ord(c)] in s:
#             total += s[t[ord(c)]].width
#         else:
#             total += s['.notdef'].width
#     total = total * float(size) / pixels_per_em
#     return int(total)
#
#
# def get_font_height(text: str, font: str):
#     tree = ElementTree.parse(FONT_LIB.get(font.lower())['file'])
#     root = tree.getroot()
#     head_obj = root.find('head')
#     OS_2_obj = root.find('OS_2')
#     pixels_per_em = head_obj.find("unitsPerEm").attrib['value']
#     ascender = OS_2_obj.find("sTypoAscender").attrib['value']
#     descender = OS_2_obj.find("sTypoDescender").attrib['value']
#     line_gap = OS_2_obj.find("sTypoLineGap").attrib['value']
#     line_height = (float(ascender) + float(descender) + float(line_gap)) / float(pixels_per_em)
#     return line_height


def get_full_information(font: str):
    tree = ElementTree.parse(FONT_LIB.get(str(font).lower())['file'])
    root = tree.getroot()
    head_obj = root.find('head')
    hhea_obj = root.find('hhea')
    OS_2_obj = root.find('OS_2')
    post_obj = root.find('post')
    flags = head_obj.find("flags").attrib['value']
    xMin = head_obj.find("xMin").attrib['value']
    yMin = head_obj.find("yMin").attrib['value']
    xMax = head_obj.find("xMax").attrib['value']
    yMax = head_obj.find("yMax").attrib['value']
    font_bbox = [xMin, yMin, xMax, yMax]
    italic_angle = post_obj.find("italicAngle").attrib['value']
    ascent = OS_2_obj.find("sTypoAscender").attrib['value']
    descent = OS_2_obj.find("sTypoDescender").attrib['value']
    ascent = hhea_obj.find("ascent").attrib['value']
    descent = hhea_obj.find("descent").attrib['value']
    cap_height = OS_2_obj.find("sCapHeight").attrib['value']
    font_weight = OS_2_obj.find("usWeightClass").attrib['value']
    # The possible values of font weight are 100, 200, 300, 400, 500, 600, 700, 800, or 900
    stemv = int(10 + 220 * (int(OS_2_obj.find("usWeightClass").attrib['value']) - 50) / 900)

    avg_char_width = OS_2_obj.find("xAvgCharWidth").attrib['value']
    max_char_width = OS_2_obj.find("xAvgCharWidth").attrib['value']
    first_char = OS_2_obj.find("usFirstCharIndex").attrib['value']
    last_char = OS_2_obj.find("usLastCharIndex").attrib['value']
    x_height = OS_2_obj.find("sxHeight").attrib['value']

    missing_width = avg_char_width

    horizontal_scale = 0.5

    root = tree.getroot()
    mtx_objs = root.find('hmtx').findall('mtx')
    map_objs = root.find('cmap').find('cmap_format_4').findall('map')

    missing_width = int(int(OS_2_obj.find("xAvgCharWidth").attrib['value']) * horizontal_scale)
    units_per_em = int(root.find('head').find('unitsPerEm').attrib['value'])
    # print(pixels_per_em)

    chars = {}
    differences = []
    for map_obj in map_objs:
        chars.update({int(map_obj.attrib.get("code"), 16): {"name": map_obj.attrib.get("name")}})
        differences.append(f"{int(map_obj.attrib.get('code'), 16)} /{map_obj.attrib.get('name')}")

    chars_list = [(code, str(char['name']), str(missing_width), "0") for code, char in chars.items()]
    chars_list = sorted(chars_list, key=lambda x: x[0])
    char_names = [char[1] for char in chars_list]
    char_codes = [char[0] for char in chars_list]

    mtx_list = [(mtx.attrib.get('name'), mtx.attrib.get('width'), mtx.attrib.get('lsb')) for mtx in mtx_objs]

    # 选取ASCII 255个标准字符
    first_char = 0
    last_char = 255
    for i in range(first_char, last_char + 1):
        if i not in char_codes:
            chars_list.append((i, "", f"{missing_width}", "0"))
        else:
            name = char_names[char_codes.index(i)]
            index = [mtx[0] for mtx in mtx_list].index(name)
            if index != -1:
                chars_list[char_codes.index(i)] = (
                    i, name, f"{int(int(mtx_list[index][1]) * horizontal_scale)}", mtx_list[index][2])
    chars_list = sorted(chars_list, key=lambda x: x[0])
    widths = [char[2] for char in chars_list[first_char:(last_char + 1)]]

    info = {
        "flags": flags,
        "font_bbox": font_bbox,
        "italic_angle": italic_angle,
        "ascent": ascent,
        "descent": descent,
        "cap_height": cap_height,
        "font_weight": font_weight,
        "stemv": stemv,

        "avg_char_width": avg_char_width,
        "max_char_width": max_char_width,
        "first_char": first_char,
        "last_char": last_char,
        "x_height": x_height,

        "missing_width": missing_width,
        "units_per_em": units_per_em,
    }

    for items in info.items():
        print(f'"{items[0]}": {items[1]}')


for font in fonts:
    # print(f"{font} line height = {get_font_height('', font=font)}")
    # get_full_information(font)
    # print("\n")
    pass

