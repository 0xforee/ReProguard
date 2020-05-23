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
        # 1.出现多个方法的混淆名称是相同的情况，所以对于这些方法，key是相同的，那么就只能以列表存储，通过参数比对还原
        # 2.出现相同方法，但是只有代码行数不同的情况
        if name in self.methods:
            if not self.try_merge(name, method): # 如果第二种情况没有合并成功
                self.methods[name].append(method)
        else:
            self.methods[name] = [method]

    def try_merge(self, name, method):
        old_methods = self.methods[name]
        for old_method in old_methods:
            if isinstance(old_method, PGMethod):
                if old_method.equal(method):
                    old_method.merge(method)
                    return True
        return False

    def add_field(self, name, field):
        if name in self.fields:
            self.fields[name].append(field)
        else:
            self.fields[name] = [field]

    """
    参考下边的 find_methods
    """
    @DeprecationWarning
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
            if source_scope and line_number and int(source_scope.split(':')[0]) <= int(line_number) <= int(source_scope.split(':')[1]):
                return method

        return None

    """
    reProguard5.2 之后，因为可能的内联功能，line_number 对应的可能是虚拟行号
    虚拟行号可能有多个，因为这多个行号对应的是 exception 的调用栈，所以返回值会是多个方法名称
    详情看：https://www.guardsquare.com/en/products/proguard/manual/retrace#
    """
    def find_methods_by_line(self, proguard_name, line_number):
        if not self.methods:
            return None
        if not (proguard_name in self.methods):
            return None
        methods = self.methods[proguard_name]
        if not methods:
            return None
        if len(methods) == 1:
            return methods
        results = []
        for method in methods:
            source_scope = method.get_source_scope()
            if source_scope and line_number:
                # 可能存在多个行号，都需要参与匹配
                for line_scope in source_scope:
                    if int(line_scope.split(':')[0]) <= int(line_number) <= int(line_scope.split(':')[1]):
                        results.append(method)

        return results

    """
    通过参数，返回值，名称找方法
    """
    def find_methods(self, proguard_name, args=None, return_type=None):
        if not self.methods:
            return None
        if not (proguard_name in self.methods):
            return None
        methods = self.methods[proguard_name]
        if not methods:
            return None

        if args is not None:
            methods = PGClass.__filter_by_args(args, methods)

        if return_type is not None:
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
        if need_args and (method.args is not None):
            pretty_args += '('
            for arg in method.args:
                pretty_args += (arg + ',')

            pretty_args = pretty_args.strip(',')
            pretty_args += ')'

        pretty_return_type = ''
        if need_return_type and (method.return_type is not None):
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
        """
        方法所在的行号
        """
        self.source_scope = []  # 方法所在的源码行号范围，例，23:32
        """
        方法所在的真实行号，如果不为空，表示 source_scope 是虚拟行号（reProguard 5.2版本之后的新逻辑）
        
        """
        self.real_source_scope = []

    def add_source_scope(self, source_scope, real_scope=''):
        if source_scope:
            self.source_scope.append(source_scope)
            self.real_source_scope.append(real_scope)

    def get_return_type(self):
        return self.return_type

    def set_return_type(self, return_type):
        self.return_type = return_type

    def add_arg(self, arg):
        self.args.append(arg)

    def get_source_scope(self):
        return self.source_scope

    """
    判断两个方法是否相等，方法名称和描述符要相等
    """
    def equal(self, other):
        if isinstance(other, PGMethod):
            if self.name != other.name:
                return False
            if self.return_type != other.return_type:
                return False
            if len(self.args) != len(other.args):
                return False
            for index in range(0, len(self.args)):
                if self.args[index] != other.args[index]:
                    return False
        else:
            return False

        return True

    """
    合并两个方法，主要是合并源码范围
    """
    def merge(self, other):
        if isinstance(other, PGMethod):
            self.source_scope.extend(other.source_scope)
            self.real_source_scope.extend(other.real_source_scope)

    def __str__(self) -> str:
        return 'ProGuardMethod: ' + str(self.__dict__)

    __repr__ = __str__
