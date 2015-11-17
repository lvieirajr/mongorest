# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import FieldLengthError
from mongorest.testcase import TestCase


class TestFieldLengthError(TestCase):

    def test_field_length_error_sets_correct_fields(self):
        self.assertEqual(
            FieldLengthError('collection', 'field', 'length'),
            {
                'error_code': 38,
                'error_type': 'FieldLengthError',
                'error_message': 'Length of field \'field\' of collection '
                                 '\'collection\' must be length.',
                'collection': 'collection',
                'field': 'field',
                'length': 'length'
            }
        )
