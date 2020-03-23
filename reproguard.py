#!/usr/bin/python3
# coding: utf-8

import re
from MappingLoader import MappingLoader
from MappingLoader import ProGuardMethod

class Transform:
    @staticmethod
    def transform_method(info):
        method = ProGuardMethod()
        engine = MappingLoader()
        transformed_info = info
        after_class = ''
        if isinstance(info, str):
            # split with space
            method.return_type = info[:info.find(r' ')]
            other = info[info.find(r' ') + 1:]
            # split with (
            pre = other[:other.find('(')]

            # split with .
            cla_name = pre[:pre.rfind('.')]
            method.name = pre[pre.rfind('.') + 1:]

            # args exits
            if other[other.find('(') + 1] == ')':
                pass
            else:
                args = other[other.find('(') + 1: other.find(')')]
                for arg in args.split(','):
                    method.add_arg(arg.strip())

            cla = engine.find_class(cla_name)
            if cla:
                after_class = cla.name
                if method.name in cla.methods:
                    methods = cla.methods[method.name]
                    if isinstance(methods, list):
                        for md in methods:
                            if isinstance(md, ProGuardMethod):
                                # match return type
                                if md.return_type == method.return_type:
                                    # match args
                                    if md.args == method.args:
                                        transformed_info = md
                    else:
                        transformed_info = methods

        after_args = ''
        if isinstance(transformed_info, ProGuardMethod):
            for arg in transformed_info.args:
                after_args = after_args + ',' + arg
            after = transformed_info.return_type + ' ' + after_class + "." + transformed_info.name + '(' + after_args[1:] + ')'
        else:
            after = 'not matched'
        print('before: %s' % info + '\nafter: ' + after)
        print('------------------------')

    @staticmethod
    def transform_field():
        pass

    @staticmethod
    def transform_class():
        pass


class ProGuardClass:
    name = ''
    proguard_name = ''
    methods = []

    def add_method(self, method):
        self.methods.append(method)

    def __str__(self):
        return 'ProGuardClass: ' + str(self.__dict__)


class ProGuardField:
    pass


class Args:
    name = ''
    type = ''



def parse_line(line):
    if re.search(r'POP', line):
        return

    # deal with proGuard string
    valid_info = line[line.index(':')+1:]
    Transform.transform_method(valid_info)


if __name__ == '__main__':
    magic_start = r'<script type="text/plain" id="tracedata">'
    with open('test.html') as input_file:
        for line in input_file:
            if line.startswith(magic_start):
                # deal with current line
                line = line.replace(magic_start, '')
                parse_line(line)
                pass
            # start with numbers
            if re.search(r'^\d', line):
                parse_line(line)

