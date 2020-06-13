import unittest

from nose2.tools import params

class ParameterizedTestCase(unittest.TestCase):

    @params('a', 'b')
    def test_param_foo(self, param):
        pass

    @params('a', 'b')
    def test_param_bar(self, param):
        pass

    @params('a', 'b')
    def test_param_baz(self, param):
        pass
