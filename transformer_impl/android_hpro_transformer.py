#!/usr/bin/python3
# coding: utf-8

from transform.transformer import ITransformer
import re
from proguard_bean.pg_class import PGClass, PGMethod
import transform.transform_manager as transform_manager
from transform.transform_api import Request, Response

from transform.transformer import ITransformer


class AndroidHprofTransformer(ITransformer):
    def __init__(self):
        pass

    def start(self, file):
        pass