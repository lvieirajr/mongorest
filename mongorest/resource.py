# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six
from datetime import datetime
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
            serialize([
                document['_id']
                for document in self.collection.aggregate(
                    [{'$match': deserialize(dict(request.args.items()))}],
                )
            ]),
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
            self.collection.aggregate(
                [{'$match': deserialize(dict(request.args.items()))}],
                serialize=True
            ),
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
        document.created_at = datetime.utcnow()
        document.updated_at = document.created_at
        created = document.save()

        return Response(
            serialize(created),
            content_type='application/json',
            status=201 if '_id' in created else 400
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
        document = self.collection.find_one(
            dict(request.args, **{'_id': deserialize(_id)})
        )

        if document:
            return Response(
                serialize(document),
                content_type='application/json',
                status=200
            )
        else:
            return Response(
                serialize({
                    '{0}_not_found'.format(self.collection.__name__.lower()):
                    'Could not find a {0} document with the given _id.'.format(
                        self.collection.__name__
                    )
                }),
                content_type='application/json',
                status=404
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
        to_update = self.collection.find_one(
            dict(request.args, **{'_id': deserialize(_id)})
        )

        if to_update:
            document = self.collection(
                dict(to_update, **deserialize(request.get_data(as_text=True)))
            )
            document.updated_at = datetime.utcnow()
            updated = document.save()

            return Response(
                serialize(updated),
                content_type='application/json',
                status=200 if '_id' in updated else 400
            )
        else:
            return Response(
                serialize({
                    '{0}_not_found'.format(self.collection.__name__.lower()):
                    'Could not find a {0} document with the given _id.'.format(
                        self.collection.__name__
                    )
                }),
                content_type='application/json',
                status=404
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
        to_delete = self.collection.find_one(
            dict(request.args, **{'_id': deserialize(_id)})
        )

        if to_delete:
            deleted = self.collection.delete_one({'_id': deserialize(_id)})

            return Response(
                serialize(to_delete),
                content_type='application/json',
                status=200 if deleted.get('ok', 0) == 1 else 400
            )
        else:
            return Response(
                serialize({
                    '{0}_not_found'.format(self.collection.__name__.lower()):
                    'Could not find a {0} document with the given _id.'.format(
                        self.collection.__name__
                    )
                }),
                content_type='application/json',
                status=404
            )
