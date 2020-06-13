import os
import functools

from nose2.tests._common import FunctionalTestCase
from nose2.tests._common import NotReallyAProc

HERE = os.path.dirname(__file__)
scenario = functools.partial(os.path.join, HERE, 'scenario')


class TestNamePatternsDocTests(FunctionalTestCase):

    def runIn(self, testdir, *args, **kw):
        kw['cwd'] = testdir
        return NotReallyAProc(args, **kw)

    def test_list_plugins(self):
        proc = self.runIn(
            scenario('doctests'),
            '--plugin=nose2.plugins.doctests',
            '--plugin=nose2_kflag',
            '-h',
        )
        self.assertTestRunOutputMatches(proc, stdout='--with-doctest')
        self.assertTestRunOutputMatches(proc, stdout='-K TEST_NAME_PATTERN')
        self.assertEqual(proc.poll(), 0)

    def test_find_doctests(self):
        proc = self.runIn(
            scenario('doctests'),
            '--plugin=nose2.plugins.doctests',
            '--plugin=nose2_kflag',
            '-v',
            '--with-doctest',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 7 tests')
        self.assertTestRunOutputMatches(proc, stderr='pymodule \.\.\. ok')
        self.assertTestRunOutputMatches(proc, stderr='pymodule.func_foo')
        self.assertTestRunOutputMatches(proc, stderr='pymodule.func_bar')
        self.assertTestRunOutputMatches(proc, stderr='pymodule.func_baz')
        self.assertTestRunOutputMatches(proc, stderr='tests.test_foo.txt')
        self.assertTestRunOutputMatches(proc, stderr='tests.test_bar.txt')
        self.assertTestRunOutputMatches(proc, stderr='tests.test_baz.txt')
        self.assertEqual(proc.poll(), 0)

    def test_filter_doctests(self):
        proc = self.runIn(
            scenario('doctests'),
            '--plugin=nose2.plugins.doctests',
            '--plugin=nose2_kflag',
            '-v',
            '--with-doctest',
            '-K', 'foo',
            '-K', '.txt',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 4 tests')
        self.assertTestRunOutputMatches(proc, stderr='func_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_foo.txt')
        self.assertTestRunOutputMatches(proc, stderr='test_bar.txt')
        self.assertTestRunOutputMatches(proc, stderr='test_baz.txt')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_test_module(self):
        proc = self.runIn(
            scenario('doctests'),
            '--plugin=nose2.plugins.doctests',
            '--plugin=nose2_kflag',
            '-v',
            '--with-doctest',
            '-K', 'pymodule',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 4 tests')
        self.assertTestRunOutputMatches(proc, stderr='pymodule \.\.\. ok')
        self.assertTestRunOutputMatches(proc, stderr='func_foo')
        self.assertTestRunOutputMatches(proc, stderr='func_bar')
        self.assertTestRunOutputMatches(proc, stderr='func_baz')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_test_path(self):
        proc = self.runIn(
            scenario('doctests'),
            '--plugin=nose2.plugins.doctests',
            '--plugin=nose2_kflag',
            '-v',
            '--with-doctest',
            '-K', 'tests',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_foo.txt')
        self.assertTestRunOutputMatches(proc, stderr='test_bar.txt')
        self.assertTestRunOutputMatches(proc, stderr='test_baz.txt')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_full_name(self):
        proc = self.runIn(
            scenario('doctests'),
            '--plugin=nose2.plugins.doctests',
            '--plugin=nose2_kflag',
            '-v',
            '--with-doctest',
            '-K', 'tests.test_',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_foo.txt')
        self.assertTestRunOutputMatches(proc, stderr='test_bar.txt')
        self.assertTestRunOutputMatches(proc, stderr='test_baz.txt')
        self.assertEqual(proc.poll(), 0)

