#!/bin/python
# coding: utf-8


class Request:
    pg_class = None

    def __init__(self, pg_class):
        self.pg_class = pg_class

    def get_class(self):
        return self.pg_class


class Response:
    request = None
    trans_class = None

    def __init__(self, request, trans_class):
        self.request = request
        self.trans_class = trans_class
