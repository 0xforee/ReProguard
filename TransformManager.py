#!/bin/python
# coding: utf-8
from MappingLoader import MappingLoader

ENGINE = None


def transform(pg_class):
    global ENGINE
    if not ENGINE:
        ENGINE = MappingLoader()

    # do transform


    # 三个方法
    # 解析类名
    # 解析方法名
    # 解析字段名