# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import UnidentifiedDocumentError
from mongorest.testcase import TestCase


class TestUnidentifiedDocumentError(TestCase):

    def test_unidentified_document_error_sets_correct_fields(self):
        self.assertEqual(
            UnidentifiedDocumentError('collection', 'document'),
            {
                'error_code': 11,
                'error_type': 'UnidentifiedDocumentError',
                'error_message': 'The given document from collection '
                                 '\'collection\' has no _id.',
                'collection': 'collection',
                'document': 'document',
            }
        )
