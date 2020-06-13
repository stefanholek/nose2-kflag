import os
import functools

from nose2.tests._common import FunctionalTestCase
from nose2.tests._common import NotReallyAProc

HERE = os.path.dirname(__file__)
scenario = functools.partial(os.path.join, HERE, 'scenario')


class TestNamePatternsFunctionTests(FunctionalTestCase):

    def runIn(self, testdir, *args, **kw):
        kw['cwd'] = testdir
        return NotReallyAProc(args, **kw)

    def test_list_plugins(self):
        proc = self.runIn(
            scenario('loadtests'),
            '--plugin=nose2_kflag',
            '-h',
        )
        self.assertTestRunOutputMatches(proc, stdout='-K TEST_NAME_PATTERN')
        self.assertEqual(proc.poll(), 0)

    def test_find_loaded_tests(self):
        proc = self.runIn(
            scenario('loadtests'),
            '--plugin=nose2_kflag',
            '-v',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='foo_func')
        self.assertTestRunOutputMatches(proc, stderr='bar_func')
        self.assertTestRunOutputMatches(proc, stderr='baz_func')
        self.assertEqual(proc.poll(), 0)

    def test_filter_loaded_tests(self):
        proc = self.runIn(
            scenario('loadtests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo'
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='foo_func')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_test_module(self):
        proc = self.runIn(
            scenario('loadtests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'test_loadtests'
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='foo_func')
        self.assertTestRunOutputMatches(proc, stderr='bar_func')
        self.assertTestRunOutputMatches(proc, stderr='baz_func')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_full_name(self):
        proc = self.runIn(
            scenario('loadtests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'test_loadtests.bar_func'
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 1 test')
        self.assertTestRunOutputMatches(proc, stderr='bar_func')
        self.assertEqual(proc.poll(), 0)

