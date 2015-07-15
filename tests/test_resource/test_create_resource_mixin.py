# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from werkzeug.wrappers import Response

from mongorest.collection import Collection
from mongorest.resource import CreateResourceMixin
from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIDispatcher
from mongorest.utils import deserialize, serialize


class TestCreateResourceMixin(TestCase):

    def setUp(self):
        class Test(Collection):
            meta = {'required': {'test': six.integer_types}}

        class TestCollectionCreate(CreateResourceMixin):
            collection = Test

        self.create_client = self.client(
            WSGIDispatcher(resources=[TestCollectionCreate]),
            Response
        )

    def test_create_mixin_rule(self):
        rules = CreateResourceMixin.rules

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/')
        self.assertEqual(rules[0].methods, set(['POST']))
        self.assertEqual(rules[0].endpoint, 'create')

    def test_create_mixin_url_map(self):
        urls = list(CreateResourceMixin.url_map.iter_rules())

        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].rule, '/')
        self.assertEqual(urls[0].methods, set(['POST']))
        self.assertEqual(urls[0].endpoint, 'create')

    def test_create_mixin_returns_errors_if_invalid_data(self):
        response = self.create_client.post('/', data=serialize({}))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            {'test': 'Field \'test\' is required.'}
        )

    def test_create_mixin_returns_201_and_created_documents_id(self):
        response = self.create_client.post(
            '/', data=serialize({'test': 1, '_id': 1})
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(deserialize(response.get_data(as_text=True)), 1)
        self.assertEqual(self.db.test.find_one({'_id': 1})['test'], 1)
