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
            scenario('generators'),
            '--plugin=nose2_kflag',
            '-h',
        )
        self.assertTestRunOutputMatches(proc, stdout='-K TEST_NAME_PATTERN')
        self.assertEqual(proc.poll(), 0)

    def test_find_generators(self):
        proc = self.runIn(
            scenario('generators'),
            '--plugin=nose2_kflag',
            '-v',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 12 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_foo:1')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_foo:2')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_bar:1')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_bar:2')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_baz:1')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_baz:2')
        self.assertTestRunOutputMatches(proc, stderr='test_func_foo:1')
        self.assertTestRunOutputMatches(proc, stderr='test_func_foo:2')
        self.assertTestRunOutputMatches(proc, stderr='test_func_bar:1')
        self.assertTestRunOutputMatches(proc, stderr='test_func_bar:2')
        self.assertTestRunOutputMatches(proc, stderr='test_func_baz:1')
        self.assertTestRunOutputMatches(proc, stderr='test_func_baz:2')
        self.assertEqual(proc.poll(), 0)

    def test_filter_generators(self):
        proc = self.runIn(
            scenario('generators'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 4 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_foo:1')
        self.assertTestRunOutputMatches(proc, stderr='test_gen_foo:2')
        self.assertTestRunOutputMatches(proc, stderr='test_func_foo:1')
        self.assertTestRunOutputMatches(proc, stderr='test_func_foo:2')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_test_module(self):
        proc = self.runIn(
            scenario('generators'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'test_generators',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 12 tests')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_full_name(self):
        proc = self.runIn(
            scenario('generators'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'test_generators.test_func_',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 6 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_func_foo:1')
        self.assertTestRunOutputMatches(proc, stderr='test_func_foo:2')
        self.assertTestRunOutputMatches(proc, stderr='test_func_bar:1')
        self.assertTestRunOutputMatches(proc, stderr='test_func_bar:2')
        self.assertTestRunOutputMatches(proc, stderr='test_func_baz:1')
        self.assertTestRunOutputMatches(proc, stderr='test_func_baz:2')
        self.assertEqual(proc.poll(), 0)

