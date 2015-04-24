# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId
from werkzeug.wrappers import Response

from mongorest.resource import ListResourceMixin
from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIDispatcher


class TestResource(TestCase):

    def setUp(self):
        self.list_client = self.client(
            WSGIDispatcher([ListResourceMixin]),
            Response
        )

    def test_list_resource_mixin_returns_serialized_empty_list_if_no_documents(self):
        response = self.list_client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'[]')

    def test_list_resource_mixin_returns_serialized_documents_if_documents(self):
        self.db.collection.insert_one({
            '_id': ObjectId('0123456789ab0123456789ab')
        })

        response = self.list_client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            '[{"_id": {"$oid": "0123456789ab0123456789ab"}}]'
        )
