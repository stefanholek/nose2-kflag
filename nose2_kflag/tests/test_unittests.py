import os
import functools

from nose2.tests._common import FunctionalTestCase
from nose2.tests._common import NotReallyAProc

HERE = os.path.dirname(__file__)
scenario = functools.partial(os.path.join, HERE, 'scenario')


class TestNamePatternsTests(FunctionalTestCase):

    def runIn(self, testdir, *args, **kw):
        kw['cwd'] = testdir
        return NotReallyAProc(args, **kw)

    def test_list_plugins(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-h',
        )
        self.assertTestRunOutputMatches(proc, stdout='-K TEST_NAME_PATTERN')
        self.assertEqual(proc.poll(), 0)

    def test_find_unittests(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 6 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_baz')
        self.assertTestRunOutputMatches(proc, stderr='test_class_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_class_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_class_baz')
        self.assertEqual(proc.poll(), 0)

    def test_filter_positive_pattern(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_class_foo')
        self.assertEqual(proc.poll(), 0)

    def test_filter_positive_patterns(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo',
            '-K', 'bar',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 4 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_class_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_class_bar')
        self.assertEqual(proc.poll(), 0)

    def test_filter_negative_pattern(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', '!foo',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 4 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_baz')
        self.assertTestRunOutputMatches(proc, stderr='test_class_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_class_baz')
        self.assertEqual(proc.poll(), 0)

    def test_filter_negative_patterns(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', '!foo',
            '-K', '!bar',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_baz')
        self.assertTestRunOutputMatches(proc, stderr='test_class_baz')
        self.assertEqual(proc.poll(), 0)

    def test_filter_mixed_patterns(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo',
            '-K', 'bar',
            '-K', '!class',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_bar')
        self.assertEqual(proc.poll(), 0)

    def test_filter_identity(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo',
            '-K', '!foo',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 0 tests')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_test_module(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'test_unittests',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_baz')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_test_class(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'UnitTestCase',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_baz')
        self.assertEqual(proc.poll(), 0)

    def test_filter_by_full_name(self):
        proc = self.runIn(
            scenario('unittests'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'test_unittests.UnitTestCase.test_unit_',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 3 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_foo')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_bar')
        self.assertTestRunOutputMatches(proc, stderr='test_unit_baz')
        self.assertEqual(proc.poll(), 0)

    def test_find_parameterized_tests(self):
        proc = self.runIn(
            scenario('parameters'),
            '--plugin=nose2_kflag',
            '-v',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 6 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_param_foo:1')
        self.assertTestRunOutputMatches(proc, stderr='test_param_foo:2')
        self.assertTestRunOutputMatches(proc, stderr='test_param_bar:1')
        self.assertTestRunOutputMatches(proc, stderr='test_param_bar:2')
        self.assertTestRunOutputMatches(proc, stderr='test_param_baz:1')
        self.assertTestRunOutputMatches(proc, stderr='test_param_baz:2')
        self.assertEqual(proc.poll(), 0)

    def test_filter_parameterized_tests(self):
        proc = self.runIn(
            scenario('parameters'),
            '--plugin=nose2_kflag',
            '-v',
            '-K', 'foo',
        )
        self.assertTestRunOutputMatches(proc, stderr='Ran 2 tests')
        self.assertTestRunOutputMatches(proc, stderr='test_param_foo:1')
        self.assertTestRunOutputMatches(proc, stderr='test_param_foo:2')
        self.assertEqual(proc.poll(), 0)

