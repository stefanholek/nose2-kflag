===========
nose2-kflag
===========
------------------------------------------------------------------
Only run tests which match a given substring
------------------------------------------------------------------

Overview
========

This package provides a nose2 plugin implementing the -k flag known from
unittest discover. The plugin allows to select tests by specifying on or more
substring patterns.

Patterns
========

Matching is performed against the full dotted name of each test. If a pattern
is prefixed with '!' its meaning is inverted, and only tests not matching
the pattern will be selected. Multiple -K flags (plugin rules mandate
uppercase) may be given. A test is selected if *any* of the given
positive patterns and *all* of the given negative patterns apply.
Patterns are case sensitive.

Examples
========

Run one test::

    nose2 -K test_foo

Run one test of a specific test class::

    nose2 -K FooTestCase.test_bar

Run all tests of a test class::

    nose2 -K FooTestCase

Run all foo and bar tests except those in the functional directory::

    nose2 -K foo -K bar -K '!functional'

Installation
============
::

    pip install nose2-kflag

Then add the plugin to your nose2.cfg::

    [unittest]
    plugins = nose2_kflag

