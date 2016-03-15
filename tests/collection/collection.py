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

    @patch('mongorest.collection.Collection.after_validation_failed')
    def test_init_does_not_call_after_validation_failed_if_validation_fails_and_after_validation_returns_something(self, after_validation_failed):
        self.collection.schema = {'test': {'required': True}}
        self.collection.after_validation = lambda self: True

        self.collection()

        self.collection.schema = {}
        self.collection.after_validation = lambda self: None



        self.assertEqual(after_validation_failed.call_count, 0)

    @patch('mongorest.collection.Collection.after_validation')
    def test_init_calls_after_validation_if_validation_succeeds(self, after_validation):
        self.collection()

        self.assertEqual(after_validation.call_count, 1)

    @patch('mongorest.collection.Collection.after_validation_succeeded')
    def test_init_calls_after_validation_succeeded_if_validation_succeeds_and_after_validation_returns_none(self, after_validation_succeeded):
        self.collection()

        self.assertEqual(after_validation_succeeded.call_count, 1)

    @patch('mongorest.collection.Collection.after_validation_succeeded')
    def test_init_does_not_call_after_validation_succeeded_if_validation_succeeds_and_after_validation_returns_something(self, after_validation_succeeded):
        self.collection.after_validation = lambda self: True

        self.collection()

        self.collection.after_validation = lambda self: None

        self.assertEqual(after_validation_succeeded.call_count, 0)

    # __setattr__
    def test___setattr____correctly_sets_collection(self):
        document = Collection()

        self.assertEqual(document.collection, self.db['collection'])

        document.collection = self.db['test_collection']

        self.assertEqual(document.collection, self.db['test_collection'])

        document.collection = self.db['collection']

    def test___setattr____correctly_sets_schema(self):
        document = Collection()

        self.assertEqual(document.schema, {})

        document.schema = {'test': {'required': True}}

        self.assertEqual(document.schema, {'test': {'required': True}})

        document.schema = {}

    def test___setattr____correctly_sets_allow_unknown(self):
        document = Collection()

        self.assertEqual(document.allow_unknown, True)

        document.allow_unknown = False

        self.assertEqual(document.allow_unknown, False)

        document.allow_unknown = True

    def test___setattr____correctly_sets__document(self):
        document = Collection()

        self.assertEqual(document._document, {})

        document._document = {'test': 'test'}

        self.assertEqual(document._document, {'test': 'test'})

    def test___setattr____correctly_sets__errors(self):
        document = Collection()

        self.assertEqual(document._errors, {})

        document._errors = {'error': 'error'}

        self.assertEqual(document._errors, {'error': 'error'})

    # __getattr__
    def test___getattr___raises_attribute_error_if_can_not_find_attribute(self):
        with self.assertRaises(AttributeError):
            Collection._()

    # __repr__
    def test___repr___returns_correct_representation_of_the_document(self):
        document = Collection()

        self.assertEqual(
            document.__repr__(),
            '<Document<Collection> object at {0}>'.format(hex(id(document)))
        )

    # document
    def test_document_returns_empty_dict_if_no_fields_on_document(self):
        document = Collection()

        self.assertEqual(document.document, {})

    def test_document_returns_dict_of_fields_from_the_document(self):
        _id = ObjectId()
        document = Collection({'_id': _id})

        self.assertEqual(document.document, {'_id': _id})

    # errors
    def test_errors_returns_empty_dict_if_no_errors_on_document(self):
        document = Collection()

        self.assertEqual(document.errors, {})

    def test_errors_returns_dict_of_errors_from_the_document(self):
        document = Collection()
        document._errors = {'error': 'error'}

        self.assertEqual(document.errors, {'error': 'error'})

    # is_valid
    def test_is_valid_returns_true_if_no_errors_on_document(self):
        document = Collection()

        self.assertTrue(document.is_valid)

    def test_is_valid_returns_false_if_document_has_errors(self):
        document = Collection()
        document._errors = {'error': 'error'}

        self.assertFalse(document.is_valid)

    # insert
    def test_insert_is_decorated_with_serializable(self):
        self.assertIn('serializable', Collection.insert.decorators)

    def test_insert_returns_errors_if_document_is_not_valid(self):
        Collection.schema = {'test': {'required': True}}
        errors = Collection().insert()
        Collection.schema = {}

        self.assertEqual(
            errors,
            {
                'error_code': 21,
                'error_type': 'DocumentValidationError',
                'error_message': 'Validation of document from collection \'Collection\' failed.',
                'errors': [
                    {
                        'error_code': 23,
                        'error_type': 'RequiredFieldError',
                        'error_message': 'Field \'test\' on collection \'Collection\' is required.',
                        'collection': 'Collection',
                        'field': 'test',
                    },
                ],
                'collection': 'Collection',
                'schema': {'test': {'required': True}},
                'document': {},
            }
        )

    def test_insert_returns_errors_if_error_ocurred_during_save(self):
        Collection.collection.create_index('test', unique=True)
        Collection.insert_one({'test': 'test'})

        errors = Collection({'test': 'test'}).insert()

        self.assertEqual(errors['error_code'], 0)
        self.assertEqual(errors['error_type'], 'PyMongoError')

        Collection.drop_index('test_1')

    def test_insert_returns_error_if_restricted_unique(self):
        Collection.before_save = lambda self: {
            'error_code': 7, 'error_type': 'NotUnique',
            'error_message': 'Document is not unique.',
        }

        errors = Collection().insert()
        self.assertEqual(
            errors,
            {
                'error_code': 7, 'error_type': 'NotUnique',
                'error_message': 'Document is not unique.'
            }
        )

        Collection.before_save = lambda self: None

    def test_insert_returns_document_if_is_valid(self):
        document = Collection()

        self.assertEqual(document.insert(), document.document)

    # update
    def test_update_is_decorated_with_serializable(self):
        self.assertIn('serializable', Collection.update.decorators)

    def test_update_returns_before_if_before_update_returns_something(self):
        Collection.before_update = lambda self, old: {
            'error_code': 7, 'error_type': 'NotUnique',
            'error_message': 'Document is not unique.',
        }

        Collection({'_id': 1}).insert()
        errors = Collection({'_id': 1}).update()

        self.assertEqual(
            errors,
            {
                'error_code': 7, 'error_type': 'NotUnique',
                'error_message': 'Document is not unique.'
            }
        )

        Collection.before_update = lambda self, old: None

    # delete
    def test_delete_is_decorated_with_serializable(self):
        self.assertIn('serializable', Collection.delete.decorators)

    def test_delete_returns_errors_if_document_has_no_id(self):
        errors = Collection().delete()

        self.assertEqual(
            errors,
            {
                'error_code': 11,
                'error_type': 'UnidentifiedDocumentError',
                'error_message': 'The given document from collection \'Collection\' has no _id.',
                'collection': 'Collection',
                'document': {},
            }
        )

    def test_delete_returns_before_if_before_update_returns_something(self):
        Collection.before_delete = lambda self: {
            'error_code': 9, 'error_type': 'RestrictedDelete',
            'error_message': 'Document can not be deleted.'
        }

        Collection({'_id': 1}).insert()
        errors = Collection({'_id': 1}).delete()

        self.assertEqual(
            errors,
            {
                'error_code': 9, 'error_type': 'RestrictedDelete',
                'error_message': 'Document can not be deleted.'
            }
        )

        Collection.before_delete = lambda self: None

    def test_delete_returns_errors_if_document_not_found(self):
        errors = Collection({'_id': 1}).delete()

        self.assertEqual(
            errors,
            {
                'error_code': 12,
                'error_type': 'DocumentNotFoundError',
                'error_message': '1 is not a valid _id for a document from collection \'Collection\'.',
                'collection': 'Collection',
                '_id': 1,
            }
        )

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
