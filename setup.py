# -*- coding: utf-8 -*-

import re

from setuptools import setup, find_packages

with open('anthem/__init__.py') as f:
    version = re.search('^__version__\s*=\s*"(.*)"', f.read(), re.M).group(1)
with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()

setup(
    name='anthem',
    version=version,
    description='Make your Odoo scripts sing.',
    long_description=readme + '\n\n' + history,
    author='Camptocamp',
    author_email='info@camptocamp.com',
    url='https://github.com/camptocamp/anthem',
    license='LGPLv3+',
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': ['anthem = anthem.cli:main']
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
