#!/usr/bin/python3
# coding: utf-8

import re
from proguard_bean.pg_class import PGClass, PGMethod
import transform.transform_manager as transform_manager
from transform.transform_api import Request, Response


class Transform:
    @staticmethod
    def transform_method(info):
        cla = PGClass()
        method = PGMethod()
        response = None
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

            # transform
            cla.name = cla_name
            cla.add_method(method.name, method)

            response = transform_manager.transform(Request(cla))

        print('before: %s, after: %s' % (info, response) )
        print('------------------------')


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

