# -*- encoding: UTF-8 -*-
from __future__ import absolute_import

try:
    from setuptools import setup
except:
    from distutils.core import setup


install_requires = ['pymongo', 'werkzeug', 'six']
try:
    import importlib
except ImportError:
    install_requires.append('importlib')



setup(
    name='mongorest',
    packages=['mongorest'],
    version='2.0.0',
    description='Easy REST APIs using MongoDB.',
    author='Luis Vieira',
    author_email='lvieira@lvieira.com',
    url='https://github.com/lvieirajr/mongorest',
    download_url='https://github.com/lvieirajr/mongorest/tarball/2.0.0',
    install_requires=install_requires,
    keywords=['mongodb', 'mongo', 'rest', 'api', 'pymongo', 'werkzeug'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
