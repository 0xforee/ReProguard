#!/usr/bin/python3
# coding: utf-8

from transform.transformer import ITransformer
import re
from proguard_bean.pg_class import PGClass, PGMethod
import transform.transform_manager as transform_manager
from transform.transform_api import Request, Response


class NanoScopeTransformer(ITransformer):
    def __init__(self):
        pass

    def start(self, file_path):
        pass


class Transform:
    def transform_method(info):
        if isinstance(info, str):
            # split with space
            method_return_type = info[:info.find(r' ')]
            other = info[info.find(r' ') + 1:]
            # split with (
            pre = other[:other.find('(')]

            method_add_arg = []

            # split with .
            cla_name = pre[:pre.rfind('.')]
            method_name = pre[pre.rfind('.') + 1:]

            # args exits
            if other[other.find('(') + 1] == ')':
                pass
            else:
                args = other[other.find('(') + 1: other.find(')')]
                for arg in args.split(','):
                    method_add_arg.append(arg.strip())

            # transform

            response = transform_manager.transform(Request(cla_name))
            if response and response.trans_class and response.trans_class.name:
                out.write('before: ' + method_name + '\n')
                out.write('after: ' + response.trans_class.name + '\n')
            pretty_print(response)

            # if response:
            #     trans_class = response.get_trans_class()
            #     if isinstance(trans_class, PGClass):
            #         method = trans_class.find_method(method_name, method_line_number)
            #         trans_method = trans_class.pretty_method(method)
            #
            #         if trans_method:
            #             trans = origin_line.replace(info[info.find(' ') + 1:info.find('(')], trans_method)
            #             print(trans)
        # print('before: %s, after: %s' % (info, response) )
        print('------------------------')



def pretty_print(clas, indent=0):

    print(' ' * indent +  type(clas).__name__ +  ':')
    indent += 4
    for k,v in clas.__dict__.items():
        if '__dict__' in dir(v):
            pretty_print(v,indent)
        else:
            print(' ' * indent +  k + ': ' + str(v))


def parse_line(line):
    if re.search(r'POP', line):
        return

    # deal with proGuard string
    valid_info = line[line.index(':')+1:]
    Transform.transform_method(valid_info)


if __name__ == '__main__':
    with open('output', 'w') as out:

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
