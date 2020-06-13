from nose2.tools import params
from nose2.tools.decorators import with_setup

def test_func_foo():
    pass

def test_func_bar():
    pass

@params('a', 'b')
def test_func_baz(param):
    pass

def _setup():
    pass

@with_setup(_setup)
def test_func_peng():
    pass
