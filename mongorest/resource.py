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

    @classmethod
    def __prepare__(mcs, name, bases):
        urls = [
            rule
            for base in bases
            for rule in base.rules
            if hasattr(base, 'rules')
        ]

        return {
            'urls': urls,
            'url_map': Map(urls),
            'collection': Collection,
            'endpoint': 'collections',
        }


class Resource(WSGIWrapper, metaclass=ResourceMeta):
    pass


class ListResourceMixin(Resource):
    rules = [Rule('/', methods=['GET'], endpoint='list')]

    def list(self, request):
        return Response(
            self.collection.find(serialized=True),
            content_type='application/json',
            status=200
        )


class CreateResourceMixin(Resource):
    rules = [Rule('/', methods=['POST'], endpoint='create')]

    def create(self, request):
        fields = {
            key: request.form.get(key)
            for key in request.form
        }

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
    rules = [Rule('/<_id>/', methods=['GET'], endpoint='retrieve')]

    def retrieve(self, request, _id=None):
        return Response(
            self.collection.find_one(
                {'_id': deserialize(_id)},
                serialized=True,
            ),
            content_type='application/json',
            status=200
        )


class UpdateResourceMixin(Resource):
    rules = [Rule('/<_id>/', methods=['PUT'], endpoint='update')]

    def update(self, request, _id=None):
        return Response(255)


class DeleteResourceMixin(Resource):
    rules = [Rule('/<_id>/', methods=['DELETE'], endpoint='delete')]

    def delete(self, request, _id=None):
        return Response(355)
