# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import SchemaMissingError
from mongorest.testcase import TestCase


class TestSchemaMissingError(TestCase):

    def test_schema_missing_error_sets_correct_fields(self):
        self.assertEqual(
            SchemaMissingError('collection'),
            {
                'error_code': 10,
                'error_type': 'SchemaMissingError',
                'error_message': 'Validation schema for collection '
                                 '\'collection\' is missing.',
                'collection': 'collection',
            }
        )
