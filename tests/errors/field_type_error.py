# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import FieldTypeError
from mongorest.testcase import TestCase


class TestFieldTypeError(TestCase):

    def test_field_type_error_sets_correct_fields(self):
        self.assertEqual(
            FieldTypeError('collection', 'field', 'type'),
            {
                'error_code': 25,
                'error_type': 'FieldTypeError',
                'error_message': 'Field \'field\' on collection '
                                 '\'collection\' must be of type type.',
                'collection': 'collection',
                'field': 'field',
                'type': 'type',
            }
        )
