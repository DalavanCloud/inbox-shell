#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click==6.0',
    'watchdog==0.8.3',
    'celery==3.1.23',
    'requests==2.11.1'
]

test_requirements = [
    'nose',
    'coverage'
]

setup(
    name='inbox_shell',
    version='0.1.0',
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    long_description=readme + '\n\n' + history,
    author="Fabio Batalha",
    author_email='fabio.batalha@scielo.org',
    url='https://github.com/fabiobatalha/inbox_shell',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='inbox_shell',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=["nose>=1.0", "coverage"],
    entry_points={
        'console_scripts': [
            'inbox_monitor=inbox_shell.cli:main'
        ]
    }
)
