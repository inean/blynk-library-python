#!/usr/bin/env python

from setuptools import setup

setup(
    name         = "blynk-library-python",
    version      = "0.0.1", #blynk.lib.__version__
    description  = "Client-side implementation of the Blynk protocol",
    platforms    = "any",
    url          = "http://www.blynk.cc",
    license      = "MIT",
    author       = "Maksym Ivanov",
    author_email = "ulidtko@gmail.com",

    packages     = ["blynk.library"],
    classifiers  = [
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X"
    ],
    install_requires = [
        "Enum34"
    ]
)
