#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

import os
import sys

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


base_dir = os.path.dirname(__file__)
requirements_dir = os.path.join(base_dir, 'requirements')
base_reqs = parse_requirements(os.path.join(requirements_dir, 'production.txt'), session=False)
requirements = [str(br.req) for br in base_reqs]
ci_reqs = parse_requirements(os.path.join(requirements_dir, 'ci.txt'), session=False)
test_requirements = [str(cr.req) for cr in ci_reqs]

setup(
    name='nm_launch_api',
    version='0.0.1',
    description="API backend to search launch data to the frontend.",
    long_description=readme + '\n\n' + history,
    author="Mark Liederbach",
    author_email='contact@markliederbach.com',
    url='https://github.com/markliederbach/nm-launch-catalog',
    packages=[
        'nm_launch_api',
    ],
    package_dir={'nm_launch_api':
                 'nm_launch_api'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'nm_launch_api=nm_launch_api.runserver:main',
        ],
    },
    license="ISCL",
    zip_safe=False,
    keywords='nm_launch_api',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
