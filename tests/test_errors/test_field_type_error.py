# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import FieldTypeError
from mongorest.testcase import TestCase


class TestFieldTypeError(TestCase):

    def test_field_type_error_sets_correct_fields(self):
        self.assertEqual(
            FieldTypeError('collection', 'field', 'types'),
            {
                'error_code': 3,
                'error_type': 'FieldTypeError',
                'error_message': 'Field \'field\' must be of type(s): types.',
                'collection': 'collection',
                'field': 'field',
                'types': 'types',
            }
        )
