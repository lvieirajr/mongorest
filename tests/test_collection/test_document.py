# -*- encoding: UTF-8 -*-

from unittest.mock import patch

from mongorest.collection import Collection, Document
from mongorest.testcase import TestCase

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

    def test_process_calls_process_functions(self):
        class TestCollection(Collection):
            def process1(self):
                pass

        with patch.object(TestCollection, 'process1') as process1:
            Document(TestCollection)

            self.assertEqual(process1.call_count, 1)

    