"""
Only run tests which match a given substring.

This plugin implements :func:`getTestCaseNames` and :func:`startTestRun` to
exclude non-matching tests from execution.

Matching occurs against the full dotted name of each test. If a pattern is
prefixed with ``!`` its meaning is inverted, and only tests *not* matching
the pattern will be selected. Multiple -K flags may be specified. A test is
selected if *any* of the given positive patterns and *all* of the given
negative patterns apply. Patterns are case sensitive.

Supports all types of nose2 tests:

    - TestCase (loader.testcases)
    - MethodTestCase (loader.testclasses)
    - DocTestCase (loader.doctests)
    - DocFileCase (loader.doctests)
    - FunctionTestCase (loader.functions)
    - Parameterized tests (loader.parameters)
    - Test generators (loader.generators)

Installation
------------
::

    [unittest]
    plugins = nose2_kflag

Debugging
---------

Set ``--log-level=DEBUG`` to see which tests get in- or excluded.

"""
import os
import sys
import logging
import unittest
import doctest

from fnmatch import fnmatchcase
from itertools import chain

from nose2 import events

log = logging.getLogger(__name__)


if sys.version_info >= (3, 3):
    def strclass(cls):
        return '%s.%s' % (cls.__module__, cls.__qualname__)
else:
    def strclass(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)


def testname(name):
    return name.split('\n', 1)[0]


class TestNamePatterns(events.Plugin):

    configSection = 'nose2-kflag'

    def __init__(self):
        super(TestNamePatterns, self).__init__()

        self.testNamePatterns = []
        self.positivePatterns = []
        self.negativePatterns = []

        self.testNamePatternsFromConfig = self.config.as_list('patterns', [])
        self.skipPhase1 = self.config.as_bool('skip-phase-1', False)
        self.skipPhase2 = self.config.as_bool('skip-phase-2', False)

        self.addArgument(self.testNamePatterns.extend, 'K', 'test-name-pattern',
            'Only run tests which match the given substring (multi-allowed)')

    def handleArgs(self, event):
        self.testNamePatterns = self.testNamePatterns or self.testNamePatternsFromConfig
        self.testNamePatterns = list(map(self._convertPattern, self.testNamePatterns))
        log.debug('Positive patterns: %s' % self.positivePatterns)
        log.debug('Negative patterns: %s' % self.negativePatterns)

        if self.testNamePatterns:
            self.register()

    def getTestCaseNames(self, event):
        # Phase 1: Exclude test case methods
        if self.skipPhase1:
            return

        def shouldExcludeMethod(attrname, clsname=strclass(event.testCase)):
            return not self._matchPatterns('%s.%s' % (clsname, attrname))

        names = map(testname, filter(event.isTestMethod, dir(event.testCase)))
        event.excludedNames.extend(filter(shouldExcludeMethod, names))

    def startTestRun(self, event):
        # Phase 2: Exclude doctests, test functions, and test generators
        if self.skipPhase2:
            return

        self._removeNonMatching(event.suite)

    def _removeNonMatching(self, suite):
        for test in list(suite):
            if isinstance(test, unittest.TestCase):
                if not self._matchPatterns(self._nameFromTest(test)):
                    suite._tests.remove(test)
            elif isinstance(test, unittest.TestSuite):
                self._removeNonMatching(test)

    def _nameFromTest(self, test):
        if isinstance(test, doctest.DocFileCase):
            return self._nameFromPath(test._dt_test.filename)
        if isinstance(test, unittest.FunctionTestCase):
            if not hasattr(test, '_funcName'):
                return testname(strclass(test._testFunc))
        return testname(test.id())

    def _nameFromPath(self, path):
        return self._stripPrefix(path).replace(os.sep, '.').replace('/', '.')

    def _stripPrefix(self, path):
        # top-level-directory and code-directories are on the sys.path
        for prefix in sorted(sys.path, key=len, reverse=True):
            if path.startswith(prefix):
                return path[len(prefix)+1:]
        return os.path.basename(path)

    def _matchPatterns(self, fullname, strbool=('[-]', '[+]')):
        match = len(self.positivePatterns) == 0
        match = any(chain(self._matchPositivePatterns(fullname), (match,)))
        match = all(chain(self._matchNegativePatterns(fullname), (match,)))
        log.debug('%s %s', strbool[match], fullname)
        return match

    def _matchPositivePatterns(self, fullname):
        return (fnmatchcase(fullname, pattern) for pattern in self.positivePatterns)

    def _matchNegativePatterns(self, fullname):
        return (not fnmatchcase(fullname, pattern) for pattern in self.negativePatterns)

    def _convertPattern(self, pattern):
        positive = True
        pattern = pattern.strip()
        if pattern.startswith('!'):
            pattern, positive = pattern[1:], False
        if not pattern.startswith('*'):
            pattern = '*' + pattern
        if not pattern.endswith('*'):
            pattern += '*'
        if positive:
            self.positivePatterns.append(pattern)
        else:
            self.negativePatterns.append(pattern)

    def getTestMethodNames(self, event):
        return self.getTestCaseNames(event)

    def registerInSubprocess(self, event):
        event.pluginClasses.append(self.__class__)

