# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in pointage_cdk/__init__.py
from pointage_cdk import __version__ as version

setup(
	name='pointage_cdk',
	version=version,
	description='application pointage cdk',
	author='dHaj',
	author_email='admin@admin.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
