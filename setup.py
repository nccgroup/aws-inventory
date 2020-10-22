#!/usr/bin/env python

"""Python code for installing this repository via `pip`."""

from setuptools import setup, find_packages
import aws_inventory

with open('README.md') as fd:
    long_description = fd.read()

with open('requirements.txt') as fd:
    install_requires = [x.strip() for x in fd.readlines() if x.strip() != '']

setup(
    name='aws_inventory',
    version=aws_inventory.__version__,
    description='A Python package for enumerating the resources of an AWS account',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='ApacheV2',
    url='https://github.com/nccgroup/aws-inventory',
    author='NCC Group',
    author_email='erik.steringer@nccgroup.com',
    scripts=[],
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=3.5,<4',  # assume Python 4 is not compatible
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'aws-inventory = aws_inventory.__main__:main'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Security'
    ],
    keywords=[
        'AWS', 'Enumeration', 'Security', 'Inventory', 'NCC Group'
    ],
    zip_safe=False
)
