#!/usr/bin/python3
# coding: utf-8
from transform.transformer import ITransformer
import re
from proguard_bean.pg_class import PGClass, PGMethod
import transform.transform_manager as transform_manager
from transform.transform_api import Request, Response


class StackTraceTransformer(ITransformer):
    def __init__(self):
        pass

    def start(self, file):
        for line in file:
            stack_trace.parse_line(line)

    def parse_line(self, line):
        obj = re.search(r'[ $0-9a-zA-Z.:]+\([$0-9a-zA-Z.:]*\)+', line)
        if obj:
            print(obj.group())
            self.transform_method(line, obj.group())

    def transform_method(self, origin_line, info):
        if isinstance(info, str):
            info = info.strip()
            other = info[info.find(r' ') + 1:]
            pre = other[:other.find('(')]
            method_args = []

            cla_name = pre[:pre.rfind('.')]
            method_name = pre[pre.rfind('.') + 1:]
            method_line_number = ''

            # args exits
            if other[other.find('(') + 1] == ')':
                pass
            else:
                if other.find(':'): # 包含源码信息而不是参数信息
                    method_line_number = other[other.find(':') + 1:other.find(')')]
                else:
                    args = other[other.find('(') + 1: other.find(')')]
                    for arg in args.split(','):
                        method_args.append(arg.strip())

            # transform
            response = transform_manager.transform(Request(cla_name))

            if response:
                trans_class = response.get_trans_class()
                if isinstance(trans_class, PGClass):
                    method = trans_class.find_method(method_name, method_line_number)
                    trans_method = trans_class.pretty_method(method)

                    if trans_method:
                        trans = origin_line.replace(info[info.find(' ') + 1:info.find('(')], trans_method)
                        print(trans)

            print('---------------------')


def pretty_print(clas, indent=0):
    if not clas:
        print('None')
        return

    print(' ' * indent + type(clas).__name__ + ':')
    indent += 4
    for k,v in clas.__dict__.items():
        if '__dict__' in dir(v):
            pretty_print(v, indent)
        else:
            print(' ' * indent + k + ': ' + str(v))


if __name__ == '__main__':
    stack_trace = StackTraceTransformer()
    with open('trace') as input_file:
        for line in input_file:
            stack_trace.parse_line(line)
