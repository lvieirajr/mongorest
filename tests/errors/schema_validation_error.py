# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import SchemaValidationError
from mongorest.testcase import TestCase


class TestSchemaValidationError(TestCase):

    def test_schema_validation_error_sets_correct_fields(self):
        self.assertEqual(
            SchemaValidationError(),
            {
                'error_code': 20,
                'error_type': 'SchemaValidationError',
                'error_message': 'SchemaValidationError',
            }
        )
