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
            scenario('such'),
            '--plugin=nose2.plugins.layers',
            '--plugin=nose2_kflag',
            '-h',
        )
        self.assertTestRunOutputMatches(proc, stdout='--layer-report')
        self.assertTestRunOutputMatches(proc, stdout='-K TEST_NAME_PATTERN')
        self.assertEqual(proc.poll(), 0)

    def test_find_tests(self):
        proc = self.runIn(
            scenario('such'),
            '--plugin=nose2.plugins.layers',
            '--plugin=nose2_kflag',
            '-v',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='test 0000.*foo test')
        self.assertTestRunOutputMatches(proc, stderr='test 0001.*foo test')
        self.assertTestRunOutputMatches(proc, stderr='test 0000.*bar test')
        self.assertEqual(proc.poll(), 0)

    def test_filter_tests(self):
        proc = self.runIn(
            scenario('such'),
            '--plugin=nose2.plugins.layers',
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertTestRunOutputMatches(proc, stderr='test 0000.*foo test')
        self.assertTestRunOutputMatches(proc, stderr='test 0001.*foo test')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_test_module(self):
        proc = self.runIn(
            scenario('such'),
            '--plugin=nose2.plugins.layers',
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'test_such',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='test 0000.*foo test')
        self.assertTestRunOutputMatches(proc, stderr='test 0001.*foo test')
        self.assertTestRunOutputMatches(proc, stderr='test 0000.*bar test')
        self.assertEqual(proc.poll(), 0)

