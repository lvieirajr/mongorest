# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import ValuesNotAllowedError
from mongorest.testcase import TestCase


class TestValuesNotAllowedError(TestCase):

    def test_values_not_allowed_error_sets_correct_fields(self):
        self.assertEqual(
            ValuesNotAllowedError('collection', 'field', 'values'),
            {
                'error_code': 31,
                'error_type': 'ValuesNotAllowedError',
                'error_message': 'Values \'values\' are not allowed for field '
                                 '\'field\' on collection \'collection\'.',
                'collection': 'collection',
                'field': 'field',
                'values': 'values'
            }
        )
