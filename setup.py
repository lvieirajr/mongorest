# -*- encoding: UTF-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='mongorest',
    packages=['mongorest'],
    version='1.0.1',
    description='Easy REST APIs using MongoDB.',
    author='Luis Vieira',
    author_email='lvieira@lvieira.com',
    url='https://github.com/lvieirajr/mongorest',
    download_url='https://github.com/lvieirajr/mongorest/tarball/1.0.1',
    install_requires=['pymongo'],
    keywords=['python', 'mongodb', 'mongo', 'pymongo', 'rest', 'api'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
