#!/usr/bin/env python

"""Sappho package installer.

Distributing:

  $ setup.py sdist bdist_wheel
  $ twine upload dist/sappho-0.2.3.tar.gz dist/sappho-0.2.3*.whl
  $ rm -rf dist

  You'll need the wheel, twine package for bdist_wheel. Don't forget
  to clear your dist when finished.

Installing:
  `pip install .` in the project root. This script detects the
  python version and builds the install_requires accordingly.

  Does not install pygame. See `README.md`.

Notes:
    Pygame is a hassle to install, use the boostrap (whenever
    it's ported from Hypatia Engine).

"""

import sys
from setuptools import setup
from distutils.version import StrictVersion


# Build the list of packages required according to Python version
# Pygame isn't on Pypi.
install_requires = ['Pillow>=2, <4']  # NOTE: why this specific Pillow range?

# x.y.z
python_version = StrictVersion('.'.join(str(n) for n in sys.version_info[:3]))

# the `enum` package is a backport of Python 3.5 enum,
# we only want it in earlier versions of python
if python_version < StrictVersion('3.5'):
    install_requires.append('enum34')

exec(open('sappho/__init__.py').read())
setup(name='sappho',
      packages=['sappho'],
      version=__version__,
      description='2D game engine (pygame)',
      setup_requires=['setuptools-markdown'],
      install_requires=install_requires,
      long_description_markdown_filename='README.md',
      author='Lillian Lemmer',
      author_email='lillian.lemmer@hypatiasoftware.org',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Games/Entertainment :: Role-Playing',
                   'Topic :: Software Development :: Libraries :: pygame',
                  ],
      keywords=('games gaming development sprites adventure game tilemap '
                'tilesheet zelda gamedev 2d')
    )

