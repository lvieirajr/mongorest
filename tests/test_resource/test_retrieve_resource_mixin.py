# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from werkzeug.wrappers import Response

from mongorest.resource import RetrieveResourceMixin
from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIDispatcher
from mongorest.utils import deserialize


class TestRetrieveResourceMixin(TestCase):

    def setUp(self):
        self.retrieve_client = self.client(
            WSGIDispatcher([RetrieveResourceMixin]),
            Response
        )

    def test_retrieve_mixin_rule(self):
        rules = RetrieveResourceMixin.rules

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/<_id>/')
        self.assertEqual(rules[0].methods, set(['GET', 'HEAD']))
        self.assertEqual(rules[0].endpoint, 'retrieve')

    def test_retrieve_mixin_url_map(self):
        urls = list(RetrieveResourceMixin.url_map.iter_rules())

        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].rule, '/<_id>/')
        self.assertEqual(urls[0].methods, set(['GET', 'HEAD']))
        self.assertEqual(urls[0].endpoint, 'retrieve')

    def test_retrieve_mixin_returns_none_if_no_document_matches_id(self):
        response = self.retrieve_client.get('/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            None
        )

    def test_retrieve_mixin_returns_document_containing_given_id(self):
        self.db.collection.insert_one({'_id': 1})

        response = self.retrieve_client.get('/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            {'_id': 1}
        )
