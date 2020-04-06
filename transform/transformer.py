#!/usr/bin/python3
# coding: utf-8

from abc import ABCMeta
from transform.transformer_config import TransformerConfig


class ITransformer(metaclass=ABCMeta):
    @classmethod
    def start(cls, config: TransformerConfig):
        """
        转换器实现自己的转换方式
        :param config: transform 需要的一些参数
        :return:
        """
        pass
