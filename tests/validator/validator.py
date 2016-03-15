# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.objectid import ObjectId
from mock import patch

from mongorest.collection import Collection
from mongorest.errors import *
from mongorest.testcase import TestCase
from mongorest.validator import Validator

__all__ = [
    'TestValidator',
]


class TestValidator(TestCase):

    def setUp(self):
        self.validator = Validator()

    def test_validate_type_objectid_sets_error_if_not_objectid(self):
        document = Collection({'test': 1})
        document.schema = {'test': {'type': 'objectid'}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            self.validator.errors, {'test': 'must be of ObjectId type'}
        )

    def test_validate_type_objectid_does_not_set_error_if_type_is_correct(self):
        document = Collection({'test': ObjectId()})
        document.schema = {'test': {'type': 'objectid'}}

        self.assertTrue(self.validator.validate_document(document))
        self.assertEqual(self.validator.errors, {})

    def test_validate_returns_true_if_no_errors_are_found(self):
        document = Collection()
        document.schema = {}

        self.assertTrue(self.validator.validate_document(document))
        self.assertEqual(self.validator.errors, {})

    def test_validate_returns_false_if_errors_are_found(self):
        document = Collection({'test': 'test'})
        document.schema = {'test': {'type': 'objectid'}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            self.validator.errors, {'test': 'must be of ObjectId type'}
        )

    def test_validate_sets_correct_errors_on_document_if_unknown_field_error(self):
        document = Collection({'test': '1'})
        document.schema = {}
        self.validator.allow_unknown = False

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={},
                errors=[
                    UnknownFieldError(collection='Collection', field='test')
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_required_field_error(self):
        document = Collection({})
        document.schema = {'test': {'required': True}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'required': True}
                }, errors=[
                    RequiredFieldError(collection='Collection', field='test')
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_read_only_field_error(self):
        document = Collection({'test': 'test'})
        document.schema = {'test': {'readonly': True}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'readonly': True}
                }, errors=[
                    ReadOnlyFieldError(collection='Collection', field='test')
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_field_type_error(self):
        document = Collection({'test': 'test'})
        document.schema = {'test': {'type': 'integer'}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'integer'}
                }, errors=[
                    FieldTypeError(
                        collection='Collection', field='test',
                        field_type='integer'
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_regex_match_error(self):
        document = Collection({'test': '123456'})
        document.schema = {'test': {'type': 'string', 'regex': '[a-z]+'}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'string', 'regex': '[a-z]+'}
                }, errors=[
                    RegexMatchError(
                        collection='Collection', field='test',
                        regex='[a-z]+'
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_min_length_error(self):
        document = Collection({'test': '12'})
        document.schema = {'test': {'type': 'string', 'minlength': 3}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'string', 'minlength': 3}
                }, errors=[
                    MinLengthError(
                        collection='Collection', field='test',
                        min_length=3
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_max_length_error(self):
        document = Collection({'test': '1234'})
        document.schema = {'test': {'type': 'string', 'maxlength': 3}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'string', 'maxlength': 3}
                }, errors=[
                    MaxLengthError(
                        collection='Collection', field='test',
                        max_length=3
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_length_error(self):
        document = Collection({'test': ['test', 'test']})
        document.schema = {
            'test': {'type': 'list', 'items': [{'type': 'string'}]}
        }

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'list', 'items': [{'type': 'string'}]}
                }, errors=[
                    LengthError(
                        collection='Collection', field='test', length=1
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_value_not_allowed_error(self):
        document = Collection({'test': 'not_test'})
        document.schema = {
            'test': {'type': 'string', 'allowed': ['test']}
        }

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'string', 'allowed': ['test']}
                }, errors=[
                    ValueNotAllowedError(
                        collection='Collection', field='test', value='not_test'
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_values_not_allowed_error(self):
        document = Collection({'test': ['not_test', 'test']})
        document.schema = {
            'test': {'type': 'list', 'allowed': ['test']}
        }

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'list', 'allowed': ['test']}
                }, errors=[
                    ValuesNotAllowedError(
                        collection='Collection', field='test',
                        values='[\'not_test\']'
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_min_value_error(self):
        document = Collection({'test': 0})
        document.schema = {'test': {'type': 'integer', 'min': 10}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'integer', 'min': 10}
                }, errors=[
                    MinValueError(
                        collection='Collection', field='test',
                        min_value=10
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_max_value_error(self):
        document = Collection({'test': 11})
        document.schema = {'test': {'type': 'integer', 'max': 10}}

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test': {'type': 'integer', 'max': 10}
                }, errors=[
                    MaxValueError(
                        collection='Collection', field='test',
                        max_value=10
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_more_than_one_error(self):
        document = Collection({'test2': 1})
        document.schema = {
            'test1': {'required': True}, 'test2': {'type': ['list', 'string']},
        }

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.document, schema={
                    'test1': {'required': True}, 'test2': {'type': ['list', 'string']}
                }, errors=[
                    RequiredFieldError(collection='Collection', field='test1'),
                    FieldTypeError(
                        collection='Collection', field='test2',
                        field_type='list or string'
                    )
                ]
            )
        )

    @patch('mongorest.validator.Validator.flatten')
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
            'test': {'type': 'dict', 'schema': {'test': {'required': True}}}
        }

        self.assertEqual(
            self.validator.get_field_schema('test.test'), {'required': True}
        )

    def test_get_field_schema_returns_inner_schema_of_field(self):
        self.validator.schema = {
            'test': {'type': 'list', 'schema': {'type': 'integer'}}
        }

        self.assertEqual(
            self.validator.get_field_schema('test.1'), {'type': 'integer'}
        )
