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

    def test_collection_meta_sets_correct_collection_and_required_fields(self):
        self.assertEqual(Collection.collection, self.db['collection'])
        self.assertEqual(Collection.required_fields, {})

    def test_new_returns_a_document_object(self):
        self.assertIsInstance(Collection(), Document)

    def test_find_one_returns_none_if_no_document_passes_filter(self):
        document = {'_id': ObjectId()}
        self.collection.insert_one(document)

        found_document = self.collection.find_one({'_id': 'test'})

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

    def test_find_returns_empty_list_if_no_document_passes_filter(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.find({'_id': 'test'})

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

    def test_aggregate_returns_empty_list_if_pipeline_results_in_nothing(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.collection.insert_many(documents)

        found_documents = self.collection.aggregate(
            [{'$match': {'_id': 'test'}}]
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
