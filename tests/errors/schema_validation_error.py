# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import SchemaValidationError
from mongorest.testcase import TestCase


class TestSchemaValidationError(TestCase):

    def test_schema_validation_error_sets_correct_fields(self):
        self.assertEqual(
            SchemaValidationError('collection', {}, 'document', [1, 2, 3]),
            {
                'error_code': 30,
                'error_type': 'SchemaValidationError',
                'error_message': 'Validation of document from collection '
                                 '\'collection\' failed.',
                'collection': 'collection',
                'schema': {},
                'document': 'document',
                'errors': [1, 2, 3],
            }
        )
