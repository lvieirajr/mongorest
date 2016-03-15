# # -*- encoding: UTF-8 -*-
# from __future__ import absolute_import, unicode_literals
#
# from bson.objectid import ObjectId
# from mock import patch
#
# from mongorest.collection import Collection
# from mongorest.testcase import TestCase
#
# __all__ = [
#     'TestDocument',
# ]
#
#
# class TestDocument(TestCase):
#     def test_update_returns_errors_if_document_has_no_id(self):
#         errors = Document(Collection).update()
#
#         self.assertEqual(
#             errors,
#             {
#                 'error_code': 11,
#                 'error_type': 'UnidentifiedDocumentError',
#                 'error_message': 'The given document from collection \'Collection\' has no _id.',
#                 'collection': 'Collection',
#                 'document': {},
#             }
#         )
#
#     def test_update_returns_errors_if_error_ocurred_during_save(self):
#         Collection.collection.create_index('test', unique=True)
#         Collection.insert_one({'test': 'test1'})
#         _id = Collection.insert_one({'test': 'test2'})
#
#         errors = Document(Collection, {'_id': _id, 'test': 'test1'}).update()
#
#         errors.pop('error_message')
#         self.assertEqual(
#             errors,
#             {
#                 'error_code': 0,
#                 'error_type': 'PyMongoError',
#                 'operation': 'update',
#                 'collection': 'Collection',
#                 'document': {'_id': _id, 'test': 'test1'}
#             }
#         )
#
#         Collection.drop_index('test_1')
#
#     def test_update_returns_errors_if_document_not_found(self):
#         errors = Document(Collection, {'_id': 1}).update()
#
#         self.assertEqual(
#             errors,
#             {
#                 'error_code': 12,
#                 'error_type': 'DocumentNotFoundError',
#                 'error_message': '1 is not a valid _id for a document from collection \'Collection\'.',
#                 'collection': 'Collection',
#                 '_id': 1,
#             }
#         )
#
#     @patch('mongorest.collection.Collection.cascade_update')
#     def test_update_updates_calls_cascade_and_returns_updated_document_if_document_is_valid(self, cascade):
#         _id = Collection.insert_one({'test': 'test1'})
#         updated = Document(Collection, {'_id': _id, 'test': 'test2'}).update()
#
#         self.assertEqual(updated, {'_id': _id, 'test': 'test2'})
#         self.assertEqual(cascade.call_count, 1)
