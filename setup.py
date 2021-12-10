# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cocojson",
    version="0.1.1",
    author="levan92",
    author_email="lingevan0208@gmail.com",
    description="Utility functions for manipulating COCO json annotation format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/levan92/cocojson",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("docs",)),
    install_requires=["numpy", "opencv-python>=4.5", "tqdm", "Pillow"],
)
