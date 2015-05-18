# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from werkzeug.wrappers import Response

from mongorest.resource import DocumentsResourceMixin
from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIDispatcher
from mongorest.utils import deserialize


class TestDocumentsResourceMixin(TestCase):

    def setUp(self):
        self.documents_client = self.client(
            WSGIDispatcher([DocumentsResourceMixin]),
            Response
        )

    def test_documents_mixin_rule(self):
        rules = DocumentsResourceMixin.rules

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/documents/')
        self.assertEqual(rules[0].methods, set(['GET', 'HEAD']))
        self.assertEqual(rules[0].endpoint, 'documents')

    def test_documents_mixin_url_map(self):
        urls = list(DocumentsResourceMixin.url_map.iter_rules())

        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].rule, '/documents/')
        self.assertEqual(urls[0].methods, set(['GET', 'HEAD']))
        self.assertEqual(urls[0].endpoint, 'documents')

    def test_documents_mixin_returns_empty_list_if_no_documents_in_collection(self):
        response = self.documents_client.get('/documents/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)), []
        )

    def test_documents_mixin_returns_list_of_collection_documents(self):
        self.db.collection.insert_one({'_id': 1, 'test': 'test1'})
        self.db.collection.insert_one({'_id': 2, 'test': 'test2'})

        response = self.documents_client.get('/documents/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            [{'_id': 1, 'test': 'test1'}, {'_id': 2, 'test': 'test2'}]
        )
