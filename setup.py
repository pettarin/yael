#!/usr/bin/env python

import os

from distutils.core import setup

setup(
    name='yael',
    packages=['yael'],
    version='0.0.7',
    description='yael (Yet Another EPUB Library) is a Python library for reading, manipulating, and writing EPUB 2/3 files.',
    author='Alberto Pettarin',
    author_email='alberto@albertopettarin.it',
    url='https://github.com/pettarin/yael',
    license='MIT',
    long_description=open('README.txt').read(),
    keywords=['epub', 'yael', 'EPUB 2', 'EPUB 3'],
    install_requires='lxml >= 3.4.0, simplejson >= 3.6.0',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
