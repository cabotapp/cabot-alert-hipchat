#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '2.0.2'

setup(name='cabot-alert-hipchat',
      version=VERSION,
      description='A Hipchat alert plugin for Cabot by Arachnys',
      author='Arachnys',
      author_email='info@arachnys.com',
      url='http://cabotapp.com',
      packages=find_packages(),
      download_url='https://github.com/cabotapp/cabot-alert-hipchat/archive/{}.zip'.format(VERSION),
     )
