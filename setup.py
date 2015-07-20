# -*- coding: utf-8 -*-

# from __future__ import unicode_literals

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-mercadopago',
    version='0.0.2',
    packages=['djmercadopago', 'djmercadopago.migrations'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to use MercadoPago.',
    long_description=README,
    url='https://github.com/data-tsunami/django-mercadopago',
    author='Horacio Guillermo de Oro',
    author_email='hgdeoro@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
