# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from bson.objectid import ObjectId
from mock import patch

from mongorest.collection import Collection
from mongorest.document import Document
from mongorest.testcase import TestCase

__all__ = [
    'TestCollection',
]


class TestCollection(TestCase):

    def setUp(self):
        self.collection = Collection

    # __new__
    def test_new_returns_a_document_object(self):
        self.assertIsInstance(Collection(), Document)

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

    def test_udpate_one_updates_a_document_that_passes_the_filter(self):
        _id = self.collection.insert_one({})

        self.assertIsNone(self.collection.find_one().get('test'))

        self.collection.update_one({'_id': _id}, {'$set': {'test': 'test'}})

        self.assertEqual(self.collection.find_one().get('test'), 'test')

    # update_many
    def test_update_many_is_decorated_with_serializable(self):
        self.assertIn('serializable', self.collection.update_many.decorators)

    def test_udpate_many_updates_all_documents_that_pass_the_filter(self):
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
    def test_get_returns_a_document_object_if_at_least_one_passes_filter(self):
        self.collection.insert_one({'test': 'test'})

        document = self.collection.get({'test': 'test'})

        self.assertIsInstance(document, Document)

    def test_get_returns_none_if_no_documents_pass_the_filter(self):
        self.collection.insert_one({'test': 'test'})

        document = self.collection.get({'test': 'not_test'})

        self.assertIsNone(document)

    # documents
    def test_documents_returns_a_list_of_document_objects_if_at_least_one_passes_filter(self):
        self.collection.insert_many([{'test': 'test'}, {'test': 'test'}])

        documents = self.collection.documents({'test': 'test'})

        self.assertIsInstance(documents, list)
        self.assertEqual(len(documents), 2)

        for document in documents:
            self.assertIsInstance(document, Document)
            self.assertEqual(document.test, 'test')

    def test_documents_returns_empty_list_if_no_documents_pass_the_filter(self):
        self.collection.insert_one({'test': 'test'})

        self.assertEqual(self.collection.documents({'test': 'not_test'}), [])

    def test_restrict_unique_returns_false(self):
        self.assertFalse(self.collection.restrict_unique(None))
        self.assertFalse(self.collection.restrict_unique(1))
        self.assertFalse(self.collection.restrict_unique({}))
        self.assertFalse(self.collection.restrict_unique([]))
        self.assertFalse(self.collection.restrict_unique('test'))

    def test_restrict_update_returns_false(self):
        self.assertFalse(self.collection.restrict_update(None))
        self.assertFalse(self.collection.restrict_update(1))
        self.assertFalse(self.collection.restrict_update({}))
        self.assertFalse(self.collection.restrict_update([]))
        self.assertFalse(self.collection.restrict_update('test'))

    def test_cascade_update_returns_none_and_does_nothing(self):
        self.assertIsNone(self.collection.cascade_update(None))
        self.assertIsNone(self.collection.cascade_update(1))
        self.assertIsNone(self.collection.cascade_update({}))
        self.assertIsNone(self.collection.cascade_update([]))
        self.assertIsNone(self.collection.cascade_update('test'))

    def test_restrict_delete_returns_false(self):
        self.assertFalse(self.collection.restrict_delete(None))
        self.assertFalse(self.collection.restrict_delete(1))
        self.assertFalse(self.collection.restrict_delete({}))
        self.assertFalse(self.collection.restrict_delete([]))
        self.assertFalse(self.collection.restrict_delete('test'))

    def test_cascade_delete_returns_none_and_does_nothing(self):
        self.assertIsNone(self.collection.cascade_delete(None))
        self.assertIsNone(self.collection.cascade_delete(1))
        self.assertIsNone(self.collection.cascade_delete({}))
        self.assertIsNone(self.collection.cascade_delete([]))
        self.assertIsNone(self.collection.cascade_delete('test'))
