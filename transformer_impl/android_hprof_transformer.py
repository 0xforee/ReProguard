#!/usr/bin/python3
# coding: utf-8
from transform.transformer import ITransformer
import time
from transformer_impl.ByteBuffer import ByteBuffer
from transformer_impl.HprofConstans import *
from transform.transformer import ITransformer
import re
from proguard_bean.pg_class import PGClass, PGMethod
import transform.transform_manager as transform_manager
from transform.transform_api import Request, Response


class AndroidHprofTransformer(ITransformer):
    def __init__(self):
        self.out_file = None
        self.TAG_PARSERS = {
            STRING_IN_UTF8: self.string_parse,
            LOAD_CLASS: self.class_table,
            STACK_FRAME: self.stack_frame,
            STACK_TRACE: self.stack_trace,
            HEAP_DUMP: self.heap_dump,
            HEAP_DUMP_SEGMENT: self.heap_dump_segment
        }

    def string_parse(self, tag, length, byte_buffer):
        try:
            id = byte_buffer.read_raw_int()
            if length > 4:
                content = byte_buffer.read_byte(length - 4)
                name = bytes.decode(content)
                if name.find(r'.') != -1:
                    # out.write(name + '\n')
                    trans = self.transform(name)
                    # print('before: ' + name + '\nafter: ' + trans)
                    new_length = 4 + len(trans)
                    new_len_byte = new_length.to_bytes(4, byteorder='big', signed=True)
                    self.out_file.write(new_len_byte)
                    self.out_file.write(id)
                    self.out_file.write(bytes(trans, encoding="utf8"))
                else:
                    # TODO: parse field (do not have method)
                    print('other: ' + name)
                    self.out_file.write(length.to_bytes(4, byteorder='big', signed=True))
                    self.out_file.write(id)
                    self.out_file.write(content)

            else:
                print('tag: %s, id: %s, length: %s' % (tag, id, length))

        except Exception as e:
            print('read error: ' + str(e))

    def transform(self, name):
        response = transform_manager.transform(Request(name))
        if response:
            trans_class = response.get_trans_class()
            if trans_class and trans_class.name:
                return trans_class.name

        return name

    def class_table(self, tag, length, byte_buffer):
        serial = byte_buffer.read_int()
        id = byte_buffer.read_int()
        stack_serial_num = byte_buffer.read_int()
        class_name_string_id = byte_buffer.read_int()
        print('readched class table')

    def stack_frame(self,tag, length, byte_buffer):
        print('readched stack_frame')

    def stack_trace(self,tag, length, byte_buffer):
        serial = byte_buffer.read_int()
        thread_serial = byte_buffer.read_int()
        num_frames = byte_buffer.read_int()
        print('readched stack_trace')

    def heap_dump(self,tag, length, byte_buffer):
        print('readched heap_dump')

    def heap_dump_segment(self,tag, length, byte_buffer):
        print('readched heap_dump_segment')

    def skip_fully(self, tag, length, byte_buffer):
        print('readched skip_fully')
        byte_buffer.skip_bytes(length)

    def __default_action(self):
        self.out_file.write()

    def start(self, config):
        with open(config.get_output_path(), 'wb') as out_file:
            self.out_file = out_file
            with open(config.get_input_path(), 'rb') as f:
                self.parse_hprof(f)

    def parse_hprof(self, input_file):
        byte_buffer = ByteBuffer(input_file, 'big')
        c = byte_buffer.read_byte()
        self.out_file.write(c)
        version = b''
        while c != b'\x00':
            version = version + c
            c = byte_buffer.read_byte()
            self.out_file.write(c)

        ver = bytes.decode(version)
        print(ver)

        length = byte_buffer.read_raw_int()
        self.out_file.write(length)
        print(int.from_bytes(length, byteorder='big'))

        time_stamp = byte_buffer.read_raw_long()
        time_trans = int.from_bytes(time_stamp, byteorder='big')
        time_trans = time.localtime(time_trans/1000)
        print(time_trans)
        self.out_file.write(time_stamp)

        try:
            while byte_buffer.has_remaining():
                tag = byte_buffer.read_byte()
                local_time_stamp = byte_buffer.read_raw_int()
                length = byte_buffer.read_raw_int()
                id_size = 4
                self.out_file.write(tag)
                self.out_file.write(local_time_stamp)

                if tag == STRING_IN_UTF8:
                    # write string
                    self.string_parse(tag, int.from_bytes(length, byteorder='big'), byte_buffer)
                # elif tag in self.TAG_PARSERS:
                #     self.TAG_PARSERS[tag](tag, int.from_bytes(length, byteorder='big'), byte_buffer)
                else:
                    self.out_file.write(length)
                    print('remain: ' + str(byte_buffer.get_remain()))
                    result = self.out_file.write(byte_buffer.read_byte(byte_buffer.get_remain()))
                    print('result: ' + str(result))
                    return
                    # self.skip_fully(tag, length, byte_buffer)

        except EOFError:
            print('file end')