import unittest
from transformer_impl.stack_trace_transformer import StackTraceTransformer
from transformer_impl.nanoscope_transformer import NanoscopeTransformer
import config
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(False, False)

    def test_stack_trace(self):
        config.MAPPING_FILE = os.path.abspath('mapping1.txt')
        trans = NanoscopeTransformer()
        with open('nano_test1_after.html') as result:
            with open('nano_test1.html') as f:
                for line in f:
                    trans_line = trans.enter_data_section(line)
                    self.assertEqual(trans_line, result.readline())
        

if __name__ == '__main__':
    unittest.main()
