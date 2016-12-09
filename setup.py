# -*- encoding: UTF-8 -*-
from __future__ import absolute_import

from setuptools import setup
from setuptools.command.test import test as TestCommand
from sys import exit
from mongorest import __version__ as version


class Test(TestCommand):

    def finalize_options(self):
        self.test_suite = self.test_suite or ' '
        TestCommand.finalize_options(self)

    def run_tests(self):
        from unittest import TextTestRunner, defaultTestLoader as loader

        result = TextTestRunner().run(
            loader.loadTestsFromName(
                'tests.{0}'.format(self.test_suite).strip('. ')
            )
        )

        return exit(0) if not (result.failures + result.errors) else exit(1)


install_requires = [
    'cerberus==0.9.2',
    'pymongo==3.4.0',
    'six==1.10.0',
    'werkzeug==0.11.11',
]

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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
