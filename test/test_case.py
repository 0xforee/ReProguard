import unittest
from transformer_impl.stack_trace_transformer import StackTraceTransformer
from transformer_impl.nanoscope_transformer import NanoscopeTransformer
from transform import transform_manager
import config
import os


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        transform_manager.ENGINE = None

    def test_nanoscope(self):
        print('test nanoscope')
        config.MAPPING_FILE = os.path.abspath('A_mapping.txt')
        trans = NanoscopeTransformer()
        with open('A_nano_test1_after.html') as result:
            with open('A_nano_test.html') as f:
                for line in f:
                    trans_line = trans.enter_data_section(line)
                    self.assertEqual(trans_line, result.readline())

    def test_stack_trace(self):
        print('test stack trace')
        config.MAPPING_FILE = os.path.abspath('B_mapping.txt')
        trans = StackTraceTransformer()
        with open('B_trace_after.txt') as result:
            with open('B_trace.txt') as f:
                for line in f:
                    trans_line = trans.parse_line(line)
                    self.assertEqual(trans_line, result.readline())
        pass


if __name__ == '__main__':
    unittest.main()
