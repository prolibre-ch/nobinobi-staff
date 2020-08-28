#!/usr/bin/env python
# -*- coding: utf-8 -*-

#      Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from nobinobi_staff/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("nobinobi_staff", "__init__.py")

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='nobinobi-staff',
    version=version,
    description="""Application staff for nobinobi""",
    long_description=readme + '\n\n' + history,
    author='Florian Alu',
    author_email='alu@prolibre.com',
    url='https://github.com/prolibre-ch/nobinobi-staff',
    packages=[
        'nobinobi_staff',
    ],
    include_package_data=True,
    install_requires=[
        "djangorestframework==3.11.1", "django==3.1", "django-model-utils==4.0.0", "arrow==0.16.0",
        "django-crispy-forms==1.9.2", "django-extensions==3.0.5", "django-auto-one-to-one==3.3.1",
        "django-bootstrap-datepicker-plus==3.0.5", "django-admin-rangefilter==0.6.2", "DateTimeRange==1.0.0",
        "nobinobi-core==0.1.0"],
    zip_safe=False,
    keywords='nobinobi-staff',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
