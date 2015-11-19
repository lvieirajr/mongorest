# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.objectid import ObjectId
from mock import patch

from mongorest.collection import Collection
from mongorest.errors import *
from mongorest.testcase import TestCase
from mongorest.validation import Validator

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

        document = Collection()

        self.assertTrue(self.validator.validate_document(document))
        self.assertEqual(self.validator.errors, {})

    def test_validate_returns_false_if_errors_are_found(self):
        self.validator.schema = {'test': {'type': 'objectid'}}

        document = Collection({'test': 'test'})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            self.validator.errors, {'test': 'must be of ObjectId type'}
        )

    def test_validate_sets_correct_errors_on_document_if_unknown_field_error(self):
        self.validator.allow_unknown = False
        self.validator.schema = {}

        document = Collection({'test': '1'})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={},
                errors=[
                    UnknownFieldError(collection='Collection', field='test')
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_required_field_error(self):
        self.validator.schema = {'test': {'required': True}}

        document = Collection({})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={
                    'test': {'required': True}
                }, errors=[
                    RequiredFieldError(collection='Collection', field='test')
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_read_only_field_error(self):
        self.validator.schema = {'test': {'readonly': True}}

        document = Collection({'test': 'test'})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={
                    'test': {'readonly': True}
                }, errors=[
                    ReadOnlyFieldError(collection='Collection', field='test')
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_field_type_error(self):
        self.validator.schema = {'test': {'type': 'integer'}}

        document = Collection({'test': 'test'})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={
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
        self.validator.schema = {'test': {'type': 'string', 'regex': '[a-z]+'}}

        document = Collection({'test': '123456'})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={
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
        self.validator.schema = {'test': {'type': 'string', 'minlength': 3}}

        document = Collection({'test': '12'})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={
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
        self.validator.schema = {'test': {'type': 'string', 'maxlength': 3}}

        document = Collection({'test': '1234'})

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={
                    'test': {'type': 'string', 'maxlength': 3}
                }, errors=[
                    MaxLengthError(
                        collection='Collection', field='test',
                        max_length=3
                    )
                ]
            )
        )

    def test_validate_sets_correct_errors_on_document_if_more_than_one_error(self):
        self.validator.schema = {
            'test1': {'required': True}, 'test2': {'required': True},
        }

        document = Collection()

        self.assertFalse(self.validator.validate_document(document))
        self.assertEqual(
            document.errors,
            DocumentValidationError(
                collection='Collection', document=document.fields, schema={
                    'test1': {'required': True}, 'test2': {'required': True}
                }, errors=[
                    RequiredFieldError(collection='Collection', field='test1'),
                    RequiredFieldError(collection='Collection', field='test2')
                ]
            )
        )

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
