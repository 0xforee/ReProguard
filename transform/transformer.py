#!/usr/bin/python3
# coding: utf-8

from abc import ABCMeta


class ITransformer(metaclass=ABCMeta):
    @classmethod
    def start(cls, file_path):
        """
        转换器实现自己的转换方式
        :param file_path:
        :return:
        """
        pass
