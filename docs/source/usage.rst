Usage
=====

This is a very small example on how to build a simple MongoRest API.


Project Settings
----------------

To define the settings for your project you should set the environment variable
`MONGOREST_SETTINGS_MODULE` to the module where the settings are stored::

    from os import environ
    environ['MONGOREST_SETTINGS_MODULE'] = 'project.settings'


Database
--------

To connect to your database you should specify the `MONGODB` setting on your
mongorest settings module. You can set the connection `URI`, or use other
options like setting the `HOSTS` and `PORTS` of your replica-set.
If you are not using a replica-set you can just set the one `HOST` and `PORT`::

    MONGODB = {
        'URI': '',
        'USERNAME': '',
        'PASSWORD': '',
        'HOST': 'localhost'
        'HOSTS': [],
        'PORT': 27017
        'PORTS': [],
        'DATABASE': 'mongorest',
        'OPTIONS': [],
    }


Example
-------

Here is a basic example of how easy it is to create an example library API with **MongoRest**::

    from mongorest.collection import Collection

    class Book(Collection):
        schema = {
            'name': {'type': 'string', 'required': True},
            'genre': {'type': 'string', 'required': True},
            'author': {'type': 'string', 'required': True},
            'number_of_pages': {'type': 'integer'},
            'release_date': {'type': 'datetime'},
        }

First we created our Book collection that inherited from the `mongorest.Collection` class,
then we added a `schema` to specify the fields, and their types.
For more details on schema creation visit the `Cerberus documentation <http://cerberus.readthedocs.io/>`_::

    from mongorest.resource import (
        ListResourceMixin, CreateResourceMixin
    )

    class BookResource(ListResourceMixin, CreateResourceMixin):
        collection = Book
        endpoint = 'books'

Here, by inheriting from these mongorest-builtin Mixins, our resource already has the list and create actions.
We also defined what will be the collection and endpoint this Resource refers to::


    from mongorest.wsgi import WSGIDispatcher
    from werkzeug.serving import run_simple

    if __name__ == '__main__':
        wsgi_app = WSGIDispatcher([BookResource])
        run_simple('localhost', 8000, wsgi_app)

Now we just had to instantiate the application as a `WSGIDispatcher` passing it our list of resources.
After that, we started our server and the API is ready to be consumed.
