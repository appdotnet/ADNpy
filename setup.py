#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="adnpy",
      version='0.3.0',
      description="App.net API library for python",
      long_description=open('README.rst').read(),
      license="MIT",
      author="Alex Kessinger, Bryan Berg, App.net",
      author_email="alex@app.net",
      url="http://github.com/appdotnet/adnpy",
      packages=find_packages(exclude=['tests']),
      data_files=[('examples', ['examples/send-broadcast.py'])],
      install_requires=[
          'python-dateutil>=1.5',
          'requests>=2.0.1',
      ],
      keywords="app.net api library",
      zip_safe=True)
