#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import os


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r") as f:
        return f.read()


setuptools.setup(
    name="pytest-gitlabci-parallelized",
    version="0.1.4",
    author="Michał Leśniewski, Ryan Wilson-Perkin",
    author_email="mlesniew@gmail.com",
    license="MIT",
    url="https://github.com/mlesniew/pytest-gitlabci-parallelized",
    description="Parallelize pytest across GitLab CI workers.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["pytest_gitlabci_parallelized"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=["pytest"],
    classifiers=[
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["gitlabci-parallelized = pytest_gitlabci_parallelized"]},
)
