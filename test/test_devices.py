import unittest

from devices.base_reader import *

def add_numbers(a, b):
    return a + b

class TestDevices(unittest.TestCase):
    def test_positive_numbers(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

    def test_negative_numbers(self):
        result = add_numbers(-1, -5)
        self.assertEqual(result, -6)

    def test_zero_and_positive(self):
        result = add_numbers(0, 7)
        self.assertEqual(result, 7)

if __name__ == '__main__':
    unittest.main()