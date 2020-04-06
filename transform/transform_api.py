#!/bin/python
# coding: utf-8

from proguard_bean.pg_class import PGClass, PGMethod


class Request:
    def __init__(self, pg_class_name):
        self.pg_class_name = pg_class_name

    def get_class_name(self):
        return self.pg_class_name


class Response:
    def __init__(self, request, trans_class):
        self.request = request
        self.trans_class = trans_class

    def get_trans_class(self) -> PGClass:
        return self.trans_class

    def __str__(self):
        return str(self.__dict__)
