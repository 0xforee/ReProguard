#!/usr/bin/python3
# coding: utf-8

import re
import argparse


def trans_mod_name(mod_name):
    """
    translate abc_def to AbcDef
    :param mod_name: match abc_def pattern
    :return:
    """
    after = ''
    if isinstance(mod_name, str):
        names = mod_name.split('_')
        for name in names:
            a = name[0].upper() + name[1:len(name)]
            after += a

    return after


if __name__ == '__main__':
    parse = argparse.ArgumentParser('ReProguard file from mapping')

    # -h 帮助
    # -s strategy，策略（nanoscope,systrace,stackTrace,androidHprof,Hprof)
    # -i interactive 交互模式（只适用于 stackTrace)
    # -m mapping 文件
    # -f input_file 要转译的文件
    # -o output 输出

    parse.add_argument('-s', '--strategy', choices=['nanoscope', 'systrace', 'stack_trace', 'android_hprof', 'hprof']
                       , help='which strategy? recognize by parser default')
    parse.add_argument('-i', '--interactive', help='interactive mode, only support stackTrace')
    parse.add_argument('-m', '--mapping_file', help='mapping file', required=True)
    parse.add_argument('-f', '--input_file', help='transform from which file', required=True)
    parse.add_argument('-o', '--output', help='output file, default is current dir')

    args = parse.parse_args()

    import importlib
    ip_module_name = args.strategy + '_transformer'
    ip_class_name = trans_mod_name(ip_module_name)
    ip_module = importlib.import_module('transformer_impl.' + ip_module_name)
    parse_class = getattr(ip_module, ip_class_name)

    parse_object = parse_class()

    parse_object.start(args.input_file, args.output)








