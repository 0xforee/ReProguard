#!/bin/python
# coding: utf-8


class Request:
    def __init__(self, pg_class):
        self.pg_class = pg_class

    def get_class(self):
        return self.pg_class


class Response:
    def __init__(self, request, trans_class):
        self.request = request
        self.trans_class = trans_class

    def __str__(self):
        return str(self.__dict__)
