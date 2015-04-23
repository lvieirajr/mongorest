# MongoRest

[![pypi-version]][pypi]

**Easy [REST][rest] [APIs][api] using [MongoDB][mongodb].**

# Overview

[MongoRest][mongorest] is a [Framework][framework] written in [Python][python] built on top of [PyMongo][pymongo] and [Werkzeug][werkzeug] to ease the creation of [REST][rest] [APIs][api] using [MongoDB][mongodb].


# Requirements

* Python >= 3.4.0
* MongoDB >= 3.0
* PyMongo >= 3.0
* Werkzeug >= 0.10.0

# Installation

    pip install mongorest
    
# Usage

This is a basic example where we are creating a simple API for a library, where we can list all our books, add new books and retrieve a single book:

    from mongorest.collection import Collection
    from mongorest.resource import (
        ListResourceMixin,
        CreateResourceMixin,
        RetrieveResourceMixin,
    )
    from mongorest.wsgi import WSGIDispatcher
    from werkzeug.serving import run_simple


    # Our Base Collection
    class Book(Collection):
        meta = {
            'required': {
               'name': str,
               'author': str,
               'genre': str
            }
            'optional': {
               'number_of_pages': int,
               'date_of_release': datetime,
            }
        }
        
    
    # Our API
    class BookResource(ListResourceMixin, CreateResourceMixin, RetrieveResourceMixin):
        collection = Book
        endpoint = 'books'
        
    
    # Creating the app and Running the Server
    if __name__ == '__main__':
        app = WSGIDispatcher([BookResource])
        run_simple('localhost', 8000, app)
    
All we did was: Created a collection to represent our books, the collection has a `meta` specifying the required fields and the optional ones.
Also we created a Resource inheriting from the Resource Mixins. All we had to do for the Resource was chose the collection that will be used and what will be the endpoint.
After that we are just creating the app, passing it our list of resources and running the server.

`MongoRest` also includes builtin Delete and Update mixins that were not used in this example.


Let's show a more complex example where we create a customized Resource with a nested route:

    from mongorest.collection import Collection
    from mongorest.resource import Resource
    from mongorest.utils import deserialize
    from werkzeug.wrappers import Response
    
    class School(Collection):
        meta = {
            'required': {
               'name': str,
            }
            'optional': {
               'principal': str,
            }
        }
        
        
    class Student(Collection):
        meta = {
            'required': {
               'name': str,
               'age': int,
               'school': ObjectId,
               'grade': int,
            }
        }
    
    class SchoolResource(Resource):
        collection = School
        endpoint = 'schools'
        
        urls = [Rule('/<_id>/students/<grade>/', methods=['GET'], endpoint='grade_students')]
        
        def grade_students(request, _id, grade):
            school = self.collection.find_one({'_id': deserialize(_id)})
            
            if school:
                return Response(
                    Students.find({
                        'school': school['_id'],
                        'grade': deserialize(grade),
                    }),
                    content_type='application/json',
                    status=200
                )
            else:
                return Response(
                    {'error': 'School does not exist.'},
                    status=400
                )
        
In this example, we created a nested route on our customized Resource. All we had to do was inherit from resource, chose the collection and the endpoint and add an URL for our view.
And with `MongoRest` you can easily do much more.
    
    
    
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

[pypi-version]: https://pypip.in/version/mongorest/badge.svg
[pypi]: https://pypi.python.org/pypi/mongorest

[rest]: https://en.wikipedia.org/wiki/Rest
[api]: https://en.wikipedia.org/wiki/Application_programming_interface
[mongodb]: https://www.mongodb.org/

[mongorest]: https://github.com/lvieirajr/mongorest/
[framework]: https://en.wikipedia.org/wiki/Software_framework
[python]: https://www.python.org/
[pymongo]: https://github.com/mongodb/mongo-python-driver/ 
[werkzeug]: http://werkzeug.pocoo.org/
