#!/bin/sh

python setup.py sdist
python setup.py upload

rm -rf build dist PKG-INFO
rm -rf sappho.egg-info
