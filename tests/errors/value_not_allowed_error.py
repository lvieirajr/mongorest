# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import ValueNotAllowedError
from mongorest.testcase import TestCase


class TestValueNotAllowedError(TestCase):

    def test_value_not_allowed_error_sets_correct_fields(self):
        self.assertEqual(
            ValueNotAllowedError('collection', 'field', 'value'),
            {
                'error_code': 30,
                'error_type': 'ValueNotAllowedError',
                'error_message': 'Value: value; is not allowed for field '
                                 '\'field\' on collection \'collection\'.',
                'collection': 'collection',
                'field': 'field',
                'value': 'value'
            }
        )
