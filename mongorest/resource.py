# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

from .collection import Collection
from .utils import deserialize, serialize
from .wsgi import WSGIWrapper

__all__ = [
    'Resource',
    'ListResourceMixin',
    'DocumentsResourceMixin',
    'CreateResourceMixin',
    'RetrieveResourceMixin',
    'UpdateResourceMixin',
    'DeleteResourceMixin',
]


class ResourceMeta(type):
    """
    MetaClass for the resource.
    Handles all the url rules for the Resource class and its children
    """

    def __new__(mcs, *args, **kwargs):
        """
        Handles the url_map generation based on the rules from the base classes
        Added to the class' own rules
        """
        name = args[0]
        bases = args[1]
        members = args[2].copy()

        rules = members.get('rules', [])
        for base in (base for base in bases if hasattr(base, 'rules')):
            rules.extend(base.rules)

        url_map = members.get('url_map', Map())
        for rule in rules:
            url_map.add(
                Rule(rule.rule, methods=rule.methods, endpoint=rule.endpoint)
            )

        members['rules'] = list(url_map.iter_rules())
        members['url_map'] = url_map

        return super(mcs, mcs).__new__(mcs, *(name, bases, members), **kwargs)


class Resource(six.with_metaclass(ResourceMeta, WSGIWrapper)):
    """
    Just a class that puts together te WSGIWrapper and the ResourceMeta
    To be used as base for any resource to be created.
    """
    collection = Collection


class ListResourceMixin(Resource):
    """
    Resource Mixin that provides the list action for your endpoint.
    """
    rules = [Rule('/', methods=['GET'], endpoint='list')]

    def list(self, request):
        """
        Returns the list of _ids found on the collection
        """
        return Response(
            self.collection.aggregate(
                [{'$project': {'_id': 1}}], serialize=True
            ),
            content_type='application/json',
            status=200
        )


class DocumentsResourceMixin(Resource):
    """
    Resource Mixin that provides the documents action for your endpoint.
    """
    rules = [Rule('/documents/', methods=['GET'], endpoint='documents')]

    def documents(self, request):
        """
        Returns the list of documents found on the collection
        """
        return Response(
            self.collection.aggregate(serialize=True),
            content_type='application/json',
            status=200
        )


class CreateResourceMixin(Resource):
    """
    Resource Mixin that provides the create action for your endpoint.
    """
    rules = [Rule('/', methods=['POST'], endpoint='create')]

    def create(self, request):
        """
        Creates a new document based on the given data
        """
        document = self.collection(deserialize(request.get_data(as_text=True)))

        return Response(
            serialize(document.save()),
            content_type='application/json',
            status=201 if document.is_valid else 400
        )


class RetrieveResourceMixin(Resource):
    """
    Resource Mixin that provides the retrieve action for your endpoint.
    """
    rules = [Rule('/<_id>/', methods=['GET'], endpoint='retrieve')]

    def retrieve(self, request, _id):
        """
        Returns the document containing the given _id or None
        """
        return Response(
            self.collection.find_one(deserialize(_id), serialize=True),
            content_type='application/json',
            status=200
        )


class UpdateResourceMixin(Resource):
    """
    Resource Mixin that provides the update action for your endpoint.
    """
    rules = [Rule('/<_id>/', methods=['PUT'], endpoint='update')]

    def update(self, request, _id):
        """
        Updates the document with the given _id using the given data
        """
        document = self.collection(dict(
            self.collection.find_one(deserialize(_id), serialize=False) or {},
            **deserialize(request.get_data(as_text=True))
        ))

        return Response(
            serialize(document.save()),
            content_type='application/json',
            status=200 if document.is_valid else 400
        )


class DeleteResourceMixin(Resource):
    """
    Resource Mixin that provides the delete action for your endpoint.
    """
    rules = [Rule('/<_id>/', methods=['DELETE'], endpoint='delete')]

    def delete(self, request, _id):
        """
        Deletes the document with the given _id if it exists
        """
        return Response(
            serialize(self.collection.delete_one({'_id': deserialize(_id)})),
            content_type='application/json',
            status=200
        )
