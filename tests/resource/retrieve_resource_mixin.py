# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.resource import RetrieveResourceMixin
from mongorest.testcase import TestCase
from mongorest.wrappers import Response
from mongorest.wsgi import WSGIDispatcher


class TestRetrieveResourceMixin(TestCase):

    def setUp(self):
        self.retrieve_client = self.client(
            WSGIDispatcher(resources=[RetrieveResourceMixin]),
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

    def test_retrieve_mixin_returns_not_found_if_no_document_matches_id(self):
        response = self.retrieve_client.get('/1/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json,
            {
                'error_code': 12,
                'error_type': 'DocumentNotFoundError',
                'error_message': '1 is not a valid _id for a document from collection \'Collection\'.',
                'collection': 'Collection',
                '_id': 1,
            }
        )

    def test_retrieve_mixin_returns_document_containing_given_id(self):
        self.db.collection.insert_one({'_id': 1})

        response = self.retrieve_client.get('/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {'_id': 1}
        )
