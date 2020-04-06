#!/bin/python
# coding: utf-8
from core.mapping_loader import MappingLoader
from transform.transform_api import Response, Request

ENGINE = None


def transform(request) -> Response:
    if not isinstance(request, Request):
        raise Exception(' not invalid args, need Request')

    global ENGINE
    if not ENGINE:
        ENGINE = MappingLoader()

    # do transform
    pg_class_name = request.get_class_name()

    if not pg_class_name:
        raise NameError(' not invalid args, need class name')

    cla = ENGINE.find_class(pg_class_name)

    return Response(request, cla)


