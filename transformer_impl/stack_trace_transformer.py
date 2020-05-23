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

    def start(self, config):
        with open(config.get_output_path(), 'w') as output:
            with open(config.get_input_path()) as input_file:
                for line in input_file:
                    trans_line = self.parse_line(line)
                    output.write(trans_line)

    def parse_line(self, line):
        print("trans..." + line)
        obj = re.search(r'[ $0-9a-zA-Z.:]+\([$0-9a-zA-Z.:]*\)+', line)
        if not obj:
            return line

        matched_trace_info = obj.group()
        trans = self.transform_method(line, matched_trace_info.strip())
        if trans:
            line = line.replace(matched_trace_info, trans)

        return line

    def transform_with_line(self, info: str):
        other = info[info.find(r' ') + 1:]
        full_method_name = other[:other.find('(')]

        cla_name = full_method_name[:full_method_name.rfind('.')]
        method_name = full_method_name[full_method_name.rfind('.') + 1:]
        method_line_number = other[other.find(':') + 1: other.find(')')]

        # transform
        response = transform_manager.transform(Request(cla_name))

        if not response:
            return None

        trans_class = response.get_trans_class()

        if not isinstance(trans_class, PGClass):
            return None
        methods = trans_class.find_methods_by_line(method_name, method_line_number)
        if methods:
            # TODO: 适配多个方法满足的情况
            if len(methods) > 1:
                print('warning: found multi method matched, take first one ' + str(methods))
            trans_method = methods[0]

            if trans_method:
                trans_method_str = trans_class.pretty_method(trans_method)

                # get real line number
                if trans_method.real_source_scope:
                    old_source = trans_method.source_scope[0]
                    old_line_start = old_source[:old_source.find(':')]
                    offset = int(method_line_number) - int(old_line_start)
                    new_source = trans_method.real_source_scope[0]
                    new_line_start = new_source[:new_source.find(':')]
                    new_line = int(new_line_start) + offset
                    info = info.replace(method_line_number, str(new_line))

                trans = info.replace(info[info.find(' ') + 1:info.find('(')], trans_method_str)
                return trans

        return None

    def transform_with_args(self, info: str):
        other = info[info.find(r' ') + 1:]
        full_method_name = other[:other.find('(')]
        method_args = []
        cla_name = full_method_name[:full_method_name.rfind('.')]
        method_name = full_method_name[full_method_name.rfind('.') + 1:]

        # args or sourceFile not exits
        if other[other.find('(') + 1] == ')':
            pass
        else:
            args = other[other.find('(') + 1: other.find(')')]
            for arg in args.split(','):
                arg_response = transform_manager.transform(Request(arg.strip()))
                if not arg_response:
                    method_args.append(arg.strip())
                else:
                    trans_arg = arg_response.get_trans_class()
                    method_args.append(trans_arg.name)
        # transform
        response = transform_manager.transform(Request(cla_name))

        if not response:
            return None

        trans_class = response.get_trans_class()

        if not isinstance(trans_class, PGClass):
            return None

        methods = trans_class.find_methods(method_name, method_args)
        if methods:
            # TODO: 适配多个方法满足的情况
            if len(methods) > 1:
                print('warning: found multi method matched, take first one ' + str(methods))
            trans_method = methods[0]

            if trans_method:
                trans_method_str = trans_class.pretty_method(trans_method, need_args=True)
                trans = info.replace(info[info.find(' ') + 1:info.find('(') + 1], trans_method_str)
                return trans

        return None

    def transform_method(self, info: str):
        print('info : ' + info)

        # found line number
        if info.find(':') != -1:
            return self.transform_with_line(info)
        else:
            return self.transform_with_args(info)


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
