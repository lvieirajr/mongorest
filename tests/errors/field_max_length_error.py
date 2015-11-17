# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import FieldMaxLengthError
from mongorest.testcase import TestCase


class TestFieldMaxLengthError(TestCase):

    def test_field_max_length_error_sets_correct_fields(self):
        self.assertEqual(
            FieldMaxLengthError('collection', 'field', 'max_length'),
            {
                'error_code': 37,
                'error_type': 'FieldMaxLengthError',
                'error_message': 'Length of field \'field\' of collection '
                                 '\'collection\' must be at most max_length.',
                'collection': 'collection',
                'field': 'field',
                'max_length': 'max_length'
            }
        )
