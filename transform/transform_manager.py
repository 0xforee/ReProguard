#!/bin/python
# coding: utf-8
from core.mapping_loader import MappingLoader
from proguard_bean.pg_class import PGClass
from transform.transform_api import Response, Request

ENGINE = None


def transform(request):
    if not isinstance(request, Request):
        raise Exception(' not invalid args, need Request')

    global ENGINE
    if not ENGINE:
        ENGINE = MappingLoader()

    # do transform
    pg_class = request.get_class()
    if not isinstance(pg_class, PGClass):
        raise NameError(' not invalid args, need PGClass')

    if not pg_class.name:
        raise NameError(' not invalid args, need PGClass name')

    cla = ENGINE.find_class(pg_class.name)
    response_class = PGClass()
    response = Response(request, response_class)
    if cla:
        # 解析方法名
        if pg_class.methods:
            for md_name in pg_class.methods:
                # 获取方法
                md_list = pg_class.methods[md_name]
                for md in md_list:
                    reproguard_md = cla.match_method(md)
                    response_class.add_method(md_name, reproguard_md)

        # 解析字段名
        if pg_class.fields:
            for fd_name in pg_class.fields:
                # 获取方法
                fd_list = pg_class.fields[fd_name]
                for fd in fd_list:
                    reproguard_fd = cla.match_field(fd)
                    response_class.add_field(fd_name, reproguard_fd)

    return response


