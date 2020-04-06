#!/bin/python3
# coding:utf-8


class TransformerConfig:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def get_input_path(self):
        return self.input_path

    def get_output_path(self):
        return self.output_path