#!/usr/bin/python3
# coding: utf-8

from abc import ABCMeta


class ITransformer(metaclass=ABCMeta):
    @classmethod
    def start(cls, file):
        """
        转换器实现自己的转换方式
        :param file:
        :return:
        """
        pass
