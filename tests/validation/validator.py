# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.objectid import ObjectId
from mock import patch

from mongorest.collection import Collection
from mongorest.validation import Validator
from mongorest.testcase import TestCase

__all__ = [
    'TestValidator',
]


class TestValidator(TestCase):

    def setUp(self):
        self.validator = Validator()

    def test_validate_type_objectid_sets_error_if_not_objectid(self):
        self.validator.schema = {'test': {'type': 'objectid'}}
        self.validator.validate_document(Collection({'test': 1}))

        self.assertEqual(
            self.validator.errors, {'test': 'must be of ObjectId type'}
        )

    def test_validate_type_objectid_does_not_set_error_if_type_is_correct(self):
        self.validator.schema = {'test': {'type': 'objectid'}}
        self.validator.validate_document(Collection({'test': ObjectId()}))

        self.assertEqual(self.validator.errors, {})

    def test_validate_returns_true_if_no_errors_are_found(self):
        self.validator.schema = {}

        self.assertTrue(
            self.validator.validate_document(Collection({'test': ObjectId()}))
        )
        self.assertEqual(self.validator.errors, {})

    @patch('mongorest.validation.Validator.flatten')
    def test_flattened_errors_returns_flaten_call(self, flatten):
        with self.validator.flattened_errors:
            flatten.assert_called_once_with({}, '', '.')

    def test_flatten_returns_flattened_dict(self):
        flattened = self.validator.flatten({
            'outter1': {'inner': 'test'}, 'outter2': 'test'
        })

        self.assertEqual(
            flattened, {'outter1.inner': 'test', 'outter2': 'test'}
        )

    def test_get_field_schema_returns_schema_of_outer_field(self):
        self.validator.schema = {'test': {'required': True}}

        self.assertEqual(
            self.validator.get_field_schema('test'), {'required': True}
        )

    def test_get_field_schema_returns_schema_of_inner_field(self):
        self.validator.schema = {
            'test': {
                'type': 'dict', 'schema': {
                    'test': {'required': True}
                }
            }
        }

        self.assertEqual(
            self.validator.get_field_schema('test.test'), {'required': True}
        )

