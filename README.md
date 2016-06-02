# MongoRest

[![pypi-version]][pypi] [![pypi-downloads]][pypi] [![read-the-docs]][mongorest-read-the-docs] [![build-status]][travis] [![coveralls-status]][coveralls] [![landscape-health]][landscape] [![codacy-grade]][codacy] 

**Easy [REST][rest] [APIs][api] using [MongoDB][mongodb].**


# Overview

[MongoRest][mongorest] is a [Framework][framework] written in [Python][python] built on top of [PyMongo][pymongo] and [Werkzeug][werkzeug] to ease the creation of [REST][rest] [APIs][api] using [MongoDB][mongodb].


# Python Compatibility

* Python >= 2.7
* Python3 >= 3.3
* Pypy >= 2.6
* Pypy3 >= 2.4


# Mongo Compatibility

* MongoDB >= 2.4


# Requirements

* Cerberus >= 0.9.0
* PyMongo >= 3.0.0
* Six >= 1.10.0
* Werkzeug >= 0.10.0


# Installation

    pip install mongorest
    
    
# Usage

To define the settings for your project you should set the environment variable `MONGOREST_SETTINGS_MODULE` to the module where the settings are stored:

```python
from os import environ
environ['MONGOREST_SETTINGS_MODULE'] = 'project.settings'
```

To connect to your database you should specify the `MONGODB` setting on your mongorest settings module.
You can set the connection `URI`, or use other options like setting the `HOSTS` and `PORTS` of your replica-set.
If you are not using a replica-set you can just set the one `HOST` and `PORT`.

```python
MONGODB = {
    'URI': '',
    'USERNAME': '',
    'PASSWORD': '',
    'HOSTS': ['localhost'],
    'PORTS': [27017],
    'DATABASE': 'mongorest-test',
    'OPTIONS': [],
}
```

Here is a basic example of how easy it is to create an example library API with **MongoRest**:

```python
from mongorest.collection import Collection

class Book(Collection):
    schema = {
        'name': {'type': 'string', 'required': True},
        'genre': {'type': 'string', 'required': True},
        'author': {'type': 'string', 'required': True},
        'number_of_pages': {'type': 'integer'},
        'release_date': {'type': 'datetime'},
    }
```

First we created our Book collection that inherited from the `mongorest.Collection` class, then ee added a `schema` to specify the fields, and their types.
For more details on schema creation visit the documentation for **Cerberus** in this [LINK][cerberus].

```python
from mongorest.resource import ListResourceMixin, CreateResourceMixin

class BookResource(ListResourceMixin, CreateResourceMixin):
    collection = Book
    endpoint = 'books'
```

Here, by inheriting from these mongorest-builtin Mixins, our resource already has the list and create actions.
We also defined what will be the collection and endpoint this Resource refers to.

```python        
from mongorest.wsgi import WSGIDispatcher
from werkzeug.serving import run_simple

if __name__ == '__main__':
    wsgi_app = WSGIDispatcher([BookResource])
    run_simple('localhost', 8000, wsgi_app)
```

Now we just had to instantiate the application as a `WSGIDispatcher` passing it our list of resources.
After that, we started our server and the API is ready to be consumed.


For more details, read the [MongoRest Documentation][mongorest_docs]

    
# License

Copyright (c) 2015, Luis Antônio Vieira Junior.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

\*  Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

\*  Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

\*  Neither the name of MongoRest nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[pypi-version]: https://img.shields.io/pypi/v/MongoRest.svg
[pypi-downloads]: https://img.shields.io/pypi/dm/MongoRest.svg
[pypi]: https://pypi.python.org/pypi/mongorest

[read-the-docs]: https://readthedocs.org/projects/docs/badge/?version=latest
[mongorest-read-the-docs]: https://mongorest.readthedocs.io/

[build-status]: https://travis-ci.org/lvieirajr/mongorest.svg?branch=master
[travis]: https://travis-ci.org/lvieirajr/mongorest

[coveralls-status]: https://coveralls.io/repos/lvieirajr/mongorest/badge.svg?branch=master
[coveralls]: https://coveralls.io/r/lvieirajr/mongorest?branch=master

[landscape-health]: https://landscape.io/github/lvieirajr/mongorest/master/landscape.svg?style=flat
[landscape]: https://landscape.io/github/lvieirajr/mongorest/master

[codacy-grade]: https://www.codacy.com/project/badge/de84ced5bfa241b3a1a64f73146a03e3
[codacy]: https://www.codacy.com/app/lvieira/mongorest

[rest]: https://en.wikipedia.org/wiki/Rest
[api]: https://en.wikipedia.org/wiki/Application_programming_interface
[mongodb]: https://www.mongodb.org/

[mongorest]: https://github.com/lvieirajr/mongorest/
[framework]: https://en.wikipedia.org/wiki/Software_framework
[python]: https://www.python.org/
[pymongo]: https://github.com/mongodb/mongo-python-driver/ 
[werkzeug]: http://werkzeug.pocoo.org/
[cerberus]: http://cerberus.readthedocs.io/
