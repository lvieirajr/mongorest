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

Here is a basic example of how easy it is to create an API with **MongoRest**:


    from mongorest.collection import Collection

    class Book(Collection):
        meta = {
            'required': {
               'name': str, 'author': str, 'genre': str
            }
            'optional': {
               'number_of_pages': int, 'date_of_release': datetime,
            }
        }

First we created our Book collection, that inherited from the `Collection` class. <br />
We added a `meta` to specify the required and optional fields, and their types. <br />


    from mongorest.resource import (
        ListResourceMixin, CreateResourceMixin, RetrieveResourceMixin,
    )


    class BookResource(ListResourceMixin, CreateResourceMixin, RetrieveResourceMixin):
        collection = Book
        endpoint = 'books'
        
Here, by inheriting from these Mixins our Resource already has the list, create and retrieve actions. <br />
We also defined what will be the collection and endpoint this Resource refers to. <br />

        
    from mongorest.wsgi import WSGIDispatcher
    from werkzeug.serving import run_simple


    if __name__ == '__main__':
        app = WSGIDispatcher([BookResource])
        run_simple('localhost', 8000, app)
    
Now we just had to instantiate the app as a `WSGIDispatcher` passing it our list of resources. <br />
Then we started our server and the API is ready. <br />


Now lets go for an example that is a little bit more complex:

    from mongorest.collection import Collection
    
    
    class School(Collection):
        meta = {
            'required': {'name': str}
            'optional': {'principal': str}
        }
        
 
    class Student(Collection):
        meta = {
            'required': {
               'name': str, 'age': int, 'school': ObjectId, 'grade': int,
            }
        }
        
Again, here we are simply defining our collections. <br />


    from mongorest.resource import Resource
    from mongorest.utils import deserialize, serialize
    from werkzeug.wrappers import Response
    
    class SchoolResource(Resource):
        collection = School
        endpoint = 'schools'
        
        urls = [Rule('/<_id>/students/<grade>/', methods=['GET'], endpoint='grade_students')]
        
        def grade_students(request, _id, grade):
            school = self.collection.find_one({'_id': deserialize(_id)})
            
            if school:
                return Response(
                    Students.find(
                        {'school': school['_id'], 'grade': deserialize(grade)}
                        serialized=True
                    ),
                    content_type='application/json',
                    status=200
                )
            else:
                return Response(
                    serialize({'error': 'School does not exist.'}),
                    status=400
                )
                
Now we have created a custom Resource, inheriting from the `Resource` class. <br />
Again we defined the collection and the endpoint for the resource, but we also defined the urls for the views we created. Only one in this case. <br />
Then comes the view itself, that is a view with a nested route that returns all students who go to that school from a given grade.

    
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
