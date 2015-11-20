# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

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
    def test_init_sets_collection(self):
        document = Document(Collection)

        self.assertEqual(document._collection, Collection)

    def test_init_sets_correct_fields(self):
        document = Document(Collection, {'test': 'test'})

        self.assertEqual(document._fields, {'test': 'test'})

    @patch('mongorest.document.Document._process')
    def test_init_calls_process_if_not_processed(self, process):
        Document(Collection, processed=False)

        self.assertEqual(process.call_count, 1)

    @patch('mongorest.document.Document._process')
    def test_init_does_not_call_process_if_processed(self, process):
        Document(Collection, processed=True)

        self.assertEqual(process.call_count, 0)

    @patch('mongorest.validator.Validator.validate_document')
    def test_init_calls_validate_document(self, validate_document):
        try:
            Document(Collection, processed=True)
        except:
            pass

        self.assertEqual(validate_document.call_count, 1)

    def test_get_attr_raises_attribute_error_if_can_not_find_attribute(self):
        with self.assertRaises(AttributeError):
            Document(None).test()

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

    # _process
    def test_process_calls_collections_process_functions(self):
        class TestCollection(Collection):
            def _process1(self):
                pass

        with patch.object(TestCollection, '_process1') as process1:
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
            schema = {'test': {'type': 'string', 'required': True}}

        document = Document(TestCollection, {'test': ObjectId()})

        self.assertEqual(document._errors, document.errors)

    # save
    def test_save_is_decorated_with_serializable(self):
        self.assertIn('serializable', Document.save.decorators)

    def test_save_returns_errors_if_document_is_not_valid(self):
        class TestCollection(Collection):
            schema = {'test': {'required': True, 'type': 'objectid'}}

        errors = Document(TestCollection).save()

        self.assertEqual(
            errors,
            {
                'error_code': 21,
                'error_type': 'DocumentValidationError',
                'error_message': 'Validation of document from collection \'TestCollection\' failed.',
                'errors': [
                    {
                        'error_code': 23,
                        'error_type': 'RequiredFieldError',
                        'error_message': 'Field \'test\' on collection \'TestCollection\' is required.',
                        'collection': 'TestCollection',
                        'field': 'test',
                    },
                ],
                'collection': 'TestCollection',
                'schema': {'test': {'required': True, 'type': 'objectid'}},
                'document': {},
            }
        )

    def test_save_returns_errors_if_error_ocurred_during_save(self):
        Collection.collection.create_index('test', unique=True)
        Collection.insert_one({'test': 'test'})

        document = Document(Collection)
        document.test = 'test'
        errors = document.save()

        self.assertEqual(errors['error_code'], 0)
        self.assertEqual(errors['error_type'], 'PyMongoError')

        Collection.drop_index('test_1')

    def test_save_returns_error_if_restricted_unique(self):
        class TestCollection(Collection):

            @classmethod
            def restrict_unique(cls, document):
                return {
                    'error_code': 7, 'error_type': 'NotUnique',
                    'error_message': 'Document is not unique.',
                }

        errors = Document(TestCollection).save()
        self.assertEqual(
            errors,
            {
                'error_code': 7, 'error_type': 'NotUnique',
                'error_message': 'Document is not unique.'
            }
        )

    def test_save_returns_fields_if_document_does_not_have_id_and_is_valid(self):
        document = Document(Collection)
        fields = document.save()

        self.assertEqual(fields, document._fields)

    def test_save_returns_fields_if_document_has_id_and_is_valid(self):
        document = Document(Collection)
        document._id = ObjectId()
        fields = document.save()

        self.assertEqual(fields, document._fields)

    #update
    def test_update_is_decorated_with_serializable(self):
        self.assertIn('serializable', Document.update.decorators)

    def test_update_returns_error_if_restricted_unique(self):
        class TestCollection(Collection):

            @classmethod
            def restrict_unique(cls, document):
                return {
                    'error_code': 7, 'error_type': 'NotUnique',
                    'error_message': 'Document is not unique.',
                }

        errors = Document(TestCollection, {'_id': 1}).update()
        self.assertEqual(
            errors,
            {
                'error_code': 7, 'error_type': 'NotUnique',
                'error_message': 'Document is not unique.'
            }
        )

    def test_update_returns_error_if_restricted_update(self):
        class TestCollection(Collection):

            @classmethod
            def restrict_update(cls, document):
                return {
                    'error_code': 8, 'error_type': 'RestrictedUpdate',
                    'error_message': 'Document can not be updated.'
                }

        errors = Document(TestCollection, {'_id': 1}).update()
        self.assertEqual(
            errors,
            {
                'error_code': 8, 'error_type': 'RestrictedUpdate',
                'error_message': 'Document can not be updated.'
            }
        )

    def test_update_returns_errors_if_document_is_not_valid(self):
        class TestCollection(Collection):
            schema = {'test': {'required': True}}

        errors = Document(TestCollection).update()

        self.assertEqual(
            errors,
            {
                'error_code': 21,
                'error_type': 'DocumentValidationError',
                'error_message': 'Validation of document from collection \'TestCollection\' failed.',
                'errors': [
                    {
                        'error_code': 23,
                        'error_type': 'RequiredFieldError',
                        'error_message': 'Field \'test\' on collection \'TestCollection\' is required.',
                        'collection': 'TestCollection',
                        'field': 'test',
                    },
                ],
                'collection': 'TestCollection',
                'schema': {'test': {'required': True}},
                'document': {},
            }
        )

    def test_update_returns_errors_if_document_has_no_id(self):
        errors = Document(Collection).update()

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

    def test_update_returns_errors_if_error_ocurred_during_save(self):
        Collection.collection.create_index('test', unique=True)
        Collection.insert_one({'test': 'test1'})
        _id = Collection.insert_one({'test': 'test2'})

        errors = Document(Collection, {'_id': _id, 'test': 'test1'}).update()

        errors.pop('error_message')
        self.assertEqual(
            errors,
            {
                'error_code': 0,
                'error_type': 'PyMongoError',
                'operation': 'update',
                'collection': 'Collection',
                'document': {'_id': _id, 'test': 'test1'}
            }
        )

        Collection.drop_index('test_1')

    def test_update_returns_errors_if_document_not_found(self):
        errors = Document(Collection, {'_id': 1}).update()

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

    @patch('mongorest.collection.Collection.cascade_update')
    def test_update_updates_calls_cascade_and_returns_updated_document_if_document_is_valid(self, cascade):
        _id = Collection.insert_one({'test': 'test1'})
        updated = Document(Collection, {'_id': _id, 'test': 'test2'}).update()

        self.assertEqual(updated, {'_id': _id, 'test': 'test2'})
        self.assertEqual(cascade.call_count, 1)

    #delete
    def test_delete_is_decorated_with_serializable(self):
        self.assertIn('serializable', Document.delete.decorators)

    def test_delete_returns_errors_if_document_has_no_id(self):
        errors = Document(Collection).delete()

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

    def test_delete_returns_error_if_restricted_delete(self):
        class TestCollection(Collection):

            @classmethod
            def restrict_delete(cls, document):
                return {
                    'error_code': 9, 'error_type': 'RestrictedDelete',
                    'error_message': 'Document can not be deleted.'
                }

        errors = Document(TestCollection, {'_id': 1}).delete()
        self.assertEqual(
            errors,
            {
                'error_code': 9, 'error_type': 'RestrictedDelete',
                'error_message': 'Document can not be deleted.'
            }
        )

    def test_delete_returns_errors_if_document_not_found(self):
        errors = Document(Collection, {'_id': 1}).delete()

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
