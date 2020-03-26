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

    def find_method(self, proguard_name, line_number):
        if not self.methods:
            return None
        if not (proguard_name in self.methods):
            return None
        methods = self.methods[proguard_name]
        if not methods:
            return None
        if len(methods) == 1:
            return methods[0]
        for method in methods:
            source_scope = method.get_source_scope()
            if source_scope and line_number and source_scope.split(':')[0] <= line_number <= source_scope.split(':')[1]:
                return method

        return None

    def find_methods(self, proguard_name, args=None, return_type=None):
        if not self.methods:
            return None
        if not (proguard_name in self.methods):
            return None
        methods = self.methods[proguard_name]
        if not methods:
            return None

        if args:
            methods = PGClass.__filter_by_args(args, methods)

        if return_type:
            methods = PGClass.__filter_by_return_type(return_type, methods)

        return methods

    @staticmethod
    def __filter_by_args(args, methods):
        return_methods = []
        for method in methods:
            if method.args == args:
                return_methods.append(method)

        return return_methods

    @staticmethod
    def __filter_by_return_type(return_type, methods):
        return_methods = []
        for method in methods:
            if method.return_type == return_type:
                return_methods.append(method)

        return return_methods

    def find_field(self, proguard_name, field_type):
        if not self.fields:
            return None
        if not (proguard_name in self.fields):
            return None
        fields = self.fields[proguard_name]
        if not fields:
            return None

        for field in fields:
            if field.type == field_type:
                return field

        return None

    def pretty_method(self, method, need_args=False, need_return_type=False):
        if not method:
            return None

        pretty_args = ''
        if need_args and method.args:
            pretty_args += '('
            for arg in method.args:
                pretty_args += (arg + ',')

        pretty_args = pretty_args.strip(',')

        pretty_return_type = ''
        if need_return_type and method.return_type:
            pretty_return_type = method.return_type + ' '

        return pretty_return_type + self.name + '.' + method.name + pretty_args

    def pretty_field(self, field, need_type=False):
        if not field:
            return None
        pretty_type = ''
        if need_type and field.type:
            pretty_type = field.type + ' '

        return pretty_type + field.name

    def __str__(self):
        return 'ProGuardClass: ' + str(self.__dict__)

    __repr__ = __str__


class PGField:
    def __init__(self):
        self.name = ''
        self.type = ''

    def __str__(self):
        return "ProguardField: " + str(self.__dict__)

    __repr__ = __str__


class PGMethod:

    def __init__(self):
        self.name = ''
        self.return_type = ''
        self.args = []  # 注意顺序
        self.source_scope = ''  # 方法所在的源码行号范围，例，23:32

    def get_return_type(self):
        return self.return_type

    def set_return_type(self, return_type):
        self.return_type = return_type

    def add_arg(self, arg):
        self.args.append(arg)

    def get_source_scope(self):
        return self.source_scope

    def __str__(self) -> str:
        return 'ProGuardMethod: ' + str(self.__dict__)

    __repr__ = __str__
