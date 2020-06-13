import doctest

def foo_func():
    """
    >>> print('foo')
    foo
    """

def bar_func():
    """
    >>> print('bar')
    bar
    """

def baz_func():
    """
    >>> print('baz')
    baz
    """

def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite(__name__))
    return tests
