# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import SchemaFieldTypeError
from mongorest.testcase import TestCase


class TestSchemaFieldTypeError(TestCase):

    def test_schema_field_type_error_sets_correct_fields(self):
        self.assertEqual(
            SchemaFieldTypeError('collection', 'field'),
            {
                'error_code': 12,
                'error_type': 'SchemaFieldTypeError',
                'error_message': 'Type of field \'field\' on collection '
                                 '\'collection\' must be either a list or a '
                                 'dict.',
                'collection': 'collection',
                'field': 'field'
            }
        )
