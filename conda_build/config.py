'''
Module to store conda build settings.
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import sys
from os.path import abspath, expanduser, join

import conda.config as cc

CONDA_PERL = os.getenv('CONDA_PERL', '5.18.2')
CONDA_PY = int(os.getenv('CONDA_PY', cc.default_python.replace('.', '')))
CONDA_NPY = int(os.getenv('CONDA_NPY', 18))
PY3K = int(bool(CONDA_PY >= 30))

_bld_root_env = os.getenv('CONDA_BLD_PATH')
_bld_root_rc = cc.rc.get('conda-build', {}).get('root-dir')
if _bld_root_env:
    croot = abspath(expanduser(_bld_root_env))
elif _bld_root_rc:
    croot = abspath(expanduser(_bld_root_rc))
elif cc.root_writable:
    croot = join(cc.root_dir, 'conda-bld')
else:
    croot = abspath(expanduser('~/conda-bld'))

build_prefix = join(cc.envs_dirs[0], '_build')
test_prefix = join(cc.envs_dirs[0], '_test')

def _get_python(prefix):
    if sys.platform == 'win32':
        res = join(prefix, 'python.exe')
    else:
        res = join(prefix, 'bin/python')
    return res

def _get_perl(prefix):
    if sys.platform == 'win32':
        res = join(prefix, 'perl.exe')
    else:
        res = join(prefix, 'bin/perl')
    return res

build_python = _get_python(build_prefix)
test_python = _get_python(test_prefix)
build_perl = _get_perl(build_prefix)
test_perl = _get_perl(test_prefix)

bldpkgs_dir = join(croot, cc.subdir)

use_new_rpath_logic = bool(cc.rc.get('use_new_rpath_logic', False))
verify_rpaths = bool(cc.rc.get('verify_rpaths', False))

if verify_rpaths:
    if use_new_rpath_logic:
        print('~/.condarc note: `verify_rpaths=True` has no effect '
              'when `use_new_rpath_logic=True` is also set')

def show():
    import conda.config as cc

    print('CONDA_PY:', CONDA_PY)
    print('CONDA_NPY:', CONDA_NPY)
    print('subdir:', cc.subdir)
    print('croot:', croot)
    print('build packages directory:', bldpkgs_dir)


if __name__ == '__main__':
    show()
