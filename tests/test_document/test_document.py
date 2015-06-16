# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six

from bson.objectid import ObjectId
from mock import patch

from mongorest.collection import Collection
from mongorest.document import Document
from mongorest.testcase import TestCase

__all__ = [
    'TestDocument',
]


class TestDocument(TestCase):

    # __init__
    def test_init_sets_correct_collection_if_inherits_from_collection(self):
        document = Document(Collection)

        self.assertEqual(document._collection, Collection)

    def test_init_raises_error_if_collection_does_not_inherit_from_collection(self):
        with self.assertRaises(AttributeError):
            Document(Document)

    def test_init_sets_correct_fields(self):
        document = Document(Collection, {'test': 'test'})

        self.assertEqual(document._fields, {'test': 'test'})

    @patch('mongorest.document.Document._validate')
    def test_init_calls_validate(self, validate):
        Document(Collection)

        self.assertEqual(validate.call_count, 1)

    @patch('mongorest.document.Document._process')
    def test_init_calls_process_if_not_processed(self, process):
        Document(Collection, processed=False)

        self.assertEqual(process.call_count, 1)

    @patch('mongorest.document.Document._process')
    def test_init_does_not_call_process_if_processed(self, process):
        Document(Collection, processed=True)

        self.assertEqual(process.call_count, 0)

    # __getattr__ is not being formally tested.
    # Its usage on the other tested functions will make sure it works.

    def test_set_attr_correctly_sets__errors(self):
        document = Document(Collection)
        document._errors = {'test': 'test'}

        self.assertEqual(document._errors, {'test': 'test'})

    def test_set_attr_correctly_sets__fields(self):
        document = Document(Collection)
        document._fields = {'test': 'test'}

        self.assertEqual(document._fields, {'test': 'test'})

    def test_set_attr_correctly_sets__collection(self):
        document = Document(Collection)

        class TestCollection(Collection):
            pass

        document._collection = TestCollection

        self.assertEqual(document._collection, TestCollection)

    def test_set_attr_correctly_sets_field(self):
        document = Document(Collection)
        document.test = 1

        self.assertEqual(document._fields['test'], 1)

    def test_repr_returns_correct_representation_of_the_document(self):
        document = Document(Collection)

        self.assertEqual(
            document.__repr__(),
            '<Document<Collection> object at {0}>'.format(hex(id(document)))
        )

    # _validate
    def test_validate_sets_error_if_required_field_is_not_present_on_document(self):
        class TestCollection(Collection):
            meta = {
                'required': {'test': six.string_types + six.integer_types},
                'optional': {}
            }

        document = Document(TestCollection)

        self.assertEqual(len(document.errors), 1)

    def test_validate_sets_error_if_required_field_has_wrong_type(self):
        class TestCollection(Collection):
            meta = {
                'required': {'test': six.string_types + six.integer_types},
                'optional': {}
            }

        document = Document(TestCollection, {'test': 1.1})

        self.assertEqual(len(document.errors), 1)

    def test_validate_sets_error_if_optional_field_has_wrong_type(self):
        class TestCollection(Collection):
            meta = {
                'required': {},
                'optional': {'test': ObjectId}
            }

        document = Document(TestCollection, {'test': 1.1})

        self.assertEqual(len(document.errors), 1)

    # _process
    def test_process_calls_collections_process_functions(self):
        class TestCollection(Collection):
            def process1(self):
                pass

        with patch.object(TestCollection, 'process1') as process1:
            Document(TestCollection)

            self.assertEqual(process1.call_count, 1)

    # is_valid
    def test_is_valid_returns_true_if_no_errors(self):
        document = Document(Collection)
        document._errors = {}

        self.assertTrue(Document(Collection).is_valid)

    def test_is_valid_returns_false_if_there_are_errors(self):
        document = Document(Collection)
        document._errors = {'test': 'test'}

        self.assertFalse(document.is_valid)

    # fields
    def test_fields_returns_empty_dict_if_no_fields(self):
        document = Document(Collection, {})

        self.assertEqual({}, document.fields)

    def test_fields_returns_documents_fields(self):
        document = Document(Collection, {'test': ObjectId()})

        self.assertEqual(document._fields, document.fields)

    # errors
    def test_errors_returns_empty_dict_if_no_errors(self):
        document = Document(Collection, {})
        document._errors = {}

        self.assertEqual({}, document.errors)

    def test_errors_returns_documents_errors(self):
        class TestCollection(Collection):
            meta = {
                'required': {'test': six.string_types + six.integer_types},
                'optional': {}
            }

        document = Document(TestCollection, {'test': ObjectId()})

        self.assertEqual(document._errors, document.errors)

    # save
    def test_save_returns_errors_if_document_is_not_valid(self):
        class TestCollection(Collection):
            meta = {
                'required': {'test': six.string_types},
                'optional': {}
            }

        errors = Document(TestCollection).save()

        self.assertEqual(errors, {'test': 'Field \'test\' is required.'})

    def test_save_returns_errors_if_error_ocurred_during_save(self):
        Collection.collection.create_index('test', unique=True)
        Collection.insert_one({'test': 'test'})

        document = Document(Collection)
        document.test = 'test'
        errors = document.save()

        self.assertIsInstance(errors['save'], six.string_types)

        Collection.collection.drop_index('test_1')

    def test_save_returns__id_if_document_does_not_have_id_and_is_valid(self):
        document = Document(Collection)
        _id = document.save()

        self.assertEqual(_id, document._id)

    def test_save_returns__id_if_document_has_id_and_is_valid(self):
        document = Document(Collection)
        document._id = ObjectId()
        _id = document.save()

        self.assertEqual(_id, document._id)
