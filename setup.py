# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='cocojson',
    version='0.1.0',
    description='Utility scripts for COCO json annotation format',
    author='levan92',
    author_email='lingevan0208@gmail.com',
    url='https://github.com/levan92/cocojson',
    license='MIT',
    packages=find_packages(exclude=('docs',))
)
