# -*- encoding: UTF-8 -*-

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

from .collection import Collection
from .utils import deserialize
from .wsgi import WSGIWrapper

__all__ = [
    'Resource',
    'ListResource',
    'CreateResource',
    'RetrieveResource',
    'UpdateResource',
    'DeleteResource',
]


class ResourceMeta(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        return {
            'url_map': Map([
                rule
                for base in bases
                for rule in base.rules
                if hasattr(base, 'rules')
            ]),
        }


class Resource(WSGIWrapper, metaclass=ResourceMeta):
    collection = Collection
    endpoint = 'collections'


class ListResource(Resource):
    rules = [Rule('/', methods=['GET'], endpoint='list')]

    def list(self, request):
        return Response(
            self.collection.find(serialized=True),
            content_type='application/json',
            status=200
        )


class CreateResource(Resource):
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
                status=200
            )
        else:
            return Response(
                document.errors(serialized=True),
                content_type='application/json',
                status=400
            )


class RetrieveResource(Resource):
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


class UpdateResource(Resource):
    rules = [Rule('/<_id>/', methods=['PUT'], endpoint='update')]

    def update(self, request, _id=None):
        return Response(255)


class DeleteResource(Resource):
    rules = [Rule('/<_id>/', methods=['DELETE'], endpoint='delete')]

    def delete(self, request, _id=None):
        return Response(355)


class Test(ListResource, CreateResource, RetrieveResource, UpdateResource, DeleteResource):
    pass