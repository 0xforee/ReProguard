#!/usr/bin/python
# coding: utf-8

import re

from proguard_bean.pg_class import PGClass, PGMethod, PGField

import config


class MappingLoader:

    def __init__(self):
        self.load_all = False
        self.cache = {}
        self.mapping_file = open(config.MAPPING_FILE)
        self.load_all_class()

    def __del__(self):
        if not self.mapping_file.closed:
            self.mapping_file.close()

    def find_class(self, proguard_cla_name):
        """
        从 map 中查找指定的class
        :return:
        """
        if proguard_cla_name in self.cache:
            return self.cache[proguard_cla_name]

        if self.load_all:
            return None

        cla = self.__load_class(proguard_cla_name)
        if cla:
            self.cache[proguard_cla_name] = cla

        return cla

    def load_all_class(self):
        """
        加载所有的类
        :return:
        """
        cla = None
        for line in self.mapping_file:
            if line.startswith(' '):
                self.__parse_other(line, cla)
            else:
                cla = self.__parse_class(line)

        self.load_all = True

    def __parse_other(self, line, cla):
        if not cla:
            return
        if line.find('(') != -1:
            result = MappingLoader.build_method(line)
            cla.add_method(result[0], result[1])
        else:
            # read field
            result = MappingLoader.build_field(line)
            cla.add_field(result[0], result[1])

    def __parse_class(self, line):
        cla = None
        cla_list = line.split('->')
        if len(cla_list) > 1:
            origin_cla = cla_list[0].strip()
            proguard_cla = cla_list[1].strip().strip(':')
            # load class
            cla = PGClass()
            cla.name = origin_cla
            self.cache[proguard_cla] = cla

        return cla

    def __load_class(self, proguard_cla_name):
        """
        加载 class，将 mapping 的类块，变为 Class
        :param proguard_cla_name:
        :return:
        """
        cla = None
        find_class = False
        for line in self.mapping_file:
            if not find_class:
                # find class
                if line.startswith(' '):
                    continue
                cla_list = line.split('->')
                if len(cla_list) > 1:
                    origin_cla = cla_list[0].strip()
                    proguard_cla = cla_list[1].strip().strip(':')
                    if proguard_cla_name == proguard_cla:
                        find_class = True
                        # load class
                        cla = PGClass()
                        cla.name = origin_cla
                        self.cache[proguard_cla] = cla
            else:
                # find field and method
                if not line.startswith(' '):
                    # class block finish, break
                    break

                # read method
                if line.find('(') != -1:
                    result = MappingLoader.build_method(line)
                    cla.add_method(result[0], result[1])
                else:
                    # read field
                    result = MappingLoader.build_field(line)
                    cla.add_field(result[0], result[1])

        self.mapping_file.seek(0, 0)
        return cla

    @staticmethod
    def build_method(info):
        if isinstance(info, str):
            result = info.split('->')
            method = result[0].strip()
            proguard_method_name = result[1].strip()
            md = PGMethod()
            md.return_type = method[:method.find(' ')]
            # 可能前边有行号
            if re.match(r'^\d', md.return_type):
                md.source_scope = md.return_type[:md.return_type.rfind(':')]
                md.return_type = md.return_type[md.return_type.rfind(':') + 1:]

            md.name = method[method.find(' ') + 1: method.find('(')]
            # parse arg
            md_args = method[method.find('(') + 1: method.find(')')]
            if len(md_args) > 0:
                md.args = md_args.split(',')

            return proguard_method_name, md

        return None

    @staticmethod
    def build_field(info):
        if isinstance(info, str):
            result = info.split('->')
            field = result[0].strip()
            proguard_name = result[1].strip()
            fd = PGField()
            fd.type = field[:field.find(' ')]
            fd.name = field[field.find(' ') + 1:]
            return proguard_name, fd

        return None


if __name__ == '__main__':
    maping = MappingLoader()
    # test_class = maping.find_class('androidx.core.app.Person')
    # print(test_class)
    maping.load_all_class()
    print('hahaha')

