# -*- encoding: UTF-8 -*-

from werkzeug.wrappers import Response

from mongorest.resource import DeleteResourceMixin
from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIDispatcher
from mongorest.utils import deserialize


class TestDeleteResourceMixin(TestCase):

    def setUp(self):
        self.delete_client = self.client(
            WSGIDispatcher([DeleteResourceMixin]),
            Response
        )

    def test_delete_mixin_rule(self):
        rules = DeleteResourceMixin.rules

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].rule, '/<_id>/')
        self.assertEqual(rules[0].methods, {'DELETE'})
        self.assertEqual(rules[0].endpoint, 'delete')

    def test_delete_mixin_url_map(self):
        urls = list(DeleteResourceMixin.url_map.iter_rules())

        self.assertEqual(len(urls), 1)
        self.assertEqual(urls[0].rule, '/<_id>/')
        self.assertEqual(urls[0].methods, {'DELETE'})
        self.assertEqual(urls[0].endpoint, 'delete')

    def test_delete_returns_error_if_no_document_with_given_id(self):
        response = self.delete_client.delete('/1/')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)),
            {'_id': 'The given _id is not related to a document.'}
        )

    def test_delete_returns_raw_result_of_deletion_if_id_exists(self):
        self.db.collection.insert_one({'_id': 1})

        response = self.delete_client.delete('/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            deserialize(response.get_data(as_text=True)), {'ok': 1, 'n': 1}
        )
        self.assertIsNone(self.db.test.find_one({'_id': 1}))
