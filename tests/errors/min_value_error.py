# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import MinValueError
from mongorest.testcase import TestCase


class TestMinValueError(TestCase):

    def test_min_value_error_sets_correct_fields(self):
        self.assertEqual(
            MinValueError('collection', 'field', 'min_value'),
            {
                'error_code': 32,
                'error_type': 'MinValueError',
                'error_message': 'Minimum value for field \'field\' on '
                                 'collection \'collection\' is min_value.',
                'collection': 'collection',
                'field': 'field',
                'min_value': 'min_value'
            }
        )
