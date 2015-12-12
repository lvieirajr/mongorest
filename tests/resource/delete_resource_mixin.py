# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.resource import DeleteResourceMixin
from mongorest.testcase import TestCase
from mongorest.wrappers import Response
from mongorest.wsgi import WSGIDispatcher


class TestDeleteResourceMixin(TestCase):

    def setUp(self):
        self.delete_client = self.client(
            WSGIDispatcher(resources=[DeleteResourceMixin]),
            Response
        )

    def test_delete_mixin_rule(self):
        rules = DeleteResourceMixin.rules

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/<_id>/')
        self.assertEqual(rules[0].methods, set(['DELETE']))
        self.assertEqual(rules[0].endpoint, 'delete')

    def test_delete_mixin_url_map(self):
        urls = list(DeleteResourceMixin.url_map.iter_rules())

        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].rule, '/<_id>/')
        self.assertEqual(urls[0].methods, set(['DELETE']))
        self.assertEqual(urls[0].endpoint, 'delete')

    def test_delete_mixin_returns_not_found_if_no_document_matches_id(self):
        response = self.delete_client.delete('/1/')

        self.assertEqual(response.status_code, 404)
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

    def test_delete_deletes_and_returns_deleted_document(self):
        self.db.collection.insert_one({'_id': 1})

        self.assertIsNotNone(self.db.collection.find_one({'_id': 1}))

        response = self.delete_client.delete('/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'_id': 1})
        self.assertIsNone(self.db.collection.find_one({'_id': 1}))
