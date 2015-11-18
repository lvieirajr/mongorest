# -*- encoding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

from mongorest.errors import EmptyNotAllowedError
from mongorest.testcase import TestCase


class TestEmptyNotAllowedError(TestCase):

    def test_empty_not_allowed_error_sets_correct_fields(self):
        self.assertEqual(
            EmptyNotAllowedError('collection', 'field'),
            {
                'error_code': 43,
                'error_type': 'EmptyNotAllowedError',
                'error_message': 'Empty values are not allowed for field '
                                 '\'field\' on collection \'collection\'.',
                'collection': 'collection',
                'field': 'field',
            }
        )
