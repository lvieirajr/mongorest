# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId
from unittest.mock import patch

from mongorest.collection import Collection, Document
from mongorest.testcase import TestCase
from mongorest.utils import serialize

__all__ = [
    'TestDocument',
]


class TestDocument(TestCase):

    def test_init_sets_correct_collection(self):
        document = Document(Collection)

        self.assertEqual(document._cls, Collection)

    def test_init_sets_correct_fields(self):
        document = Document(Collection, {'test': 'test'})

        self.assertEqual(document._fields, {'test': 'test'})

    @patch('mongorest.collection.Document._validate')
    def test_init_calls_validate(self, validate):
        Document(Collection)

        self.assertEqual(validate.call_count, 1)

    @patch('mongorest.collection.Document._process')
    def test_init_calls_process_if_not_processed(self, process):
        Document(Collection, processed=False)

        self.assertEqual(process.call_count, 1)

    @patch('mongorest.collection.Document._process')
    def test_init_does_not_call_process_if_processed(self, process):
        Document(Collection, processed=True)

        self.assertEqual(process.call_count, 0)

    # __getattr__, __setattr__ and __repr__ are not being formally tested.
    # Their usage on the other tested functions will make sure they work.

    def test_validate_sets_error_if_field_is_not_present_on_document(self):
        class TestCollection(Collection):
            required_fields = {'test': (str, int)}

        document = Document(TestCollection)

        self.assertEqual(len(document._errors), 1)

    def test_validate_sets_error_if_field_has_wrong_type(self):
        class TestCollection(Collection):
            required_fields = {'test': (str, int)}

        document = Document(TestCollection, {'test': 1.1})

        self.assertEqual(len(document._errors), 1)

    def test_process_calls_collections_process_functions(self):
        class TestCollection(Collection):
            def process1(self):
                pass

        with patch.object(TestCollection, 'process1') as process1:
            Document(TestCollection)

            self.assertEqual(process1.call_count, 1)

    def test_fields_returns_non_serialized_fields_if_not_serialized(self):
        document = Document(Collection, {'test': ObjectId()})

        self.assertEqual(document._fields, document.fields(serialized=False))

    def test_fields_returns_serialized_fields_if_serialized(self):
        document = Document(Collection, {'test': ObjectId()})

        self.assertEqual(
            serialize(document._fields), document.fields(serialized=True)
        )

    def test_get_returns_none_if_field_does_not_exist(self):
        document = Document(Collection)

        self.assertIsNone(document.get('test'))

    def test_get_returns_non_serialized_field_if_not_serialized(self):
        document = Document(Collection, {'test': ObjectId()})

        self.assertIsInstance(document.get('test'), ObjectId)

    def test_get_returns_serialized_field_if_serialized(self):
        document = Document(Collection, {'test': ObjectId()})

        self.assertIsInstance(
            document.get('test', serialized=True)['$oid'], str
        )

    def test_errors_returns_documents_errors(self):
        document = Document(Collection)
        document._errors = {'test': 'test'}

        self.assertEqual(document.errors, document._errors)

    def test_is_valid_returns_true_if_no_errors(self):
        document = Document(Collection)

        self.assertTrue(document.is_valid)

    def test_is_valid_returns_false_if_there_are_errors(self):
        document = Document(Collection)
        document._errors = {'test': 'test'}

        self.assertFalse(document.is_valid)

    def test_pk_returns_the_non_serialized__id(self):
        document = Document(Collection, {'_id': ObjectId()})

        self.assertEqual(document.pk, document.get('_id', serialized=False))
