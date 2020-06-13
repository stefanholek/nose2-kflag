import unittest

class GeneratorsTestCase(unittest.TestCase):

    def test_gen_foo(self):
        yield lambda x: x, 'a'
        yield lambda x: x, 'b'

    def test_gen_bar(self):
        yield lambda x: x, 'a'
        yield lambda x: x, 'b'

    def test_gen_baz(self):
        yield lambda x: x, 'a'
        yield lambda x: x, 'b'

def test_func_foo():
    yield lambda x: x, 'a'
    yield lambda x: x, 'b'

def test_func_bar():
    yield lambda x: x, 'a'
    yield lambda x: x, 'b'

def test_func_baz():
    yield lambda x: x, 'a'
    yield lambda x: x, 'b'
