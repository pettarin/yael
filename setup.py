#!/usr/bin/env python

from distutils.core import setup

setup(
    name='yael',
    version='0.0.1',
    author='Alberto Pettarin',
    author_email='alberto@albertopettarin.it',
    packages=['yael'],
    url='https://github.com/pettarin/yael',
    license='LICENSE',
    description='yael (Yet Another EPUB Library) is a Python library for reading, manipulating, and writing EPUB 2/3 files.',
    long_description=open('README.md').read(),
    install_requires='lxml >= 3.4.0, simplejson >= 3.6.0',
)
