# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import DocumentNotFoundError
from mongorest.testcase import TestCase


class TestDocumentNotFoundError(TestCase):

    def test_document_not_found_error_sets_correct_fields(self):
        self.assertEqual(
            DocumentNotFoundError('collection', '_id'),
            {
                'error_code': 5,
                'error_type': 'DocumentNotFoundError',
                'error_message': '_id is not a valid collection document _id.',
                'collection': 'collection',
                '_id': '_id',
            }
        )
