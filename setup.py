# -*- encoding: UTF-8 -*-
from __future__ import absolute_import

from setuptools import setup
from setuptools.command.test import test as TestCommand
from sys import exit
from mongorest import __version__ as version


class Test(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tests import run_tests
        return exit(0) if run_tests() else exit(1)


install_requires = ['pymongo', 'werkzeug', 'six']
try:
    import importlib
except ImportError:
    install_requires.append('importlib')


setup(
    name='mongorest',
    packages=['mongorest'],
    version=version,
    description='Easy REST APIs using MongoDB.',
    author='Luis Vieira',
    author_email='lvieira@lvieira.com',
    url='https://github.com/lvieirajr/mongorest',
    download_url='github.com/lvieirajr/mongorest/tarball/{0}'.format(version),
    install_requires=install_requires,
    cmdclass={'test': Test},
    keywords=['mongodb', 'mongo', 'rest', 'api', 'pymongo', 'werkzeug'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: PyPy :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
