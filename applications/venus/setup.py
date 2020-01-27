#!/usr/bin/python3
from setuptools import setup, find_packages
from src import __version__ as v
setup(
        name='venus',
        version=v,
        packages=find_packages(),
        author='Fred Monster',
        author_email='hezhiyuan_tju@163.com',
        url='https://github.com/FrederichRiver/neutrino',
        license='LICENSE',
        description='None'
        )
