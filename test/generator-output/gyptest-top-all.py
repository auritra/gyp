#!/usr/bin/env python

"""
Verifies building a project hierarchy created when the --generator-output=
option is used to put the build configuration files in a separate
directory tree.
"""

import sys

import TestGyp

test = TestGyp.TestGyp()

test.writable(test.workpath('src'), False)

test.run_gyp('prog1.gyp',
             '-Dset_symroot=1',
             '--generator-output=' + test.workpath('gypfiles'),
             chdir='src')

test.writable(test.workpath('src/build'), True)
test.writable(test.workpath('src/subdir2/build'), True)
test.writable(test.workpath('src/subdir3/build'), True)

test.build_all('prog1.gyp', chdir='gypfiles')

chdir = 'gypfiles'

expect = """\
Hello from %s
Hello from inc.h
Hello from inc1/include1.h
Hello from inc2/include2.h
Hello from inc3/include3.h
Hello from subdir2/deeper/deeper.h
"""

if sys.platform in ('darwin',):
  chdir = 'src'
test.run_built_executable('prog1', chdir=chdir, stdout=expect % 'prog1.c')

if sys.platform in ('darwin',):
  chdir = 'src/subdir2'
test.run_built_executable('prog2', chdir=chdir, stdout=expect % 'prog2.c')

if sys.platform in ('darwin',):
  chdir = 'src/subdir3'
test.run_built_executable('prog3', chdir=chdir, stdout=expect % 'prog3.c')

test.pass_test()