# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import FieldMinLengthError
from mongorest.testcase import TestCase


class TestFieldMinLengthError(TestCase):

    def test_field_min_length_error_sets_correct_fields(self):
        self.assertEqual(
            FieldMinLengthError('collection', 'field', 'min_length'),
            {
                'error_code': 36,
                'error_type': 'FieldMinLengthError',
                'error_message': 'Length of field \'field\' of collection '
                                 '\'collection\' must be at least min_length.',
                'collection': 'collection',
                'field': 'field',
                'min_length': 'min_length'
            }
        )
