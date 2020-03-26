#!/usr/bin/python3
# coding: utf-8


STRING_IN_UTF8 = b'\x01'

LOAD_CLASS = b'\x02'


UNLOAD_CLASS = b'\x03'

STACK_FRAME = b'\x04'

STACK_TRACE = b'\x05'


ALLOC_SITES = b'\x06'


HEAP_SUMMARY = b'\x07'


START_THREAD = b'\x0a'


END_THREAD = b'\x0b'

HEAP_DUMP = b'\x0c'

HEAP_DUMP_SEGMENT = b'\x1c'


HEAP_DUMP_END = b'\x2c'


CPU_SAMPLES = b'\x0d'


CONTROL_SETTINGS = b'\x0e'

ROOT_UNKNOWN = b'\xff'

ROOT_JNI_GLOBAL = b'\x01'

ROOT_JNI_LOCAL = b'\x02'

ROOT_JAVA_FRAME = b'\x03'

ROOT_NATIVE_STACK = b'\x04'

ROOT_STICKY_CLASS = b'\x05'

ROOT_THREAD_BLOCK = b'\x06'

ROOT_MONITOR_USED = b'\x07'

ROOT_THREAD_OBJECT = b'\x08'

CLASS_DUMP = b'\x20'

INSTANCE_DUMP = b'\x21'

OBJECT_ARRAY_DUMP = b'\x22'

PRIMITIVE_ARRAY_DUMP = b'\x23'

"""
/**
 * Android format addition
 *
 * Specifies information about which heap certain objects came from. When a sub-tag of this type
 * appears in a HPROF_HEAP_DUMP or HPROF_HEAP_DUMP_SEGMENT record, entries that follow it will
 * be associated with the specified heap.  The HEAP_DUMP_INFO data is reset at the end of the
 * HEAP_DUMP[_SEGMENT].  Multiple HEAP_DUMP_INFO entries may appear in a single
 * HEAP_DUMP[_SEGMENT].
 *
 * Format: u1: Tag value (0xFE) u4: heap ID ID: heap name string ID
 */
"""
HEAP_DUMP_INFO = b'\xfe'

ROOT_INTERNED_STRING = b'\x89'

ROOT_FINALIZING = b'\x8a'

ROOT_DEBUGGER = b'\x8b'

ROOT_REFERENCE_CLEANUP = b'\x8c'

ROOT_VM_INTERNAL = b'\x8d'

ROOT_JNI_MONITOR = b'\x8e'

ROOT_UNREACHABLE = b'\x90'

PRIMITIVE_ARRAY_NODATA = b'\xc3'
