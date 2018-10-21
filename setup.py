#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="aarghparse",
    version="0.0.1",  # also in __init__.py
    url="https://github.com/jbasko/aarghparse",
    license="MIT",
    author="Jazeps Basko",
    author_email="jazeps.basko@gmail.com",
    maintainer="Jazeps Basko",
    maintainer_email="jazeps.basko@gmail.com",
    description="A collection of argparse extensions",
    keywords="argparse cli",
    long_description=read("README.rst"),
    packages=["aarghparse"],
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)
