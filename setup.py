# -*- encoding: UTF-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='mongorest',
    packages=['mongorest'],
    version='1.1.3',
    description='Easy REST APIs using MongoDB.',
    author='Luis Vieira',
    author_email='lvieira@lvieira.com',
    url='https://github.com/lvieirajr/mongorest',
    download_url='https://github.com/lvieirajr/mongorest/tarball/1.1.3',
    install_requires=['pymongo', 'werkzeug', 'six'],
    keywords=['python', 'mongodb', 'rest', 'api', 'pymongo', 'werkzeug'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.4',
    ],
)
