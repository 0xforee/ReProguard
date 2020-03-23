#!/usr/bin/python
# coding: utf-8

import re

class ProGuardClass:
    name = ''
    proguard_name = ''
    methods = {}
    fields = {}

    def add_method(self, proguard_name, method):
        # 可能会出现多个方法混淆之后的名称是相同的情况
        if proguard_name in self.methods:
            origin_method = self.methods[proguard_name]
            if isinstance(origin_method, list):
                origin_method.append(method)
            else:
                merge_method = [origin_method, method]
                self.methods[proguard_name] = merge_method
        else:
            self.methods[proguard_name] = method

    def add_field(self, proguard_name, field):
        self.fields[proguard_name] = field

    def __str__(self):
        return 'ProGuardClass: ' + str(self.__dict__) + '\n' + str(self.methods) + '\n' + str(self.fields)


class ProGuardField:
    name = ''
    type = ''

    def __str__(self):
        return "ProguardField: " + str(self.__dict__)


class ProGuardMethod:
    name = ''
    proguard_name = ''
    return_type = ''
    args = []

    def get_return_type(self):
        return self.return_type

    def set_return_type(self, return_type):
        self.return_type = return_type

    def add_arg(self, arg):
        self.args.append(arg)

    def __str__(self) -> str:
        return 'ProGuardMethod: ' + str(self.__dict__)


class Args:
    type = ''


class MappingLoader:
    cache = {}

    def main(self):
        """
        load map file
        :return:
        """
        num = 0
        with open('mapping.txt') as f:
            for line in f:
                if line.startswith(' '):
                    continue
                num = num + 1
                print(line)
        print(num)

    def find_class(self, proguard_cla_name):
        """
        从 map 中查找指定的class
        :return:
        """
        if proguard_cla_name in self.cache:
            return self.cache[proguard_cla_name]

        cla = self.load_class(proguard_cla_name)
        if cla:
            self.cache[proguard_cla_name] = cla

        return cla

    def load_class(self, proguard_cla_name):
        """
        加载 class，将 mapping 的类块，变为 Class
        :param proguard_cla_name:
        :return:
        """
        cla = None
        with open('mapping.txt') as f:
            find_class = False
            for line in f:
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
                            cla = ProGuardClass()
                            cla.name = origin_cla
                            self.cache[proguard_cla] = cla
                else:
                    # find field and method
                    if not line.startswith(' '):
                        # class block finish, break
                        break

                    # read method
                    if line.find('(') != -1:
                        result = build_method(line)
                        cla.add_method(result[0], result[1])
                    else:
                        # read field
                        result = build_field(line)
                        cla.add_field(result[0], result[1])

        return cla


def build_method(info):
    if isinstance(info, str):
        result = info.split('->')
        method = result[0].strip()
        proguard_method = result[1].strip()
        md = ProGuardMethod()
        md.return_type = method[:method.find(' ')]
        # 可能前边有行号
        if re.match(r'^\d', md.return_type):
            md.return_type = md.return_type[md.return_type.rfind(':') + 1:]

        md.name = method[method.find(' ') + 1: method.find('(')]
        # parse arg
        md_args = method[method.find('(') + 1: method.find(')')]
        if len(md_args) > 0:
            md.args = md_args.split(',')

        return proguard_method, md

    return None


def build_field(info):
    if isinstance(info, str):
        result = info.split('->')
        field = result[0].strip()
        proguard_name = result[1].strip()
        fd = ProGuardField()
        fd.type = field[:field.find(' ')]
        fd.name = field[field.find(' ') + 1:]
        return proguard_name, fd

    return None


if __name__ == '__main__':
    maping = MappingLoader()
    cla = maping.load_class('f.O00000o0.O000000o')
    print(cla)

