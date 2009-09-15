#!/usr/bin/env python

"""
Verifies that a project hierarchy created with the --generator-output=
option can be built even when it's relocated to a different path.
"""

import sys

import TestGyp

test = TestGyp.TestGyp()

test.writable(test.workpath('src'), False)

test.run_gyp('prog1.gyp',
             '-Dset_symroot=1',
             '--generator-output=' + test.workpath('gypfiles'),
             chdir='src')

test.writable(test.workpath('src'), True)

test.relocate('src', 'relocate/src')
test.relocate('gypfiles', 'relocate/gypfiles')

test.writable(test.workpath('relocate/src'), False)

test.writable(test.workpath('relocate/src/build'), True)
test.writable(test.workpath('relocate/src/subdir2/build'), True)
test.writable(test.workpath('relocate/src/subdir3/build'), True)

test.build_all('prog1.gyp', chdir='relocate/gypfiles')

chdir = 'relocate/gypfiles'

expect = """\
Hello from %s
Hello from inc.h
Hello from inc1/include1.h
Hello from inc2/include2.h
Hello from inc3/include3.h
Hello from subdir2/deeper/deeper.h
"""

if sys.platform in ('darwin',):
  chdir = 'relocate/src'
test.run_built_executable('prog1', chdir=chdir, stdout=expect % 'prog1.c')

if sys.platform in ('darwin',):
  chdir = 'relocate/src/subdir2'
test.run_built_executable('prog2', chdir=chdir, stdout=expect % 'prog2.c')

if sys.platform in ('darwin',):
  chdir = 'relocate/src/subdir3'
test.run_built_executable('prog3', chdir=chdir, stdout=expect % 'prog3.c')

test.pass_test()