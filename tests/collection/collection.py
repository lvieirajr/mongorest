# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.objectid import ObjectId
from mock import patch

from mongorest.collection import Collection
from mongorest.testcase import TestCase

__all__ = [
    'TestCollection',
]


class TestCollection(TestCase):

    def setUp(self):
        self.collection = Collection

    # __init__
    def test_init_sets_correct_fields(self):
        document = Collection({'test': 'test'})

        self.assertEqual(document.document, {'test': 'test'})

    @patch('mongorest.collection.Collection.before_validation')
    def test_init_calls_before_validation(self, before_validation):
        self.collection()

        self.assertEqual(before_validation.call_count, 1)

    @patch('mongorest.collection.Collection.after_validation')
    def test_init_calls_after_validation_if_validation_fails(self, after_validation):
        self.collection.schema = {'test': {'required': True}}
        self.collection()
        self.collection.schema = {}

        self.assertEqual(after_validation.call_count, 1)

    @patch('mongorest.collection.Collection.after_validation_failed')
    def test_init_calls_after_validation_failed_if_validation_fails_and_after_validation_returns_none(self, after_validation_failed):
        self.collection.schema = {'test': {'required': True}}
        self.collection()
        self.collection.schema = {}

        self.assertEqual(after_validation_failed.call_count, 1)

    @patch('mongorest.collection.Collection.after_validation')
    def test_init_calls_after_validation_if_validation_succeeds(self, after_validation):
        self.collection()

        self.assertEqual(after_validation.call_count, 1)

    @patch('mongorest.collection.Collection.after_validation_succeeded')
    def test_init_calls_after_validation_succeeded_if_validation_succeeds_and_after_validation_returns_none(self, after_validation_succeeded):
        self.collection()

        self.assertEqual(after_validation_succeeded.call_count, 1)

    # find_one
    def test_find_one_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.find_one.decorators)

    def test_find_one_returns_none_if_no_document_passes_the_filter(self):
        self.assertIsNone(self.collection.find_one('test'))

    def test_find_one_returns_document_dict_if_any_document_passes_the_filter(self):
        self.collection.insert_one({})
        document = self.collection.find_one({})

        self.assertIsInstance(document, dict)
        self.assertIsNotNone(document.get('_id'))

    # find
    def test_find_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.find.decorators)

    def test_find_returns_empty_list_if_no_documents_pass_the_filter(self):
        self.assertEqual(self.collection.find({}), [])

    def test_find_returns_list_of_documents_that_passed_the_filter(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        self.assertEqual(self.collection.find({}), documents)

    # aggregate
    def test_aggregate_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.aggregate.decorators)

    def test_aggregate_returns_empty_list_if_no_document_returns_from_the_pipeline(self):
        self.assertEqual(self.collection.aggregate([]), [])

    def test_aggregate_returns_list_of_documents_that_result_from_the_pipeline(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        self.assertEqual(self.collection.aggregate([]), documents)

    # insert_one
    def test_insert_one_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.insert_one.decorators)

    def test_insert_one_inserts_document_into_the_collection(self):
        self.assertEqual(self.collection.count(), 0)

        self.collection.insert_one({})

        self.assertEqual(self.collection.count(), 1)

    # insert_many
    def test_insert_many_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.insert_many.decorators)

    def test_insert_many_inserts_documents_into_the_collection(self):
        self.assertEqual(self.collection.count(), 0)

        self.collection.insert_many([{}, {}, {}])

        self.assertEqual(self.collection.count(), 3)

    # update_one
    def test_update_one_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.update_one.decorators)

    def test_update_one_updates_a_document_that_passes_the_filter(self):
        _id = self.collection.insert_one({})

        self.assertIsNone(self.collection.find_one().get('test'))

        self.collection.update_one({'_id': _id}, {'$set': {'test': 'test'}})

        self.assertEqual(self.collection.find_one().get('test'), 'test')

    # update_many
    def test_update_many_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.update_many.decorators)

    def test_update_many_updates_all_documents_that_pass_the_filter(self):
        self.collection.insert_many([{}, {}, {}])

        for document in self.collection.find():
            self.assertIsNone(document.get('test'))

        self.collection.update_many({}, {'$set': {'test': 'test'}})

        for document in self.collection.find():
            self.assertEqual(document.get('test'), 'test')

    # replace_one
    def test_replace_one_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.replace_one.decorators)

    def test_replace_one_replaces_a_document_that_passes_the_filter(self):
        _id = self.collection.insert_one({})

        self.assertIsNone(self.collection.find_one().get('test'))

        self.collection.replace_one({'_id': _id}, {'_id': _id, 'test': 'test'})

        self.assertEqual(self.collection.find_one().get('test'), 'test')

    # delete_one
    def test_delete_one_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.delete_one.decorators)

    def test_delete_one_deletes_a_single_document_that_passes_the_filter(self):
        self.collection.insert_many([{}, {}, {}])

        self.assertEqual(self.collection.count(), 3)

        self.collection.delete_one({})

        self.assertEqual(self.collection.count(), 2)

    # delete_many
    def test_replace_many_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.delete_many.decorators)

    def test_delete_many_deletes_all_documents_that_pass_the_filter(self):
        self.collection.insert_many([{}, {}, {}])

        self.assertEqual(self.collection.count(), 3)

        self.collection.delete_many({})

        self.assertEqual(self.collection.count(), 0)

    # count
    def test_count_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.count.decorators)

    def test_count_returns_number_of_documents_that_pass_the_filter(self):
        self.collection.insert_many([{'1': '1'}, {'1': '1'}, {'1': '2'}, {}])

        self.assertEqual(self.collection.count({'1': '1'}), 2)
        self.assertEqual(self.collection.count({'1': '2'}), 1)
        self.assertEqual(self.collection.count(), 4)

    # get
    def test_get_returns_a_collection_object_if_at_least_one_passes_filter(self):
        self.collection.insert_one({'test': 'test'})

        document = self.collection.get({'test': 'test'})

        self.assertIsInstance(document, Collection)

    def test_get_returns_none_if_no_documents_pass_the_filter(self):
        self.collection.insert_one({'test': 'test'})

        document = self.collection.get({'test': 'not_test'})

        self.assertIsNone(document)

    # documents
    def test_documents_returns_a_list_of_collection_objects_if_at_least_one_passes_filter(self):
        self.collection.insert_many([{'test': 'test'}, {'test': 'test'}])

        documents = self.collection.documents({'test': 'test'})

        self.assertIsInstance(documents, list)
        self.assertEqual(len(documents), 2)

        for document in documents:
            self.assertIsInstance(document, Collection)
            self.assertEqual(document.test, 'test')

    def test_documents_returns_empty_list_if_no_documents_pass_the_filter(self):
        self.collection.insert_one({'test': 'test'})

        self.assertEqual(self.collection.documents({'test': 'not_test'}), [])

    def test_before_validation_returns_none(self):
        self.assertIsNone(self.collection().before_validation())

    def test_after_validation_returns_none(self):
        self.assertIsNone(self.collection().after_validation())

    def test_after_validation_failed_returns_none(self):
        self.assertIsNone(self.collection().after_validation_failed())

    def test_after_validation_succeeded_returns_none(self):
        self.assertIsNone(self.collection().after_validation_succeeded())

    def test_before_save_returns_none(self):
        self.assertIsNone(self.collection().before_save())

    def test_after_save_returns_none(self):
        self.assertIsNone(self.collection().after_save())

    def test_before_update_returns_none(self):
        self.assertIsNone(self.collection().before_update(self.collection()))

    def test_after_update_returns_none(self):
        self.assertIsNone(self.collection().after_update(self.collection()))

    def test_before_delete_returns_none(self):
        self.assertIsNone(self.collection().before_delete())

    def test_after_delete_returns_none(self):
        self.assertIsNone(self.collection().after_delete())
