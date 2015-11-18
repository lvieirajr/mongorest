# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import MaxValueError
from mongorest.testcase import TestCase


class TestMaxValueError(TestCase):

    def test_max_value_error_sets_correct_fields(self):
        self.assertEqual(
            MaxValueError('collection', 'field', 'max_value'),
            {
                'error_code': 33,
                'error_type': 'MaxValueError',
                'error_message': 'Maximum value for field \'field\' on '
                                 'collection \'collection\' is max_value.',
                'collection': 'collection',
                'field': 'field',
                'max_value': 'max_value'
            }
        )
