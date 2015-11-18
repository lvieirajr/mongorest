# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import DocumentError
from mongorest.testcase import TestCase


class TestDocumentError(TestCase):

    def test_document_error_sets_correct_fields(self):
        self.assertEqual(
            DocumentError(),
            {
                'error_code': 10,
                'error_type': 'DocumentError',
                'error_message': 'DocumentError',
            }
        )
