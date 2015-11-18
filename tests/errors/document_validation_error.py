# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import DocumentValidationError
from mongorest.testcase import TestCase


class TestDocumentValidationError(TestCase):

    def test_document_validation_error_sets_correct_fields(self):
        self.assertEqual(
            DocumentValidationError('collection', {}, 'document', [1, 2, 3]),
            {
                'error_code': 21,
                'error_type': 'DocumentValidationError',
                'error_message': 'Validation of document from collection '
                                 '\'collection\' failed.',
                'collection': 'collection',
                'schema': {},
                'document': 'document',
                'errors': [1, 2, 3],
            }
        )
