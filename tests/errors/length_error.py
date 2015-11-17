# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import LengthError
from mongorest.testcase import TestCase


class TestLengthError(TestCase):

    def test_length_error_sets_correct_fields(self):
        self.assertEqual(
            LengthError('collection', 'field', 'length'),
            {
                'error_code': 38,
                'error_type': 'LengthError',
                'error_message': 'Length of field \'field\' of collection '
                                 '\'collection\' must be length.',
                'collection': 'collection',
                'field': 'field',
                'length': 'length'
            }
        )
