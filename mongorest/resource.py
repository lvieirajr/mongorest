# -*- encoding: UTF-8 -*-

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

from .collection import Collection
from .utils import deserialize
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
    Adds some neat functionalities to the resource classes.
    Adds together urls from all the bases, sets collection and endpoint...
    """

    @classmethod
    def __prepare__(mcs, name, bases):
        """
        Puts together all the urls from each base class
        Adds them to a map and returns it on the member dict
        Together with the base collection and endpoint
        """
        rules = [
            rule
            for base in bases
            for rule in base.rules
            if hasattr(base, 'rules')
        ]

        return {
            'rules': rules,
            'url_map': Map(rules),
            'collection': Collection,
            'endpoint': '/',
        }

    def __call__(self, *args, **kwargs):
        if not len(list(self.url_map.iter_rules())):
            for rule in self.rules:
                self.url_map.add(Rule(
                    rule.rule,
                    methods=rule.methods,
                    endpoint=rule.endpoint
                ))

        return super(self.__class__, self).__call__(*args, **kwargs)


class Resource(WSGIWrapper, metaclass=ResourceMeta):
    """
    Just a class that puts together te WSGIWrapper and the ResourceMeta
    To be used as base for any resource to be created.
    """
    pass


class ListResourceMixin(Resource):
    """
    Resource Mixin that provides the list action for your endpoint.
    """
    rules = [Rule('/', methods=['GET'], endpoint='list')]

    def list(self, request):
        """
        Returns a serialized list of documents _ids from the collection
        """
        return Response(
            self.collection.aggregate(
                [{'$project': {'_id': 1}}],
                serialized=True
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
        fields = deserialize(request.get_data(as_text=True))

        document = self.collection(fields)
        if document.is_valid:
            return Response(
                document.save(serialized=True),
                content_type='application/json',
                status=201
            )
        else:
            return Response(
                document.errors(serialized=True),
                content_type='application/json',
                status=400
            )


class RetrieveResourceMixin(Resource):
    """
    Resource Mixin that provides the retrieve action for your endpoint.
    """
    rules = [Rule('/<_id>/', methods=['GET'], endpoint='retrieve')]

    def retrieve(self, request, _id):
        """
        Returns the serialized document with the given _id
        """
        document = self.collection.get({'_id': deserialize(_id)})

        if document:
            return Response(
                document.fields(serialized=True),
                content_type='application/json',
                status=200
            )
        else:
            return Response(
                {'error': 'The given _id is not related to a document.'},
                content_type='application/json',
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
        document = self.collection.get({'_id': deserialize(_id)})

        if document:
            fields = dict(
                document.fields(serialized=False),
                **deserialize(request.get_data(as_text=True))
            )

            document = self.collection(fields)
            if document.is_valid:
                return Response(
                    document.save(serialized=True),
                    content_type='application/json',
                    status=200
                )
            else:
                return Response(
                    document.errors(serialized=True),
                    content_type='application/json',
                    status=400
                )
        else:
            return Response(
                {'error': 'The given _id is not related to a document.'},
                content_type='application/json',
                status=400
            )


class DeleteResourceMixin(Resource):
    """
    Resource Mixin that provides the delete action for your endpoint.
    """
    rules = [Rule('/<_id>/', methods=['DELETE'], endpoint='delete')]

    def delete(self, request, _id):
        """
        Deletes the document with the given _id
        """
        document = self.collection.get({'_id': deserialize(_id)})

        if document:
            return Response(
                self.collection.delete_one(
                    {'_id': document._id},
                    serialized=True
                ),
                content_type='application/json',
                status=200
            )
        else:
            return Response(
                {'error': 'The given _id is not related to a document.'},
                content_type='application/json',
                status=400
            )
