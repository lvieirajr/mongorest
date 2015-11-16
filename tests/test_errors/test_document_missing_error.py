# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import DocumentMissingError
from mongorest.testcase import TestCase


class TestDocumentMissingError(TestCase):

    def test_document_missing_error_sets_correct_fields(self):
        self.assertEqual(
            DocumentMissingError('collection'),
            {
                'error_code': 20,
                'error_type': 'DocumentMissingError',
                'error_message': 'Document missing for collection '
                                 '\'collection\'.',
                'collection': 'collection',
            }
        )
