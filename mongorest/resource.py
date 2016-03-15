# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six
from datetime import datetime
from werkzeug.routing import Map, Rule

from .collection import Collection
from .errors import DocumentNotFoundError
from .utils import deserialize, serialize
from .wrappers import Response
from .wsgi import WSGIWrapper

__all__ = [
    'Resource',
    'ListResourceMixin',
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
            for base_rule in base.rules:
                if not any(base_rule.rule == rule.rule and
                        set(base_rule.methods).intersection(set(rule.methods))
                            for rule in rules):
                    rules.append(base_rule)

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
        Returns the list of documents found on the collection
        """
        pipeline = [{'$match': request.args.pop('match', {})}]

        sort = request.args.pop('sort', {})
        if sort:
            pipeline.append({'$sort': sort})

        project = request.args.pop('project', {})
        if project:
            pipeline.append({'$project': project})

        return Response(serialize(self.collection.aggregate(pipeline)))


class CreateResourceMixin(Resource):
    """
    Resource Mixin that provides the create action for your endpoint.
    """
    rules = [Rule('/', methods=['POST'], endpoint='create')]

    def create(self, request):
        """
        Creates a new document based on the given data
        """
        document = self.collection(request.json)
        document.created_at = datetime.utcnow()
        document.updated_at = document.created_at

        created = document.insert()
        return Response(
            response=serialize(created),
            status=(
                201 if not all(
                    key in created for key in [
                        'error_code', 'error_type', 'error_message'
                    ]
                ) else 400
            )
        )


class RetrieveResourceMixin(Resource):
    """
    Resource Mixin that provides the retrieve action for your endpoint.
    """
    rules = [Rule('/<_id>/', methods=['GET'], endpoint='retrieve')]

    def retrieve(self, request, _id):
        """
        Returns the document containing the given _id or 404
        """
        _id = deserialize(_id)

        retrieved = self.collection.find_one({'_id': _id})
        if retrieved:
            return Response(serialize(retrieved))
        else:
            return Response(
                response=serialize(
                    DocumentNotFoundError(self.collection.__name__, _id)
                ),
                status=400
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
        _id = deserialize(_id)

        to_update = self.collection.find_one({'_id': _id})
        if to_update:
            document = self.collection(dict(to_update, **request.json))
            document.updated_at = datetime.utcnow()

            updated = document.update()
            return Response(
                response=serialize(updated),
                status=(
                    200 if not all(
                        key in updated for key in [
                            'error_code', 'error_type', 'error_message'
                        ]
                    ) else 400
                )
            )
        else:
            return Response(
                response=serialize(
                    DocumentNotFoundError(self.collection.__name__, _id)
                ),
                status=400
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
        _id = deserialize(_id)

        to_delete = self.collection.get({'_id': _id})
        if to_delete:
            deleted = to_delete.delete()

            return Response(
                response=serialize(deleted),
                status=(
                    200 if not all(
                        key in deleted for key in [
                            'error_code', 'error_type', 'error_message'
                        ]
                    ) else 400
                )
            )
        else:
            return Response(
                response=serialize(
                    DocumentNotFoundError(self.collection.__name__, _id)
                ),
                status=404
            )
