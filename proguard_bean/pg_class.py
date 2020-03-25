#!/usr/bin/python
# coding: utf-8

import re


class PGClass:
    """
    混淆以类为单位
    """

    def __init__(self):
        # 类名
        self.name = ''
        # 方法，以混淆之后的值为 key，以 PGMethod 列表为值
        self.methods = {}
        # 字段，以混淆之后的值为 key，以 PGField 列表为值
        self.fields = {}

    def add_method(self, name, method):
        # 可能会出现多个方法的混淆名称是相同的情况，所以对于这些方法，key是相同的，那么就只能以列表存储，通过参数比对还原
        if name in self.methods:
            self.methods[name].append(method)
        else:
            self.methods[name] = [method]

    def add_field(self, name, field):
        if name in self.fields:
            self.fields[name].append(field)
        else:
            self.fields[name] = [field]

    def match_method(self, method):
        if self.methods:
            md_list = self.methods[method.name]
            for md in md_list:
                if md.match(method):
                    return md

        return None

    def match_field(self, field):
        if self.fields:
            fd_list = self.fields[field.name]
            for fd in fd_list:
                if fd.match(field):
                    return fd

        return None

    def __str__(self):
        return 'ProGuardClass: ' + str(self.__dict__)

    __repr__ = __str__


class PGField:
    def __init__(self):
        self.name = ''
        self.type = ''

    def match(self, other):
        return self.type == other.type

    def __str__(self):
        return "ProguardField: " + str(self.__dict__)

    __repr__ = __str__


class PGMethod:

    def __init__(self):
        self.name = ''
        self.return_type = ''
        self.args = []  # 注意顺序

    def get_return_type(self):
        return self.return_type

    def set_return_type(self, return_type):
        self.return_type = return_type

    def add_arg(self, arg):
        self.args.append(arg)

    def match(self, other):
        return self.return_type == other.return_type \
               and self.args == other.args

    def __eq__(self, other):
        return self.name == other.name \
               and self.return_type == other.return_type \
               and self.args == other.args

    def __str__(self) -> str:
        return 'ProGuardMethod: ' + str(self.__dict__)

    __repr__ = __str__
