# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from werkzeug.wrappers import Response

from mongorest.resource import ListResourceMixin
from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIDispatcher
from mongorest.utils import deserialize


class TestListResourceMixin(TestCase):

    def setUp(self):
        self.documents_client = self.client(
            WSGIDispatcher(resources=[ListResourceMixin]),
            Response
        )

    def test_list_mixin_rule(self):
        rules = ListResourceMixin.rules

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/')
        self.assertEqual(rules[0].methods, set(['GET', 'HEAD']))
        self.assertEqual(rules[0].endpoint, 'list')

    def test_list_mixin_url_map(self):
        urls = list(ListResourceMixin.url_map.iter_rules())

        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].rule, '/')
        self.assertEqual(urls[0].methods, set(['GET', 'HEAD']))
        self.assertEqual(urls[0].endpoint, 'list')

    def test_list_mixin_returns_empty_list_if_no_documents_in_collection(self):
        response = self.documents_client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)), []
        )

    def test_list_mixin_returns_list_of_all_collection_documents_if_no_filter(self):
        self.db.collection.insert_one({'_id': 1, 'test': 'test1'})
        self.db.collection.insert_one({'_id': 2, 'test': 'test2'})

        response = self.documents_client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            [{'_id': 1, 'test': 'test1'}, {'_id': 2, 'test': 'test2'}]
        )

    def test_list_mixin_returns_list_of_collection_documents_that_pass_filter(self):
        self.db.collection.insert_one({'_id': 1, 'test': 'test1', 'number': 1})
        self.db.collection.insert_one({'_id': 2, 'test': 'test2', 'number': 1})

        response = self.documents_client.get('/?match={"number": 1, "test": "test1"}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            [{'_id': 1, 'test': 'test1', 'number': 1}]
        )

    def test_list_mixin_returns_list_of_collection_documents_that_pass_filter_with_only_specified_fields(self):
        self.db.collection.insert_one({'_id': 1, 'test': 'test1', 'number': 1})
        self.db.collection.insert_one({'_id': 2, 'test': 'test2', 'number': 1})

        response = self.documents_client.get('/?match={"number": 1, "test": "test1"}&project={"test": 1, "_id": 1}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            [{'_id': 1, 'test': 'test1'}]
        )

    def test_list_mixin_returns_list_of_collection_documents_sorted_by_given_sort_keys(self):
        self.db.collection.insert_one({'_id': 1, 'test': 1, 'number': 1})
        self.db.collection.insert_one({'_id': 2, 'test': 1, 'number': 2})
        self.db.collection.insert_one({'_id': 3, 'test': 2, 'number': 2})

        response = self.documents_client.get('/?sort={"number": -1, "test": 1}&project={"number": 1, "test": 1, "_id": 0}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            [
                {'number': 2, 'test': 1}, {'number': 2, 'test': 2},
                {'number': 1, 'test': 1}
            ]
        )
