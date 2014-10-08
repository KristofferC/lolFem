#!/usr/bin/env python

from distutils.core import setup
from Cython.Build import cythonize

setup(name='lolFem',
      version='0.1',
      description='FEM analysis with Python',
      author='Kristoffer Carlsson',
      author_email='kcarlsson89@gmail.com',
      url='',
      ext_modules=cythonize("lolFem/*.pyx"),
      packages=['lolFem'], requires=['numpy', 'scipy']
      )
