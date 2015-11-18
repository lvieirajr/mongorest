# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import NullNotAllowedError
from mongorest.testcase import TestCase


class TestNullNotAllowedError(TestCase):

    def test_null_not_allowed_error_sets_correct_fields(self):
        self.assertEqual(
            NullNotAllowedError('collection', 'field'),
            {
                'error_code': 44,
                'error_type': 'NullNotAllowedError',
                'error_message': 'Null values are not allowed for field '
                                 '\'field\' on collection \'collection\'.',
                'collection': 'collection',
                'field': 'field',
            }
        )
