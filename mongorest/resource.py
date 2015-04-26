# -*- encoding: UTF-8 -*-

import six

from werkzeug.routing import Map, Rule

from .collection import Collection
from .wsgi import WSGIWrapper

__all__ = [
    'Resource',
    # 'ListResourceMixin',
    # 'CreateResourceMixin',
    # 'RetrieveResourceMixin',
    # 'UpdateResourceMixin',
    # 'DeleteResourceMixin',
]


class ResourceMeta(type):
    """
    MetaClass for the resource.
    Adds some neat functionalities to the resource classes.
    Adds together urls from all the bases, sets collection and endpoint...
    """
    def __new__(mcs, *args, **kwargs):
        class_name = args[0]
        bases = args[1]

        member_dict = args[2].copy()
        member_dict['rules'] = member_dict.get('rules', [])
        member_dict['url_map'] = member_dict.get('url_map', Map())

        for base in bases:
            if hasattr(base, 'rules'):
                member_dict['rules'].extend(base.rules)

        for rule in member_dict['rules']:
            rule = Rule(
                rule.rule,
                methods=rule.methods,
                endpoint=rule.endpoint
            )
            member_dict['url_map'].add(rule)

        return super(mcs, mcs).__new__(
            mcs,
            *(class_name, bases, member_dict),
            **kwargs
        )


class Resource(six.with_metaclass(ResourceMeta, WSGIWrapper)):
    """
    Just a class that puts together te WSGIWrapper and the ResourceMeta
    To be used as base for any resource to be created.
    """
    collection = Collection


# class ListResourceMixin(Resource):
#     """
#     Resource Mixin that provides the list action for your endpoint.
#     """
#     rules = [Rule('/', methods=['GET'], endpoint='list')]
#
#     def list(self, request):
#         """
#         Returns a serialized list of documents _ids from the collection
#         """
#         return Response(
#             self.collection.aggregate(
#                 [{'$project': {'_id': 1}}],
#                 serialized=True
#             ),
#             content_type='application/json',
#             status=200
#         )
#
#
# class CreateResourceMixin(Resource):
#     """
#     Resource Mixin that provides the create action for your endpoint.
#     """
#     rules = [Rule('/', methods=['POST'], endpoint='create')]
#
#     def create(self, request):
#         """
#         Creates a new document based on the given data
#         """
#         fields = deserialize(request.get_data(as_text=True))
#
#         document = self.collection(fields)
#         if document.is_valid:
#             return Response(
#                 document.save(serialized=True),
#                 content_type='application/json',
#                 status=201
#             )
#         else:
#             return Response(
#                 document.errors(serialized=True),
#                 content_type='application/json',
#                 status=400
#             )
#
#
# class RetrieveResourceMixin(Resource):
#     """
#     Resource Mixin that provides the retrieve action for your endpoint.
#     """
#     rules = [Rule('/<_id>/', methods=['GET'], endpoint='retrieve')]
#
#     def retrieve(self, request, _id):
#         """
#         Returns the serialized document with the given _id
#         """
#         document = self.collection.get({'_id': deserialize(_id)})
#
#         if document:
#             return Response(
#                 document.fields(serialized=True),
#                 content_type='application/json',
#                 status=200
#             )
#         else:
#             return Response(
#                 {'error': 'The given _id is not related to a document.'},
#                 content_type='application/json',
#                 status=400
#             )
#
#
# class UpdateResourceMixin(Resource):
#     """
#     Resource Mixin that provides the update action for your endpoint.
#     """
#     rules = [Rule('/<_id>/', methods=['PUT'], endpoint='update')]
#
#     def update(self, request, _id):
#         """
#         Updates the document with the given _id using the given data
#         """
#         document = self.collection.get({'_id': deserialize(_id)})
#
#         if document:
#             fields = dict(
#                 document.fields(serialized=False),
#                 **deserialize(request.get_data(as_text=True))
#             )
#
#             document = self.collection(fields)
#             if document.is_valid:
#                 return Response(
#                     document.save(serialized=True),
#                     content_type='application/json',
#                     status=200
#                 )
#             else:
#                 return Response(
#                     document.errors(serialized=True),
#                     content_type='application/json',
#                     status=400
#                 )
#         else:
#             return Response(
#                 {'error': 'The given _id is not related to a document.'},
#                 content_type='application/json',
#                 status=400
#             )
#
#
# class DeleteResourceMixin(Resource):
#     """
#     Resource Mixin that provides the delete action for your endpoint.
#     """
#     rules = [Rule('/<_id>/', methods=['DELETE'], endpoint='delete')]
#
#     def delete(self, request, _id):
#         """
#         Deletes the document with the given _id
#         """
#         document = self.collection.get({'_id': deserialize(_id)})
#
#         if document:
#             return Response(
#                 self.collection.delete_one(
#                     {'_id': document._id},
#                     serialized=True
#                 ),
#                 content_type='application/json',
#                 status=200
#             )
#         else:
#             return Response(
#                 {'error': 'The given _id is not related to a document.'},
#                 content_type='application/json',
#                 status=400
#             )
