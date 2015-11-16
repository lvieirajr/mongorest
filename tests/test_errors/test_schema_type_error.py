# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import SchemaTypeError
from mongorest.testcase import TestCase


class TestSchemaTypeError(TestCase):

    def test_schema_type_error_sets_correct_fields(self):
        self.assertEqual(
            SchemaTypeError('collection', 'schema'),
            {
                'error_code': 11,
                'error_type': 'SchemaTypeError',
                'error_message': 'Validation schema for collection '
                                 '\'collection\' must be a dict.',
                'collection': 'collection',
                'schema': 'schema'
            }
        )
