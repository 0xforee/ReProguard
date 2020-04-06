#!/usr/bin/python3
# coding: utf-8

from abc import ABCMeta
from transform.transformer_config import TransformerConfig
import transform.transform_manager as transform_manager
from transform.transform_api import Request, Response


class ITransformer(metaclass=ABCMeta):
    @classmethod
    def start(cls, config: TransformerConfig):
        """
        转换器实现自己的转换方式
        :param config: transform 需要的一些参数
        :return:
        """
        pass

    def get_raw_type(self, proguard_type: str):
        response = transform_manager.transform(Request(proguard_type))
        if response:
            trans_class = response.get_trans_class()
            if trans_class:
                return trans_class.name

        return proguard_type



