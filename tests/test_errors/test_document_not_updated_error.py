# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import DocumentNotUpdatedError
from mongorest.testcase import TestCase


class TestDocumentNotUpdatedError(TestCase):

    def test_document_not_updated_error_sets_correct_fields(self):
        self.assertEqual(
            DocumentNotUpdatedError('collection', '_id', 'document'),
            {
                'error_code': 6,
                'error_type': 'DocumentNotUpdatedError',
                'error_message': 'No fields were updated for collection '
                                 'document with _id _id.',
                'collection': 'collection',
                '_id': '_id',
                'document': 'document',
            }
        )
