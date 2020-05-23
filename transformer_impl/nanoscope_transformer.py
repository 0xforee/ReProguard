#!/usr/bin/python3
# coding: utf-8

from transform.transformer import ITransformer
import re
from proguard_bean.pg_class import PGClass, PGMethod
import transform.transform_manager as transform_manager
from transform.transform_api import Request, Response


class NanoscopeTransformer(ITransformer):
    MAGIC_START = '<script type="text/plain" id="tracedata'
    MAGIC_END = '</script>'

    def __init__(self):
        self.data_enter = False
        self.data_section_pass = False
        pass

    def enter_data_section(self, line: str):
        # already parse data section
        if self.data_section_pass:
            return line
        # data start
        if self.data_enter:
            # data end
            if line.startswith(NanoscopeTransformer.MAGIC_END):
                self.data_enter = False
                self.data_section_pass = True
                return line
            else:
                if re.search(r'POP', line):
                    return line
                else:
                    # deal with proGuard string
                    valid_info = line[line.index(':') + 1:]
                    trans = self.transform_method(line, valid_info)
                    if trans:
                        return trans
                    return line

        else:
            if line.startswith(NanoscopeTransformer.MAGIC_START):
                self.data_enter = True
                # do parse
                # deal with proGuard string
                if line.find(':') != -1:
                    valid_info = line[line.index(':') + 1:]
                    trans = self.transform_method(line, valid_info)
                    if trans:
                        return trans
                return line
            else:
                return line

    def transform_method(self, origin_line: str, info: str):
        # split with space
        method_return_type = self.get_raw_type(info[:info.find(r' ')])

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
                trans_arg = self.get_raw_type(arg.strip())
                method_add_arg.append(trans_arg)

        # transform
        response = transform_manager.transform(Request(cla_name))

        if response:
            trans_class = response.get_trans_class()
            if isinstance(trans_class, PGClass):
                methods = trans_class.find_methods(method_name, method_add_arg, method_return_type)
                if methods and len(methods) > 0:
                    if len(methods) > 1:
                        print('found more than one method match, class: ' + cla_name + ", method: " + method_name + ", skip")
                        return origin_line
                    trans_method = trans_class.pretty_method(methods[0], True, True)
                    if trans_method:
                        trans = origin_line.replace(info[info.find(':') + 1:info.find(')') + 1], trans_method)
                        return trans

        return origin_line

    def start(self, config):
        with open(config.get_output_path(), 'w') as out:
            with open(config.get_input_path()) as input:
                for line in input:
                    trans = self.enter_data_section(line)
                    out.write(trans)


def pretty_print(clas, indent=0):

    print(' ' * indent +  type(clas).__name__ +  ':')
    indent += 4
    for k,v in clas.__dict__.items():
        if '__dict__' in dir(v):
            pretty_print(v,indent)
        else:
            print(' ' * indent +  k + ': ' + str(v))


if __name__ == '__main__':
    with open('output', 'w') as out:
        transformer = NanoscopeTransformer()
        magic_start = r'<script type="text/plain" id="tracedata">'
        with open('../test.html') as input_file:
            for line in input_file:
                if line.startswith(magic_start):
                    # deal with current line
                    line = line.replace(magic_start, '')
                    transformer.enter_data_section(line)
                    pass
                # start with numbers
                if re.search(r'^\d', line):
                    transformer.enter_data_section(line)
