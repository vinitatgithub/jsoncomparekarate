#!/usr/bin/env python
# coding: utf-8
from distutils.core import setup
from os import path, chdir, system
from sys import argv

from setuptools import find_packages

if "upload" in argv:
    chdir("jsoncomparekarate")
    print("running test")
    assert system("python3 jsoncomparekaratetest.py") == 0
    chdir("..")

this_directory = path.abspath(path.dirname(__file__))

setup(
    name='json-compare-karate',
    version='1.0',
    packages=find_packages(),
    test_suite='jsoncomparekaratetest.py',
    author='Vin Pat',
    author_email='eatfrogfirst@outlook.com',
    description='A recursive json comparison library that handles karate style json comparison',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/vinitatgithub/jsoncomparekarate',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='json comparison order karate optional fields',
    python_requires=">=3.5"
)
