# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import FieldDefinitionError
from mongorest.testcase import TestCase


class TestFieldDefinitionError(TestCase):

    def test_field_definition_error_sets_correct_fields(self):
        self.assertEqual(
            FieldDefinitionError('collection', 'field'),
            {
                'error_code': 14,
                'error_type': 'FieldDefinitionError',
                'error_message': 'Schema definition for field \'field\' of '
                                 'collection \'collection\' must be a dict.',
                'collection': 'collection',
                'field': 'field',
            }
        )
