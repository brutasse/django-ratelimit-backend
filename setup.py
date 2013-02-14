# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

import ratelimitbackend


setup(
    name='django-ratelimit-backend',
    version=ratelimitbackend.__version__,
    author='Bruno Renié',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/brutasse/django-ratelimit-backend',
    license='BSD licence, see LICENCE file',
    description='Login rate-limiting at the auth backend level',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    test_suite='runtests.runtests',
    zip_safe=False,
)
