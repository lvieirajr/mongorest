# -*- encoding: UTF-8 -*-

from bson.objectid import ObjectId

from mongorest.collection import Collection, Document
from mongorest.testcase import TestCase
from mongorest.utils import serialize

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
    def test_find_one_returns_null_if_no_document_passes_filter_and_serialized(self):
        document = {'_id': ObjectId()}
        self.collection.insert_one(document)

        found_document = self.collection.find_one(
            {'_id': 'test'}, serialized=True
        )

        self.assertEqual('null', found_document)

    def test_find_one_returns_none_if_no_document_passes_filter_and_not_serialized(self):
        document = {'_id': ObjectId()}
        self.collection.insert_one(document)

        found_document = self.collection.find_one(
            {'_id': 'test'}, serialized=False
        )

        self.assertIsNone(found_document)

    def test_find_one_returns_non_serialized_dict_if_not_serialized(self):
        document = {'_id': ObjectId()}
        self.collection.insert_one(document)

        found_document = self.collection.find_one({}, serialized=False)

        self.assertEqual(document, found_document)

    def test_find_one_returns_serialized_dict_if_serialized(self):
        document = {'_id': ObjectId()}
        self.collection.insert_one(document)

        found_document = self.collection.find_one({}, serialized=True)

        self.assertEqual(serialize(document), found_document)

    # find
    def test_find_returns_serialized_empty_list_if_no_document_passes_filter_and_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.find(
            {'_id': 'test'}, serialized=True
        )

        self.assertEqual('[]', found_documents)

    def test_find_returns_empty_list_if_no_document_passes_filter_and_not_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.find(
            {'_id': 'test'}, serialized=False
        )

        self.assertEqual([], found_documents)

    def test_find_returns_non_serialized_dicts_if_not_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.find({}, serialized=False)

        self.assertEqual(documents, found_documents)

    def test_find_returns_serialized_dicts_if_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.find({}, serialized=True)

        self.assertEqual(serialize(documents), found_documents)

    # aggregate
    def test_aggregate_returns_serialized_empty_list_if_pipeline_results_in_nothing_and_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.aggregate(
            [{'$match': {'_id': 'test'}}], serialized=True
        )

        self.assertEqual('[]', found_documents)

    def test_aggregate_returns_empty_list_if_pipeline_results_in_nothing_and_not_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.aggregate(
            [{'$match': {'_id': 'test'}}], serialized=False
        )

        self.assertEqual([], found_documents)

    def test_aggregate_returns_non_serialized_dicts_if_not_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.aggregate([], serialized=False)

        self.assertEqual(documents, found_documents)

    def test_aggregate_returns_serialized_dicts_if_serialized_is_true(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.aggregate([], serialized=True)

        self.assertEqual(serialize(documents), found_documents)

    # insert_one
    def test_insert_one_returns_non_serialized_inserted_id_if_not_serialized(self):
        self.assertEqual(self.collection.count(), 0)

        document = {'_id': ObjectId()}
        inserted_id = self.collection.insert_one(document, serialized=False)

        self.assertEqual(self.collection.count(), 1)
        self.assertEqual(document['_id'], inserted_id)

    def test_insert_one_returns_serialized_inserted_id_if_serialized(self):
        self.assertEqual(self.collection.count(), 0)

        document = {'_id': ObjectId()}
        inserted_id = self.collection.insert_one(document, serialized=True)

        self.assertEqual(self.collection.count(), 1)
        self.assertEqual(serialize(document['_id']), inserted_id)

    # insert_many
    def test_insert_many_returns_non_serialized_inserted_ids_if_not_serialized(self):
        self.assertEqual(self.collection.count(), 0)

        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        inserted_ids = self.collection.insert_many(documents, serialized=False)

        self.assertEqual(self.collection.count(), 2)
        self.assertEqual([doc['_id'] for doc in documents], inserted_ids)

    def test_insert_many_returns_serialized_inserted_ids_if_serialized(self):
        self.assertEqual(self.collection.count(), 0)

        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        inserted_ids = self.collection.insert_many(documents, serialized=True)

        self.assertEqual(self.collection.count(), 2)
        self.assertEqual(
            serialize([doc['_id'] for doc in documents]), inserted_ids
        )

    # UPDATE_ONE, UPDATE_MANY, REPLACE_ONE
    # These functions functionalities are not actually being tested here
    # Just if the output is being serialized or not
    # Because the function only calls pymongo's function with the same name
    # The only difference is in the output that will be the raw_result
    # That will be serialized or not, depending on the 'serialized' parameter

    # update_one
    def test_update_one_returns_non_serialized_raw_result_if_not_serialized(self):
        updated = self.collection.update_one(
            {}, {'$set': {'test': 'test'}}, upsert=True, serialized=False
        )

        self.assertIsInstance(updated['upserted'], ObjectId)

    def test_update_one_returns_serialized_raw_result_if_serialized(self):
        updated = self.collection.update_one(
            {}, {'$set': {'test': 'test'}}, upsert=True, serialized=True
        )

        self.assertIsInstance(updated, str)

    # update_many
    def test_update_many_returns_non_serialized_raw_result_if_not_serialized(self):
        updated = self.collection.update_many(
            {}, {'$set': {'test': 'test'}}, upsert=True, serialized=False
        )

        self.assertIsInstance(updated['upserted'], ObjectId)

    def test_update_many_returns_serialized_raw_result_if_serialized(self):
        updated = self.collection.update_many(
            {}, {'$set': {'test': 'test'}}, upsert=True, serialized=True
        )

        self.assertIsInstance(updated, str)

    # replace_one
    def test_replace_one_returns_non_serialized_raw_result_if_not_serialized(self):
        replaced = self.collection.replace_one(
            {}, {'_id': ObjectId()}, upsert=True, serialized=False
        )

        self.assertIsInstance(replaced['upserted'], ObjectId)

    def test_replace_one_returns_serialized_raw_result_if_serialized(self):
        replaced = self.collection.replace_one(
            {}, {'_id': ObjectId()}, upsert=True, serialized=True
        )

        self.assertIsInstance(replaced, str)

    # DELETE_ONE, DELETE_MANY
    # These functions functionalities are not actually being tested here|
    # Only the output, to check if it is really the raw_result dict
    # Instead of pymongo's Result Object

    # delete_one
    def test_delete_one_returns_non_serialized_raw_result_if_not_serialized(self):
        deleted = self.collection.delete_one({}, serialized=False)

        self.assertIsInstance(deleted, dict)

    def test_delete_one_returns_serialized_raw_result_if_serialized(self):
        deleted = self.collection.delete_one({}, serialized=True)

        self.assertIsInstance(deleted, str)

    # delete_many
    def test_delete_many_returns_non_serialized_raw_result_if_not_serialized(self):
        deleted = self.collection.delete_one({}, serialized=False)

        self.assertIsInstance(deleted, dict)

    def test_delete_many_returns_serialized_raw_result_if_serialized(self):
        deleted = self.collection.delete_many({}, serialized=True)

        self.assertIsInstance(deleted, str)

    # count
    def test_count_returns_number_of_documents_that_pass_the_filter(self):
        self.collection.insert_many([{'1': '1'}, {'1': '1'}, {'1': '2'}, {}])

        self.assertEqual(self.collection.count({'1': '1'}), 2)
        self.assertEqual(self.collection.count({'1': '2'}), 1)

    # get
    def test_get_returns_a_document_object_if_at_least_one_passes_filter(self):
        self.collection.insert_one({'test': 'test'})

        document = self.collection.get({'test': 'test'})

        self.assertIsInstance(document, Document)

    def test_get_returns_none_if_no_documents_pass_the_filter(self):
        self.collection.insert_one({'test': 'test'})

        document = self.collection.get({'test': 'not_test'})

        self.assertIsNone(document)
