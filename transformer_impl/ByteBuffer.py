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

    def get_remain(self):
        if self.has_remaining():
            return self.file_length - self.offset
        return None

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

    def read_raw_char(self):
        return self.read_byte(16)

    def read_char(self):
        return bytes.decode(self.read_raw_char())

    def read_raw_int(self):
        return self.read_byte(4)

    def read_int(self):
        return int.from_bytes(self.read_raw_int(), byteorder=self.order)

    def read_raw_long(self):
        return self.read_byte(8)

    def read_long(self):
        return int.from_bytes(self.read_raw_long(), byteorder=self.order)