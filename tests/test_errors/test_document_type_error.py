# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import DocumentTypeError
from mongorest.testcase import TestCase


class TestDocumentTypeError(TestCase):

    def test_document_type_error_sets_correct_fields(self):
        self.assertEqual(
            DocumentTypeError('collection', 'document'),
            {
                'error_code': 21,
                'error_type': 'DocumentTypeError',
                'error_message': 'Document for collection \'collection\' must '
                                 'be a dict.',
                'collection': 'collection',
                'document': 'document',
            }
        )
