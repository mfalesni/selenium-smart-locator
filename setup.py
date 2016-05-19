#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#   Author(s): Milan Falesnik   <milan@falesnik.net>
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from setuptools import setup


setup(
    name="selenium-smart-locator",
    use_scm_version=True,
    author="Milan Falesnik",
    author_email="milan@falesnik.net",
    description="A (somewhat) smart locator class for Selenium.",
    license="GPLv3",
    keywords="locator,selenium",
    url="https://github.com/mfalesni/selenium-smart-locator",
    packages=["smartloc"],
    package_dir={'': 'src'},
    install_requires=['selenium', 'six'],
    setup_requires=[
        'setuptools_scm',
    ],
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
    ]
)
