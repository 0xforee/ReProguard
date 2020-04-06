#!/usr/bin/python3
# coding: utf-8
from transform.transformer import ITransformer
import time
from transformer_impl.ByteBuffer import ByteBuffer
from transformer_impl.HprofConstans import *


def string_parse(tag, length, byte_buffer):
    try:
        id = byte_buffer.read_int()
        if length > 4:
            xx = byte_buffer.read_byte(length - 4)
            name = bytes.decode(xx)
            if name.find(r'.') != -1:
                # out.write(name + '\n')
                print(name)
        else:
            print('tag: %s, id: %s, length: %s' % (tag, id, length))

    except Exception as e:
        print('read error: ' + str(e))

def load_class(tag, length, byte_buffer):
    serial = byte_buffer.read_int()
    id = byte_buffer.read_int()
    print('readched class table')

def stack_frame(tag, length, byte_buffer):
    print('readched stack_frame')

def stack_trace(tag, length, byte_buffer):
    print('readched stack_trace')


def heap_dump(tag, length, byte_buffer):
    print('readched heap_dump')


def heap_dump_segment(tag, length, byte_buffer):
    print('readched heap_dump_segment')

def skip_fully(tag, length, byte_buffer):
    print('readched skip_fully')
    byte_buffer.skip_bytes(length)



TAG_PARSERS = {
    STRING_IN_UTF8: string_parse,
    LOAD_CLASS: load_class,
    STACK_FRAME: stack_frame,
    STACK_TRACE: stack_trace,
    HEAP_DUMP: heap_dump,
    HEAP_DUMP_SEGMENT: heap_dump_segment
}


class AndroidHprofTransformer(ITransformer):
    def __init__(self):
        pass

    def start(self, config):
        self.parse_hprof()

    def parse_hprof(self):
        with open('xxx', 'rb') as f:
            byte_buffer = ByteBuffer(f, 'big')
            c = byte_buffer.read_byte()
            version = b''
            while c != b'\x00':
                version = version + c
                c = byte_buffer.read_byte()

            ver = bytes.decode(version)
            print(ver)

            print(byte_buffer.read_int())

            time_stamp = byte_buffer.read_long()
            time_stamp = time.localtime(time_stamp/1000)
            print(time_stamp)

            try:
                while byte_buffer.has_remaining():
                    tag = byte_buffer.read_byte()
                    time_stam = byte_buffer.read_int()
                    length = byte_buffer.read_int()
                    id_size = 4

                    if tag in TAG_PARSERS:
                        TAG_PARSERS[tag](tag, length, byte_buffer)
                    else:
                        skip_fully(tag, length, byte_buffer)

            except EOFError:
                print('file end')