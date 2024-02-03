#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - base
# ==========================================
#
#
# 
"""


def snake_to_camel(snake: str):
    return "".join([each.capitalize() for each in snake.split("_")])


def camel_to_snake(camel: str):
    return "".join([("_" + each.lower()) if index != 0 and each.capitalize() == each else each for index, each in enumerate(camel)])


print(snake_to_camel("mod_data"))
print(snake_to_camel("mod_data_str"))
print(snake_to_camel("mod_data_str_"))
print(snake_to_camel("_mod_data_str_"))
print(camel_to_snake("ModDate"))
print(camel_to_snake("MODDate"))
print(camel_to_snake("ModDateTest"))
print(camel_to_snake("ModDateTestSS"))
