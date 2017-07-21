#!/usr/bin/env python
"""
Library to create/handle geometries and tight-binding parameters in Python. Made with DFT in mind.
"""

from __future__ import print_function

if __doc__ is None:
    __doc__ = """sisl: Creating and handling of geometries.

Enables tight-binding models etc."""

DOCLINES = __doc__.split("\n")

import sys
import subprocess
import os
import os.path as osp

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Topic :: Software Development
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Physics
Topic :: Utilities
"""

MAJOR = 0
MINOR = 8
MICRO = 5
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
GIT_REVISION = "306456a709f74bfa3a512e4d35546195d03705a6"

# The MANIFEST should be updated (which it only is
# if it does not exist...)
# So we try and delete it...
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')


def generate_cython():
    cwd = osp.abspath(osp.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable,
                         osp.join(cwd, 'tools', 'cythonize.py'),
                         'sisl'],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")

build_requires = ['six', 'setuptools', 'numpy>=1.9', 'scipy', 'netCDF4']

# Create list of all sub-directories with
#   __init__.py files...
packages = ['sisl']
for subdir, dirs, files in os.walk('sisl'):
    if '__init__.py' in files:
        packages.append(subdir.replace(os.sep, '.'))
        if 'tests' in 'dirs':
            packages.append(subdir.replace(os.sep, '.') + '.tests')

metadata = dict(
    name='sisl',
    maintainer="Nick R. Papior",
    maintainer_email="nickpapior@gmail.com",
    description="Tight-binding models and interfacing the tight-binding transport calculator TBtrans",
    long_description="""Manipulating with SIESTA output files.

Creation of geometries using simple IO interfaces with multiple formats.

Tight-binding models and interfacing the tight-binding transport calculator TBtrans.
""",
    url="http://github.com/zerothi/sisl",
    download_url="http://github.com/zerothi/sisl/releases",
    license='LGPLv3',
    packages=packages,
    entry_points={
        'console_scripts':
        ['sgeom = sisl.geometry:sgeom',
         'sgrid = sisl.grid:sgrid',
         'sdata = sisl.utils.sdata:sdata']
    },
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    platforms='any',
    install_requires=build_requires,
)

cwd = osp.abspath(osp.dirname(__file__))
if not osp.exists(osp.join(cwd, 'PKG-INFO')):
    # Generate Cython sources, unless building from source release
    # generate_cython()
    pass


# Generate configuration
def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('sisl')

    return config


metadata['version'] = VERSION
if not ISRELEASED:
    metadata['version'] = VERSION + '-dev'

# With credits from NUMPY developers we use this
# routine to get the git-tag


def git_version():
    global GIT_REVISION

    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        rev = out.strip().decode('ascii')
    except OSError:
        # Retain the revision name
        rev = GIT_REVISION

    return rev


def write_version(filename='sisl/info.py'):
    version_str = """
# This file is automatically generated from sisl setup.py
major   = {version[0]}
minor   = {version[1]}
micro   = {version[2]}
version = '.'.join(map(str,[major, minor, micro]))
release = version
# Git information
git_revision = '{git}'
git_revision_short = git_revision[:7]

if not release:
    version = version + '-' + git_revision
"""
    # If we are in git we try and fetch the
    # git version as well
    GIT_REV = git_version()

    with open(filename, 'w') as fh:
        fh.write(version_str.format(version=[MAJOR, MINOR, MICRO], git=GIT_REV))

if __name__ == '__main__':

    # First figure out if we should define the
    # version file
    try:
        only_idx = sys.argv.index('only-version')
    except:
        only_idx = 0
    if only_idx > 0:
        # Figure out if we should write a specific file
        print("Only creating the version file")
        if len(sys.argv) > only_idx + 1:
            vF = sys.argv[only_idx+1]
            write_version(vF)
        else:
            write_version()
        sys.exit(0)

    try:
        # Create version file
        # if allowed
        write_version()
    except:
        pass

    # Be sure to import this before numpy setup
    from setuptools import setup

    # Now we import numpy distutils for installation.
    from numpy.distutils.core import setup
    metadata['configuration'] = configuration

    # Main setup of python modules
    setup(**metadata)
