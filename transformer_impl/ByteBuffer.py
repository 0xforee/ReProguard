#!/usr/bin/python3
# coding: utf-8


class ByteBuffer:
    def __init__(self, file, order):
        self.offset = 0
        self.file = file
        self.order = order
        self.file.seek(0, 2)
        self.file_length = self.file.tell()
        self.file.seek(0, 0)

    def has_remaining(self):
        return self.offset < self.file_length

    def skip_bytes(self, size=1):
        self.offset += size
        self.file.seek(self.offset)

    def read_byte(self, size=1):
        result = self.file.read(size)
        self.offset += size
        self.file.seek(self.offset)
        return result

    def read_char(self):
        result = self.read_byte(16)
        return bytes.decode(result)

    def read_int(self):
        result = self.read_byte(4)
        return int.from_bytes(result, byteorder=self.order)

    def read_long(self):
        result = self.read_byte(8)
        return int.from_bytes(result, byteorder=self.order)