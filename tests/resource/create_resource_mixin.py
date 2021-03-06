# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.collection import Collection
from mongorest.resource import CreateResourceMixin
from mongorest.testcase import TestCase
from mongorest.utils import serialize
from mongorest.wrappers import Response
from mongorest.wsgi import WSGIDispatcher


class TestCreateResourceMixin(TestCase):

    def setUp(self):
        class Test(Collection):
            schema = {'test': {'required': True, 'type': 'integer'}}

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

        errors = response.json
        errors['document'].pop('created_at')
        errors['document'].pop('updated_at')

        self.assertEqual(
            errors,
            {
                'error_code': 21,
                'error_type': 'DocumentValidationError',
                'error_message': 'Validation of document from collection \'Test\' failed.',
                'errors': [
                    {
                        'error_code': 23,
                        'error_type': 'RequiredFieldError',
                        'error_message': 'Field \'test\' on collection \'Test\' is required.',
                        'collection': 'Test',
                        'field': 'test',
                    },
                ],
                'collection': 'Test',
                'schema': {'test': {'required': True, 'type': 'integer'}},
                'document': {},
            }
        )

    def test_create_mixin_returns_201_and_created_documents_id(self):
        response = self.create_client.post(
            '/', data=serialize({'test': 1, '_id': 1})
        )

        data = response.json
        data.pop('created_at')
        data.pop('updated_at')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'test': 1, '_id': 1})
        self.assertEqual(self.db.test.find_one({'_id': 1})['test'], 1)
