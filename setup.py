#!/usr/bin/env python
from setuptools import setup, find_packages


requires = [
    'jmespath>=0.9.3',
    'python-decouple>=3.1',
    'requests>=2.18.4',
    'sessionlib>=0.2.0',
    'tenacity>=4.9.0'
]

setup(
    name='onegram',
    version='1.3.1',
    description='A simplistic api-like instagram bot powered by requests',
    url='https://github.com/pauloromeira/onegram',
    author='Paulo Romeira',
    author_email='paulo@pauloromeira.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.6',
    install_requires=requires
)
