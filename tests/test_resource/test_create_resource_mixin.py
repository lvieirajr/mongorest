# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId
from werkzeug.wrappers import Response

from mongorest.collection import Collection
from mongorest.resource import CreateResourceMixin
from mongorest.testcase import TestCase
from mongorest.utils import deserialize
from mongorest.wsgi import WSGIDispatcher


# class TestResource(TestCase):
#
#     def setUp(self):
#         class TestCollection(Collection):
#             meta = {'required': {'number': int}}
#
#         class CreateResource(CreateResourceMixin):
#             collection = TestCollection
#
#         self.create_client = self.client(
#             WSGIDispatcher([CreateResourceMixin]),
#             Response
#         )
#
#     def test_create_creates_resource_if_valid_data(self):
#         response = self.create_client.post('/', data=b'{"number": 1}')
#
#         self.assertEqual(response.status_code, 201)
#         self.assertIsInstance(
#             deserialize(response.get_data(as_text=True)),
#             ObjectId
#         )