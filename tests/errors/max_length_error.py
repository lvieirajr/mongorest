# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import MaxLengthError
from mongorest.testcase import TestCase


class TestMaxLengthError(TestCase):

    def test_max_length_error_sets_correct_fields(self):
        self.assertEqual(
            MaxLengthError('collection', 'field', 'max_length'),
            {
                'error_code': 37,
                'error_type': 'MaxLengthError',
                'error_message': 'Maximum length for field \'field\' on '
                                 'collection \'collection\' is max_length.',
                'collection': 'collection',
                'field': 'field',
                'max_length': 'max_length'
            }
        )
