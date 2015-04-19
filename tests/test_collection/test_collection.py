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
        self.db.collection.insert_one(document)

        found_document = self.collection.find_one({'_id': 'test'})

        self.assertIsNone(found_document)

    def test_find_one_returns_non_serialized_dict_if_not_serialized(self):
        document = {'_id': ObjectId()}
        self.db.collection.insert_one(document)

        found_document = self.collection.find_one({}, False)

        self.assertEqual(document, found_document)

    def test_find_one_returns_serialized_dict_if_serialized(self):
        document = {'_id': ObjectId()}
        self.db.collection.insert_one(document)

        found_document = self.collection.find_one({}, True)

        self.assertEqual(serialize(document), found_document)

    def test_find_returns_empty_list_if_no_document_passes_filter(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.db.collection.insert_many(documents)

        found_documents = self.collection.find({'_id': 'test'})

        self.assertEqual([], found_documents)

    def test_find_returns_non_serialized_dicts_if_not_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.db.collection.insert_many(documents)

        found_documents = self.collection.find({}, False)

        self.assertEqual(documents, found_documents)

    def test_find_returns_serialized_dicts_if_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.db.collection.insert_many(documents)

        found_documents = self.collection.find({}, True)

        self.assertEqual(serialize(documents), found_documents)

    def test_aggregate_returns_empty_list_if_pipeline_results_in_nothing(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.db.collection.insert_many(documents)

        found_documents = self.collection.aggregate(
            [{'$match': {'_id': 'test'}}]
        )

        self.assertEqual([], found_documents)

    def test_aggregate_returns_non_serialized_dicts_if_not_serialized(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.db.collection.insert_many(documents)

        found_documents = self.collection.aggregate([], False)

        self.assertEqual(documents, found_documents)

    def test_aggregate_returns_serialized_dicts_if_serialized_is_true(self):
        documents = [{'_id': ObjectId()}, {'_id': ObjectId()}]
        self.db.collection.insert_many(documents)

        found_documents = self.collection.aggregate([], True)

        self.assertEqual(serialize(documents), found_documents)
